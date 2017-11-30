import sys, gzip, random
from collections import defaultdict
from itertools import repeat
from scipy.stats import sem
from numpy import array, vectorize, mean
from ete3 import *

ORG_ID = 0
ORG_SOURCE = 1
ORG_PARENT_ID = 3
ORG_CUR_LIVING = 4
ORG_BORN = 11
ORG_DIED = 12

ORG_PHENOTYPE_ID = 0
ORG_PHENOTYPE_BIN_STR = 1

ABUNDANCE_THRESHOLD = 15

#detail file to do most of the work
DETAIL_FILENAME = "detail-100000.spop"

#for phenotype data, need some analyze mode data
#set this = none to avoid trying to add in phenotype data
#PHENOTYPE_FILE = "phylo_file.dat"
PHENOTYPE_FILE = "org_phenotypes.dat"


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
    content =  [i.strip().split() for i in content.split('\n') if len(i) > 1 and i[0] != "#"]
    content = [array(i[0:], str) for i in content]

    toReturn = [i[column] for i in content]
    return toReturn

org_id = get_avida_column(DETAIL_FILENAME, ORG_ID)
org_source = get_avida_column(DETAIL_FILENAME, ORG_SOURCE)
org_parent_id = get_avida_column(DETAIL_FILENAME, ORG_PARENT_ID)
org_currently_living = get_avida_column(DETAIL_FILENAME, ORG_CUR_LIVING)
org_update_born = get_avida_column(DETAIL_FILENAME, ORG_BORN)
org_update_died = get_avida_column(DETAIL_FILENAME, ORG_DIED)

if PHENOTYPE_FILE:
    org_phenotype_id = get_avida_column(PHENOTYPE_FILE, ORG_PHENOTYPE_ID)
    org_phenotype_bin_str = get_avida_column(PHENOTYPE_FILE, ORG_PHENOTYPE_BIN_STR)
    org_phenotype_dict = dict(zip(org_phenotype_id, org_phenotype_bin_str))


#setup a few dictionaries to aid in building the trees
children = defaultdict(list)
update_born = defaultdict(int)
currentl_living_counts = defaultdict(int)
below_threshold_orgs = []
above_threshold_orgs = []
parents = defaultdict(str)
for i in range(len(org_id)):
    if org_source[i].startswith("div:"):    
        update_born[org_id[i]] = int(org_update_born[i])
        currentl_living_counts[org_id[i]] = int(org_currently_living[i])
    
        if org_parent_id[i] == "(none)":
            org_parent_id[i] = "-1"
        
        children[org_parent_id[i]].append(str(org_id[i]))
        parents[org_id[i]] = str(org_parent_id[i])
        
#second pass required to do our own pruning, ETE's pruning is horrible
new_children = defaultdict(list)
for i in range(len(org_id)):
#    if len(children[org_id[i]]) == 0:
#        #and it has enough offspring...
    if currentl_living_counts[org_id[i]] > ABUNDANCE_THRESHOLD:
        #consider it one of the genotypes to keep
        above_threshold_orgs.append(str(org_id[i]))
            
#recursively add children map from the leaf nodes we want to include     
def build_new_children(leaf_node):
    if len(new_children[parents[leaf_node]]) > 0:
        new_children[parents[leaf_node]].append(leaf_node)
        return 
    else:
        new_children[parents[leaf_node]].append(leaf_node)
        build_new_children(parents[leaf_node])
    return
    
#do the recursion
for c in above_threshold_orgs:
    build_new_children(str(c))
    
     
            

#recursively build the tree
t = Tree()
def build_tree(tree_root, org_id):
    for c in new_children[org_id]:
        #distance is supposed to be "distance from node to parent",
        #I interpreted that as how old the child node is, but it is only one way to do this
        p = tree_root.add_child(name=c, dist=update_born[c] - update_born[org_id])
        
        #decorate the leaf nodes with their phenotype map
        if PHENOTYPE_FILE:
            if len(new_children[c]) == 0:
                p.add_face(SequenceFace(org_phenotype_dict[c], fsize=65, seqtype="aa", fg_colors={"0":"Grey", "1":"Red"}, bg_colors={"0":"White", "1":"White"}), column=0, position="aligned")
            
        build_tree(p, c)
                    
build_tree(t, '-1')


#decorate all nodes, including non-leaf nodes, with their abundance
for n in t.traverse():
    num_alive = currentl_living_counts[n.name]
    nstyle = NodeStyle()
    
    if num_alive == 0:
        nstyle["fgcolor"] = "black"
        nstyle["size"] = 5
    else:
        nstyle["size"] = num_alive*2
        nstyle["fgcolor"] = "green"
        
    n.set_style(nstyle)

#style the tree as a arc
ts = TreeStyle()
ts.show_leaf_name = False
ts.mode="c"
ts.arc_start = -165 # 0 degrees = 3 o'clock
ts.arc_span = 150
t.render("phylo-with_paras.pdf", w=5000, units="px", tree_style=ts)
