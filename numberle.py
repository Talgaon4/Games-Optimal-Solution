from tkinter import *
from tkinter import messagebox
from random import shuffle
from colors import Color

colors = Color()

BACKGROUND = colors.background
DIG_LENGTH = 4
DIGITS = "12345"
GUESSES = 6


class Numberle:
    def __init__(self, window):
        self.window = window
        self.window.title("Numberle")
        self.window.geometry('600x520')

        self.random_number_list = []
        self.random_number = ""
        self.create_random_number()

        self.user_guess = None
        self.guess_num = 1
        self.guesses_cnt = 0
        self.guess = None
        self.is_valid = True

        self.entry_frame = self.create_entry_frame()
        self.entry_frame.grid(row=1, column=0)
        self.grid_canvas = self.create_grid_canvas()
        self.grid_canvas.grid(row=0, column=0, pady=10)
        self.window.mainloop()

    def create_random_number(self):
        random_number_list = [1, 2, 3, 4, 5]
        shuffle(random_number_list)
        self.random_number_list = random_number_list[0:4]
        self.random_number = ""
        for i in range(DIG_LENGTH):
            self.random_number += str(self.random_number_list[i])

    def create_entry_frame(self):
        entry_frame = Frame(self.window, bg=BACKGROUND)

        self.guess = Entry(entry_frame)

        self.window.guess_img = PhotoImage(file='images/button_guess.png')
        self.window.new_game_img = PhotoImage(file="images/button_new-game152x53.png")
        self.window.return_menu_img = PhotoImage(file='images/button_menu.png')

        Label(image=self.window.guess_img)
        Label(image=self.window.new_game_img)
        Label(image=self.window.return_menu_img)

        word_guess_button = Button(entry_frame, image=self.window.guess_img, bg=BACKGROUND, bd=0,
                                   command=self.game)
        new_game_button = Button(entry_frame, image=self.window.new_game_img, bg=BACKGROUND, bd=0,
                                 command=self.new_game)
        return_menu_button = Button(entry_frame, image=self.window.return_menu_img, bg=BACKGROUND, bd=0,
                                    command=self.return_menu)

        self.guess.grid(row=0, column=2, padx=5, pady=10)
        word_guess_button.grid(row=0, column=3)
        new_game_button.grid(row=0, column=1, padx=5)
        return_menu_button.grid(row=0, column=0, padx=5)
        return entry_frame

    def create_grid_canvas(self):
        grid_canvas = Canvas(self.window, bg=BACKGROUND, width=435, height=420)
        x0, y0, x1, y1 = 5, 5, 65, 65
        space_x, space_y = 0, 0
        for row in range(GUESSES):
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

# Get a guess from the user and check if the guess is a valid guess.
    def get_guess(self):
        self.is_valid = True
        count = {}
        self.user_guess = str(self.guess.get())
        print(self.user_guess)
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
            messagebox.showinfo("Error", f"You number is to long, please insert a {DIG_LENGTH} digits number")
            self.is_valid = False

    def get_greens(self, random_num):
        green_digits = 0
        for i in range(DIG_LENGTH):
            if random_num[i] == self.user_guess[i]:
                green_digits += 1
        return green_digits

    def get_yellows(self, random_num):
        yellow_digits = 0
        for i in range(DIG_LENGTH):
            if self.user_guess[i] in random_num and self.user_guess[i] != random_num[i]:
                yellow_digits += 1
        return yellow_digits

    def game(self):
        g_y_list = [0, 0]
        if self.guesses_cnt < GUESSES:
            self.get_guess()
            print(f"2, {self.user_guess}, {self.random_number}")
            if not self.is_valid:
                return 0

            g_y_list[0] = self.get_greens(self.random_number)
            g_y_list[1] = self.get_yellows(self.random_number)
            x, y = 26, 20 + (self.guesses_cnt * 70)
            for i in range(DIG_LENGTH):
                label = Label(self.grid_canvas, text=self.user_guess[i])
                label.place(x=x, y=y)
                label.config(bg="#fb0", font="Ariel 15 bold")
                x += 70
            greens_label = Label(self.grid_canvas, text=g_y_list[0])
            yellow_labels = Label(self.grid_canvas, text=g_y_list[1])
            greens_label.place(x=x + 20, y=y)
            greens_label.config(bg="green", font="Ariel 15 bold")
            yellow_labels.place(x=x + 90, y=y)
            yellow_labels.config(bg="yellow", font="Ariel 15 bold")
            if g_y_list[0] == DIG_LENGTH:
                messagebox.showinfo("correct!", f"correct! the number was {self.random_number}")
            self.guesses_cnt += 1
            if self.guesses_cnt == GUESSES:
                messagebox.showinfo("You Lost", f"wrong! the number was {self.random_number}")

    def new_game(self):
        self.clear_window()
        self.window.title("Numberle")
        self.window.geometry('600x520')

        self.create_random_number()
        self.random_number_list = []
        self.random_number = ""

        self.user_guess = None
        self.guess_num = 1
        self.guesses_cnt = 0
        self.guess = None
        self.is_valid = True

        self.entry_frame = self.create_entry_frame()
        self.entry_frame.grid(row=1, column=0)
        self.grid_canvas = self.create_grid_canvas()
        self.grid_canvas.grid(row=0, column=0, pady=10)

    def return_menu(self):
        self.window.quit()

    def clear_window(self):
        for widget in self.window.winfo_children():
            widget.destroy()








