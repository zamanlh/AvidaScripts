import gzip
import sys
import random
from collections import defaultdict
from itertools import ifilter, repeat
from scipy.stats import sem
from numpy import array, vectorize, mean, log2, transpose

DETAIL_FILENAME = "detail-4500.spop"

ORG_SOURCE = 1
ORG_CUR_LIVING = 4
ORG_GENOME = 16
ORG_CELL_LIST = 17


#handle gzip files or non-gzip files
def open_file(file_name):
    if file_name.endswith('.gz'):
        f = gzip.open(file_name)
    else:
        f = open(file_name)
    
    return f
    
def get_avida_column(file_name, column):
    f = open_file(file_name)
    content = f.read()
    content =  [i.strip().split(' ') for i in content.split('\n') if len(i) > 1 and i[0] != "#"]
    content = [array(i[0:], str) for i in content]
    
    toReturn = []
    for row in content:
      if len(row) > column:
        toReturn.append(row[column])
      else:
        toReturn.append(None)
        
    return toReturn
    
org_source = get_avida_column(DETAIL_FILENAME, ORG_SOURCE)
org_currently_living = get_avida_column(DETAIL_FILENAME, ORG_CUR_LIVING)
org_seq = get_avida_column(DETAIL_FILENAME, ORG_GENOME)
org_cell_list = get_avida_column(DETAIL_FILENAME, ORG_CELL_LIST)

parasites = []
hosts = []
for i in range(len(org_source)):
  if int(org_currently_living[i]) > 0:
    if org_source[i].startswith("div"):
      hosts.append( (org_seq[i], org_cell_list[i].split(",")) )
    elif org_source[i].startswith("horz"):
      parasites.append( (org_seq[i], org_cell_list[i].split(",")) )
    else:
      print "Error: encountered unknown organism!"
      print org_source[i]
    
for h in hosts:
  for cell in h[1]:
    print "i InjectSequence {0} {1}".format(h[0], cell)
for p in parasites:
  for cell in p[1]:
    print "i InjectParasiteSequence {0} AABBB {1}".format(p[0], cell)
