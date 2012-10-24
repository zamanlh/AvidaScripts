#!/usr/bin/env python

#usage: graphAvidaColumn.py <filename> <column>
#produces a simple line graph of this column

# Luis Zaman
# 5/18
import sys, gzip, csv, os.path
from numpy import transpose, array, average, arange
from matplotlib import pyplot
from scipy.stats import sem
from collections import defaultdict
from itertools import ifilter

#MAIRIN CHESNEY
#handles gzip files or non-gzip files
def open_file(file_name):
  if file_name.endswith('.gz'):
    f = gzip.open(file_name)
  else:
    f = open(file_name)
  
  return f

#MAIRIN CHESNEY
#parses a files layed out as avida dump grids (space delimited cells, new line delimited rows of cells)
#returns a 2d array of ints
def get_grid(afile, cast_function=int):
  f = open_file(afile)
  fileData = f.read()
  f.close()
  lines = fileData.split('\n')
  lines = [l.strip() for l in lines][:-1]
  grid = [l.split(' ') for l in lines]
  return grid

#MAIRIN CHESNEY
#LZ - to make things easier to read, this should return 1 if they interact and 0 if they don't
#resistance then can just be 1-(do_phenotypes_interact)
def do_phenotypes_interact(parasite_phenotypeA, host_phenotypeB):
  interaction = (int(parasite_phenotypeA) ^ int(host_phenotypeB)) & int(parasite_phenotypeA)
  if interaction == 0:
    return 0.0
  else:
    return 1.0

#LZ - given a 2d list of phenotypes, flatten the list and return only valid phenotypes
#returns an ittertool class, so you can itterate through it normally, but 
#to use it like a list, you must cast it first 
def get_valid_phenotypes(a_grid):
    #flatten the list of lists into a single list of phenotypes
    phenotypes = list(array(a_grid).ravel())
    
    #remove all 0s (invalid phenotypes) and -1s (empty spots in the grid)
    phenotypes = ifilter(lambda x: x != "-1" and x != "0", phenotypes)
    
    return phenotypes

#MAIRIN CHESNEY
#Returns resistance for a specific treatment and update
def calculate_resistance(treatment_name, treatment_num, host_update, parasite_update):
    resistance = 0.0

    parasite_phenotype_counts = defaultdict(int)
    host_phenotype_counts = defaultdict(int)

    host_grid = [[]]
    parasite_grid = [[]]

    if os.path.isfile("%s_%d/data/grid_task_hosts.%d.dat.gz"%(treatment_name, treatment_num, host_update)):
        host_grid = get_grid("%s_%d/data/grid_task_hosts.%d.dat.gz"%(treatment_name, treatment_num, host_update))
        
    if os.path.isfile("%s_%d/data/grid_task_parasite.%d.dat.gz"%(treatment_name, treatment_num, parasite_update)):
        parasite_grid = get_grid("%s_%d/data/grid_task_parasite.%d.dat.gz"%(treatment_name, treatment_num, parasite_update))
        
    #LZ - use one of the functions from my grid script to get out only valid phenotypes, no 0s or -1s since those will mess up calculations
    for host_p in get_valid_phenotypes(host_grid):
        host_phenotype_counts[host_p] += 1
	
    for parasite_p in get_valid_phenotypes(parasite_grid):
        parasite_phenotype_counts[parasite_p] += 1
	
    
    #LZ - use sum() instead of looping ourselves
    host_total = float(sum(host_phenotype_counts.values()))
    parasite_total = float(sum(parasite_phenotype_counts.values()))
    
    #LZ - we don't need to try and calculate resistance if there are no parasites, the hosts are just 100% resistant
    if parasite_total == 0:
        resistance = 1.0
    else:
        #LZ - here is where your main error was, you were calculating interaction between the counts of parasites and hosts, and not their phenotypes
        #so you could imagine those numbers were weird. Also, these were all being done originally as integer division and multiplication, but changing
        #all the default values from 0 to 0.0 or from 1 to 1.0 fixes this problem. With dictionaries you can get a return of key and value with the
        #iteritems() function.
        for host_phenotype, host_count in host_phenotype_counts.iteritems():
            for parasite_phenotype, parasite_count in parasite_phenotype_counts.iteritems():
                #LZ - 1-interaction so we're counting the probability of a host being resistant to a particular parasite with a given frequency
                resistance += (1-do_phenotypes_interact(parasite_phenotype, host_phenotype)) * (parasite_count/parasite_total) * (host_count/host_total)	
    
    return resistance


#Returns an array of floats for a given column in a file assuming the columns are 
#seperated by spaces and the rows by new lines, and comments start with "#"
def get_avida_column(filename, column):
    #handle either .gz or non zipped files
    if filename.endswith('.gz'):
        f = gzip.open(filename)
    else:
        f = open(filename)
 
    content = f.read()
  
    #parse into 2d array
    content =  [i.strip().split() for i in content.split('\n') if len(i) > 1 and i[0] != "#"]

    #transpose the 2d array, so we can index the column directly
    content_transposed = transpose(content)
  
    return content_transposed[column]
    
    
folder = "Para_1.00_4/data/"
for i in range(0,100000,1000):
    for j in range(0, 100000, 1000):
        res = calculate_resistance("Para_1.00", 4, i, j)
        print i,j,res
        


