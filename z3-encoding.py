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
            b_vars[f'x_{i}_{j}_{s}'] = Bool(f'x_{i}_{j}_{s}')
            b_vars[f'o_{i}_{j}_{s}'] = Bool(f'o_{i}_{j}_{s}')
    return b_vars

def generate_move_at_step(player, step, bvars):
    '''
        bvars containts the vars for this step and the next, indexed by 0 and 1.
    '''
    global BOARD_I
    global BOARD_J
    
    const = []

    for i in range(BOARD_I):
        for j in range(BOARD_J):
            cond = []
            for k in range(BOARD_I):
                for l in range(BOARD_J):
                    if i != k or j != l:
                        cond.append(bvars[0][f'x_{k}_{l}_{step}'] == bvars[1][f'x_{k}_{l}_{step + 1}'])
                        cond.append(bvars[0][f'o_{k}_{l}_{step}'] == bvars[1][f'o_{k}_{l}_{step + 1}'])
            
            cond.append(Not(bvars[0][f'x_{i}_{j}_{step}']))
            cond.append(Not(bvars[0][f'o_{i}_{j}_{step}']))
            if player == 'x':
                cond.append(Not(bvars[1][f'o_{i}_{j}_{step + 1}']))
                cond.append(bvars[1][f'x_{i}_{j}_{step + 1}'])
            else:
                cond.append(Not(bvars[1][f'x_{i}_{j}_{step + 1}']))
                cond.append(bvars[1][f'o_{i}_{j}_{step + 1}'])
            const.append(And(cond))

    return Or(const)



def generate_wining_cond(final_step_vars: list) -> BoolRef:
    global BOARD_I
    global BOARD_J
    global STEPS

    row = Or([
        And([final_step_vars[f'x_{i}_{j}_{STEPS - 1}'] for j in range(BOARD_J)]) for i in range(BOARD_I)
    ])
    col = Or([
        And([final_step_vars[f'x_{i}_{j}_{STEPS - 1}'] for i in range(BOARD_I)]) for j in range(BOARD_J)
    ])
    mdiag = And([final_step_vars[f'x_{i}_{i}_{STEPS - 1}'] for i in range(BOARD_I)])
    diag = And([final_step_vars[f'x_{i}_{BOARD_J - 1 - i}_{STEPS - 1}'] for i in range(BOARD_I)])
    return Or(row, col, mdiag, diag)


# List of all variables, paired by steps
all_vars = []
for s in range(STEPS):
    all_vars.append(generate_vars_at_step(s))

# Initial Condition: Every cell must be empty at step 0
init_cond = Not(Or(list(generate_vars_at_step(0).values())))

# Wining condition for X
x_wins = generate_wining_cond(generate_vars_at_step(STEPS - 1))

# Connecting all the pieces together
enc = None
for k in range(STEPS - 1, -1, -1):
    if k == 9:
        enc = Exists(list(all_vars[k].values()), And(generate_move_at_step('x', k-1, all_vars[(k - 1):(k + 1)]), generate_wining_cond(all_vars[k])))
    elif k != 0:
        if k % 2 == 0:
            # Universal Quantifier
            enc = ForAll(list(all_vars[k].values()), Implies(generate_move_at_step('o', k-1, all_vars[(k - 1):(k + 1)]), enc))
        else:
            enc = Exists(list(all_vars[k].values()), And(generate_move_at_step('x', k-1, all_vars[(k - 1):(k + 1)]), enc))
    else:
        enc = Exists(list(all_vars[k].values()), And(init_cond, enc))
