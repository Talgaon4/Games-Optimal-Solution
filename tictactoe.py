from tkinter import *
import tkinter as tk
from math import inf
from colors import Color

X_VAL = 1
O_VAL = -1

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
        "text": "⚫",
        "color": O_COLOR
    }
}


class TicTacToe:
    def __init__(self, window):
        self.window = window
        self.player_turn = 1  # 1 -> X turn, -1 -> O turn
        self.cells_buttons = []
        self.board = [[0] * 3 for _ in range(3)]  # 3x3 matrix of zeros

        self.menu_frame = self.create_menu()
        self.grid_frame = self.create_game_grid()
        self.message_frame = Frame(self.window, bg=BACKGROUND)

        self.display_message = tk.Label(self.window, font="Ariel 30", bg=BACKGROUND)
        self.display_message.grid(row=0, column=1, padx=120)

        self.menu_frame.grid(row=0, column=0, pady=150, padx=(40, 0), sticky=W)
        self.message_frame.grid(row=0, column=1)
        self.grid_frame.grid(row=0, column=2)

        self.window.mainloop()

    def create_game_grid(self):
        """ Creates a 3x3 grid of buttons for the TicTacToe game inside a frame and returns it"""
        grid_frame = Frame(self.window, bg=X_COLOR)
        for row in range(3):
            for col in range(3):
                button = Button(grid_frame, text="", font="Ariel", bg=GRID_COLOR,
                                fg="black", width=6, height=3, command=lambda val=(row, col): self.clicked_cell(val))
                self.cells_buttons.append(button)
                button.grid(row=row, column=col, padx=5, pady=5, sticky="nsew")
        return grid_frame

    def create_menu(self):
        """ Creates and places all the buttons needed to run the game inside a frame and returns it """
        menu_frame = Frame(self.window, bg=BACKGROUND)

        self.window.new_game_img = PhotoImage(file='images/button_new-game152x53.png')
        self.window.return_menu_img = PhotoImage(file='images/button_menu.png')
        self.window.optimal_move = PhotoImage(file='images/button_optimal-move183x53.png')

        Label(image=self.window.new_game_img)
        Label(image=self.window.return_menu_img)
        Label(image=self.window.optimal_move)

        new_game_button = tk.Button(menu_frame, image=self.window.new_game_img, bg=BACKGROUND, bd=0,
                                    command=self.new_game)

        return_menu_button = tk.Button(menu_frame, image=self.window.return_menu_img, bg=BACKGROUND, bd=0,
                                       command=self.return_to_menu)

        best_move = tk.Button(menu_frame, image=self.window.optimal_move, bg=BACKGROUND, bd=0,
                              command=self.get_best_move)

        return_menu_button.grid(row=0, column=0, pady=10)
        new_game_button.grid(row=1, column=0, pady=10)
        best_move.grid(row=2, column=0, pady=10)

        return menu_frame

    def clicked_cell(self, index):
        """ Handles a button press event,
        if the button pressed is empty then display the player's move on the screen
        and updates the board with the correct value for the current player's turn.
        At the end, calls display_result that displays a message if the game is over """
        row, col = index[0], index[1]
        if self.board[row][col] == 0:
            self.display_player_move(index)
            self.board[row][col] = self.player_turn
            self.player_turn *= -1  # change player's turn
            self.change_grid_color()
            self.display_game_over_result()

    def change_grid_color(self):
        """ Changes the color of the background according to the current player's turn"""
        if len(self.empty_cells()) == 0:
            self.grid_frame.config(bg="yellow")
        elif self.player_turn == 1:
            self.grid_frame.config(bg=X_COLOR)
        else:
            self.grid_frame.config(bg=O_COLOR)

    def display_game_over_result(self):
        """ Checks if the game is over and shows the winner or a draw on the screen """
        result = self.check_game_state()

        if result == 1:
            self.display_message.configure(text="X Won", fg=X_COLOR)
        elif result == -1:
            self.display_message.configure(text="O Won", fg=O_COLOR)
        elif len(self.empty_cells()) == 0:
            self.display_message.configure(text="Tie", fg="yellow")

    def display_player_move(self, index):
        """ Updates the move on the screen according to the received index and the current player's turn"""
        btn_index = index[0] * 3 + index[1]  # Convert an index of a 3x3 matrix to an index of a list of size 9
        clicked_btn = self.cells_buttons[btn_index]
        if self.player_turn == 1:
            text = PLAYER["player x"]["text"]
            color = PLAYER["player x"]["color"]
        else:
            text = PLAYER["player o"]["text"]
            color = PLAYER["player o"]["color"]
        clicked_btn.config(text=text, fg=color)

    def empty_cells(self):
        """ Returns list of cells with the value 0 (empty) in the board
        Using an index conversion from an index of a list of length 9 to an index of a 3x3 matrix"""
        return [[i // 3, i % 3] for i in range(9) if self.board[i // 3][i % 3] == 0]

    def check_game_state(self):
        """ Returns 1 or -1 if there is an X or O won respectively, 0 otherwise.
            win_state contains all possible winning states: the same value in row/column/diagonal"""
        win_state = [
            [self.board[0][0], self.board[0][1], self.board[0][2]],
            [self.board[1][0], self.board[1][1], self.board[1][2]],
            [self.board[2][0], self.board[2][1], self.board[2][2]],
            [self.board[0][0], self.board[1][0], self.board[2][0]],
            [self.board[0][1], self.board[1][1], self.board[2][1]],
            [self.board[0][2], self.board[1][2], self.board[2][2]],
            [self.board[0][0], self.board[1][1], self.board[2][2]],
            [self.board[2][0], self.board[1][1], self.board[0][2]], ]

        if [X_VAL, X_VAL, X_VAL] in win_state:  # X won
            return 1
        elif [O_VAL, O_VAL, O_VAL] in win_state:  # O Won
            return -1
        else:
            return 0

    def minimax(self, depth, player_turn):
        """ Minimax algorithm for finding the best current move"""
        best = [-1, -1, -player_turn * inf]  # -inf for player_turn == 1, else inf

        if depth == 0 or self.game_over():
            result = self.check_game_state()
            return [-1, -1, result]

        for cell in self.empty_cells():
            row, col = cell[0], cell[1]
            self.board[row][col] = player_turn

            minimax_result = self.minimax(depth - 1, -player_turn)
            self.board[row][col] = 0
            minimax_result[0], minimax_result[1] = row, col
            if player_turn == -1:
                if minimax_result[2] < best[2]:
                    best = minimax_result
            else:
                if minimax_result[2] > best[2]:
                    best = minimax_result
        return best

    def game_over(self):
        """Returns if the game is over"""
        return bool(self.check_game_state()) or len(self.empty_cells()) == 0

    def get_best_move(self):
        depth = len(self.empty_cells())  # The remaining of empty cells
        row, col, _ = self.minimax(depth, self.player_turn)  # the optimal move for computer
        self.clicked_cell([row, col])

    def clear_window(self):
        for widget in self.window.winfo_children():
            widget.destroy()

    def return_to_menu(self):
        self.window.quit()

    def new_game(self):
        self.clear_window()
        self.player_turn = 1
        self.cells_buttons = []
        self.board = [[0] * 3 for _ in range(3)]

        self.menu_frame = self.create_menu()
        self.grid_frame = self.create_game_grid()
        self.message_frame = Frame(self.window, bg=BACKGROUND)

        self.display_message = tk.Label(self.window, font="Ariel 30", bg=BACKGROUND)
        self.display_message.grid(row=0, column=1, padx=120)

        self.menu_frame.grid(row=0, column=0, pady=150, padx=(40, 0), sticky=W)
        self.message_frame.grid(row=0, column=1)
        self.grid_frame.grid(row=0, column=2)

