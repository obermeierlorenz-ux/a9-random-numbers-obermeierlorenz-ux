import numpy as np
import sys
import matplotlib.pyplot as plt 

if len(sys.argv) > 1:
    k = int(sys.argv[1])
else:
    k = 10000

if len(sys.argv) > 2:
    seed = int(sys.argv[2])
else:
    seed = 44

rng = np.random.default_rng(seed)
print(f'Seed: {seed}')

N_doors = [2, 3, 10, 100]


def validate_monty_inputs(k, N_doors):

    if not isinstance(k, int) or k < 1:
        raise ValueError('k must be a positive integer.')

    for N in N_doors:
        if not isinstance(N, int) or N < 2:
            raise ValueError('Each number of doors must be an integer of at least 2.')


def monty_hall_switch(k, N_doors, rng):

    validate_monty_inputs(k, N_doors)

    wins_per_N = []
    losses_per_N = []
    switch_fractions_per_N = []

    for N in N_doors:

        wins = 0
        losses = 0
        win_fractions = []

        for iters in range(k):

            #arry erstllen in dem alle türeden sind also vill zero arry
            #all N instead of u are goats in array machen 
            doors = np.full(N, 'goat', dtype=object)

            
            #random zahl von 1 bis N als intiger = price in array machen
            u = rng.integers(N)
            doors[u] = 'prize'
            
            #beginn
            #random tür auswählen erster versuch
            t1 = rng.integers(N)

            opened_doors = []

            # Host opens N - 2 goat doors
            while len(opened_doors) < N - 2:

                opened_door = rng.integers(N)

                while (
                    opened_door == t1
                    or opened_door == u
                    or opened_door in opened_doors
                ):
                    opened_door = rng.integers(N)

                opened_doors.append(opened_door)
                doors[opened_door] = 'opened goat'


            # Find the one other unopened door
            for door in range(N):
                if door != t1 and door not in opened_doors:
                    t2 = door

            if doors[t2] == 'prize':
                wins += 1
            else:
                losses += 1

            win_fractions.append(wins / (iters + 1 ))

        switch_fractions_per_N.append(win_fractions)
        wins_per_N.append(wins)
        losses_per_N.append(losses)

    return wins_per_N, losses_per_N, switch_fractions_per_N

def monty_hall_stay(k, N_doors, rng):

    validate_monty_inputs(k, N_doors)

    wins_per_N = []
    losses_per_N = []
    stay_fractions_per_N = []

    for N in N_doors:

        wins = 0
        losses = 0
        win_fractions = []

        for iters in range(k):

            #arry erstllen in dem alle türeden sind also vill zero arry
            #all N instead of u are goats in array machen 
            doors = np.full(N, 'goat', dtype=object)

            
            #random zahl von 1 bis N als intiger = price in array machen
            u = rng.integers(N)
            doors[u] = 'prize'
            
            #beginn
            #random tür auswählen erster versuch
            t1 = rng.integers(N)

            if doors[t1] == 'prize':
                wins += 1
            else:
                losses += 1

            win_fractions.append(wins / (iters + 1 ))

        stay_fractions_per_N.append(win_fractions)
        wins_per_N.append(wins)
        losses_per_N.append(losses)

    return wins_per_N, losses_per_N, stay_fractions_per_N

switch_wins, switch_losses , switch_fractions_per_N = monty_hall_switch(k, N_doors, rng)
stay_wins, stay_loses, stay_fractions_per_N = monty_hall_stay(k, N_doors, rng)

print('N values:',N_doors)
print('wins per N:', switch_wins)
print('losses per N:', switch_losses)


#plot 1
trial_numbers = np.arange(1, k + 1)

fig, axes = plt.subplots(2, 2, figsize=(10, 7))

for ax, N, win_fractions in zip(
    axes.flat,
    N_doors,
    switch_fractions_per_N

):
    ax.semilogx(
        trial_numbers,
        win_fractions,
        label='Switch'
    )

    # Expected switch probability
    ax.axhline(
        (N - 1) / N,
        color='black',
        linestyle='--',
        label='Expected value'
    )

    ax.axhline(
    1 / N,
    color='gray',
    linestyle=':',
    label='Expected stay value'
)


    ax.semilogx(
    trial_numbers,
    stay_fractions_per_N[N_doors.index(N)],
    label='Stay'
)

    ax.set_xlabel('Trial number j')
    ax.set_ylabel('Win fraction')
    ax.set_title(f'N = {N}')
    ax.set_xlim(1, k)
    ax.set_ylim(0, 1)
    ax.grid()
    ax.legend()

plt.tight_layout()
plt.show()

print()
print(' N | Stay measured | Stay predicted | Switch measured | Switch predicted')
print('-' * 70)

for i, N in enumerate(N_doors):

    stay_measured = stay_wins[i] / k
    switch_measured = switch_wins[i] / k

    stay_predicted = 1 / N
    switch_predicted = 1 - (1 / N)

    print(
        f'{N:2d} | '
        f'{stay_measured:13.4f} | '
        f'{stay_predicted:14.4f} | '
        f'{switch_measured:15.4f} | '
        f'{switch_predicted:16.4f}'
    )

