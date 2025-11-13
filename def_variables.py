# Use this file to set network parameters (globally) 

# Define network setup
class Params:
	N = 4  			# Number of parties
	m = 5    		# Number of memories
	m_total = N*m   # Total number of memories
	p = 0.7  		# Transmittivity in Quantum channel
	repetitions = 1000  # Number of samples 


graph_file = 'Sample_graphs/Ex_D.npy'		# Format: Adjacency matrix with m*N x m*N dimension, nodes without any edges are 
											# treated as non-existent. This format is important to know to which party a node
											# belongs (i.e. in case not all parties have the same number of nodes).




