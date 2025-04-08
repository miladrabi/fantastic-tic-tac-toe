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

# Enable model construction
set_option(model=True)

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



# step must be one lower
def generate_wining_cond(step_vars: list, step: int) -> BoolRef:
    global BOARD_I
    global BOARD_J

    row_x = Or([
        And([step_vars[f'x_{i}_{j}_{step}'] for j in range(BOARD_J)]) for i in range(BOARD_I)
    ])
    col_x = Or([
        And([step_vars[f'x_{i}_{j}_{step}'] for i in range(BOARD_I)]) for j in range(BOARD_J)
    ])
    mdiag_x = And([step_vars[f'x_{i}_{i}_{step}'] for i in range(BOARD_I)])
    diag_x = And([step_vars[f'x_{i}_{BOARD_J - 1 - i}_{step}'] for i in range(BOARD_I)])

    row_o = Or([
        And([step_vars[f'o_{i}_{j}_{step}'] for j in range(BOARD_J)]) for i in range(BOARD_I)
    ])
    col_o = Or([
        And([step_vars[f'o_{i}_{j}_{step}'] for i in range(BOARD_I)]) for j in range(BOARD_J)
    ])
    mdiag_o = And([step_vars[f'o_{i}_{i}_{step}'] for i in range(BOARD_I)])
    diag_o = And([step_vars[f'o_{i}_{BOARD_J - 1 - i}_{step}'] for i in range(BOARD_I)])
    
    win_x = Or(row_x, col_x, mdiag_x, diag_x)
    win_o = Or(row_o, col_o, mdiag_o, diag_o)

    return And(win_x, Not(win_o))

# Encode the current state of the board as a constraint
def encode_board(board, bvars, step):
    # Board is a 3x3 array
    global BOARD_I
    global BOARD_J
    const = []
    for i in range(BOARD_I):
        for j in range(BOARD_J):
            if board[i][j] == 'x':
                const.append(bvars[f'x_{i}_{j}_{step}'])
                const.append(Not(bvars[f'o_{i}_{j}_{step}']))
            elif board[i][j] == 'o':
                const.append(bvars[f'o_{i}_{j}_{step}'])
                const.append(Not(bvars[f'x_{i}_{j}_{step}']))
            else:
                const.append(Not(bvars[f'x_{i}_{j}_{step}']))
                const.append(Not(bvars[f'o_{i}_{j}_{step}']))
    return And(const)


def check_wining_strategy(board, step):
    # Sanity check
    if step % 2 != 0 or step > 8:
        return -1
    
    global STEPS
    enc = True
    all_vars = []
    # TODO: We don't need all variables at this state. Delete those that are not used.
    for s in range(STEPS):
        all_vars.append(generate_vars_at_step(s))

    if step == 0:
        # Initial State condition
        enc = Not(Or(list(generate_vars_at_step(0).values())))
    else:
        enc = encode_board(board, all_vars[step], step)

    # Generate the constraint for the current move
    curr_move = generate_move_at_step('x', step, all_vars[step:(step + 2)])

    enc = And(enc, curr_move)

    if step == 8:
        # Final Step, No need to use a quantifier
        enc = And(enc, generate_wining_cond(all_vars[step + 1]))
    else:
        # We are going to build the constraint for the next move of the opponent
        enc_prime = None
        for k in range(STEPS - 1, step + 1, -1):
            if k == 9:
                enc_prime = Exists(list(all_vars[k].values()), And(generate_move_at_step('x', k - 1, all_vars[(k - 1):(k + 1)]), generate_wining_cond(all_vars[k], k)))
            else:
                if k % 2 == 0:
                    # Universal Quantifier
                    enc_prime = ForAll(list(all_vars[k].values()), Implies(generate_move_at_step('o', k - 1, all_vars[(k - 1):(k + 1)]), enc_prime))
                else:
                    if k >= 5:
                        enc_prime = Exists(list(all_vars[k].values()), And(generate_move_at_step('x', k - 1, all_vars[(k - 1):(k + 1)]), Or(generate_wining_cond(all_vars[k], k), enc_prime)))
                    else:
                        enc_prime = Exists(list(all_vars[k].values()), And(generate_move_at_step('x', k - 1, all_vars[(k - 1):(k + 1)]), enc_prime))
        enc = And(enc, enc_prime)

    return enc
    
def get_move_from_model(model):
    global BOARD_I
    global BOARD_J
    transition = {d.name(): str(model[d]) for d in model}
    # extract the states from variable names
    states = []
    for name in transition.keys():
        state = int(name[-1])
        if state not in states:
            states.append(state)

    # Sort the states
    states.sort()
    # Unpack
    s0, s1 = states
    # Moves - Might be more than one, which counts as an error
    moves = []
    for i in range(BOARD_I):
        for j in range(BOARD_J):
            x_cur = f'x_{i}_{j}_{s0}'
            x_nxt = f'x_{i}_{j}_{s1}'
            if transition[x_cur] != transition[x_nxt]:
                moves.append((i, j))
    assert len(moves) == 1, 'More than One valid move found - This might be an error!'
    return moves

if __name__ == '__main__':

    all_vars = []
    # TODO: We don't need all variables at this state. Delete those that are not used.
    for s in range(STEPS):
        all_vars.append(generate_vars_at_step(s))


    board = [
        ['x', ' ', ' '],
        [' ', 'o', ' '],
        ['o', ' ', 'x']
    ]

    enc = check_wining_strategy(board, 4)

    s = Solver()

    s.add(enc)

    res = s.check()

    model = s.model()

    print(get_move_from_model(model))