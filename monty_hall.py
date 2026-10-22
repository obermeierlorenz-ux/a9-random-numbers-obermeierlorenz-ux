import numpy as np
import sys

if len(sys.argv) > 1:
    k = int(sys.argv[1])
else:
    k = 10000

N_doors = [2, 3, 10, 100]

def monty_hall(k, N_doors):

    rng = np.random.defaul_rng(44)

    wins_per_N = []
    losses_per_N = []

    for N in N_doors:

        wins = 0
        losses = 0

        for iters in range(k):

            #arry erstllen in dem alle türeden sind also vill zero arry
            #all N instead of u are goats in array machen 
            doors = np.full(N, 'goat', dtype=object)

            
            #random zahl von 1 bis N als intiger = price in array machen
            u = rng.integers(1, N +1)
            doors[u] = 'prize'
            
            #beginn
            #random tür auswählen erster versuch
            t = rng.integers(1, N+1)

            while open == t:
                open = rng.integers(1, N+1)
                

            doors[open] = 'opend'

            if N != 2:

                while t2 == open and t2 == t:
                    t2 = rng.integer(1, N+1)
            else:
                pass

            if doors[t2] == 'prize':
                wins += 1
            else:
                losses += 1

        wins_per_N.append(wins)
        losses_per_N.append(losses)

    return wins_per_N, losses_per_N

wins_per_N, losses_per_N = monty_hall(k)

print('N values:',N_doors)
print('wins per N:', wins_per_N)
print('losses per N:', losses_per_N)




            
 
            

            

