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

a1 = 113
a2 = 887 
a3 = 0 
a4 = 0
a5 = 0 
a6 = 0

b1 = 108
b2 = 892
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


# p_del = 0.1

a1 = 852
a2 = 148 
a3 = 0 
a4 = 0
a5 = 0 
a6 = 0

b1 = 701
b2 = 298
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


# p_del = 0.2

a1 = 946
a2 = 54 
a3 = 0 
a4 = 0
a5 = 0 
a6 = 0

b1 = 807
b2 = 191
b3 = 2
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


# p_del = 0.3

a1 = 977
a2 = 23 
a3 = 0 
a4 = 0
a5 = 0 
a6 = 0

b1 = 853
b2 = 145
b3 = 2
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
#plt.show()




############# Example B ########################

x = np.linspace(0, 5, 6)
r = 1000

# p_del = 0

a1 = 912
a2 = 88 
a3 = 0 
a4 = 0
a5 = 0 
a6 = 0

b1 = 525
b2 = 475
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


# p_del = 0.1

a1 = 897
a2 = 103 
a3 = 0 
a4 = 0
a5 = 0 
a6 = 0

b1 = 625
b2 = 754
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

# p_del = 0.2

a1 = 957
a2 = 43
a3 = 0 
a4 = 0
a5 = 0 
a6 = 0

b1 = 761
b2 = 223
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


# p_del = 0.3

a1 = 989
a2 = 11
a3 = 0 
a4 = 0
a5 = 0 
a6 = 0

b1 = 845
b2 = 152
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
#plt.show()



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

b1 = 104
b2 = 896
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

# p_del = 0.1

a1 = 983
a2 = 17 
a3 = 0 
a4 = 0
a5 = 0 
a6 = 0

b1 = 549
b2 = 446
b3 = 5
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

# p_del = 0.2

a1 = 974
a2 = 26
a3 = 0 
a4 = 0
a5 = 0 
a6 = 0

b1 = 717
b2 = 276
b3 = 7
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

# p_del = 0.3

a1 = 982
a2 = 18
a3 = 0 
a4 = 0
a5 = 0 
a6 = 0

b1 = 878
b2 = 121
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
#plt.show()




############# Example D ########################

x = np.linspace(0, 5, 6)
r = 1000

# p_del = 0

a1 = 405
a2 = 595 
a3 = 0 
a4 = 0
a5 = 0 
a6 = 0

b1 = 176
b2 = 693
b3 = 131
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

# p_del = 0.1

a1 = 824
a2 = 176 
a3 = 0 
a4 = 0
a5 = 0 
a6 = 0

b1 = 556
b2 = 408
b3 = 36
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


# p_del = 0.2

a1 = 945
a2 = 55
a3 = 0 
a4 = 0
a5 = 0 
a6 = 0

b1 = 690
b2 = 291
b3 = 19
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

# p_del = 0.3

a1 = 987
a2 = 13 
a3 = 0 
a4 = 0
a5 = 0 
a6 = 0

b1 = 807
b2 = 184
b3 = 9
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
#plt.show()

















