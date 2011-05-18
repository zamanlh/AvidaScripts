#!/usr/bin/env python

#usage: graphAvidaColumn.py <filename> <column>
#produces a simple line graph of this column

# Luis Zaman
# 5/18
import sys
from numpy import array
from matplotlib import pyplot
import gzip

#Returns an array of floats for a given column in a file 
#assuming the columns are seperated by spaces and the rows by new lines
#with # comment, and only numeric values (breaks with non-numeric values)
def get_avida_column(filename, column):
  #handle either .gz or non zipped files
  if filename.endswith('.gz'):
      f = gzip.open(filename)
  else:
      f = open(filename)
 
  content = f.read()
  content =  [i.strip().split() for i in content.split('\n') if len(i) > 1 and i[0] != "#"]
  content = [array(i[0:], float) for i in content]

  to_return = [i[column] for i in content]
  return to_return

#get command line args
filename = sys.argv[1]
column = int(sys.argv[2])

#get the column to graph
to_graph = get_avida_column(filename, column)

#graph it
pyplot.plot(to_graph)
pyplot.show()