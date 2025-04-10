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


def suggestion(board):
    s = Solver()
    available_cell = available_cells(board)
    state = 9 - len(available_cell) 
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
            pass
        else:
            cause.append(move)
        s.pop()
    if len(cause) >0:
        return cause
    else:
        string = "No suggestions Found!!"
        return string
    
def explain(board, row, column):
    s = Solver()
    available_cell = available_cells(board)
    state = 9 - len(available_cell)
    move = (row -1 , column -1)
    if move not in available_cell:
        print(f'Invalid move {move}')
        return
    print(f'Checking explain\n')
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
        return [(sug_i, sug_j)]
    else:
        return

    


if __name__ == "__main__":
    # Example usage
    board = [
        ['x', ' ', ' '],
        [' ', 'o', ' '],
        ['x', ' ', ' ']
    ]
    print(explain(board, 1,3))