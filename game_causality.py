from z3_encoding import *

def print_board(board):
    for i in range(BOARD_I):
        print('\t' + ' | '.join(board[i]))
        if i != (BOARD_I - 1):
            print('\t' + '-' * 10)


def available_cells(board):
    return [(i, j) for i in range(len(board)) for j in range(len(board[i])) if board[i][j] == ' ']

def check_winner(board):
    def clean(cell):
        return cell.strip()

    for row in board:
        if clean(row[0]) != "" and clean(row[0]) == clean(row[1]) == clean(row[2]):
            return clean(row[0])

    for col in range(3):
        if clean(board[0][col]) != "" and clean(board[0][col]) == clean(board[1][col]) == clean(board[2][col]):
            return clean(board[0][col])

    if clean(board[0][0]) != "" and clean(board[0][0]) == clean(board[1][1]) == clean(board[2][2]):
        return clean(board[0][0])

    if clean(board[0][2]) != "" and clean(board[0][2]) == clean(board[1][1]) == clean(board[2][0]):
        return clean(board[0][2])

    return None

# Initialize an empty board
board = [
    [' ', ' ', ' '],
    [' ', ' ', ' '],
    [' ', ' ', ' ']
]




print('X always starts the game.')
print('To mark cell (i,j) enter `ij`, i.e. 12 means cell (1,2)')

s = Solver()

state = 0
while(True):
    print(state)
    print_board(board)
    player = 'x' if state % 2 == 0 else 'o'
    if state % 2 == 0 and state != 0:
        enc = check_wining_strategy(board, state)
        # Create a new scope and proceed
        s.push()
        s.add(enc)
        res = s.check()
        if res == sat:
            model = s.model()
            sug_i, sug_j = get_move_from_model(model)[0]
            print(f'Solver suggests you play: ({sug_i + 1}, {sug_j + 1})')
        else:
            print('No winning startegy available!')
        s.pop()
    elif state % 2 == 1: 
        available_cell = available_cells(board)
        print(f'Available cells: {available_cell}')
        print(f'Checking Hints for player O to win ...\n')
        cause = list()
        countefactual = list()
        for move in available_cell:
            i, j = [int(v) for v in move]
            tempboard = [row.copy() for row in board]
            tempboard[i][j] = 'o'
            enc = check_wining_strategy(tempboard, state+1)
            s.push()
            s.add(enc)
            res = s.check()
            if res == sat:
                model = s.model()
                sug_i, sug_j = get_move_from_model(model)[0]
                countefactual.append([move,(sug_i, sug_j)])
            else:
                cause.append(move)
            s.pop()
        if len(cause) == 1 :
            print(f'Actual Cause of not Loosing is: {(cause[0][0]+1 , cause[0][1]+1)}, if you play counterfactual moves: \n\n')
            for i,cf in enumerate(countefactual):
                print(f'{i+1} - Counterfactual move: {(cf[0][0]+1, cf[0][1]+1)} -> X has winning Startegy: {(cf[1][0]+1, cf[1][1]+1)} \n')
        elif len(cause) > 1:
            print(f'Disjunctive Actual Cause of not loosing are : {[(c[0]+1 , c[1]+1) for c in cause]}.\n\n')

        else:
            print(f'No Actual Cuase Found for not loosig.\n\n')


    move = input(f'\nYour move(Player {player.capitalize()}, Q to quit): ')
    if move in 'Qq':
        break
    i, j = [int(v) for v in move]
    board[i - 1][j - 1] = player
    state += 1
    winner = check_winner(board)
    if winner:
        print(f"\n\n################\n\n################\nWinner: {winner}")
        break
    else:
        continue