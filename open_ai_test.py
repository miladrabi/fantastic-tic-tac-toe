from openai import OpenAI
import os
import json
def ask_ai(prompt):
    key = os.environ.get("OPENAI_API_KEY")
    client = OpenAI(api_key=key)

    def solve(location_row, location_col):
        print(f"Executing move: {location_row}, {location_col}")
        return f"Move executed at {location_row}, {location_col}"

    def next_move():
        print("Calculating the next move recommendation.")
        recommendation = "Consider placing your piece in the top-left corner."
        return recommendation

    def call_function(name, args):
        if name == "next_move":
            return next_move()
        elif name == "solve":
            location_row = args.get("location_row")
            location_col = args.get("location_col")
            return solve(location_row, location_col)

    messages = [
        {"role": "system", "content": "You simply need to extract the row and column from the user message for only 'what if ' moves and not 'instead of <location>' in tic-tac-toe and call the solver function, where top-middle is 1,2, or if the user wants help, call next_move."},
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
    prompt = "What would happen if I place my move in the bottom-right corner instead?"
    result = ask_ai(prompt)
    print(result)  