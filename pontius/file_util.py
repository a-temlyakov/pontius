__author__ = """Andrew Temlyakov (temlyaka@gmail.com)"""

import os

def load_file(file_path):
    """ Load a file into a dictionary
    
        Expected file format is:
        md5_hash full/path/to/file
    """
    duplicates_dict = {}
    input_file = open(file_path, 'r')
   
    for line in input_file:
        if line.strip():
            key,value = line.rstrip().split(' ', 1)
    
            if key in duplicates_dict:
                duplicates_dict[key].append(value.lstrip())
            else:
                duplicates_dict[key] = [value.lstrip()]
    
    input_file.close()
    return duplicates_dict

def save_file(duplicates_dict, file_path):
    """ Save a file given a dictionary
    
        File output format is:
        md5_hash full/path/to/file
    """
    output_file = open(file_path, 'w')

    for key in duplicates_dict:
        # Only save values that still have duplicates
        list_of_paths = duplicates_dict[key]
        if len(list_of_paths) > 1: 
            for path in list_of_paths:
                output_file.write(key + " " + path + "\n")

    output_file.close() 

def delete_file(file_path):
    """ Delete a file from file system """
    os.remove(file_path)

