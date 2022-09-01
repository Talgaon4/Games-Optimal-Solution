import tkinter as tk
from tkinter import *
from tkinter.ttk import *
from numberle import Numberle
from shutTheBox import ShutTheBox
from tictactoe import TicTacToe
from colors import Color

colors = Color()
BACKGROUND_COLOR = Color.background
OPEN_CARD_COLOR = '#E4DCAD'
CLOSE_CARD_COLOR = '#D36B00'


class Intro:

    def __init__(self):
        self.window = Tk()
        self.window.title("World Of Games")
        self.window.geometry('550x400')
        self.window.configure(bg=BACKGROUND_COLOR)
        # windows only (remove the minimize/maximize button)
        self.window.attributes('-toolwindow', True)

        self.window.columnconfigure(0, weight=4)
        title_frame = self.create_title_frame()
        buttons_frame = self.create_buttons()

        title_frame.grid(column=0, row=0, pady=40)
        buttons_frame.grid(column=0, row=1, pady=20)

        self.window.mainloop()

    def create_title_frame(self):

        title_frame = tk.Frame(self.window)

        self.window.title_image = PhotoImage(file="images/button_world-of-games.png")
        tk.Label(title_frame, image=self.window.title_image, bg=BACKGROUND_COLOR).pack()

        return title_frame

    def create_buttons(self):
        buttons_frame = tk.Frame(self.window, bg=BACKGROUND_COLOR)

        self.window.shut_the_box_image = PhotoImage(file="images/button_shut-the-box.png")
        tk.Label(buttons_frame, image=self.window.shut_the_box_image)
        shut_the_box_btn = tk.Button(buttons_frame, bg=BACKGROUND_COLOR, bd=0, image=self.window.shut_the_box_image,
                                     command=self.shut_the_box)
        shut_the_box_btn.grid(row=0, column=0, pady=5)

        self.window.tic_tac_toe_image = PhotoImage(file="images/button_tic-tac-toe.png")
        tk.Label(buttons_frame, image=self.window.shut_the_box_image)
        tic_tac_toe_btn = tk.Button(buttons_frame, bg=BACKGROUND_COLOR, bd=0, image=self.window.tic_tac_toe_image,
                                    command=self.tic_tac_toe)
        tic_tac_toe_btn.grid(row=1, column=0, pady=5)

        self.window.numberle_image = PhotoImage(file="images/button_numberle.png")
        tk.Label(buttons_frame, image=self.window.shut_the_box_image)
        numberle_btn = tk.Button(buttons_frame, bg=BACKGROUND_COLOR, bd=0, image=self.window.numberle_image,
                                 command=self.numberle)
        numberle_btn.grid(row=2, column=0, pady=5)

        return buttons_frame

    def upload_menu(self):
        self.window.title("World Of Games")
        self.window.geometry('550x400')
        self.window.resizable(None, None)
        # windows only (remove the minimize/maximize button)
        self.window.attributes('-toolwindow', True)

        self.window.columnconfigure(0, weight=4)
        title_frame = self.create_title_frame()
        buttons_frame = self.create_buttons()

        title_frame.grid(column=0, row=0, pady=30)
        buttons_frame.grid(column=0, row=1)

        self.window.mainloop()

    def clear(self):
        for widget in self.window.winfo_children():
            widget.destroy()

    def shut_the_box(self):
        self.clear()
        ShutTheBox(window=self.window)
        self.clear()
        self.upload_menu()

    def numberle(self):
        self.clear()
        Numberle(window=self.window)
        self.clear()
        self.upload_menu()

    def tic_tac_toe(self):
        self.clear()
        TicTacToe(window=self.window)
        self.clear()
        self.upload_menu()


Intro()
