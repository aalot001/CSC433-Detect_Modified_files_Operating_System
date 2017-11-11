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
    """Returns all the files inside the directory without
    looking into the subdirs in the form of alist"""
    def filesInDir(self,directory):
        return [listdir(directory)]
    """Retrieves the files' properties and returns a dictionary containing the
    file name as the key and another dictionary as its value with the details
    of the file"""
    def filesInDirWithInfo(self,directory):
        values = {0:'protection bits: ',
                  1:'inode number: ',
                  2:'device: ',
                  3:'number of hard links: ',
                  4:'user id of owner: ',
                  5:'group id of owner: ',
                  6:'size of file in bytes: ',
                  7:'time of most recent access: ',
                  8:'time of most recent modification: ',
                  9:'time of most metadata change: '}
        files =  [[f,os.stat("{0}/{1}".format(directory,f))]
                     for f in listdir(directory)]       
        p = {files[filename][0]: {v:files[i][1][k]
                for i in range(len(files))
              for k,v in values.items() }
            for filename in range(len(files)) }
        return(p)

    #Returns a list containing file names(and path) as well as the properties
    def allFilesInfo(self,directory):
        x = []
        for dirpath, subdirs, files in os.walk(directory):
            for file in files:
                x.append(os.path.join(dirpath,file))
        data = [[x[p],os.stat(x[p])]
                for p in range(len(x))]
        return data
    #Writes the returned value of allFilesInfo to an external file called
    #"file data.txt"
    def store(self,directory):
        with open('data.txt','w') as f:
            k = [[j for j in i]
                 for i in self.allFilesInfo(directory)]
            f.write(str(k)+"\n")
    #Checks to see if the data from the file is the same as the files' data now
    def check(self,directory):
        with open('file data.txt', 'r') as f:
            ls = f.read()
        k = [[j for j in i]
             for i in self.allFilesInfo(directory)]
        with open('file data.txt', 'r') as f:
            old = f.read()
        if old == str(k):
            print('nothing changed')
        else:
            print("something changed")

def main():
    path = input("please enter the directory you want to search in: ")
    test = Files()
    print("\n")
    print("Files found in the given directory: ")
    pprint.pprint(test.filesInDir(path))
    print("\n")
    print("Files' information found in the given directory: ")
    pprint.pprint(test.filesInDirWithInfo(path))
    test.store(path)
    print("you have 15 seconds to make changes")
    time.sleep(15)
    test.check(path)

if __name__== "__main__":
    main()
