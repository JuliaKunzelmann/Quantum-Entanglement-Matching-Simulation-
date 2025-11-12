# Find matching using stratgey 1

import numpy as np 
import math 
from numpy.random import rand
import random
import networkx as nx 

from def_variables import * 
from Library import *



def Strategy_1(matr): 
	
	# Store edges and nodes for potential matching (contains marked edges and nodes)  
	edges_for_matching = []
	nodes_for_matching = []
	
	filled_nodes_a = get_m_a(matr)  
	filled_nodes_a, matr = remove_orphaned_nodes(filled_nodes_a, matr) 
	
	 
	checked = []
	
	repeat = True
	while repeat:
		repeat = False

		# Repeat, until no more changes are made 
		# Check edges from center to peers
		check_party_A = True
		while check_party_A:
			checked_nodes = []
			check_party_A = False
			filled_nodes_a, matr = remove_orphaned_nodes(filled_nodes_a, matr)
			# Check, if any node m_a has a single edge to a peer
			for m_a in filled_nodes_a:
				#  Only check nodes that haven't been checked before  
				if m_a in checked_nodes:
					continue

				else:
					# Go through all peers P_i
					for party in range(1, N):
						matr_party = matr[m_a][party*m:(party+1)*m]
						
						# If node m_a with single edge to one P_i found, add this edge to set of edges for matching
						if matr_party.tolist().count(1) == 1:
							checked.append(m_a)
							checked_nodes.append(m_a)
							
							# Get index of node in P_i
							idx = matr_party.tolist().index(1) 
							m_P = party*m + idx 
							
							# Save nodes and edges for matching
							if (m_a, m_P) not in edges_for_matching:
								edges_for_matching.append((m_a, m_P))
								repeat = True
								check_party_A = True
							if m_P not in nodes_for_matching:
								nodes_for_matching.append(m_P)
								nodes_for_matching.append(m_a)
								
							# Delete all other edges to the peer's node 
							for i in filled_nodes_a:
								if i != m_a:
									matr[i][m_P] = 0
							
							# Check again, if nodes in m_a have to be deleted 
							filled_nodes_a, matr = remove_orphaned_nodes(filled_nodes_a, matr)

		# Repeat the same for all peers P_i
		# Transpose matrix to go through all P_i
		matr_trans = matr.T
		
		# Find all filled nodes of peers P_i
		filled_nodes_P_i = get_m_P_i(matr_trans)

		# Repeat, until no more changes are made
		check_P_i = True
		checked_nodes_p_i = []

		while check_P_i:  
			check_P_i = False 
			# Check, if any node m_P has a single edge to the center
			for m_i in filled_nodes_P_i:
				if m_i in checked_nodes_p_i or m_i in nodes_for_matching:
					continue
					
				else:
					# If node m_P with single edge to C found, add this edge to set of edges for matching
					if matr_trans[m_i].tolist().count(1) == 1:
						checked_nodes_p_i.append(m_i)
						
						# Get index of node in P_i
						m_a = matr_trans[m_i].tolist().index(1)
						
						# Save nodes and edges for matching
						if (m_a, m_i) not in edges_for_matching:
							edges_for_matching.append((m_a, m_i))
							check_P_i = True
							repeat = True
						if m_a not in nodes_for_matching:
							nodes_for_matching.append(m_i)
							nodes_for_matching.append(m_a)
						party = int(m_i/m)
						
						
						# Delete all other edges from the center's node
						for i in range(len(matr_trans)):
							if i != m_i and int(i/m) == party :
								matr_trans[i][m_a] = 0
								
						# Check again, if nodes in m_a have to be deleted 
						filled_nodes_a, matr = remove_orphaned_nodes(filled_nodes_a, matr_trans.T)   

	# Check for matching 
	filled_nodes_a, matr = remove_orphaned_nodes(filled_nodes_a, matr)

	if check_for_matching(matr, filled_nodes_a):
		return matr, len(filled_nodes_a)
	
	# Solve matching by choosing random edge 
	else:
		for m_a in filled_nodes_a:
			for party in range(1, N):
				idx = []
				matr_party = matr[m_a][party*m:(party+1)*m]
				
				# Check that no other row has connection to the same m_P, otherwise delete connection and nodes
				if matr_party.tolist().count(1) == 1:
					tmp = matr_party.tolist().index(1)
					m_P = party*m + tmp
					for i in filled_nodes_a:
						if i != m_a:
							matr[i][m_P] = 0
					filled_nodes_a, matr = remove_orphaned_nodes(filled_nodes_a, matr)
				
				# Choose random connection from all possible ones 
				elif matr_party.tolist().count(1) > 1: 
					for j in range(m):
						if matr_party[j] == 1:
							idx.append(j)
					
					# Get chosen node m_P
					tmp = random.choice(idx)
					m_P = party*m + tmp
					
					# Delete all other edges to the peer's node 
					for i in filled_nodes_a:
						if i != m_a:
							matr[i][m_P] = 0
					
					# Delete all other edges from the center's node
					for i in range(m):
						if i != tmp:
							matr_party[i] = 0
					filled_nodes_a, matr = remove_orphaned_nodes(filled_nodes_a, matr)

		if check_for_matching(matr, filled_nodes_a):
			return matr, len(filled_nodes_a)

		else:
			raise Exception("PROBELM S1!!!")




    
    
    
    
    
    
    
    
    
    
    
    
