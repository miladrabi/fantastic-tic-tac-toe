from z3_encoding import *

def print_board(board):
    for i in range(BOARD_I):
        print('\t' + ' | '.join(board[i]))
        if i != (BOARD_I - 1):
            print('\t' + '-' * 10)


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
            print('Your opponent still has a chance to not lose!')
        s.pop()
    move = input(f'\nYour move(Player {player.capitalize()}, Q to quit): ')
    if move in 'Qq':
        break
    i, j = [int(v) for v in move]
    board[i - 1][j - 1] = player
    state += 1
    if state > 9:
        print('End of the game!')
        break