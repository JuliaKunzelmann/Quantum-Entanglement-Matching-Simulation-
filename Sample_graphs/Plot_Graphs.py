# Plot given example graphs 


import numpy as np
import matplotlib.pyplot as plt 
import networkx as nx


############ Plot graphs ###################

parties = 4
memories_per_party = 5

# Compute positions for drawing
pos = dict()
for i in range(0, parties*memories_per_party):
	if i//memories_per_party == 0:
		pos[i] = (0, i%memories_per_party)
	elif i//memories_per_party == 1:
		pos[i] = (1 + i%memories_per_party, -1)
	elif i//memories_per_party == 2:
		pos[i] = (memories_per_party + 1, i%memories_per_party)
	else:
		pos[i] = (1 + i%memories_per_party, memories_per_party)


colors = ['r'] * memories_per_party + ['b'] * memories_per_party + ['m'] * memories_per_party + ['y'] * memories_per_party

matr = np.load('Ex_D.npy')
matrix = matr.astype(int)
G1 = nx.from_numpy_array(matrix)

nx.draw(G1, pos=pos, with_labels=True, node_color = colors)
plt.show()
