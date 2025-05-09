import tkinter as tk
from tkinter import simpledialog, messagebox, font
#from open_ai_test import *

# Colors
PLAYER_X = '#c72c41'
PLAYER_O = '#fed053'
WINDOW_BACKGROUND = '#404040'
CHAT_BACKGROUND = '#717171'
TEXT_COLOR = 'white'
STATE_COLOR = 'grey'
GRID_COLOR = '#ffffff'
BUTTON_COLOR = 'white'
BUTTON_TEXT_COLOR = 'black'


def create_rounded_rect(canvas, x1, y1, x2, y2, radius=25, **kwargs):
    """
    Draws a rounded rectangle on the provided canvas from (x1, y1) to (x2, y2) with the given radius.
    """
    points = [
        x1+radius, y1,
        x2-radius, y1,
        x2, y1,
        x2, y1+radius,
        x2, y2-radius,
        x2, y2,
        x2-radius, y2,
        x1+radius, y2,
        x1, y2,
        x1, y2-radius,
        x1, y1+radius,
        x1, y1
    ]
    return canvas.create_polygon(points, smooth=True, **kwargs)

class RoundedButton(tk.Canvas):
    def __init__(self, master, width, height, radius=20,
                 bg_color="#171717",  # Black fill
                 fg_color="white",    # White text
                 text="",
                 font_spec=("Helvetica", 20, "bold"),
                 command=None,
                 state=None,
                 state_font=("Helvetica", 10),
                 state_color=STATE_COLOR,
                 **kwargs):
        # Set the border to 0 and background same as parent's bg
        tk.Canvas.__init__(self, master, width=width, height=height, bg=master["bg"],
                           highlightthickness=0, bd=0, **kwargs)
        self.width = width
        self.height = height
        self.radius = radius
        self.bg_color = bg_color
        self.fg_color = fg_color
        self.command = command
        self.font_spec = font_spec

        # Draw the rounded rectangle (we use the full widget size)
        self.round_rect = create_rounded_rect(self, 0, 0, width, height, radius,
                                               fill=bg_color, outline=bg_color)
        # Create text in the center
        self.text_item = self.create_text(width//2, height//2, text=text,
                                          fill=fg_color, font=font_spec)
        
        # If a state value is provided, display it in bottom right.
        if state is not None:
            self.state_item = self.create_text(width - 10, height - 10,
                                               text=str(state),
                                               fill=state_color,
                                               font=state_font,
                                               anchor="se")
        else:
            self.state_item = None

        # Bind click event
        self.bind("<Button-1>", self.on_click)
        # Also ensure clicks on drawn elements trigger the event
        # self.tag_bind(self.round_rect, "<Button-1>", self.on_click)
        self.tag_bind(self.text_item, "<Button-1>", self.on_click)
        
        if self.state_item:
            self.tag_bind(self.state_item, "<Button-1>", self.on_click)

    # Marks the state at the bottom right of each cell
    def set_state(self, new_state):
        if self.state_item is not None:
            self.itemconfigure(self.state_item, text=str(new_state))

    # Set the text color of the button dynamically
    def set_text_color(self, new_color):
        self.itemconfigure(self.text_item, fill=new_color)

    def on_click(self, event):
        if self.command:
            self.command()

    def set_text(self, new_text):
        self.itemconfigure(self.text_item, text=new_text)

    def get_text(self):
        return self.itemcget(self.text_item, "text")

class TicTacToeGUI(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Tic Tac Toe")
        self.configure(bg=WINDOW_BACKGROUND)
        self.geometry("1200x800")
        
        # Ask the player to choose X or O before starting.
        self.player_choice = self.ask_player_choice()
        self.board = [[' ' for _ in range(3)] for _ in range(3)]
        
        # state of the game
        self.state = 0
        
        # ----------------- Tic Tac Toe Board -----------------
        self.board_frame = tk.Frame(self, bg=WINDOW_BACKGROUND)
        self.board_frame.pack(pady=10)
        
        self.buttons = [[None for _ in range(3)] for _ in range(3)]
        button_size = 120  # width and height for board buttons
        
        for i in range(3):
            for j in range(3):
                # Create each rounded button with no padding between cells.
                btn = RoundedButton(self.board_frame,
                                    width=button_size,
                                    height=button_size,
                                    radius=20,
                                    bg_color=GRID_COLOR,
                                    fg_color="white",
                                    text="",
                                    font_spec=("Helvetica", 30, "bold"),
                                    command=lambda i=i, j=j: self.cell_clicked(i, j),
                                    state='-')
                btn.grid(row=i, column=j, padx=5, pady=5)
                self.buttons[i][j] = btn
                
        # Ensure the grid cells expand evenly if the frame is resized.
        for i in range(3):
            self.board_frame.grid_rowconfigure(i, weight=1)
            self.board_frame.grid_columnconfigure(i, weight=1)

        # ------------- Reset Button -------------
        reset_btn = RoundedButton(self,
                                  width=150,
                                  height=50,
                                  radius=20,
                                  bg_color=BUTTON_COLOR,
                                  fg_color=BUTTON_TEXT_COLOR,
                                  text="Reset Game",
                                  font_spec=("Helvetica", 14, "bold"),
                                  command=self.reset_game)
        reset_btn.pack(pady=(10, 20))

        # ----------------- Chat Area -----------------
        self.chat_frame = tk.Frame(self, bg=WINDOW_BACKGROUND)
        self.chat_frame.pack(padx=10, pady=(20, 10), fill="both", expand=True)
        
        chat_label = tk.Label(self.chat_frame, text="Have a question? Ask me!", bg=WINDOW_BACKGROUND,
                              fg=TEXT_COLOR, font=("Helvetica", 16))
        chat_label.pack(pady=(10, 5), anchor="w", padx=10)
        
        # Chat log with a light green background (or any color you prefer)
        self.chat_log = tk.Text(self.chat_frame, height=10, bg=CHAT_BACKGROUND, fg=TEXT_COLOR,
                                font=("Helvetica", 16), wrap="word", bd=0, relief="flat")
        self.chat_log.config(state="disabled")
        self.chat_log.pack(padx=10, pady=5, fill="both", expand=True)
        
        # Chat input field frame
        self.input_frame = tk.Frame(self.chat_frame, bg=WINDOW_BACKGROUND)
        self.input_frame.pack(padx=10, pady=10, fill="x")
        
        # Larger text input (use ipady for extra internal vertical space)
        self.chat_entry = tk.Entry(self.input_frame, font=("Helvetica", 16), bd=2, relief="flat")
        self.chat_entry.pack(side="left", fill="x", expand=True, ipady=6, padx=(0,10))
        self.chat_entry.bind("<Return>", lambda e: self.send_chat_command())
        
        send_btn = RoundedButton(self.input_frame,
                                 width=80,
                                 height=40,
                                 radius=10,
                                 bg_color=BUTTON_COLOR,
                                 fg_color=BUTTON_TEXT_COLOR,
                                 text="Send",
                                 font_spec=("Helvetica", 14, "bold"),
                                 command=self.send_chat_command)
        send_btn.pack(side="right")

    def ask_player_choice(self):
        """Prompt the user to choose X or O."""
        while True:
            answer = simpledialog.askstring("Player Choice", "Choose X or O:", parent=self)
            if answer is None:
                self.destroy()
                exit()
            answer = answer.strip().upper()
            if answer in 'xoXO':
                return answer.lower()
            else:
                messagebox.showerror("Invalid Input", "Please enter X or O.", parent=self)

    def cell_clicked(self, i, j):
        """Handle board button click."""
        btn = self.buttons[i][j]
        if btn.get_text() == "":
            current_symbol = self.player_choice
            btn.set_text(current_symbol)
            btn.set_state(self.state)
            if self.player_choice == 'x':
                btn.set_text_color(PLAYER_X)
            else:
                btn.set_text_color(PLAYER_O)
            self.board[i][j] = current_symbol
            self.player_choice = 'o' if current_symbol == 'x' else 'x'
            # Increment the state
            self.state += 1
        else:
            self.log_chat(f"Cell ({i}, {j}) is already taken.")

    def send_chat_command(self):
        """Send the command entered in the chat input."""
        command = self.chat_entry.get().strip()
        if command:
            self.process_command(command)
            self.chat_entry.delete(0, tk.END)

    def process_command(self, command):
        """Process chat commands."""
        self.log_chat('User: %s' % command)
        self.log_chat('Response: %s' % ask_ai(command, self.board))

    def log_chat(self, message):
        """Log a message in the chat log."""
        self.chat_log.config(state="normal")
        self.chat_log.insert(tk.END, message + "\n")
        self.chat_log.config(state="disabled")
        self.chat_log.see(tk.END)

    def reset_game(self):
        """Reset the board and optionally choose side again."""
        answer = messagebox.askyesno("Reset Game", "Do you want to choose X or O again?")
        if answer:
            self.player_choice = self.ask_player_choice()
        
        # Clear all buttons
        for i in range(3):
            for j in range(3):
                self.buttons[i][j].set_text("")
                self.buttons[i][j].set_state('-')

        # Clear the board
        self.board = [[' ' for _ in range(3)] for _ in range(3)]

        # Reset the state
        self.state = 0

        self.log_chat('#' * 100)
        self.log_chat("Game reset.")
        self.log_chat('#' * 100)



app = TicTacToeGUI()
app.mainloop()
