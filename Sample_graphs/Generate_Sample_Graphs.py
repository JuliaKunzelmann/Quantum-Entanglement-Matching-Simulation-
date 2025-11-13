# Generate graphs of given size 
# Graph types: - only neighboring nodes are connected 
#			   - completely random connections 

import networkx as nx
import matplotlib.pyplot as plt
import numpy as np
from def_variables import Params

parties = Params.N
memories_per_party = Params.m

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

# Only neighboring nodes (direct, one up + one down)
G1 = nx.DiGraph()
G1.add_nodes_from(range(0, parties*memories_per_party))

for i in range(1, parties):
	for mem in range(memories_per_party):
		offset = i*memories_per_party
		G1.add_edge(mem, offset + mem) # direct neighbor
		if (offset + mem -1)//memories_per_party == i:
			G1.add_edge(mem, offset + mem - 1) # one up (if exists)
		if (offset + mem +1)//memories_per_party == i:
			G1.add_edge(mem, offset + mem + 1) # one down (if exists)

nx.draw(G1, pos=pos, with_labels=True)
plt.show()
array = nx.to_numpy_array(G1)
np.save(Params.graph_path, array)

# Random connections
G2 = nx.DiGraph()
G2.add_nodes_from(range(0, parties*memories_per_party))
for i in range(1, parties):
	for mem in range(memories_per_party):
		offset = i*memories_per_party
		for target in range(memories_per_party):
			if np.random.rand() < 0.4:
				G2.add_edge(mem, offset + target)

nx.draw(G2, pos=pos, with_labels=True)
plt.show()
array = nx.to_numpy_array(G2)
np.save(Params.graph_path, array)
