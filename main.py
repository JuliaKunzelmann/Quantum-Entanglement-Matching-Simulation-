# Start the simulation

import os
import argparse
import numpy as np
from Simulation import * 
from tqdm import tqdm
from def_variables import *
from Generate_Sample_Graphs import create_graph

random.seed(5142412)
np.random.seed(412412)

def main():
	parser = argparse.ArgumentParser(description="Override simulation parameters.")
	parser.add_argument("--N", type=int, default=Params.N)
	parser.add_argument("--m", type=int, default=Params.m)
	parser.add_argument("--p-del", type=float, default=Params.p_del)
	parser.add_argument("--reps", type=int, default=Params.repetitions)
	parser.add_argument("--graph-file", type=str, default=Params.graph_file)
	parser.add_argument("--graph-type", type=str, default=Params.graph_type)
	args = parser.parse_args()


	Params.N = args.N
	Params.m = args.m
	Params.m_total = Params.N * Params.m
	Params.p_del = args.p_del
	Params.repetitions = args.reps
	Params.graph_file = args.graph_file
	Params.graph_path = "Sample_graphs/" + Params.graph_file + ".npy"
	Params.graph_type = args.graph_type

	print("Running simulation with parameters:")
	print(f"N = {Params.N}")
	print(f"m = {Params.m}")
	print(f"p-del = {Params.p_del}")
	print(f"repetitions = {Params.repetitions}")
	#print(f"Graph file: {Params.graph_file}")

	G = None
	if not os.path.exists(Params.graph_path):
		print("Did not find graph, creating new")
		# Create graph
		create_graph()

	# Load graph from file 
	matr = np.load(Params.graph_path)
	matrix = matr.astype(int)
	G = nx.from_numpy_array(matrix)
	print(f"Loaded graph from {Params.graph_path}")

	assert matr.shape == (Params.m_total, Params.m_total), f"Loaded graph does not match passed arguments N={Params.N} adn m={Params.m}]"
	l_S1 = [] 
	l_S2 = []
	l_exact = []

	# Prepare histogram
	c1 = [0]*(Params.m+1)
	c2 = [0]*(Params.m+1)

	for i in tqdm(range(Params.repetitions)):
		l_1, l_2, l_opt = Simulate_single_repetition(matr.copy(), G)
		l_S1.append(l_1)
		l_S2.append(l_2)
		l_exact.append(l_opt)

	# Get average cardinality over all repetitions of exact matching 
	print("Average cardinality (exact algorithm): ", sum(l_exact)/Params.repetitions)

	for r in range(Params.repetitions):
		assert l_S1[r] <= l_exact[r], "S1 found a larger matching than the exact. This hints at an error in the code"
		assert l_S2[r] <= l_exact[r], "S2 found a larger matching than the exact. This hints at an error in the code"

		c1[l_exact[r] - l_S1[r]] += 1
		c2[l_exact[r] - l_S2[r]] += 1

	print("Histograms of difference between exact and heuristic matching cardinality:")
	print("Strategy 1", c1)
	print("Strategy 2", c2)

if __name__ == "__main__":
	main()