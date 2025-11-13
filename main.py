# Start the simulation

import numpy as np
from Simulation import * 
from def_variables import * 
from tqdm import tqdm

random.seed(5142412)
np.random.seed(412412)

l_S1 = [] 
l_S2 = []
l_exact = []

# Prepare histogram
c1 = [0]*(m+1)
c2 = [0]*(m+1)

for i in tqdm(range(repetitions)):
	l_1, l_2, l_opt = Simulate_single_repetition()
	l_S1.append(l_1)
	l_S2.append(l_2)
	l_exact.append(l_opt)

# Get average cardinality over all repetitions of exact matching 
print("Average (exact  algorithm): ", sum(l_exact)/repetitions)

for r in range(repetitions):
	assert l_S1[r] <= l_exact[r], "S1 found a larger matching than the exact. This hints at an error in the code"
	assert l_S2[r] <= l_exact[r], "S2 found a larger matching than the exact. This hints at an error in the code"

	c1[l_exact[r] - l_S1[r]] += 1
	c2[l_exact[r] - l_S2[r]] += 1


print("Strategy 1", c1)
print("Strategy 2", c2)
