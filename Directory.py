#!/usr/bin/env python3
# Ahmed Alotaibi, Akshay Singh
# 11/8/2017
# A program that store the files' data in a given directory
# then to compare them later to see if any changes happend.

import os
import time
from os import listdir
from os.path import isfile, join
import pprint

class Files():

    """Returns all files name in a given directory"""
    def filesInDir(self, directory):
        return [listdir(directory)]
    """Directory: the directory to be searched for files
       Returns: a dictionary with key of filename(and path)
       and value of another dictionary containing the files'
       properties.
    """
    def filesInDirWithInfo(self,directory):
        values = {0:'protection bits: ',      1:'inode number: ',
                  2:'device: ',               3:'number of hard links: ',
                  4:'user id of owner: ',     5:'group id of owner: ',
                  6:'size of file in bytes: ',7:'time of most recent access: ',
                  8:'time of most recent modification: ',
                              9:'time of most metadata change: '}
        filepaths = []
        for dirpath, subdirs, files in os.walk(directory):
            for file in files:
                filepaths.append(os.path.join(dirpath,file))
        files =  [[f,os.stat(f)]
                  for f in filepaths]
        properties = {filepaths[i]:{v:files[i][1][k]
                    for k,v in values.items() }
                        for i in range(len(filepaths))}
        return properties
    """
    Directory: the directory to be searched for files
    using filesInDirWithInfo function.
    Stores the files data as a string in a files called data.txt
    """
    def store(self,directory):
        k = self.filesInDirWithInfo(directory)
        with open('data.txt','w') as f:
            f.write(str(k))
            
    """
    Needs to be used after the store function
    check for change in the current files using the filesInDirWithInfo
    function against the text retrieved from the data.txt file
    and report any changes to the files.
    """
    def check(self,directory):
        new = self.filesInDirWithInfo(directory)
        with open('data.txt', 'r') as f:
            old = eval(f.read())
        if new == old:
            print('There is nothing changed')
        else:
            print("\nChanges found: \n")
            for i in set(new).intersection(set(old)):
                for j in new[i]:
                    if new[i][j] != old[i][j]:
                        print("\n\"{}\"\nFile path: /{}\
                              \n\tNew value: {} to {}\n".format(j,i,old[i][j],new[i][j]))
            for i in set(new).symmetric_difference(set(old)):
                try:
                    if old[i]:
                        print("\nFile: /{}\
                              has changed or is no longer exist".format(i))
                except:
                    if new[i]:
                        print("\nChanges found: \n")
                        print("The file /{}\ is a new file".format(i))

def main():
    path = input("Please enter the directory you want to search in: ")
    test = Files()
    print("\n")
    print("Files found in the given directory: ")
    pprint.pprint(test.filesInDir(path))
    print("\n")
    print("Files' information found in the given directory: ")
    pprint.pprint(test.filesInDirWithInfo(path))
    test.store(path)
    print("\n20 seconds to make changes to the Directory:\n\
          Try Creating, editing or deleting a file")
    time.sleep(20)
    test.check(path)

if __name__== "__main__":
    main()
