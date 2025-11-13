# Find matching using exact stratgey 

import numpy as np
import itertools
import networkx as nx 
from itertools import permutations 

from def_variables import * 
from Library import *

def get_exact_l(matr):

	# remove orphaned nodes
	matr = remove_orphaned_nodes(matr)
	matrix = matr.astype(int)
	G = nx.from_numpy_array(matrix)
	
	# get arrays each with filled nodes per party 
	filled_nodes_party_A = []
	filled_nodes_per_party = []
	number_filled_nodes_per_party = []
    
	for edge in G.edges():
		if edge[0] not in filled_nodes_party_A:
			filled_nodes_party_A.append(edge[0])

	filled_nodes_per_party.append(filled_nodes_party_A)
	number_filled_nodes_per_party.append(len(filled_nodes_party_A))

	for party in range (Params.N-1):
		filled_nodes_P_i_tmp = []
		for edge in G.edges():
			node = edge[1]
			if node >= (party+1)*Params.m and node < (party+2)*Params.m :
				if node not in filled_nodes_P_i_tmp:
					filled_nodes_P_i_tmp.append(node)
					

		filled_nodes_per_party.append(filled_nodes_P_i_tmp)
		number_filled_nodes_per_party.append(len(filled_nodes_P_i_tmp))

	# If one party has no filled memories, matching is empty -> cardinality is zero 
	if min(number_filled_nodes_per_party) == 0:
		return 0
	

	
	# Get all combinations of hyperedges including a center node C
	valid_hyperedges = []
	for mem in filled_nodes_party_A:
		edges_per_memory = []
		for edge in G.edges():
			if edge[0] == mem:
				edges_per_memory.append(edge)

		hyperedges = list(itertools.combinations(edges_per_memory, Params.N-1))
		
		# check that all peers have exactly one node in the hyperedge 
		for hyperedge in hyperedges:
			check = True
			party_list = [0] * Params.N 
			for idx in range(len(hyperedge)):
				node_B = hyperedge[idx][1]
				party = int(node_B/Params.m) 
				if party_list[party] == 0:
					party_list[party] = 1
				else:
					check = False
			if check:   
				valid_hyperedges.append(hyperedge)  

	counter = min(number_filled_nodes_per_party) # Maximum possible cardinality of matching
	
	# Start with l_max = min(number of filled nodes per party) and check for valid matching with |M| = l_max 
	while counter > 0:
		
		
		for matching_candidate in itertools.combinations(valid_hyperedges, counter): 
			nodes = []
			
			for hyperedge in matching_candidate:
				for edge in hyperedge:
					node_1 = edge[0]
					node_2 = edge[1]
					if node_1 not in nodes:
						nodes.append(node_1)
					if node_2 not in nodes:
						nodes.append(node_2)
						
			if len(nodes) == counter*Params.N:
				return len(matching_candidate)     
		
		counter -= 1
	return 0


def remove_orphaned_nodes(matr):

    # Delete all center nodes, that have no edge to at least one peer
    # Delete all peer nodes that have no connection to a center node
    delete_nodes = []
    
    # Go through A's nodes 
    for m_a in range(Params.m):
		# Go through all peers
        for party in range(1, Params.N):
            matr_party = matr[m_a][party*Params.m:(party+1)*Params.m]
			
			# Delete all entries in matr to delete remaining edges from note that is to be deleted 
            if matr_party.tolist().count(1) == 0:
                matr[m_a] = [0 if x==1 else x for x in matr[m_a]]
                if m_a not in delete_nodes:
                    delete_nodes.append(m_a)
    

    return matr        
        
