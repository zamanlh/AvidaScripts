#!/usr/bin/env python

#usage: graphAvidaColumn.py <filename> <column>
#produces a simple line graph of this column

# Luis Zaman
# 5/18
import sys
from numpy import array, transpose
from matplotlib import pyplot
import gzip

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
  
#get command line args
filename = sys.argv[1]
column = int(sys.argv[2])

#get the column to graph
to_graph = get_avida_column(filename, column)

#turn it into an array of floats (new matplotlib doesn't require this step)
to_graph = array(to_graph, float)

#graph it
pyplot.plot(to_graph)
pyplot.show()