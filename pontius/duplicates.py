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
        """ Save remaining list duplicates to a file """
        file_util.save_file(self.duplicates_dict, file_path)

    def delete(self):
        """ Delete all duplicates currently selected """
        list_of_kept_values = []
        
        for key,value in self.filtered_tuples:
            if len(self.duplicates_dict[key]) > 1:
                file_util.delete_file(value)
                self.duplicates_dict[key].remove(value)
            else:
                """ Nuke the key, since it's no longer a duplicate """
                self.duplicates_dict.pop(key)
                list_of_kept_values.append(value)
 
        if len(list_of_kept_values) > 0:
            message = ("The following values have not been deleted, "
                       "because duplicates\n are no longer detected for "
                       "them:")
            print message

            for value in list_of_kept_values:
                print value
    
        self.reset()

