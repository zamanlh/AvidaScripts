#!/usr/local/epd/bin/python

import sys, gzip, random
from itertools import ifilter, repeat
from scipy.stats import sem
from numpy import array, vectorize, mean

#handle gzip files or non-gzip files
def open_file(file_name):
    if file_name.endswith('.gz'):
        f = gzip.open(file_name)
    else:
        f = open(file_name)
    
    return f
    
#parses a file layed out as avida dumps grids (space delimited cells, new line delimited rows of cells)
#returns a 2d array of strings
def get_grid(afile, cast_function=int):
   f = open_file(afile)
   fileData = f.read()
   f.close()
   lines = fileData.split('\n')
   lines = [l.strip() for l in lines][:-1]
   grid = [l.split(' ') for l in lines]
   #grid = [[cast_function(i) for i in l.split(' ')] for l in lines]
   return grid

#open file and look at column for a value > 0, useful for making sure 
#you still have parasites, for example, or you still have orgs doing task X
def check_for_presence(file_name, absence_symbols = ["0", "-1"], column=1, row=-1):
   #open and read file contents
   f = open_file(file_name)
   content = f.read()
   #parse into 2d array
   content =  [i.strip().split() for i in content.split('\n') if len(i) > 1 and i[0] != "#"]

   if content[row][column] in absence_symbols:
       return False
   return True
   
   
#turns the integer into a 9-bit little endian "string"   
def get_binary_string(strNum):
  num = int(strNum)
  binString = bin(num)[2:].zfill(9)[::-1]
  return binString   
  
#given a 2d list of phenotypes, flatten the list and return only valid phenotypes
#returns an ittertool class, so you can itterate through it normally, but 
#to use it like a list, you must cast it first 
def get_valid_phenotypes(a_grid):
    #flatten the list of lists into a single list of phenotypes
    phenotypes = list(array(a_grid).ravel())
    #remove all 0s (invalid phenotypes) and -1s (empty spots in the grid)
    phenotypes = ifilter(lambda x: x != "-1" and x != "0", phenotypes)
    
    return phenotypes

    
# ----- example usage --------
#first make sure parasites were around in this run at 10,000 updates (recorded every 100 updates)
if check_for_presence('ParasiteData.dat', row = 10000/100):
    print "parasites persisted"
    grid = get_grid('grid_task_hosts.10000.dat')
    phenotypes = get_valid_phenotypes(grid)
    
    #count the number of ones in the binary representation of the phonetype
    num_ones = [get_binary_string(p).count('1') for p in phenotypes]
    
    #average the number of ones in this population
    avg_num_ones = mean(num_ones)
    
    print avg_num_ones
else:
    print "parasites did not persist"

    
    