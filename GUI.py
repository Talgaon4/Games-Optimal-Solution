from tkinter import *
import random
from bestMove import BestMove


BOX_LENGTH = 9
BACKGROUND_COLOR = "#2B2B2B"
OPEN_CARD_COLOR = '#E4DCAD'
CLOSE_CARD_COLOR = '#D36B00'


class GUI:

    def __init__(self, window):
        self.window = window
        self.window.title("Shut The Box")
        self.window.config(padx=0, pady=30, bg=BACKGROUND_COLOR)
        self.canvas = Canvas(width=88 * BOX_LENGTH, height=270)
        self.available_cards = [True] * 12
        self.is_first_roll = True
        self.can_roll_again = True
        self.already_choose_card = False
        self.cards_list = []
        self.dice_sum_left = 0
        self.dice_sum = 0
        self.dice_sum_used = 0
        self.open_cards = set()
        self.create_cards()
        self.roll()
        self.create_new_game_button()
        self.create_show_opt_move_button()
        self.sum_left = self.canvas.create_text(25 * BOX_LENGTH, 200, text="", font=("Ariel", 30))
        self.opt_move_txt = self.canvas.create_text(70 * BOX_LENGTH, 250, text="", font=("Ariel", 15))
        self.dice_1_2 = self.canvas.create_text(44 * BOX_LENGTH, 170, text=f"", font=("Ariel", 40))
        self.dice_sum_text = self.canvas.create_text(44 * BOX_LENGTH, 250, text=f"", font=("Ariel", 20))
        self.best = BestMove()
        self.window.mainloop()

    def create_cards(self):
        x, y, card_width, card_height = 50, 0, 60, 90

        for col in range(BOX_LENGTH):
            card = self.canvas.create_rectangle(x, y, x + card_width, y + card_height, fill=OPEN_CARD_COLOR)
            self.cards_list.append(card)
            self.canvas.create_text(x + 30, 45, text=f"{col + 1}", font=("Ariel", 40))

            card_button = Button(text=f"{col + 1}", highlightthickness=0, command=lambda val=col: self.card_down(val))
            card_button.place(x=x+23, y=y+100)

            x += 80  # space between the cards

            self.canvas.grid(row=0, column=col)
            self.canvas.config(bg=BACKGROUND_COLOR, highlightthickness=0)

    def generate_dices(self, roll_1_t_2_f):
        if not self.can_roll_again:
            return 0

        self.canvas.itemconfig(self.opt_move_txt, text=f"", fill="red")

        dice = ['\u2680', '\u2681', '\u2682', '\u2683', '\u2684', '\u2685']  # dice uni-code
        dice_value = {'\u2680': 1, '\u2681': 2, '\u2682': 3, '\u2683': 4, '\u2684': 5, '\u2685': 6}

        dice_1, dice_2 = random.choice(dice), random.choice(dice)
        if roll_1_t_2_f:
            self.dice_sum = dice_value[dice_1]
            self.canvas.itemconfig(self.dice_1_2, text=f" {dice_1}", fill="white")
        else:
            self.dice_sum = dice_value[dice_1] + dice_value[dice_2]
            self.canvas.itemconfig(self.dice_1_2, text=f"{dice_1} {dice_2}", fill="white")

        self.dice_sum_left = self.dice_sum

        self.canvas.itemconfig(self.sum_left, text=f"Left: {self.dice_sum}", fill="red")
        self.canvas.itemconfig(self.dice_sum_text, text=f"Dice Rolled: {self.dice_sum}", fill="black")
        self.can_roll_again = False

    def is_7_8_9_down(self):
        if self.available_cards[6] or self.available_cards[7] or self.available_cards[8]:
            return False
        return True

    def roll(self):
        roll_button = Button(text="Roll 2", highlightthickness=0, command=lambda val=False: self.generate_dices(val))
        roll_button.place(x=43*BOX_LENGTH, y=200)

    def card_down(self, card_val):
        if not self.card_is_legal(self.dice_sum_left, card_val + 1):
            return 0  # can add here a message
        self.canvas.itemconfig(self.cards_list[card_val], fill=CLOSE_CARD_COLOR)
        self.available_cards[card_val] = False
        self.already_choose_card = True
        self.dice_sum_used += card_val + 1
        self.dice_sum_left = self.dice_sum - self.dice_sum_used
        self.canvas.itemconfig(self.sum_left, text=f"Left: {self.dice_sum_left}", fill="red")
        self.canvas.itemconfig(self.opt_move_txt, text="", fill="green")

        if self.dice_sum_left == 0:
            self.dice_sum_used = 0
            self.can_roll_again = True
            if self.is_7_8_9_down():
                self.roll_1_btn()

    def roll_1_btn(self):
        roll_1_button = Button(text="Roll 1", highlightthickness=0, command=lambda val=True: self.generate_dices(val))
        roll_1_button.place(x=38 * BOX_LENGTH, y=200)

    def card_is_legal(self, rolled_val, card_val):
        if rolled_val == 0:
            return False
        return self.available_cards[card_val - 1] and rolled_val >= card_val

    def new_game(self):
        self.clear_window()
        self.set_starting_values()
        self.create_cards()
        self.roll()
        self.create_new_game_button()
        self.create_show_opt_move_button()

    def clear_window(self):
        for widget in self.window.winfo_children():
            widget.destroy()

    def create_new_game_button(self):
        new_game_button = Button(text="New Game", highlightthickness=0, command=self.new_game)
        new_game_button.place(x=55*BOX_LENGTH, y=200)

    def set_starting_values(self):
        self.canvas = Canvas(width=88 * BOX_LENGTH, height=270)
        self.available_cards = [True] * 12
        self.is_first_roll = True
        self.can_roll_again = True
        self.already_choose_card = False
        self.cards_list = []
        self.dice_sum_left = 0
        self.dice_sum = 0
        self.dice_sum_used = 0
        self.open_cards = set()
        self.sum_left = self.canvas.create_text(25 * BOX_LENGTH, 200, text="", font=("Ariel", 30))
        self.opt_move_txt = self.canvas.create_text(70 * BOX_LENGTH, 250, text="", font=("Ariel", 15))
        self.dice_1_2 = self.canvas.create_text(44 * BOX_LENGTH, 170, text=f"", font=("Ariel", 40))
        self.dice_sum_text = self.canvas.create_text(44 * BOX_LENGTH, 250, text=f"", font=("Ariel", 20))

    def get_open_cards(self):
        for i in range(BOX_LENGTH):
            if self.available_cards[i]:
                self.open_cards.add(i + 1)
        return frozenset(self.open_cards)

    def display_opt_move(self):
        self.open_cards = set()
        open_cards = self.get_open_cards()
        opt_move = self.best.ret_best_move(open_cards, self.dice_sum_left)

        if opt_move is None:
            self.canvas.itemconfig(self.opt_move_txt, text=f"No moves left", fill="red")
        else:
            self.canvas.itemconfig(self.opt_move_txt, text=f"The optimal move is: {list(opt_move)}", fill="green")

    def create_show_opt_move_button(self):
        opt_move_button = Button(text="Best Move", highlightthickness=0, command=self.display_opt_move)
        opt_move_button.place(x=70 * BOX_LENGTH, y=200)


