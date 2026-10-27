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


#decay probability, constn and expected population
fig, axes = plt.subplots(1, 2, figsize=(11, 4))

for ax, p in zip(axes, p_values):

    # plot all five independent runs
    for run_number, survivors in enumerate(all_runs[p], start=1):

        # logarithmic plots cannt show zero values
        positive_values = survivors > 0

        ax.semilogy(
            time_values[positive_values],
            survivors[positive_values],
            label=f'Run {run_number}'
        )

    # expected population
    expected_population = M0 *(1 - p)**np.arange(n_steps + 1 )

    ax.semilogy(
        time_values,
        expected_population,
        color='black',
        linestyle='--',
        linewidth=2,
        label='Expected population'
    )

    
    #average population across the five runs
    runs_array = np.array(all_runs[p])

    average_population = np.mean(runs_array, axis=0)

    positive_average = average_population > 0

    ax.semilogy(
        time_values[positive_average],
        average_population[positive_average],
        color='red',
        linewidth=1.5,
        label='Average of 5 runs'
    )

    decay_constant = -np.log(1 - p) / dt

    ax.set_xlabel('Time t (s)')
    ax.set_ylabel('Remaining nuclei M')
    ax.set_title(f'Decay probability p = {p}, lambda ={decay_constant:.4f} 1/s')
    ax.grid()
    ax.legend()

plt.tight_layout()
plt.show()


#estimate the half time

half_life_result = {}

for p in p_values: 

    runs_array = np.array(all_runs[p])

    #avverage population of each runs at every time
    average_population= np.mean(runs_array, axis = 0 )

    #sample time closest to M0/2
    half_population= M0/2 

    differences=np.abs(average_population - half_population)
    half_index = np.armin(differences)
    measured_half_life = time_values[half_index]

    #decay constant
    decay_constant=-np.log(1 - p) / dt

    #predicted half life
    predicted_half_life = np.log(2) / decay_constant

    relative_difference = (measured_half_life- predicted_half_life) / predicted_half_life

    half_life_result[p] = (
         average_population,
         half_index, 
         measured_half_life,
         predicted_half_life, 
         decay_constant,
         relative_difference
    )

    print()
    print(f'p = {p}')
    print(f'lambda = {decay_constant:.6f} 1/s')
    print(f'predicted half-life = {predicted_half_life:.4f} s')
    print(f'measured half-life = {measured_half_life:.4f} s')
    print(f'relative difference = {relative_difference:.4%}')

    for ax, p in zip(axes, p_values):

        (
        average_population,
        half_index,
        measured_half_life,
        predicted_half_life,
        decay_constant,
        relative_difference
        ) = half_life_result[p]


        #plot

            # Half of the initial population
    ax.axhline(
        M0 / 2,
        color='gray',
        linestyle=':',
        linewidth=2,
        label='M0 / 2'
    )

    # Measured half-life
    ax.axvline(
        measured_half_life,
        color='purple',
        linestyle='--',
        linewidth=2,
        label='Measured half-life'
    )