# Quantum-Entanglement-Matching-Simulation
Supplementary material for our work `The Complexity of Matching in Multipartite
Quantum Routers`

# Installation

	git clone git@github.com:JuliaKunzelmann/Quantum-Entanglement-Matching-Simulation-.git
	cd Quantum-Entanglement-Matching-Simulation-
	python -m venv .venv
	source .venv/bin/activate
	pip install -r requirements.txt


# Usage

Basic usage is `python main.py`

This will run the simulation on sample graph Ex_A with N=4, m=5.

The following command line options exist:

--N    			(Number of parties, default 4)  
--m    			(Number of memories per party, default 5)  
--p-del   		(Qubit deletion probability, default 0.3)  
--reps 			(Number of iterations for the simulation, default 1000)  
--graph-file 	(File where the graph instance is located, default Ex_A)  
--graph-type	(Whether to create a 'random' or 'neighboring' graph, default "random")  
--num-workers   (How many cores to use for parallelizing the simulation)  


A new graph instance is only created when there is no instance found at the passed graph-file. When using an existing graph instance, make sure to pass the correct values for N and m of that graph.

For example, to create a random graph with N=3 and m=7 and run the simulation, call
`python main.py --N=3 --m=7 --graph-file="graphName" --graph-type="random"
`



Basic usage for Large-scale simulations is `python Run_Simulations.py`

The simulations consider

- N = 10, 20, 30, 40, 50 parties
- m = 10, 15, 20 memories per party
- rho = 0.2, 0.3, 0.4 for the sparse topologies
- p_del = 0, 0.05, 0.1, 0.2
- 10 independent base graphs and 5 realizations per base graph

The following router topologies are considered:

- Sparse Random
- Power-Law Center-Degree
- Fully Connected

The results are written to `Results_extended/results_large_N50_final.csv`

To analyze the results and generate the figures, run `python Analyze_Results.py`

The generated summaries and figures are stored in `Results_extended`.
