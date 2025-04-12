from openai import OpenAI
import os
import json
import pretty_output

def ask_ai(prompt, board_pos):
    key = os.environ.get("OPENAI_API_KEY")
    client = OpenAI(api_key=key)

    def solve(location_row, location_col):
        return pretty_output.generate_explanation_for(board_pos, (location_row, location_col))

    def next_move():
        return pretty_output.generate_suggestion_for(board_pos)
    
    def compare_moves(moves):
        print ("Comparing moves...")
        for move in moves:
            location_row = move.get("location_row")
            location_col = move.get("location_col")
            print(f"Move: ({location_row}, {location_col})")
        return "Moves compared successfully."

    def call_function(name, args):
        if name == "next_move":
            return next_move()
        elif name == "solve":
            location_row = args.get("location_row")
            location_col = args.get("location_col")
            return solve(location_row, location_col)
        elif name == "compare_moves":
            moves = args.get("moves")
            return compare_moves(moves)

    messages = [
        {"role": "system", "content": "You simply need to extract the row and column from the user message for only 'what if?' moves and not 'instead of <location>' in tic-tac-toe and call the solver function, where top-middle is 1,2, or if the user wants help, call next_move. Also "},
        {"role": "user", "content": prompt}
    ]

    functions = [
        {
            "type": "function",
            "name": "solve",
            "description": "Place a move on the tic tac toe board.",
            "parameters": {
                "type": "object",
                "properties": {
                    "location_row": {
                        "type": "integer",
                        "description": "The board row location where the move should be placed (1-3 where 1 is the top row and 3 is the bottom row)"
                    },
                    "location_col": {
                        "type": "integer",
                        "description": "The board column location where the move should be placed (1-3 where 1 is the left column and 3 is the right column)"
                    }
                },
                "required": ["location_row", "location_col"],
                "additionalProperties": False
            }
        },
        {
            "type": "function",
            "name": "next_move",
            "description": "Suggest to the play which move to play next.",
            "parameters": None
        },
        {
            "type": "function",
            "name": "compare_moves",
            "description": "Compare two or more moves on the tic tac toe board and determine the best move, even comparing each spot in a row or column if requested.",
            "parameters": {
                "type": "object",
                "properties": {
                    "moves": {
                        "type": "array",
                        "description": "The moves to compare.",
                        "items": {
                            "type": "object",
                            "properties": {
                                "location_row": {
                                    "type": "integer",
                                    "description": "The board row location of the move (1-3 where 1 is the top row and 3 is the bottom row)"
                                },
                                "location_col": {
                                    "type": "integer",
                                    "description": "The board column location of the move (1-3 where 1 is the left column and 3 is the right column)"
                                }
                            },
                            "required": ["location_row", "location_col"],
                            "additionalProperties": False
                        }
                    }
                },
            "required": ["moves"],
            "additionalProperties": False
        }
        }
    ]

    # Make the API call with the messages and function definitions.
    response = client.responses.create(
        model="gpt-4o",          # Ensure you select a model that supports function calls.
        input=messages,
        tools=functions
    )

    # Extract the message from the response.
    print(response.output)

    for tool_call in response.output:
        if tool_call.type != "function_call":
            continue

        name = tool_call.name
        args = json.loads(tool_call.arguments)

        result = call_function(name, args)
        return result
    
if __name__ == "__main__":
    # Example usage
    prompt = "Is move (1,2) better than any move in the right column?"
    result = ask_ai(prompt, [])
    print(result)  