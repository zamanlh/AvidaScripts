#!/usr/bin/env python

#usage: graphAvidaColumn.py <filename> <column>
#produces a simple line graph of this column

# Luis Zaman
# 5/18
import sys
from numpy import array
from matplotlib import pyplot
import gzip

filename = sys.argv[1]
column = int(sys.argv[2])

#handle either .gz or non zipped files
if filename.endswith('.gz'):
    f = gzip.open(filename)
else:
    f = open(filename)

#This part works only if everything is numeric in the file
#Read in file turning them into floats
content = f.read()
content =  [i.strip().split() for i in content.split('\n') if len(i) > 1 and i[0] != "#"]
content = [array(i[0:], float) for i in content]	
toGraph = [i[column] for i in content]

#graph it
pyplot.plot(toGraph)
pyplot.show()