# Start the simulation

import argparse
import numpy as np
from Simulation import * 
from tqdm import tqdm
from def_variables import *

random.seed(5142412)
np.random.seed(412412)

def main():
	parser = argparse.ArgumentParser(description="Override simulation parameters.")
	parser.add_argument("--N", type=int, default=Params.N)
	parser.add_argument("--m", type=int, default=Params.m)
	parser.add_argument("--p", type=float, default=Params.p)
	parser.add_argument("--reps", type=int, default=Params.repetitions)
	args = parser.parse_args()

	Params.N = args.N
	Params.m = args.m
	Params.m_total = Params.N * Params.m
	Params.p = args.p
	Params.repetitions = args.reps

	print("Running simulation with parameters:")
	print(f"N = {Params.N}")
	print(f"m = {Params.m}")
	print(f"p = {Params.p}")
	print(f"repetitions = {Params.repetitions}")

	l_S1 = [] 
	l_S2 = []
	l_exact = []

	# Prepare histogram
	c1 = [0]*(Params.m+1)
	c2 = [0]*(Params.m+1)

	for i in tqdm(range(Params.repetitions)):
		l_1, l_2, l_opt = Simulate_single_repetition()
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