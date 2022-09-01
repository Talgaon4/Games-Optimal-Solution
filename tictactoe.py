from tkinter import *
import tkinter as tk
from colors import Color

colors = Color

BACKGROUND = colors.background
X_COLOR = colors.x_color
O_COLOR = colors.o_color
GRID_COLOR = colors.tte_grid_color
BG_GRID_COLOR = colors.tte_bg_grid_color

PLAYER = {"player x": {
    "text": "X",
    "color": X_COLOR
},
    "player o": {
        "text": "◯",
        "color": O_COLOR
    }
}


class TicTacToe:
    def __init__(self, window):
        self.window = window
        self.window.title("Tic Tac Toe")
        self.window.geometry('850x300')
        self.player = True
        self.cells_buttons = []
        self.board = [[0] * 3 for _ in range(3)]
        self.moves = []

        self.menu_frame = self.create_menu()
        self.grid_frame = self.create_game_grid()
        self.message_frame = Frame(self.window, bg=BACKGROUND)

        self.display_message = tk.Label(self.window, font="Ariel 30", bg=BACKGROUND)
        self.display_message.grid(row=0, column=1, padx=120)

        self.menu_frame.grid(row=0, column=0, padx=(40, 0), sticky=W)
        self.message_frame.grid(row=0, column=1)
        self.grid_frame.grid(row=0, column=2)

        self.window.mainloop()

    def create_game_grid(self):
        grid_frame = Frame(self.window, bg=BG_GRID_COLOR)
        for row in range(3):
            for col in range(3):
                button = Button(grid_frame, text="", font="Ariel", bg=GRID_COLOR,
                                fg="black", width=6, height=3, command=lambda val=(row, col): self.clicked_cell(val))
                self.cells_buttons.append(button)
                button.grid(row=row, column=col, padx=5, pady=5, sticky="nsew")
        return grid_frame

    def create_menu(self):
        menu_frame = Frame(self.window, bg=BACKGROUND)

        self.window.new_game_img = PhotoImage(file='images/button_new-game152x53.png')
        self.window.return_menu_img = PhotoImage(file='images/button_menu.png')

        Label(image=self.window.new_game_img)
        Label(image=self.window.return_menu_img)

        new_game_button = tk.Button(menu_frame, image=self.window.new_game_img, bg=BACKGROUND, bd=0,
                                    command=self.new_game)

        return_menu_button = tk.Button(menu_frame, image=self.window.return_menu_img, bg=BACKGROUND, bd=0,
                                       command=self.return_to_menu)

        new_game_button.grid(row=1, column=0, pady=10)
        return_menu_button.grid(row=0, column=0, pady=10)

        return menu_frame

    def clicked_cell(self, index):
        print(index)
        row = index[0]
        col = index[1]
        if self.board[row][col] == 0:
            self.display_player_move(index)
            self.board[row][col] = 1
            self.moves.append([row, col])
        self.check_game_state()

    def check_game_state(self):
        rows, cols = [0] * 3, [0] * 3
        diagonal_1 = 0
        diagonal_2 = 0
        player = 1
        for row, col in self.moves:
            rows[row] += player
            cols[col] += player
            if row == col:
                diagonal_1 += player
            if row + col == 2:
                diagonal_2 += player
            print(rows[row], cols[col], diagonal_1, diagonal_2)
            if abs(rows[row]) == 3 or abs(cols[col]) == 3 or abs(diagonal_1) == 3 or abs(diagonal_2) == 3:
                if player == 1:
                    self.display_message.configure(text="X Won", fg=X_COLOR)
                else:
                    self.display_message.configure(text="O Won", fg=O_COLOR)
                return 0
            player *= -1
        if len(self.moves) == 9:
            self.display_message.configure(text="Tie", fg="yellow")

    def display_player_move(self, index):
        # invert 3x3 matrix index to list at length of 9 index
        clicked_btn = self.cells_buttons[index[0] * 3 + index[1]]
        if self.player:
            text = PLAYER["player x"]["text"]
            color = PLAYER["player x"]["color"]
        else:
            text = PLAYER["player o"]["text"]
            color = PLAYER["player o"]["color"]
        self.player = not self.player
        clicked_btn.config(text=text, fg=color)

    def return_to_menu(self):
        self.window.quit()

    def new_game(self):
        self.clear_window()
        self.window.title("Tic Tac Toe")
        self.window.geometry('850x300')
        self.player = True
        self.cells_buttons = []
        self.board = [[0] * 3 for _ in range(3)]
        self.moves = []

        self.menu_frame = self.create_menu()
        self.grid_frame = self.create_game_grid()
        self.message_frame = Frame(self.window, bg=BACKGROUND)

        self.display_message = tk.Label(self.window, font="Ariel 30", bg=BACKGROUND)
        self.display_message.grid(row=0, column=1, padx=120)

        self.menu_frame.grid(row=0, column=0, padx=(40, 0), sticky=W)
        self.message_frame.grid(row=0, column=1)
        self.grid_frame.grid(row=0, column=2)

    def clear_window(self):
        for widget in self.window.winfo_children():
            widget.destroy()
