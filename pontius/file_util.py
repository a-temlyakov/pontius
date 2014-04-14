__author__ = """Andrew Temlyakov (temlyaka@gmail.com)"""

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
     
    return duplicates_dict

def save_file(duplicates_dict, file_path):
    """ Save a file given a dictionary
    
        File output format is:
        md5_hash full/path/to/file
    """
    pass

def delete_file(file_path):
    """ Delete a file from file system """
    pass
