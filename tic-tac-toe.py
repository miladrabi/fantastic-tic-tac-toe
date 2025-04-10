import tkinter as tk
from tkinter import simpledialog, messagebox, font
from open_ai_test import *

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
                 bg_color="#2ECC71",  # Green fill
                 fg_color="white",    # White text
                 text="",
                 font_spec=("Helvetica", 20, "bold"),
                 command=None, **kwargs):
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
        # Bind click event
        self.bind("<Button-1>", self.on_click)
        # Also ensure clicks on drawn elements trigger the event
        self.tag_bind(self.round_rect, "<Button-1>", self.on_click)
        self.tag_bind(self.text_item, "<Button-1>", self.on_click)

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
        self.configure(bg="white")
        self.geometry("400x600")
        
        # Ask the player to choose X or O before starting.
        self.player_choice = self.ask_player_choice()
        self.board = [[None for _ in range(3)] for _ in range(3)]
        
        # ----------------- Tic Tac Toe Board -----------------
        self.board_frame = tk.Frame(self, bg="white")
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
                                    bg_color="#2ECC71",
                                    fg_color="white",
                                    text="",
                                    font_spec=("Helvetica", 30, "bold"),
                                    command=lambda i=i, j=j: self.cell_clicked(i, j))
                btn.grid(row=i, column=j, padx=0, pady=0)
                self.buttons[i][j] = btn
                
        # Ensure the grid cells expand evenly if the frame is resized.
        for i in range(3):
            self.board_frame.grid_rowconfigure(i, weight=1)
            self.board_frame.grid_columnconfigure(i, weight=1)

        # ----------------- Chat Area -----------------
        self.chat_frame = tk.Frame(self, bg="white")
        self.chat_frame.pack(padx=10, pady=(20, 10), fill="both", expand=True)
        
        chat_label = tk.Label(self.chat_frame, text="Chat / Commands", bg="white",
                              fg="black", font=("Helvetica", 16))
        chat_label.pack(pady=(10, 5), anchor="w", padx=10)
        
        # Chat log with a light green background (or any color you prefer)
        self.chat_log = tk.Text(self.chat_frame, height=10, bg="#E8F8F2", fg="black",
                                font=("Helvetica", 12), wrap="word", bd=0, relief="flat")
        self.chat_log.config(state="disabled")
        self.chat_log.pack(padx=10, pady=5, fill="both", expand=True)
        
        # Chat input field frame
        self.input_frame = tk.Frame(self.chat_frame, bg="white")
        self.input_frame.pack(padx=10, pady=10, fill="x")
        
        # Larger text input (use ipady for extra internal vertical space)
        self.chat_entry = tk.Entry(self.input_frame, font=("Helvetica", 16), bd=2, relief="groove")
        self.chat_entry.pack(side="left", fill="x", expand=True, ipady=6, padx=(0,10))
        
        send_btn = RoundedButton(self.input_frame,
                                 width=80,
                                 height=40,
                                 radius=10,
                                 bg_color="#2ECC71",
                                 fg_color="white",
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
            if answer in ('X', 'O'):
                return answer
            else:
                messagebox.showerror("Invalid Input", "Please enter X or O.", parent=self)

    def cell_clicked(self, i, j):
        """Handle board button click."""
        btn = self.buttons[i][j]
        if btn.get_text() == "":
            btn.set_text(self.player_choice)
            self.log_chat(f"Player clicked cell ({i}, {j}).")
            self.process_move(i, j)
        else:
            self.log_chat(f"Cell ({i}, {j}) is already taken.")

    def process_move(self, i, j):
        """Placeholder for move processing (integrate your engine here)."""
        print(f"Processing move for cell: ({i}, {j})")

    def send_chat_command(self):
        """Send the command entered in the chat input."""
        command = self.chat_entry.get().strip()
        if command:
            self.log_chat(f"Command: {command}")
            self.process_command(command)
            self.chat_entry.delete(0, tk.END)

    def process_command(self, command):
        """Process chat commands."""
        self.log_chat(f"Processed command: {command}")

    def log_chat(self, message):
        """Log a message in the chat log."""
        self.chat_log.config(state="normal")
        self.chat_log.insert(tk.END, message + "\n")
        self.chat_log.config(state="disabled")
        self.chat_log.see(tk.END)


app = TicTacToeGUI()
app.mainloop()