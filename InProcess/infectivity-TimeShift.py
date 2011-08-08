#!/usr/local/epd/bin/python

import sys, gzip, random
from itertools import ifilter, repeat
from scipy.stats import sem
from numpy import array, vectorize

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

#fast sample routine, optimized strangely enough...
def get_sample(population, sample_size):
    #speedups
    n = len(population) - 1
    _random = random.randint
    return [population[_random(0,n)] for i in repeat(None, sample_size)]

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

def sample_infectivity(host_phenotypes, parasite_phenotypes, sample_size=100):
    #sample from host and parasite phenotypes
    hosts = get_sample(host_phenotypes, sample_size)
    parasites = get_sample(parasite_phenotypes, sample_size)
    
    #calculate overlaping phenotypes and percetage of sample that overlap
    overlap = [int(hosts[i]) & int(parasites[i]) for i in xrange(len(hosts))]
    percent_infective = (sample_size - list(overlap).count(0)) / float(sample_size)

    return percent_infective


class DataPoint():
    """Class that represents information to be sent to your 'compute' function"""
    def __init__(self, args):        
        #this is really it... you handle them how you want!
        #(my recommendation is to just make this a list of arguments)
        self.data = args
    def __str__(self):
        return 'DataPoint: %s' % (str(self.data)) 

def build_timeshift_grid(dir):    
    data_grid = []
    for paraUpdate in range(3000,200001,1000):
        row = []
        parasitefileName = '%s/data/grid_task_parasite.%d.dat.gz' % (dir,paraUpdate)
        for hostUpdate in range(3000,200001,1000):
            hostfileName = '%s/data/grid_task_hosts.%d.dat.gz' % (dir,hostUpdate)
        
            row.append(DataPoint([parasitefileName, hostfileName]))
        data_grid.append(row)
    
    return data_grid
     

def infectivity(data_point): 
    _data = data_point.data
    print _data[0]
    
    #get the grids for the two parameters
    h = get_grid(_data[1])
    p = get_grid(_data[0])
    
    #flatten grid into list
    h = list(array(h).ravel())
    p = list(array(p).ravel())
    
    #filter out 0s and -1s (so we're left with just hosts and parasites that were alive at particular update)
    h = ifilter(lambda x: x != "-1" and x != "0", h)
    p = ifilter(lambda x: x !="-1" and x != "0", p)
    
    return sample_infectivity(list(h), list(p), 10000)
    
    
v_infectivity = vectorize(infectivity)
infectivity_grid = v_infectivity(build_timeshift_grid(sys.argv[1]))
f_out = open('%s.dat' % (sys.argv[2]), 'w')
f_out.write(str(infectivity_grid.tolist()))
f_out.close()




        




