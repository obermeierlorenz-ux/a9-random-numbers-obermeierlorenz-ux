import numpy as np
import sys
import matplotlib.pyplot as plt 

M0 = 100_000
dt = 1.0
n_steps = 200

def validate_decay_inputs(M0, p, dt, n_steps):

    if not isinstance(M0,int) or M0 < 1:
        raise ValueError('M0 must be a positive integer.')

    if not isinstance(n_steps, int) or n_steps < 1:
        raise ValueError('n_steps must be a positive integer.')

    if not isinstance(p,(int, float)) or not 0 <= p < 1:
        raise ValueError('p must satisfy 0 <= p < 1.')

    if not isinstance(dt,(int, float)) or dt <= 0:
        raise ValueError('dt must be positive.')

time_values = np.arange(n_steps + 1) * dt

if len(sys.argv) > 1:
    seed = int(sys.argv[1])
else:
    seed = 44


def decay(M0, p, dt, n_steps, rng):

        validate_decay_inputs(M0, p, dt, n_steps)

        M = M0
        survivors = [M]


        for step in range(n_steps):

            u = rng.random(M)

            M = np.count_nonzero(u >= p)

            survivors.append(M)

        return np.array(survivors)



p_values = [0.10, 0.02]
rng = np.random.default_rng(seed)
print(f'Seed: {seed}')

all_runs = {}

for p in p_values:

    runs_for_p = []

    for run in range(5):

        survivors = decay(M0, p, dt, n_steps,rng)

        runs_for_p.append(survivors)

    all_runs[p] = runs_for_p




#estimate the half time

half_life_result = {}

for p in p_values: 

    runs_array = np.array(all_runs[p])

    #avverage population of each runs at every time
    average_population= np.mean(runs_array, axis = 0 )

    #sample time closest to M0/2
    half_population= M0/2 

    differences=np.abs(average_population - half_population)
    half_index = np.argmin(differences)
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



#decay probability, constn and expected population
#general plots
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


     # Get the measured half-life information
    half_index = half_life_result[p][1]
    measured_half_life = half_life_result[p][2]

    # Mark half of the initial population
    ax.axhline(
        M0 / 2,
        color='gray',
        linestyle=':',
        linewidth=2,
        label='M0 / 2'
    )

    # Mark measured half-life
    ax.axvline(
        measured_half_life,
        color='purple',
        linestyle='--',
        linewidth=2,
        label='Measured half-life'
    )

    # Mark the average population point used for the measurement
    ax.plot(
        measured_half_life,
        average_population[half_index],
        marker='o',
        color='purple',
        markersize=6
    )

    ax.set_xlabel('Time t (s)')
    ax.set_ylabel('Number of undecayed nuclei M')
    ax.set_title(f'Decay probability p = {p}, lambda ={decay_constant:.4f} 1/s')
    ax.grid()
    ax.legend()

plt.tight_layout()
plt.show()

#test
survivors = all_runs[0.10][0]
print()
print(np.all(survivors >= 0))
print(np.all(survivors <= M0))
print(np.all(np.diff(survivors) <= 0))

#p=0
test_p_zero = decay(M0, 0.0, dt, n_steps, rng)

print()
print(np.all(test_p_zero == M0))


# Test: an already extinct population remains extinct
M_empty = 0
empty_history = [M_empty]

for step in range(5):
    u = rng.random(M_empty)
    M_empty = np.count_nonzero(u >= 0.10)
    empty_history.append(M_empty)

print()
print(np.array(empty_history))