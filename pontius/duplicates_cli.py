#! /usr/bin/env python

__author__ = """Andrew Temlyakov (temlyaka@gmail.com)"""

import cmd
import sys

from duplicates import Duplicates

class DuplicatesCli(cmd.Cmd):
    prompt = '> '
    completekey = '\t'
    cmdqueue = []
    
    def __init__(self):
        self.duplicates = Duplicates()

    def do_load(self, duplicates_file):
        """load [duplicates_file]
        Load the data from the duplicates file
        Expected file format: md5_hash full/file/path"""
        print "Loading file: " + duplicates_file + "..."
        self.duplicates.load(duplicates_file) 

    def do_save(self, save_file):
        """save [save_file]
        Save existing duplicates that are in memory to a file.
        This is useful after doing a few deletions."""
        pass

    def do_filter(self, query):
        """filter [query]
        Finds all file paths that contain the given query"""
        self.duplicates.filter_duplicates(query)

    def do_list(self, line):
        """list 
        List all files that are currently selected for deletion"""
        self.duplicates.list_duplicates()

    def do_reset(self):
        """reset
        Reset the filtered values"""
        self.duplicates.reset()

    def do_delete(self, line):
        """delete
        Deletes all files whos filepath is currently in memory
        (after loading or filtering)
        
        Use at own risk! Will delete file entirely, without making any
        backups."""
        pass

    def do_exit(self, line):
        """exit
        Exit the CLI"""
        sys.exit(0)

if __name__ == '__main__':
    DuplicatesCli().cmdloop()
