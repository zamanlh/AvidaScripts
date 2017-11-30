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
    phenotypes = list(get_valid_phenotypes(grid))
    
    #lets fake a sample of host and parasite phenotypes
    hosts = random.sample(phenotypes, 100)
    parasites = random.sample(phenotypes, 100)
    
    parasite_only_tasks =  [(int(hosts[i]) ^ int(parasites[i]))&int(parasites[i]) for i in xrange(len(hosts))]
    print parasite_only_tasks
    
    #ugly, but fast trick to turn any non-zero value into 1, and keep 0s 0
    #you can also just wrap the parasite_only_tasks comprehension in this to do it all in one pass
    parasite_infects =  [int(bool(p)) for p in parasite_only_tasks]
    print parasite_infects
    print mean(parasite_infects)
else:
    print "parasites did not persist"

    
    