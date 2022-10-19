from tkinter import *
import random
import time
from colors import Color

colors = Color
BACK_GROUND = colors.background


class Simon:
    def __init__(self, window):
        self.window = window
        self.window.configure(bg=BACK_GROUND)
        self.score = 0
        self.high_score = self.get_high_score()
        self.buttons = []
        self.simon_sequence = []
        self.cur = 0
        self.grid_colors = ["#FFFDB7", "#AEF4A4", "#79B8D1", "#E36488"]

        self.score_msg = Label(self.window, text="Score: 0", font="Ariel 15 bold", bg=BACK_GROUND, fg="black")
        self.high_score_msg = Label(self.window, text=f"High Score: {self.high_score}", font="Ariel 15 bold", bg=BACK_GROUND, fg="black")
        self.game_over_msg = Label(self.window, text="", font="Ariel 20 bold", bg=BACK_GROUND, fg="red")

        self.grid_frame = self.create_game_grid()
        self.game_buttons_frame = self.create_game_buttons()

        self.high_score_msg.grid(row=0, column=0, pady=5)
        self.score_msg.grid(row=1, column=0, pady=2)
        self.grid_frame.grid(row=2, column=0, pady=5)
        self.game_over_msg.grid(row=3, column=0, pady=5)
        self.game_buttons_frame.grid(row=4, column=0)

        self.window.mainloop()

    def create_game_grid(self):
        """ Returns and creates a frame of 2x2 buttons in different colors"""
        grid_frame = Frame(self.window, bg=BACK_GROUND)
        for i in range(4):
            button = Button(grid_frame, bg=self.grid_colors[i], width=20, height=10,
                            command=lambda val=i: self.clicked_cell(val))
            self.buttons.append(button)
            if i < 2:
                button.grid(row=0, column=i, padx=5, pady=5)
            else:
                button.grid(row=1, column=i % 2, padx=5, pady=5)
        return grid_frame

    def create_game_buttons(self):
        """ Returns and creates a frame of buttons for all the necessary options"""
        game_buttons_frame = Frame(self.window)

        self.window.new_game_image = PhotoImage(file="images/button_new-game152x53.png")
        self.window.menu_image = PhotoImage(file="images/button_menu.png")

        Label(game_buttons_frame, image=self.window.new_game_image)
        Label(game_buttons_frame, image=self.window.menu_image)

        new_game_btn = Button(game_buttons_frame, bg=BACK_GROUND, bd=0, image=self.window.new_game_image,
                              command=self.start)
        menu_btn = Button(game_buttons_frame, bg=BACK_GROUND, bd=0, image=self.window.menu_image,
                          command=self.return_to_menu)

        menu_btn.grid(row=0, column=0)
        new_game_btn.grid(row=0, column=1)

        return game_buttons_frame

    def clicked_cell(self, cell):
        """ Checks whether the pressed button is the right button,
            if not ends the game,
            otherwise updates the result and the best result if necessary
            and increase the current index to the next index in the sequence.
            𝐜𝐮𝐫 is the current index that the user reached in the current sequence"""
        if cell != self.simon_sequence[self.cur]:  # check if the clicked cell is wrong
            self.game_over_msg.config(text="You Lost!")
        else:
            self.cur += 1  # the clicked cell is correct, move to the next one
            if self.cur == len(self.simon_sequence):  # The user clicked the entire current series
                self.score_msg.config(text=f"Score: {self.cur}")
                if self.cur > self.high_score:  # update high score if needed
                    self.high_score = self.cur
                    self.set_high_score(self.cur)
                    self.high_score_msg.config(text=f"High Score: {self.high_score}")
                self.cur = 0
                self.show_sequence()

    @staticmethod
    def get_high_score():
        high_score = 0
        try:
            with open("simon_high_score.txt", "r+") as f:
                high_score = int(f.read())

        except IOError:
            with open("simon_high_score.txt", "w+") as f:
                f.write('0')
        return high_score

    @staticmethod
    def set_high_score(score):
        with open("simon_high_score.txt", "w+") as f:
            f.write(f"{score}")

    def start(self):
        """ Resets all initial values and starts a new sequence"""
        self.score = 0
        self.simon_sequence = []
        self.cur = 0
        self.game_over_msg.config(text="")
        self.score_msg.config(text="Score: 0")
        self.show_sequence()

    def show_sequence(self):
        """ Adds one cell to the sequence and displays it by highlight the cell in sequence for one-second
            and update the grid frame each time"""
        self.simon_sequence.append(random.randint(0, 3))  # add new cell to the sequence

        self.grid_frame.update()
        time.sleep(1)
        for num in self.simon_sequence:
            self.buttons[num].config(bg="black")  # highlight the cell
            self.grid_frame.update()
            time.sleep(1)
            self.buttons[num].config(bg=self.grid_colors[num])  # cancel the highlight
            self.grid_frame.update()
            time.sleep(0.3)

    def return_to_menu(self):
        self.window.quit()
