#! /usr/bin/env python

__author__ = """Andrew Temlyakov (temlyaka@gmail.com)"""

import copy
import sys
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
    def test_filter_one_match_found(self):
        filtered_tuples = [('a1b', 'file/cat')]
        self.assertEquals(self.duplicates.filter('cat'), filtered_tuples)
    
    def test_filter_many_matches_found(self):
        filtered_tuples = [('a1b', 'file/dog/two'), ('a3b', 'file/lizard/two')]
        self.assertEquals(self.duplicates.filter('two'), filtered_tuples)
   
    def test_filter_no_matches_found(self):
        self.assertEquals(self.duplicates.filter('dino'), [])

    ###
    # duplicates.list tests
    ###
    def test_list_from_filter(self):
        filtered_tuples = [('a1b', 'file/dog/two'), ('a3b', 'file/lizard/two')]
        test_duplicates = Duplicates(self.test_dict, filtered_tuples)
        test_duplicates.list()
        self.assertEquals(self.output.getvalue(), 'a1b file/dog/two\na3b file/lizard/two\n')

    def test_list_from_empty_filter(self):
        self.duplicates.list()
        self.assertEquals(self.output.getvalue(), 'Nothing selected for deletion.\n')

    ###
    # duplicates.delete tests
    ###
    def test_delete_dictionary_updated_filter_reset(self):
        filtered_tuples = [('a1b', 'file/dog/two'), ('a3b', 'file/lizard/two')]
        test_expected_dict = {'a1b':['file/cat/one'], 
                              'a2b':['file/fish/one'], 
                              'a3b':['file/bird/one',
                                     'file/elephant/three']}
        
        test_duplicates = Duplicates(self.test_dict, filtered_tuples)
        test_duplicates.delete()
    
        self.assertEquals(test_duplicates.duplicates_dict, test_expected_dict)
        self.assertEquals(test_duplicates.filtered_tuples, [])

    def test_delete_fail_deleting_non_duplicate(self):
        filtered_tuples = [('a2b', 'file/fish/one')]
        self.duplicates.delete()
        
        self.assertEquals(self.duplicates.duplicates_dict, self.test_dict)
        self.assertEquals(self.output.getvalue(),  
            'file/fish/one is selected for deletion, but is no longer a duplicate!\n')

if __name__ == '__main__':
    unittest.main()
