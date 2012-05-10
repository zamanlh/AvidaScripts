#!/usr/bin/env python

#Luis Zaman
#5/9/12

from numpy import loadtxt, transpose
from matplotlib import pyplot
import argparse


#build the parser object for us
parser = argparse.ArgumentParser(description="Plots one or more columns from a typical Avida file")

#file to parse
parser.add_argument('-data_file', type=argparse.FileType('r'), help="the filename containing space delimited values to be plotted", required=True)
parser.add_argument('-x', type=int, help="Column to be used as the X values for the plot", required=True, nargs=1)
#label for the x-axis
parser.add_argument('-xlabel', type=str, help="x-axis label, if you need spaces you can quote the string", required=False, default="x-axis", nargs=1)
parser.add_argument('-ylabel', type=str, help="y-axis label, if you need spaces you can quote the string", required=False, default="y-axis", nargs=1)

#which columns to plot
parser.add_argument('-columns', type=int, help="Column to be used as the Y values for the plot", required=True, nargs="+")
#what to label those columns
parser.add_argument('-column_labels', type=str, help="Space delimited labels to be used for individual columns, if spaces are desired within labels the labels can be quoted", required=False, nargs="+", default=None)

#optional log axes 
parser.add_argument('-logx', help="Graph the x-axis on a log scale", required=False, default=False, action='store_true')
parser.add_argument('-logy', help="Graph the y-axis on a log scale", required=False, default=False, action='store_true')


args = parser.parse_args()


#load in the data, using the x-column and the columns to plot using numpy's handy loadtxt function
data_matrix = loadtxt(args.data_file, usecols=args.x + args.columns, unpack=True)

#plot the data we need, where x=the first row of the matrix, and the rest of the lines are
#the the rest of columns of the matrix.
plot_function = pyplot.plot


#ugly code to check which axes are transformed, and handles them appropriately
if args.logx and args.logy:
    plot_function = pyplot.loglog
elif args.logx or args.logy:
    if args.logx:
        plot_function = pyplot.semilogx
    else:
        plot_function = pyplot.semilogy

#plot using the appropriate function
plot_function(data_matrix[0], transpose(data_matrix[1:]))

#check if we need to label them, and if we do make sure we have the right number of labels
if args.column_labels:
    assert len(args.columns) == len(args.column_labels), 'Number of Columns and Column Labels do not match'
    pyplot.legend(args.column_labels)

#set labels
pyplot.xlabel(args.xlabel[0])
pyplot.ylabel(args.ylabel[0])

pyplot.show()