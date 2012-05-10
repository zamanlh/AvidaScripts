====================================================
graph_columns.py - Graph One or More Columns of Data
====================================================

:Created by:
    Luis Zaman <zamanlui@msu.edu>
:Website:
    https://github.com/zamanlh/AvidaScripts/tree/master/GenericScripts/GraphColumns

Prerequisites
=============
This script requires python 2.7 or greater, numpy, and matplotlib

Example Usage
=============

Showing some basic functionality
********************************
::

./graph_columns.py -data_file examples/parasite_phenotype_count.dat -xlabel Updates -ylabel "Shannon Diversity Index" -x 0 -columns 2
 

Producing `this figure
<https://github.com/zamanlh/AvidaScripts/blob/master/GenericScripts/GraphColumns/examples/sample1.png>`_.

Showing how to graph multiple columns at one (0s cause problems with the y-axis on a log scale)
***********************************************************************************************
::

./graph_columns.py -data_file examples/parasite_tasks.dat -xlabel Updates -ylabel "Number of Organisms"  -x 0 -columns 1 2 3 -column_labels NOT NAND AND -logy

Producing `this figure
<https://github.com/zamanlh/AvidaScripts/blob/master/GenericScripts/GraphColumns/examples/sample2.png>`_.
