# Use this file to set network parameters (globally) 

# Define network setup
class Params:
	N = 4  			# Number of parties
	m = 5    		# Number of memories
	m_total = N*m   # Total number of memories
	p_del = 0.3  		# Probability of loss in quantum channel
	repetitions = 10000  	# Number of samples 
	graph_file = "Ex_A"		# Format: Adjacency matrix with m*N x m*N dimension, nodes without any edges are 
							# treated as non-existent. This format is important to know to which party a node
							# belongs (i.e. in case not all parties have the same number of nodes).
	graph_type = "random"   # Either random or neighboring
	graph_path = "Sample_graphs/" + graph_file + ".npy"
	num_workers = None      # Number of cores used for simulation runs



