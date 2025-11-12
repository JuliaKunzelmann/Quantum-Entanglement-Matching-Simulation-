# Find matching using stratgey 2

import numpy as np 
import math 
from numpy.random import rand
import random
import networkx as nx 

from def_variables import * 
from Library import * 


def Strategy_2(matr): 

	filled_nodes_a = get_m_a(matr)  
	filled_nodes_a, matr = remove_orphaned_nodes(filled_nodes_a, matr) 

	# Select edges at random
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
		raise Exception("PROBELM S2!!!")





































