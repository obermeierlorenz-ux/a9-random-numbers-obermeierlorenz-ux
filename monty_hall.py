import numpy as np
import sys

if len(sys.argv) > 1:
    k = int(sys.argv[1])
else:
    k = 10000

def monty_hall(k):

    N_doors = [2, 3, 10, 100]
    rng = np.random.defaul_rng(44)

    for N in N_doors:
        for iters in range(k):

            #arry erstllen in dem alle türeden sind also vill zero arry

            #random zahl von 1 bis N als intiger = price in array machen
            u = rng.intergers(1, N +1)
            Price = u
            #all N instead of u are goats in array machen 

            #random tür auswählen erster versuch
            t = rng.intergers(1, N+1)

            #für N gleich 2 hat man halt gewonnen wenn das gleich der price ist
            #für N größer 2 wird eine random tür ausgewählt und wenn die nicht gleich 
            #u ist wird sie geöffnet (aus dem array gestrichen) dann switchen mit random 
            #bedingung muss sein neu tür muss ungleich t sein 
            #wenn dann neu (n) = u ist gewonnen wenn nicht dann verloren
            

            

