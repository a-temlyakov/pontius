__author__ = """Andrew Temlyakov (temlyaka@gmail.com)"""

import file_util

class Duplicates(object):
    def __init__(self, duplicates_dict={}, filtered_tuples=[]):
        self.duplicates_dict = duplicates_dict
        self.filtered_tuples = filtered_tuples

    def filter_duplicates(self, search_value):
        """ Filter duplicates whose value matches the search value """  
        if not self.filtered_tuples:
            """ search inside dictionary if no filter exists """
            for key in self.duplicates_dict:
                list_of_values = self.duplicates_dict[key]
                    
                for value in list_of_values:
                    if value.find(search_value) != -1:
                        self.filtered_tuples.append((key, value))
        else:
            """ search inside already existing tuples """
            self.filtered_tuples[:] = \
                [x for x in self.filtered_tuples if x[1].find(search_value) != -1]

    def list_duplicates(self):
        """ List all duplicates currently selected for deletion """
        if self.filtered_tuples:
            for key,value in self.filtered_tuples:
                print key,value
        else:
            print "Nothing selected for deletion."

    def reset(self):
        """ Reset/clear the filtered_tuples to start over """
        self.filtered_tuples = []

    def load(self, file_path):
        """ Load duplicates from a file """
        self.duplicates_dict = file_util.load_file(file_path)

    def save(self, file_path):
        """ Save remaining duplicates to a file """
        file_util.save(self.duplicates, file_path)

    def delete(self, file_path):
        """ Delete all duplicates currently selected """
        pass
