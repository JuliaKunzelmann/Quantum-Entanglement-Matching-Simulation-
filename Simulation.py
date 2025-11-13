# Runs a single simulation (randomly determine which memories are filled and find matching using all three strategies)


import numpy as np 
import math 
from numpy.random import rand
import networkx as nx 
import matplotlib.pyplot as plt
from sympy import cos, nsolve, Symbol
from sympy.abc import x
import statistics as st
import copy
from matplotlib.ticker import MaxNLocator

from Strategy_1 import *
from Strategy_2 import *
from Strategy_exact import *
from def_variables import * 


def Simulate_single_repetition():

	# Load graph from file 
	matr = np.load(graph_file)
	matrix = matr.astype(int)
	G = nx.from_numpy_array(matrix)
	
	# "Delete" nodes in G to simulate transition loss (deletion means removing all edges from the node)
	p_delete = 1 - Params.p
	nodes_in_G = []
	for edge in G.edges(): # Append all nodes which have at least one edge
		if edge[0] not in nodes_in_G:
			nodes_in_G.append(edge[0])
		if edge[1] not in nodes_in_G:
			nodes_in_G.append(edge[1])
	
	for node in nodes_in_G:
		if rand() <= p_delete: # Toss a coin if qubit was lost in transition
			if node < Params.m:
				for i in range(Params.m_total):
					matr[node][i] = 0
			else:
				for i in range(Params.m):
					matr[i][node] = 0
	
	# Update graph from modified matrix
	matrix = matr.astype(int)
	G = nx.from_numpy_array(matrix)
	
	# Find matching using strategy 1 and strategy 2
	matr_copy = copy.deepcopy(matr) # Copy because subroutines modify matrix
	matrix_copy = matr_copy.astype(int)
	matr_1, l_S1 = Strategy_1(matr) # Strategy 1
	matr_2, l_S2 = Strategy_2(matr_copy) # Strategy 2
	
	# Find optimal matching
	l_bound = get_upper_bound(G)
	if l_S1 == l_bound or l_S2 == l_bound:
		l_opt = l_bound # A strategy already found optimum; save time
	else:
		l_opt = get_exact_l(matrix) # Otherwise: Exact algorithm

	# Return cardinalities of matchings found by strategy 1, strategy 2, and exact algorithm 
	return l_S1, l_S2, l_opt 

# Minimum over filled nodes per party as upper bound for cardinality     
def get_upper_bound(G):
	
	filled_nodes_party_A = []
	filled_nodes_per_party = []
	number_filled_nodes_per_party = []

	for edge in G.edges():
		if edge[0] not in filled_nodes_party_A:
			filled_nodes_party_A.append(edge[0])

	filled_nodes_per_party.append(filled_nodes_party_A)
	number_filled_nodes_per_party.append(len(filled_nodes_party_A))

	for party in range (Params.N-1):
		filled_nodes_B_tmp = []
		for edge in G.edges():
			node = edge[1]
			if node >= (party+1)*Params.m and node < (party+2)*Params.m :
				if node not in filled_nodes_B_tmp:
					filled_nodes_B_tmp.append(node)
					

		filled_nodes_per_party.append(filled_nodes_B_tmp)
		number_filled_nodes_per_party.append(len(filled_nodes_B_tmp))    
	
	return min(number_filled_nodes_per_party)

