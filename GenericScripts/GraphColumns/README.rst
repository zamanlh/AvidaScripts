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

./graph_columns.py --data_file examples/parasite_phenotype_count.dat --x_label Updates --y_label "Shannon Diversity Index" --x_column 0 --columns 2 --grid --out_file sample1.png
 

Producing `this figure
<https://github.com/zamanlh/AvidaScripts/blob/master/GenericScripts/GraphColumns/examples/sample1.png>`_.

Showing how to graph multiple columns at one (0s cause problems with the y-axis on a log scale)
***********************************************************************************************
::

./graph_columns.py --data_file examples/parasite_tasks.dat --x_label Updates --y_label "Number of Organisms"  --x_column 0 --columns 1 2 3 --column_labels "task NOT" "task NAND" "task AND" --log_x 

Producing `this figure
<https://github.com/zamanlh/AvidaScripts/blob/master/GenericScripts/GraphColumns/examples/sample2.png>`_.
