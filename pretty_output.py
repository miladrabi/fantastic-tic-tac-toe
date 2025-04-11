from causal_intraction import explain, suggestion
from random import randint


position_encodings = [
    ['top left', 'top center', 'top right'],
    ['middle left', 'center', 'middle right'],
    ['bottom left', 'bottom center', 'bottom right']
]

suggestion_templates = [
    "I suggest you play %s.",
    "You should try the %s move.",
    "Consider playing at %s.",
    "My recommendation is to mark %s.",
    "Play your move at %s.",
    "How about placing your mark on %s?",
    "Have you thought about going for %s?",
    "I believe %s could be a great move!",
    "Trust me, %s is a solid choice.",
    "An optimal move would be to take %s.",
    "Analyzing your board, %s appears to be the strongest play.",
    "Considering your options, %s is a smart move.",
    "Given your situation, %s might be an intelligent choice."
]

explain_templates = [
    "Allowing your opponent to take %s will leave you with no path to force a win or even secure a draw.",
    "If your opponent plays %s, it leaves you unable to prevent a loss.",
    "Permitting your opponent to occupy %s creates a situation where you simply cannot counter their threat.",
    "The move %s is a critical spot: if your opponent claims it, they’ll block all your chances to defend effectively.",
    "Letting your opponent play %s opens up a winning line for them, while leaving you with no reliable counter.",
    "The control of %s by your opponent nullifies your best strategic efforts, preventing any chance at a tie or win.",
    "Once your opponent occupies %s, your winning chances vanish, as it effectively disrupts any chance to steer the game towards a draw.",
    "Allowing a move at %s transfers the strategic advantage to your opponent, rendering your position untenable.",
    "Avoid scenarios where your opponent can play %s; once they do, you’ll be left without any option to secure a win or even force a draw.",
    "By leaving %s available for your opponent, you give them the ability to control the game’s flow, leaving you with no realistic chance to win.",
    "Preventing your opponent from gaining %s is essential—if they occupy that spot, you won’t have a strategy left to avoid a loss."
]

free_moves_suggestions = [
    "You are free to make any move you choose, as none of them put you at a disadvantage.",
    "Feel free to pick any move—no choice here will hurt grant your opponent a win.",
    "Every move is safe in this situation, so go ahead and make the one that feels right.",
    "There’s no risk with any move you make, so trust your instincts and play the one you prefer.",
    "You have a completely free hand here—choose any move without worrying about negative effects.",
    "Since all options are equally safe, feel empowered to play whichever move suits you best.",
    "All moves are strategically neutral at this point, so you can select any move without impacting your overall position.",
    "Your performance won’t be hindered by any move; you’re free to experiment and choose as you like.",
    "No move creates a weakness in your gameplay at this stage, making every option a viable choice.",
    "Enjoy the freedom to choose any move—your performance remains strong regardless of your decision.",
    "There’s no wrong move in this scenario, so make your move with confidence and peace of mind.",
    "Your choice is entirely up to you since every move maintains your potential to win."
]

no_move_suggestions = [
    "No matter what move you make, it won’t be enough to avoid the inevitable defeat.",
    "Unfortunately, every option leads to a loss — there’s simply no move that can turn the tide.",
    "No move can save you now; the outcome is already sealed for a loss.",
    "It’s a lost cause from this point, as no action on your part can prevent the defeat.",
    "Every available move falls short; the loss is unavoidable regardless of your choice.",
    "Regrettably, the situation is beyond repair—a win or draw is out of reach no matter what you do."
]

def generate_explanation_for(board, pos):
    potential_moves = explain(board, pos)
    print('Eexplained: ', potential_moves)
    rand_idx = randint(0, len(free_moves_suggestions) - 1)

    if not potential_moves:
        return free_moves_suggestions[rand_idx]
    
    move = potential_moves[0]
    position = position_encodings[move[0]][move[1]]
    return explain_templates[rand_idx] % position

def generate_suggestion_for(board):
    sug_moves = suggestion(board)
    print('Suggested: ', sug_moves)
    rand_idx = randint(0, len(free_moves_suggestions) - 1)

    if not sug_moves:
        return no_move_suggestions[rand_idx]
    
    # Transform each position to its English encoding
    positions = list(map(lambda move: position_encodings[move[0]][move[1]], sug_moves))

    # Create a string from all positions
    s = None
    if len(positions) > 1:
        s = ', '.join(positions[:-1])
        s += ', or ' + positions[-1]
    else:
        s = positions[0]

    return suggestion_templates[rand_idx] % s


if __name__ == "__main__":
    # Example usage
    board = [
        ['x', ' ', ' '],
        [' ', ' ', ' '],
        [' ', ' ', ' ']
    ]
    print(generate_explanation_for(board, (2, 1)))
    print(generate_suggestion_for(board))