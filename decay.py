import numpy as np
import sys
import matplotlib.pyplot as plt 

M0 = 100_000
dt = 1.0
n_steps = 200

time_values = np.arange(n_steps + 1) * dt


def decay(M0, p, dt, n_steps, rng):

        M = M0
        survivors = [M]


        for step in range(n_steps):

            u = rng.random(M)

            M = np.count_nonzero(u >= p)

            survivors.append(M)

        return np.array(survivors)



p_values = [0.10, 0.02]
rng = np.random.default_rng(44)

all_runs = {}

for p in p_values:

    runs_for_p = []

    for run in range(5):

        survivors = decay(M0, p, dt, n_steps,rng)

        runs_for_p.append(survivors)

    all_runs[p] = runs_for_p