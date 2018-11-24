import numpy as np
import pandas as pd
from matplotlib import pyplot
from ete3 import Tree, TreeStyle


saved_pop_file = "detail-200000.spop"

#Load only the relevant columns into a pandas DataFrame
saved_pop = pd.read_table(saved_pop_file, sep=" ", comment="#", usecols=[0,1,3,4,11,12], header=None, 
	names=["OrgID", "Source", "ParentID", "NumAlive", "UpdateActivated", "UpdateDeactivated"])

#Split up the hosts and parasites for convinence. 
saved_pop_hosts = saved_pop[saved_pop.Source.str.startswith("div:")]
saved_pop_parasites = saved_pop[saved_pop.Source.str.startswith("horz:")]


host_phylo = Tree()

#Recursively build the tree
def build_tree_recursive(current_bud_row, phylo_tree):
	new_node = phylo_tree.add_child(name=current_bud_row.OrgID)
	#lets save some extra info in the nodes just in case 
	new_node.add_features(Num_Alive=current_bud_row.NumAlive, 
		UpdateActivated=current_bud_row.UpdateActivated, 
		UpdateDeactivated=current_bud_row.UpdateDeactivated)

	if "UpdateActivated" in phylo_tree.features:
		new_node.dist = new_node.UpdateActivated - phylo_tree.UpdateActivated
	else:
		#We're at the root node
		new_node.dist = 0

	cur_node_id = str(current_bud_row.OrgID)

	for idx, new_row in saved_pop_hosts[saved_pop_hosts.ParentID.eq(cur_node_id)].iterrows():	
		build_tree_recursive(new_row, new_node)

	return new_node


root_node_row = saved_pop_hosts[saved_pop_hosts.ParentID == "(none)"].squeeze()
print("Building Tree")
build_tree_recursive(root_node_row, host_phylo)


print("Drawing Tree")
#Some drawing code
ts = TreeStyle()
ts.show_leaf_name = True
ts.mode = "c"
ts.arc_start = -180 # 0 degrees = 3 o'clock
ts.arc_span = 180
host_phylo.render("tree.png", tree_style=ts)

print("Saving Tree")
#Write the Newick Format Tree
host_phylo.write(format=1, outfile="avida_tree.nw")

