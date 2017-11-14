#!/usr/bin/env python3

# Ahmed Alotaibi, Akshay Singh
# 11/8/2017
# A program to search, store, check for change 
# in all fills in a given directory.

import os
import time
from os import listdir
from os.path import join
import pprint
import re

class Files():

    #Returns all files name in a given directory
    def filesInDir(self, directory):
        return [listdir(directory)]

    #Directory: the directory to be searched for files
    #Returns dictionries contain files properties and their 
    #human-readable meaning.
    def filesInDirWithInfo(self,directory):
        values = {0:'protection bits: ',      1:'inode number: ',
                  2:'device: ',               3:'number of hard links: ',
                  4:'user id of owner: ',     5:'group id of owner: ',
                  6:'size of file in bytes: ',7:'time of most recent access: ',
                  8:'time of most recent modification: ',
                  9:'time of most metadata change: '}

	#empty list to populate it later.
        filepaths = []
        for dirpath, subdirs, files in os.walk(directory):
            for file in files:
		#adding the full path of every file to
		#the filepaths after merging its name with its path
                filepaths.append(os.path.join(dirpath,file))
	
	#A 2D list contains the the filepaths of a file 
	# and its second elements are os.stat applied to that file.
        files =  [[f,os.stat(f)] for f in filepaths]

	#A nested dictionary comprehension.
	#First key is a file path from filepaths
	#and its value is a dictionary whose key is
	#the value of the dictionary values.
	#Used index 1 of the ith element of the files
	#to make 10 a tuple of 10 elements representing
	#the files' properties as the value of the inner
	#dictionary. i = the range of the length of the filepaths
        properties = {filepaths[i]:{v:files[i][1][k]
               for k,v in values.items() }
                    for i in range(len(filepaths))}
        return properties
    
    #Directory: the directory to be searched for files
    #using filesInDirWithInfo function.
    #Stores the files data as a string in a files called data.txt
    def store(self,directory):
        k = self.filesInDirWithInfo(directory)
        with open('data.txt','w') as f:
            k = re.sub(r',', ",\n", str(k))
            k = re.sub(r'}}', "}}\n", str(k))
            f.write(str(k))
            
   
    #Needs to be used after the store function
    #check for change in the current files using the filesInDirWithInfo
    #function against the text retrieved from the data.txt file
    #and report any changes to the files.
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
                             \n\thas changed or is no longer exist".format(i))
                except:
                    if new[i]:
                        print("\nChanges found: \n")
                        print("The file /{}\ is a new file".format(i))

def main():
    try:
       path = input("Please enter a directory's name you want to search in: ")
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
    except IOError:
       print("\nCannot find the give directory: ")

if __name__== "__main__":
    main()
