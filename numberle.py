from tkinter import *
from tkinter import messagebox
from itertools import permutations
from random import shuffle

from colors import Color

colors = Color()

BACKGROUND = colors.background
DIG_LENGTH = 4
DIGITS = "12345"
GUESSES_LIMIT = 6


class Numberle:
    def __init__(self, window):
        self.window = window

        self.random_number_list = [1, 2, 3, 4, 5]  # this list will change latter
        self.random_number_str = ""
        self.create_random_number()
        self.g_y_history = []
        self.guesses_history_list = []
        self.temp_all_valid_permutations = []
        self.guesses_cnt = 0
        self.is_valid = True
        self.guess_entry = None
        self.user_guess = None

        self.all_valid = permutations(DIGITS, 4)  # all 4 digits permutations of 1,2,3,4,5
        self.all_valid_permutations = list(self.all_valid)

        self.entry_frame = self.create_entry_frame()
        self.grid_canvas = self.create_grid_canvas()

        self.grid_canvas.grid(row=0, column=0, pady=10)
        self.entry_frame.grid(row=1, column=0)

        self.window.mainloop()

    def create_random_number(self):
        """ Generates a random number of length 4 from the digits 1,2,3,4,5 without repetitions
            by shuffle the 1 to 5 list and slice the last index, than convert the list to a string"""
        shuffle(self.random_number_list)
        self.random_number_list = self.random_number_list[0:4]
        for i in range(DIG_LENGTH):
            self.random_number_str += str(self.random_number_list[i])

    def create_entry_frame(self):
        entry_frame = Frame(self.window, bg=BACKGROUND)

        self.guess_entry = Entry(entry_frame)

        self.window.guess_img = PhotoImage(file='images/button_guess.png')
        self.window.new_game_img = PhotoImage(file="images/button_new-game152x53.png")
        self.window.return_menu_img = PhotoImage(file='images/button_menu.png')
        self.window.best_guess_img = PhotoImage(file='images/button_best-guess.png')

        Label(image=self.window.guess_img)
        Label(image=self.window.new_game_img)
        Label(image=self.window.return_menu_img)
        Label(image=self.window.best_guess_img)

        word_guess_button = Button(entry_frame, image=self.window.guess_img, bg=BACKGROUND, bd=0,
                                   command=lambda val=False: self.game(val))
        new_game_button = Button(entry_frame, image=self.window.new_game_img, bg=BACKGROUND, bd=0,
                                 command=self.new_game)
        return_menu_button = Button(entry_frame, image=self.window.return_menu_img, bg=BACKGROUND, bd=0,
                                    command=self.return_menu)
        best_guess_button = Button(entry_frame, image=self.window.best_guess_img, bg=BACKGROUND, bd=0,
                                   command=lambda val=True: self.game(val))

        best_guess_button.grid(row=0, column=0, padx=5)
        return_menu_button.grid(row=0, column=1, padx=5)
        new_game_button.grid(row=0, column=2, padx=5)
        self.guess_entry.grid(row=0, column=3, padx=5, pady=10)
        word_guess_button.grid(row=0, column=4)

        return entry_frame

    def create_grid_canvas(self):
        """ Returns and create the grid canvas for display all the guesses.
            The values of X and Y were chosen by trial and error.
            """
        grid_canvas = Canvas(self.window, bg=BACKGROUND, width=435, height=420)
        x0, y0, x1, y1 = 5, 5, 65, 65
        space_x, space_y = 0, 0
        for row in range(GUESSES_LIMIT):
            for col in range(DIG_LENGTH):
                grid_canvas.create_rectangle(x0 + space_x, y0 + space_y, x1 + space_x, y1 + space_y,
                                             outline="#fb0", fill="#fb0")
                space_x += 70

            grid_canvas.create_rectangle(x0 + space_x + 20, y0 + space_y, x1 + space_x + 20, y1 + space_y,
                                         outline="green", fill="green")
            space_x += 70
            grid_canvas.create_rectangle(x0 + space_x + 20, y0 + space_y, x1 + space_x + 20, y1 + space_y,
                                         outline="yellow", fill="yellow")
            space_x = 0
            space_y += 70

        return grid_canvas

    def get_guess(self, is_best_move_guess):
        """ Get a guess from the user and check if the guess is a valid guess."""

        if not is_best_move_guess:  # is_best_move_guess True if the AI guessed the number, else False
            self.user_guess = str(self.guess_entry.get())
            self.check_guess_is_valid()
        else:  # if the AI guess and is it the first guess than guess random guess or 1234 in our case(improve latter)
            if self.guesses_cnt == 0:
                self.user_guess = "1234"
            else:  # get the guess from the AI
                self.user_guess = "".join(self.solver())

    def check_guess_is_valid(self):
        """ Checks if the guess is valid, if not displays a corresponding message."""
        self.is_valid = True
        count = {}
        for num in str(self.user_guess):
            if num in count:
                count[num] += 1
            else:
                count[num] = 1
            if num not in DIGITS:
                self.is_valid = False
                messagebox.showinfo("Error", f"You have to guess only  number with digits from {DIGITS}")
        for key in count:
            if count[key] > 1:
                self.is_valid = False
                messagebox.showinfo("Error", "Each digit can only appear once in a number")

        if len(self.user_guess) != DIG_LENGTH:
            messagebox.showinfo("Error", f"You number is to short/long, please insert a {DIG_LENGTH} digits number")
            self.is_valid = False

    def get_greens(self, random_num):
        """ Returns how many digits in the guess are in the correct place
            by comparing each digit in the guess to its corresponding index"""
        green_digits = 0
        for i in range(DIG_LENGTH):
            if random_num[i] == self.user_guess[i]:
                green_digits += 1
        return green_digits

    def get_yellows(self, random_num):
        """ and returns how many digits in a guess are found but not in the right place
            by checking each element to see if it is in the series but in a different index"""
        yellow_digits = 0
        for i in range(DIG_LENGTH):
            if self.user_guess[i] in random_num and self.user_guess[i] != random_num[i]:
                yellow_digits += 1
        return yellow_digits

    def game(self, is_best_move_guess):
        """ Gets the guess from the user/AI and displays it along with the greens and yellows"""
        g_y_list = [0, 0]
        if self.guesses_cnt < GUESSES_LIMIT:
            self.get_guess(is_best_move_guess)
            if not self.is_valid:
                return 0

            g_y_list[0] = self.get_greens(self.random_number_str)
            g_y_list[1] = self.get_yellows(self.random_number_str)

            self.g_y_history.append((g_y_list[0], g_y_list[1]))
            self.guesses_history_list.append(self.user_guess)

            x, y = 26, 20 + (self.guesses_cnt * 70)
            for i in range(DIG_LENGTH):
                label = Label(self.grid_canvas, text=self.user_guess[i])
                label.place(x=x, y=y)
                label.config(bg="#fb0", font="Ariel 15 bold")
                x += 70

            # creates a new labels every guess and display the amount of greens and yellows
            greens_label = Label(self.grid_canvas, text=g_y_list[0])
            yellow_labels = Label(self.grid_canvas, text=g_y_list[1])
            greens_label.config(bg="green", font="Ariel 15 bold")
            yellow_labels.config(bg="yellow", font="Ariel 15 bold")
            greens_label.place(x=x + 20, y=y)
            yellow_labels.place(x=x + 90, y=y)

            if g_y_list[0] == DIG_LENGTH:  # if there are 4 greens then the guess is correct
                messagebox.showinfo("correct!", f"correct! the number was {self.random_number_str}")
            elif self.guesses_cnt == GUESSES_LIMIT:  # if the user reach to the guesses limit than he lost
                messagebox.showinfo("You Lost", f"wrong! the number was {self.random_number_str}")
            self.guesses_cnt += 1

    def solver(self):
        """ Returns the best guess by going through the entire history of guesses
            and filtering guesses from the list of possible guesses
            according to the amount of green and yellow in each guess
            so that all remaining guesses are best guesses"""

        g_y_generator = self.greens_yellows_history()
        guesses_generator = self.guesses_history()

        for _ in range(len(self.g_y_history)):
            guess = next(guesses_generator)
            g0_y1 = next(g_y_generator)

            """ vals_list is a boolean list to help generate permutations according the amount of greens """
            vals_list = [i < g0_y1[0] for i in range(4)]

            self.temp_all_valid_permutations = []

            vals_permutations = permutations(vals_list, 4)
            vals_list = list(vals_permutations)

            """" Check for each valid permutation according the greens and yellows
                 if it match to the remaining available permutation
                 and add the permutation to a new valid permutation list: all_valid_permutations"""
            for permutation in self.all_valid_permutations:
                self.check_matches(guess, permutation, vals_list, g0_y1[0] + g0_y1[1])

            self.all_valid_permutations = set(self.temp_all_valid_permutations)  # deletes duplicates
            self.all_valid_permutations = list(self.all_valid_permutations)

        return self.all_valid_permutations[0]

    def check_matches(self, guess, curr, vals, g_y_sum):
        """ Check if the given permutation is good according al the checks and append that permutation to
            the valid permutation list.
            if the amount of greens and yellows are not 4 than the missing digit is 6 (simple and ugly solution)
            else we will filter all the permutation that include the missing digit. """
        missing_digit = ["6"]
        if g_y_sum == 4:
            s_guess = set(guess)
            missing_digit = [num for num in ["1", "2", "3", "4", "5"] if num not in s_guess]

        for i in range(len(vals)):
            if ((guess[0] == curr[0]) == vals[i][0]) and\
                    ((guess[1] == curr[1]) == vals[i][1]) and\
                    ((guess[2] == curr[2]) == vals[i][2]) and\
                    ((guess[3] == curr[3]) == vals[i][3]) and\
                    missing_digit[0] not in curr and\
                    guess != "".join(curr):

                self.temp_all_valid_permutations.append(curr)

    def greens_yellows_history(self):
        for g, y in self.g_y_history:
            yield [g, y]

    def guesses_history(self):
        for guess in self.guesses_history_list:
            yield guess

    def new_game(self):
        self.clear_window()

        self.random_number_list = [1, 2, 3, 4, 5]  # this list will change latter
        self.random_number_str = ""
        self.create_random_number()
        self.g_y_history = []
        self.guesses_history_list = []
        self.temp_all_valid_permutations = []
        self.guesses_cnt = 0
        self.is_valid = True
        self.guess_entry = None
        self.user_guess = None

        self.all_valid = permutations(DIGITS, 4)  # all 4 digits permutations of 1,2,3,4,5
        self.all_valid_permutations = list(self.all_valid)

        self.entry_frame = self.create_entry_frame()
        self.grid_canvas = self.create_grid_canvas()

        self.grid_canvas.grid(row=0, column=0, pady=10)
        self.entry_frame.grid(row=1, column=0)

    def return_menu(self):
        self.window.quit()

    def clear_window(self):
        for widget in self.window.winfo_children():
            widget.destroy()
