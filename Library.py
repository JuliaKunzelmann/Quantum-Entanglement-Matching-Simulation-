# Contains functions which are used by all strategies 


import numpy as np 
from def_variables import *

# Get all filled nodes from center party
def get_m_a(matr):
    filled_nodes_a = []
    # Iterate over A's nodes and check for any edge to P_i
    for m_a in range(m):
        edges_to_p_i = matr[m_a].tolist().count(1)
        if edges_to_p_i > 0:
            filled_nodes_a.append(m_a)
    
    return filled_nodes_a
    
     
# Get all filled nodes from peers 
def get_m_P_i(matr):
	filled_nodes_P_i = []
	# Check all memories of the peer nodes
	for m_i in range(m, m_total):
		edges_to_a = (matr[m_i]).tolist().count(1)
		if edges_to_a > 0:
			filled_nodes_P_i.append(m_i)

	return filled_nodes_P_i
	
	

    
# Remove filled nodes from peers that have no connections to center or center nodes that have no connection to at least one peer node     
def remove_orphaned_nodes(filled_nodes_a, matr):

    # Delete all center nodes, that have no edge to at least one peer
    # Delete all peer nodes that have no connection to a center node
    delete_nodes = []
    
    # Go through A's nodes 
    for m_a in filled_nodes_a:
		# Go through all peers
        for party in range(1, N):
            matr_party = matr[m_a][party*m:(party+1)*m]
			# Delete all entries in matr to delete remaining edges from note that is to be deleted 
            if matr_party.tolist().count(1) == 0:
                matr[m_a] = [0 if x==1 else x for x in matr[m_a]]
                if m_a not in delete_nodes:
                    delete_nodes.append(m_a)
    if delete_nodes != []:
        filled_nodes_a = list(set(filled_nodes_a) - set(delete_nodes))
    

    return filled_nodes_a, matr



# Check if given edges form a valid matching 
def check_for_matching(matr, filled_nodes_a):
	
	check = True
	for m_a in filled_nodes_a:
		for party in range(1, N):
			matr_party = matr[m_a][party*m:(party+1)*m]
			if matr_party.tolist().count(1) != 1: 
				check = False
				break

	return check
 


