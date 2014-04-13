__author__ = """Andrew Temlyakov (temlyaka@gmail.com)"""

class Duplicates(object):
    def __init__(self, duplicates_dict={}, filtered_tuples=[]):
        self.duplicates_dict = duplicates_dict
        self.filtered_tuples = filtered_tuples

    def filter(self, search_value):
        """ Filter duplicates whose value matches the search_value """
        if self.filtered_tuples:
            pass
        else:
            pass

    def list(self):
        """ List all duplicates currently selected for deletion """
        if self.filtered_tuples:
            for key,value in self.filtered_tuples:
                print key,value
        else:
            print "Nothing selected for deletion."
    
    def load(self, file_path):
        """ Load duplicates from a file """
        pass

    def save(self, file_path):
        """ Save remaining duplicates to a file """
        pass

    def delete(self):
        """ Delete all duplicates currently selected """
        pass

