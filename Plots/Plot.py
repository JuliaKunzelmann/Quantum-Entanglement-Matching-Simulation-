# Plot simulation results from concrete examples in paper  

import numpy as np
import matplotlib.pyplot as plt
from matplotlib.ticker import MaxNLocator
import networkx as nx


plt.rcParams.update({
    'font.size': 14,          
    'axes.titlesize': 15,     
    'axes.labelsize': 15,     
    'xtick.labelsize': 15,    
    'ytick.labelsize': 15,    
    'legend.fontsize': 15,    
    'figure.titlesize': 15    
})



############# Example A ########################

x = np.linspace(0, 5, 6)
r = 1000 

# p_del = 0

a1 = 136
a2 = 864
a3 = 0 
a4 = 0
a5 = 0 
a6 = 0

b1 = 129
b2 = 871
b3 = 0
b4 = 0 
b5 = 0
b6 = 0

plt.figure()

plt.scatter(x, [a1/r, a2/r, a3/r, a4/r, a5/r, a6/r], s=20, label='Strategy 1')
plt.scatter(x, [b1/r, b2/r, b3/r, b4/r, b5/r, b6], s=20, marker='x', label='Strategy 2')

plt.gca().xaxis.set_major_locator(MaxNLocator(integer=True))

plt.xlabel('Absolute error between heuristic and exact result') 
plt.ylabel('Proportion')

plt.grid(True)
plt.legend()
plt.savefig("Ex_A_p0.pdf")

# p_del = 0.1

a1 = 859
a2 = 141 
a3 = 0 
a4 = 0
a5 = 0 
a6 = 0

b1 = 707
b2 = 290
b3 = 3
b4 = 0 
b5 = 0
b6 = 0

plt.figure()

plt.scatter(x, [a1/r, a2/r, a3/r, a4/r, a5/r, a6/r], s=20, label='Strategy 1')
plt.scatter(x, [b1/r, b2/r, b3/r, b4/r, b5/r, b6], s=20, marker='x', label='Strategy 2')

plt.gca().xaxis.set_major_locator(MaxNLocator(integer=True))

plt.xlabel('Absolute error between heuristic and exact result') 
plt.ylabel('Proportion')

plt.grid(True)
plt.legend()
plt.savefig("Ex_A_p01.pdf")

# p_del = 0.2

a1 = 961
a2 = 39
a3 = 0 
a4 = 0
a5 = 0 
a6 = 0

b1 = 790
b2 = 209
b3 = 1
b4 = 0 
b5 = 0
b6 = 0

plt.figure()

plt.scatter(x, [a1/r, a2/r, a3/r, a4/r, a5/r, a6/r], s=20, label='Strategy 1')
plt.scatter(x, [b1/r, b2/r, b3/r, b4/r, b5/r, b6], s=20, marker='x', label='Strategy 2')

plt.gca().xaxis.set_major_locator(MaxNLocator(integer=True))

plt.xlabel('Absolute error between heuristic and exact result') 
plt.ylabel('Proportion')

plt.grid(True)
plt.legend()
plt.savefig("Ex_A_p02.pdf")

# p_del = 0.3

a1 = 983
a2 = 17
a3 = 0 
a4 = 0
a5 = 0 
a6 = 0

b1 = 857
b2 = 142
b3 = 1
b4 = 0 
b5 = 0
b6 = 0

plt.figure()
plt.legend()

plt.scatter(x, [a1/r, a2/r, a3/r, a4/r, a5/r, a6/r], s=20, label='Strategy 1')
plt.scatter(x, [b1/r, b2/r, b3/r, b4/r, b5/r, b6], s=20, marker='x', label='Strategy 2')

plt.gca().xaxis.set_major_locator(MaxNLocator(integer=True))

plt.xlabel('Absolute error between heuristic and exact result') 
plt.ylabel('Proportion')

plt.grid(True)



plt.legend()
plt.savefig("Ex_A_p03.pdf")




############# Example B ########################

x = np.linspace(0, 5, 6)
r = 1000

# p_del = 0

a1 = 914
a2 = 86
a3 = 0 
a4 = 0
a5 = 0 
a6 = 0

b1 = 531
b2 = 469
b3 = 0
b4 = 0 
b5 = 0
b6 = 0

plt.figure()

plt.scatter([0,1,2,3,4,5], [a1/r, a2/r, a3/r, a4/r, a5/r, a6/r], s=20, label='Strategy 1')
plt.scatter([0,1,2,3,4,5], [b1/r, b2/r, b3/r, b4/r, b5/r, b6], s=20, marker='x', label='Strategy 2')

plt.gca().xaxis.set_major_locator(MaxNLocator(integer=True))

plt.xlabel('Absolute error between heuristic and exact result') 
plt.ylabel('Proportion')

plt.grid(True)
plt.legend()
plt.savefig("Ex_B_p0.pdf")

# p_del = 0.1

a1 = 896
a2 = 104 
a3 = 0 
a4 = 0
a5 = 0 
a6 = 0

b1 = 599
b2 = 380
b3 = 21
b4 = 0 
b5 = 0
b6 = 0

plt.figure()

plt.scatter(x, [a1/r, a2/r, a3/r, a4/r, a5/r, a6/r], s=20, label='Strategy 1')
plt.scatter(x, [b1/r, b2/r, b3/r, b4/r, b5/r, b6], s=20, marker='x', label='Strategy 2')

plt.gca().xaxis.set_major_locator(MaxNLocator(integer=True))

plt.xlabel('Absolute error between heuristic and exact result') 
plt.ylabel('Proportion')

plt.grid(True)
plt.legend()
plt.savefig("Ex_B_p01.pdf")

# p_del = 0.2

a1 = 944
a2 = 56
a3 = 0 
a4 = 0
a5 = 0 
a6 = 0

b1 = 726
b2 = 258
b3 = 16
b4 = 0 
b5 = 0
b6 = 0

plt.figure()

plt.scatter(x, [a1/r, a2/r, a3/r, a4/r, a5/r, a6/r], s=20, label='Strategy 1')
plt.scatter(x, [b1/r, b2/r, b3/r, b4/r, b5/r, b6], s=20, marker='x', label='Strategy 2')

plt.gca().xaxis.set_major_locator(MaxNLocator(integer=True))

plt.xlabel('Absolute error between heuristic and exact result') 
plt.ylabel('Proportion')

plt.grid(True)
plt.legend()
plt.savefig("Ex_B_p02.pdf")

# p_del = 0.3

a1 = 977
a2 = 23
a3 = 0 
a4 = 0
a5 = 0 
a6 = 0

b1 = 833
b2 = 161
b3 = 3
b4 = 0 
b5 = 0
b6 = 0

plt.figure()

plt.scatter(x, [a1/r, a2/r, a3/r, a4/r, a5/r, a6/r], s=20, label='Strategy 1')
plt.scatter(x, [b1/r, b2/r, b3/r, b4/r, b5/r, b6], s=20, marker='x', label='Strategy 2')

plt.gca().xaxis.set_major_locator(MaxNLocator(integer=True))

plt.xlabel('Absolute error between heuristic and exact result') 
plt.ylabel('Proportion')

plt.grid(True)

plt.legend()
plt.savefig("Ex_B_p03.pdf")



############# Example C ########################

x = np.linspace(0, 5, 6)
r = 1000

# p_del = 0

a1 = 1000
a2 = 0
a3 = 0 
a4 = 0
a5 = 0 
a6 = 0

b1 = 73
b2 = 927
b3 = 0
b4 = 0 
b5 = 0
b6 = 0

plt.figure()

plt.scatter(x, [a1/r, a2/r, a3/r, a4/r, a5/r, a6/r], s=20, label='Strategy 1')
plt.scatter(x, [b1/r, b2/r, b3/r, b4/r, b5/r, b6], s=20, marker='x', label='Strategy 2')

plt.gca().xaxis.set_major_locator(MaxNLocator(integer=True))

plt.xlabel('Absolute error between heuristic and exact result') 
plt.ylabel('Proportion')

plt.grid(True)
plt.legend()
plt.savefig("Ex_C_p0.pdf")

# p_del = 0.1

a1 = 984
a2 = 16
a3 = 0 
a4 = 0
a5 = 0 
a6 = 0

b1 = 535
b2 = 457
b3 = 8
b4 = 0 
b5 = 0
b6 = 0

plt.figure()

plt.scatter(x, [a1/r, a2/r, a3/r, a4/r, a5/r, a6/r], s=20, label='Strategy 1')
plt.scatter(x, [b1/r, b2/r, b3/r, b4/r, b5/r, b6], s=20, marker='x', label='Strategy 2')

plt.gca().xaxis.set_major_locator(MaxNLocator(integer=True))

plt.xlabel('Absolute error between heuristic and exact result') 
plt.ylabel('Proportion')

plt.grid(True)
plt.legend()
plt.savefig("Ex_C_p01.pdf")

# p_del = 0.2

a1 = 984
a2 = 16
a3 = 0 
a4 = 0
a5 = 0 
a6 = 0

b1 = 746
b2 = 251
b3 = 3
b4 = 0 
b5 = 0
b6 = 0

plt.figure()
r = 1000
plt.scatter(x, [a1/r, a2/r, a3/r, a4/r, a5/r, a6/r], s=20, label='Strategy 1')
plt.scatter(x, [b1/r, b2/r, b3/r, b4/r, b5/r, b6], s=20, marker='x', label='Strategy 2')

plt.gca().xaxis.set_major_locator(MaxNLocator(integer=True))

plt.xlabel('Absolute error between heuristic and exact result') 
plt.ylabel('Proportion')

plt.grid(True)
plt.legend()
plt.savefig("Ex_C_p02.pdf")

# p_del = 0.3

a1 = 983
a2 = 17
a3 = 0 
a4 = 0
a5 = 0 
a6 = 0

b1 = 852
b2 = 148
b3 = 0
b4 = 0 
b5 = 0
b6 = 0

plt.figure()

plt.scatter(x, [a1/r, a2/r, a3/r, a4/r, a5/r, a6/r], s=20, label='Strategy 1')
plt.scatter(x, [b1/r, b2/r, b3/r, b4/r, b5/r, b6], s=20, marker='x', label='Strategy 2')

plt.gca().xaxis.set_major_locator(MaxNLocator(integer=True))

plt.xlabel('Absolute error between heuristic and exact result') 
plt.ylabel('Proportion')

plt.grid(True)

plt.legend()
plt.savefig("Ex_C_p03.pdf")




############# Example D ########################

x = np.linspace(0, 5, 6)
r = 1000

# p_del = 0

a1 = 390
a2 = 610 
a3 = 0 
a4 = 0
a5 = 0 
a6 = 0

b1 = 199
b2 = 680
b3 = 121
b4 = 0 
b5 = 0
b6 = 0

plt.figure()

plt.scatter(x, [a1/r, a2/r, a3/r, a4/r, a5/r, a6/r], s=20, label='Strategy 1')
plt.scatter(x, [b1/r, b2/r, b3/r, b4/r, b5/r, b6], s=20, marker='x', label='Strategy 2')

plt.gca().xaxis.set_major_locator(MaxNLocator(integer=True))

plt.xlabel('Absolute error between heuristic and exact result') 
plt.ylabel('Proportion')

plt.grid(True)
plt.legend()
plt.savefig("Ex_D_p0.pdf")

# p_del = 0.1

a1 = 860
a2 = 140
a3 = 0 
a4 = 0
a5 = 0 
a6 = 0

b1 = 553
b2 = 405
b3 = 42
b4 = 0 
b5 = 0
b6 = 0

plt.figure()

plt.scatter(x, [a1/r, a2/r, a3/r, a4/r, a5/r, a6/r], s=20, label='Strategy 1')
plt.scatter(x, [b1/r, b2/r, b3/r, b4/r, b5/r, b6], s=20, marker='x', label='Strategy 2')

plt.gca().xaxis.set_major_locator(MaxNLocator(integer=True))

plt.xlabel('Absolute error between heuristic and exact result') 
plt.ylabel('Proportion')

plt.grid(True)
plt.legend()
plt.savefig("Ex_D_p01.pdf")

# p_del = 0.2

a1 = 957
a2 = 43
a3 = 0 
a4 = 0
a5 = 0 
a6 = 0

b1 = 706
b2 = 276
b3 = 18
b4 = 0 
b5 = 0
b6 = 0

plt.figure()

plt.scatter(x, [a1/r, a2/r, a3/r, a4/r, a5/r, a6/r], s=20, label='Strategy 1')
plt.scatter(x, [b1/r, b2/r, b3/r, b4/r, b5/r, b6], s=20, marker='x', label='Strategy 2')

plt.gca().xaxis.set_major_locator(MaxNLocator(integer=True))

plt.xlabel('Absolute error between heuristic and exact result') 
plt.ylabel('Proportion')

plt.grid(True)
plt.legend()
plt.savefig("Ex_D_p02.pdf")

# p_del = 0.3

a1 = 984
a2 = 16
a3 = 0 
a4 = 0
a5 = 0 
a6 = 0

b1 = 816
b2 = 176
b3 = 8
b4 = 0 
b5 = 0
b6 = 0

plt.figure()

plt.scatter(x, [a1/r, a2/r, a3/r, a4/r, a5/r, a6/r], s=20, label='Strategy 1')
plt.scatter(x, [b1/r, b2/r, b3/r, b4/r, b5/r, b6], s=20, marker='x', label='Strategy 2')

plt.gca().xaxis.set_major_locator(MaxNLocator(integer=True))

plt.xlabel('Absolute error between heuristic and exact result') 
plt.ylabel('Proportion')

plt.grid(True)

plt.legend()
plt.savefig("Ex_D_p03.pdf")

















