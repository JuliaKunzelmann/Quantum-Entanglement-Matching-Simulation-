# Quantum-Entanglement-Matching-Simulation-
Supplementary material for our work 'Opening the Black Box of Quantum Entanglement Matching'

# Installation
'''
git clone git@github.com:JuliaKunzelmann/Quantum-Entanglement-Matching-Simulation-.git
cd Quantum-Entanglement-Matching-Simulation-
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
'''

# Usage

Basic usage is 
'''
python main.py
'''
This will run the simulation on sample graph Ex_A with N=4, m=5.

The following command line options exist:

--N    			(Number of parties, default 4)
--m    			(Number of memories per party, default 5)
--p    			(Qubit transmission probability, default 0.7)
--reps 			(Number of iterations for the simulation, default 1000)
--graph-file 	(File where the graph instance is located, default Ex_A)
--graph-type	(Whether to create a 'random' or 'neighboring' graph, default "random")

A new graph instance is only created when there is no instance found at the passed graph-file. When using an existing graph instance, make sure to pass the correct values for N and m of that graph.

For example, to create a random graph with N=3 and m=7 and run the simulation, call
'''
python main.py --N=3 --m=7 --graph-file="graphName" --graph-type="random"
'''