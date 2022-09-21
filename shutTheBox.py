from tkinter import *
import tkinter as tk
import random
from colors import Color

BOX_LENGTH = 9

colors = Color

BACKGROUND = colors.background
OPEN_CARD = colors.open_card
CLOSED_CARD = colors.closed_card


class ShutTheBox:

    def __init__(self, window):
        self.window = window
        self.available_cards = [True] * 9
        self.is_first_roll = True
        self.can_roll_again = True
        self.can_roll_1 = False
        self.already_choose_card = False
        self.cards_buttons = []
        self.dice_sum_left = 0
        self.dice_sum = 0
        self.dice_sum_used = 0
        self.open_cards = set()

        self.messages_window = tk.Frame(self.window, bg=BACKGROUND, bd=0)
        self.menu_frame = self.create_menu_frame()
        self.cards_frame = self.create_cards()

        self.dice_display = Label(self.messages_window, font="Ariel 60", bg=BACKGROUND)
        self.sum_left = Label(self.messages_window, font="Ariel 20 bold", bg=BACKGROUND)
        self.dice_sum_text = Label(self.messages_window, font="Ariel 20 bold", bg=BACKGROUND)
        self.opt_move_txt = Label(self.messages_window, font="Ariel 20 bold", bg=BACKGROUND, fg="blue")

        self.grid_frames_labels()

        self.window.mainloop()

    def grid_frames_labels(self):
        self.menu_frame.grid(column=0, row=0, pady=50, padx=(40, 0), sticky=W)
        self.messages_window.grid(column=1, row=0, pady=10, padx=(0, 150))

        self.sum_left.grid(row=0, column=0)
        self.dice_display.grid(row=1, column=0)
        self.dice_sum_text.grid(row=2, column=0)
        self.opt_move_txt.grid(row=3, column=0)

        self.cards_frame.grid(column=0, row=1, pady=(20, 0), columnspan=2)

    def create_cards(self):
        self.cards_frame = tk.Frame(self.window, bg=BACKGROUND, bd=0)

        for col in range(BOX_LENGTH):
            card_button = tk.Button(self.cards_frame, text=f"{col + 1}", font="Ariel 9", fg="white", width=9,
                                    height=6, bg=OPEN_CARD, bd=2, command=lambda val=col: self.card_down(val))
            card_button.grid(row=0, column=col + 1, padx=10)
            self.cards_buttons.append(card_button)

        return self.cards_frame

    def create_menu_frame(self):
        self.menu_frame = tk.Frame(self.window, bg=BACKGROUND, bd=0)

        self.window.new_game_img = PhotoImage(file='images/button_new-game152x53.png')
        self.window.rol_1_img = PhotoImage(file='images/button_roll91x53.png')
        self.window.rol_2_img = PhotoImage(file='images/button_roll94x53.png')
        self.window.opt_img = PhotoImage(file='images/button_optimal-move183x53.png')
        self.window.return_menu_img = PhotoImage(file='images/button_menu.png')

        Label(image=self.window.new_game_img)
        Label(image=self.window.rol_1_img)
        Label(image=self.window.rol_2_img)
        Label(image=self.window.opt_img)
        Label(image=self.window.return_menu_img)

        new_game_button = tk.Button(self.menu_frame, image=self.window.new_game_img, bg=BACKGROUND, bd=0,
                                    command=self.new_game)
        roll_1_button = tk.Button(self.menu_frame, image=self.window.rol_1_img, bg=BACKGROUND, bd=0,
                                  command=lambda val=True: self.generate_dices(val))
        roll_2_button = tk.Button(self.menu_frame, image=self.window.rol_2_img, bg=BACKGROUND, bd=0,
                                  command=lambda val=False: self.generate_dices(val))
        opt_move_button = tk.Button(self.menu_frame, image=self.window.opt_img,
                                    bg=BACKGROUND, bd=0, command=self.display_opt_move)
        return_button = tk.Button(self.menu_frame, image=self.window.return_menu_img,
                                  bg=BACKGROUND, bd=0, command=self.return_to_menu)

        return_button.grid(row=0, column=0, pady=5)
        new_game_button.grid(row=0, column=1, pady=10)
        roll_1_button.grid(row=1, column=1, pady=5)
        roll_2_button.grid(row=2, column=1, pady=5)
        opt_move_button.grid(row=3, column=1, pady=5)

        return self.menu_frame

    def generate_dices(self, roll_1_t_2_f):
        """ Creates a random roll of one or two dice depending on the user's choice and displays the roll """
        if not self.can_roll_again:
            return 0
        if roll_1_t_2_f and not self.can_roll_1:
            self.sum_left.configure(text=f"You cant roll 1 die yet")
            return 0
        dice = ['\u2680', '\u2681', '\u2682', '\u2683', '\u2684', '\u2685']  # dice uni-code
        dice_value = {'\u2680': 1, '\u2681': 2, '\u2682': 3, '\u2683': 4, '\u2684': 5, '\u2685': 6}

        dice_1, dice_2 = random.choice(dice), random.choice(dice)
        if roll_1_t_2_f:
            self.dice_sum = dice_value[dice_1]
            self.dice_display.configure(text=f"{dice_1}")
        else:
            self.dice_sum = dice_value[dice_1] + dice_value[dice_2]
            self.dice_display.configure(text=f"{dice_1} {dice_2}")
            
        self.opt_move_txt.configure(text="")

        self.dice_sum_left = self.dice_sum
        self.sum_left.configure(text=f"Left: {self.dice_sum}")

        self.dice_sum_text.configure(text=f"Dice Rolled: {self.dice_sum}")
        if self.is_game_over() == 1:
            self.sum_left.configure(text="You Lose", fg="red")

        self.can_roll_again = False

    def is_game_over(self):
        """ Returns whether the game is over,
            with the help of ret_best_move we check whether there are any possible moves left,
            if there are none and there is still an amount left from the toss then the player has lost,
            if he managed to take down all the cards, and he has no amount left then the player has won,
            otherwise the game continues."""
        opt_move = self.ret_best_move()
        if opt_move is None and self.dice_sum_left > 0:  # lose position
            return 1
        elif len(self.open_cards) == 0:  # win position
            return -1
        else:  # keep playing
            return 0

    def is_7_8_9_down(self):
        """ Returns if 7,8,9 cards are down"""
        if self.available_cards[6] or self.available_cards[7] or self.available_cards[8]:
            return False
        return True

    def card_down(self, card_val):
        """ Handles the user's card click.
            If the clicked card is up and legal, then we will take it down and update the relevant values,
            check if the game is over and return a message accordingly if so"""
        if not self.card_is_legal(self.dice_sum_left, card_val + 1):
            return 0

        self.cards_buttons[card_val].config(bg=CLOSED_CARD)
        self.available_cards[card_val] = False
        self.already_choose_card = True
        self.dice_sum_used += card_val + 1
        self.dice_sum_left = self.dice_sum - self.dice_sum_used
        self.sum_left.configure(text=f"Left: {self.dice_sum_left}")
        self.opt_move_txt.configure(text="")

        game_status = self.is_game_over()

        if game_status == -1:
            self.sum_left.configure(text=f"You Won", fg="green")
        elif game_status == 1:
            self.sum_left.configure(text=f"You Lose", fg="red")
        elif self.dice_sum_left == 0:
            self.dice_sum_used = 0
            self.can_roll_again = True
            if self.is_7_8_9_down():
                self.can_roll_1 = True

    def display_opt_move(self):
        """ Updates the opt_move when called by calling ret_best_move func"""
        opt_move = self.ret_best_move()

        if opt_move is None:
            self.opt_move_txt.configure(text=f"No moves left")
        else:
            self.opt_move_txt.configure(text=str(list(opt_move)))

    def return_to_menu(self):
        self.window.quit()

    def card_is_legal(self, sum_left, card_val):
        """ Returns if the clicked card is a valid to click: up and the sum_left is enough"""
        if sum_left == 0:
            return False
        return self.available_cards[card_val - 1] and sum_left >= card_val

    # accel-asc algorithm generates the integer partitions of n taken from Wikipedia
    @staticmethod
    def number_partitions(n):
        a = [0 for _ in range(n + 1)]
        k = 1
        y = n - 1
        while k != 0:
            x = a[k - 1] + 1
            k -= 1
            while 2 * x <= y:
                a[k] = x
                y -= x
                k += 1
            l = k + 1
            while x <= y:
                a[k] = x
                a[l] = y
                yield a[:k + 2]
                x += 1
                y -= 1
            a[k] = x + y
            y = x + y - 1
            yield a[:k + 1]

    def ret_best_move(self):
        """ Returns the best move based on the received toss and the open cards.
        The strategy is to choose the move that will leave the largest amount of
        for all the throws that will follow it,
        therefore we will find all the possible moves according to the throw
        and choose the move that lowers the highest card value possible while lowering a minimum amount of cards
        so that there are as many options as possible for the following moves.
        For example: we will prefer to choose: 9 than 8,1
        therefore we will sort the possible moves according to the largest member from largest to smallest
        In addition, we will prefer to choose: 6,4,1 than 6,3,1
        so we will sort the possible moves from the smallest to the largest."""

        self.open_cards = [i + 1 for i, num in enumerate(self.available_cards) if num]
        number_partitions = [num for num in self.number_partitions(self.dice_sum_left)]
        subsets_partitions = []
        for num in number_partitions:
            if len(set(num)) == len(num):
                subsets_partitions.append(num)
        unique_partitions = [p for p in subsets_partitions if set(p).issubset(set(self.open_cards))]

        if len(unique_partitions) == 0:
            return None

        unique_partitions.sort(key=lambda x: x[0], reverse=True)
        unique_partitions.sort(key=lambda x: x[-1], reverse=True)
        return unique_partitions[0]

    def new_game(self):
        self.clear_window()
        self.set_starting_values()

    def clear_window(self):
        for widget in self.window.winfo_children():
            widget.destroy()

    def set_starting_values(self):
        self.available_cards = [True] * 9
        self.is_first_roll = True
        self.can_roll_again = True
        self.can_roll_1 = False
        self.already_choose_card = False
        self.cards_buttons = []
        self.dice_sum_left = 0
        self.dice_sum = 0
        self.dice_sum_used = 0
        self.open_cards = set()

        self.messages_window = tk.Frame(self.window, bg=BACKGROUND, bd=0)
        self.menu_frame = self.create_menu_frame()
        self.cards_frame = self.create_cards()

        self.dice_display = Label(self.messages_window, font="Ariel 60", bg=BACKGROUND)
        self.sum_left = Label(self.messages_window, font="Ariel 20 bold", bg=BACKGROUND)
        self.dice_sum_text = Label(self.messages_window, font="Ariel 20 bold", bg=BACKGROUND)
        self.opt_move_txt = Label(self.messages_window, font="Ariel 20 bold", bg=BACKGROUND, fg="blue")

        self.grid_frames_labels()



