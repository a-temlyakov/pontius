#! /usr/bin/env python

__author__ = """Andrew Temlyakov (temlyaka@gmail.com)"""

import copy
import sys
import os.path
import StringIO
import unittest

from pontius.duplicates import Duplicates

class TestDuplicates(unittest.TestCase):
    
    def setUp(self):
        self.test_dict = {'a1b':['file/cat/one','file/dog/two'], 
                          'a2b':['file/fish/one'], 
                          'a3b':['file/bird/one',
                                 'file/lizard/two',
                                 'file/elephant/three']}
       
        self.duplicates = Duplicates(self.test_dict)

        self.output = StringIO.StringIO()
        self.saved_stdout = sys.stdout
        sys.stdout = self.output

    def tearDown(self):
        self.output.close()
        sys.stdout = self.saved_stdout

    ###
    # duplicates.filter tests
    ###

    # From dictionary
    def test_filter_dict_one_match_found(self):
        self.duplicates.filtered_tuples = []
        self.duplicates.filter_duplicates('cat')
        expected_tuples = [('a1b', 'file/cat/one')]
        self.assertEquals(self.duplicates.filtered_tuples, expected_tuples)

    def test_filter_dict_many_matches_found(self):
        self.duplicates.filtered_tuples = []
        self.duplicates.filter_duplicates('two')
        expected_tuples = [('a3b', 'file/lizard/two'), ('a1b', 'file/dog/two')]
        self.assertEquals(self.duplicates.filtered_tuples, expected_tuples)

    def test_filter_dict_no_matches_found(self):
        self.duplicates.filtered_tuples = []
        self.duplicates.filter_duplicates('dino')
        expected_tuples = []
        self.assertEquals(self.duplicates.filtered_tuples, expected_tuples)

    # From existing filter
    def test_filter_one_match_found(self):
        self.duplicates.filtered_tuples = \
            [('a3b', 'file/lizard/two'), ('a1b', 'file/dog/two')]
        self.duplicates.filter_duplicates('lizard')
        expected_tuples = [('a3b', 'file/lizard/two')]
        self.assertEquals(self.duplicates.filtered_tuples, expected_tuples)
    
    def test_filter_many_matches_found(self):
        self.duplicates.filtered_tuples = \
            [('a3b', 'file/lizard/two'), 
             ('a1b', 'file/dog/two'), 
             ('a4b', 'file/dog/three')]
        self.duplicates.filter_duplicates('dog')
        expected_tuples = [('a1b', 'file/dog/two'), ('a4b', 'file/dog/three')]
        self.assertEquals(self.duplicates.filtered_tuples, expected_tuples)
   
    def test_filter_no_matches_found(self):
        self.duplicates.filtered_tuples = \
            [('a3b', 'file/lizard/two'), 
             ('a1b', 'file/dog/two'), 
             ('a4b', 'file/dog/three')]
        self.duplicates.filter_duplicates('seven')
        expected_tuples = []
        self.assertEquals(self.duplicates.filtered_tuples, expected_tuples)

    ###
    # duplicates.list tests
    ###
    def test_list_from_filter(self):
        filtered_tuples = [('a1b', 'file/dog/two'), ('a3b', 'file/lizard/two')]
        test_duplicates = Duplicates(self.test_dict, filtered_tuples)
        test_duplicates.list_duplicates()
        self.assertEquals(self.output.getvalue(), 'a1b file/dog/two\na3b file/lizard/two\n')
        test_duplicates.filtered_tuples = []

    def test_list_from_empty_filter(self):
        duplicates = Duplicates(self.test_dict)
        duplicates.list_duplicates()
        self.assertEquals(self.output.getvalue(), 'Nothing selected for deletion.\n')

    ###
    # duplicates.delete tests
    ###
    def test_delete_dictionary_updated_filter_reset(self):
        file_to_delete_one = 'dog.two'
        file_to_delete_two = 'lizard.two'

        self.duplicates.duplicates_dict = {'a1b':['file/cat/one',file_to_delete_one], 
                                           'a2b':['file/fish/one'], 
                                           'a3b':['file/bird/one',
                                                  file_to_delete_two,
                                                  'file/elephant/three']}
        self.duplicates.filtered_tuples = [('a1b', file_to_delete_one), 
                                           ('a3b', file_to_delete_two)]

        test_expected_dict = {'a1b':['file/cat/one'], 
                              'a2b':['file/fish/one'], 
                              'a3b':['file/bird/one',
                                     'file/elephant/three']}
       
        #Create the files for deletion
        open(file_to_delete_one, 'a').close()
        open(file_to_delete_two, 'a').close()
    
        #Make sure files created succesfully
        self.assertTrue(os.path.isfile(file_to_delete_one))
        self.assertTrue(os.path.isfile(file_to_delete_two))
        
        self.duplicates.delete()

        #Make sure files are gone now
        self.assertFalse(os.path.isfile(file_to_delete_one))
        self.assertFalse(os.path.isfile(file_to_delete_two))
        
        #Make sure data updated accordingly
        self.assertEquals(self.duplicates.duplicates_dict, test_expected_dict)
        self.assertEquals(self.duplicates.filtered_tuples, [])

    def test_detele_fail_file_not_exist(self):
        self.duplicates.duplicates_dict = {'a1b':['file/cat/one','file/dog/two'], 
                                           'a2b':['file/fish/one'], 
                                           'a3b':['file/bird/one',
                                                  'file/lizard/two',
                                                  'file/elephant/three']}
        self.duplicates.filtered_tuples = [('a1b', 'file/cat/one')]
        test_expected_dict = {'a1b':['file/cat/one','file/dog/two'], 
                              'a2b':['file/fish/one'], 
                              'a3b':['file/bird/one',
                                     'file/lizard/two',
                                     'file/elephant/three']}

        #Should not fail when trying to delete non-existing file
        self.duplicates.delete()
        
        #Should not have changed duplicates dict, but cleared the filtered tuples
        self.assertEquals(self.duplicates.duplicates_dict, test_expected_dict)
        self.assertEquals(self.duplicates.filtered_tuples, [])
    
    def test_delete_fail_deleting_non_duplicate(self):
        self.duplicates.duplicates_dict = {'a1b':['file/cat/one','file/dog/two'], 
                                           'a2b':['file/fish/one'], 
                                           'a3b':['file/bird/one',
                                                  'file/lizard/two',
                                                  'file/elephant/three']}
        self.duplicates.filtered_tuples = [('a2b', 'file/fish/one')]
        
        test_expected_dict = {'a1b':['file/cat/one','file/dog/two'], 
                              'a3b':['file/bird/one',
                                     'file/lizard/two',
                                     'file/elephant/three']}
        
        self.duplicates.delete()
         
        self.assertEquals(self.duplicates.duplicates_dict, test_expected_dict)
        self.assertEquals(self.duplicates.filtered_tuples, [])

if __name__ == '__main__':
    unittest.main()
