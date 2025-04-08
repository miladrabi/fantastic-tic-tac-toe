from z3_encoding import *

def print_board(board):
    for i in range(BOARD_I):
        '|'.join(board[i])
    print()


# Initialize an empty board
board = [
    [' ', ' ', ' '],
    [' ', ' ', ' '],
    [' ', ' ', ' ']
]


print('X always starts the game.')
print('To mark cell (i,j) enter `ij`, i.e. 12 means cell (1,2)')


Quit = False
state = 0
while(not Quit):
    print_board(board)
    move = input('\nYour move: ')

s = Solver()

s.add(enc)

res = s.check()

print(res)

if res == sat:
    model = s.model()
    print(get_move_from_model(model))