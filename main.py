# Start the simulation

import numpy as np
from Simulation import * 
from def_variables import * 



l_S1 = [] 
l_S2 = []
l_exact = []

# Prepare histogram
c1 = [0]*(m+1)
c2 = [0]*(m+1)

for i in range(repetitions):
	print(str(int((i/repetitions)*100)) + "%", end="\r")
	l_1, l_2, l_opt = Simulate_single_repetition()
	l_S1.append(l_1)
	l_S2.append(l_2)
	l_exact.append(l_opt)
print()

# Get average cardinality over all repetitions of exact matching 
print("Average (exact  algorithm): ", sum(l_exact)/repetitions)

for r in range(repetitions):
	if l_S1[r] > l_exact[r] or l_S2[r] > l_exact[r]:
		print("Fehler", l_S1[r], l_S2[r], l_exact[r], r) # Inplausible values 
	else:
		c1[l_exact[r] - l_S1[r]] += 1
		c2[l_exact[r] - l_S2[r]] += 1


print(c1)
print(c2)
