from z3 import *

'''
We assume X starts the game

x^s_{ij} specifies whether (i,j) contains an X after s moves
o^s_{ij} specifies whether (i,j) contains an O after s moves
Total: 90 variables required
'''

BOARD_I = 3
BOARD_J = 3
STEPS = 10

def generate_vars_at_step(s: int) -> list:
    global BOARD_I
    global BOARD_J
    
    b_vars = {}

    for i in range(BOARD_I):
        for j in range(BOARD_J):
            b_vars[f'x_{i}_{j}_{s}'] = Bool(f'x_{i + 1}_{j + 1}_{s}')
            b_vars[f'o_{i}_{j}_{s}'] = Bool(f'o_{i + 1}_{j + 1}_{s}')
    return b_vars


def generate_wining_cond(final_step_vars: list) -> BoolRef:
    global BOARD_I
    global BOARD_J
    global STEPS

    row = Or([
        And([final_step_vars[f'x_{i}_{j}_{STEPS - 1}'] for j in range(BOARD_J)]) for i in range(BOARD_I)
    ])
    col = Or([
        And([final_step_vars[f'x_{j}_{i}_{STEPS - 1}'] for i in range(BOARD_I)]) for j in range(BOARD_J)
    ])
    mdiag = And([final_step_vars[f'x_{i}_{i}_{STEPS - 1}'] for i in range(BOARD_I)])
    diag = And([final_step_vars[f'x_{i}_{BOARD_J - i}_{STEPS - 1}'] for i in range(BOARD_I)])
    return Or(row, col, mdiag, diag)


# List of all variables, paired by steps
all_vars = []
for s in range(STEPS):
    all_vars.append(generate_vars_at_step(s))

# Initial Condition: Every cell must be empty at step 0
init_cond = Not(Or(list(generate_vars_at_step(0).values())))

# Wining condition for X
x_wins = generate_wining_cond(generate_vars_at_step(STEPS - 1))