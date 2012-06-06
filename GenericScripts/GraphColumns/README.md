graph_columns.py - Graph One or More Columns of Data
====================================================

Written and maintained by [Luis Zaman](http://luiszaman.com) <zamanlui@msu.edu>

Prerequisites
-------------
This script requires python 2.7 or greater, numpy, and matplotlib

Example Usage
=============

Showing some basic functionality
--------------------------------
    ./graph_columns.py --data_file examples/parasite_phenotype_count.dat --x_label Updates --y_label "Shannon Diversity Index" --x_column 0 --columns 2 --grid --out_file sample1.png
 

Producing this figure:
![Sample 1](https://github.com/zamanlh/AvidaScripts/raw/master/GenericScripts/GraphColumns/examples/sample1.png)

Showing how to graph multiple columns at one
--------------------------------------------
    ./graph_columns.py --data_file examples/parasite_tasks.dat --x_label Updates --y_label "Number of Organisms"  --x_column 0 --columns 1 2 3 --column_labels "task NOT" "task NAND" "task AND" --log_x 

Producing this figure:
![Sample 2](https://github.com/zamanlh/AvidaScripts/raw/master/GenericScripts/GraphColumns/examples/sample2.png)


Example phase space plot 
------------------------
    ./graph_columns.py --data_file examples/parasite_phenotype_count.dat --x_label "Parasite Richness" --y_label "Parasite Shannon Diversity" --x_column 1 --columns 2 --grid --out_file sample3.png

Producing this figure:
![Sample 3](https://github.com/zamanlh/AvidaScripts/raw/master/GenericScripts/GraphColumns/examples/sample3.png)



