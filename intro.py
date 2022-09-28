import tkinter as tk
from tkinter import *
from numberle import Numberle
from shutTheBox import ShutTheBox
from tictactoe import TicTacToe
from simon import Simon
from colors import Color

colors = Color()
BACKGROUND_COLOR = Color.background
OPEN_CARD_COLOR = '#E4DCAD'
CLOSE_CARD_COLOR = '#D36B00'


class Intro:

    def __init__(self):
        self.window = Tk()
        self.window.title("World Of Games")
        self.window.geometry('850x550')
        self.window.configure(bg=BACKGROUND_COLOR)

        self.window.columnconfigure(0, weight=4)

        self.game_frame = Frame(self.window, bg=BACKGROUND_COLOR)
        self.game_frame.grid(row=0, column=0)
        buttons_frame = self.create_buttons()
        title_frame = self.create_title_frame()
        title_frame.grid(row=1, column=0, pady=65)
        buttons_frame.grid(row=2, column=0, pady=25)
        self.create_menu_bar()

        self.window.iconbitmap('images/favicon.ico')

        self.window.mainloop()

    def create_title_frame(self):

        title_frame = tk.Frame(self.game_frame, bg=BACKGROUND_COLOR)

        self.window.title_image = PhotoImage(file="images/button_world-of-games.png")
        tk.Label(title_frame, image=self.window.title_image, bg=BACKGROUND_COLOR).pack()

        return title_frame

    def create_buttons(self):

        buttons_frame = tk.Frame(self.game_frame, bg=BACKGROUND_COLOR)

        self.window.shut_the_box_image = PhotoImage(file="images/button_shut-the-box.png")
        self.window.tic_tac_toe_image = PhotoImage(file="images/button_tic-tac-toe.png")
        self.window.numberle_image = PhotoImage(file="images/button_numberle.png")
        self.window.simon_image = PhotoImage(file="images/button_simon.png")

        tk.Label(buttons_frame, image=self.window.shut_the_box_image)
        tk.Label(buttons_frame, image=self.window.shut_the_box_image)
        tk.Label(buttons_frame, image=self.window.shut_the_box_image)
        tk.Label(buttons_frame, image=self.window.simon_image)

        shut_the_box_btn = tk.Button(buttons_frame, bg=BACKGROUND_COLOR, bd=0, image=self.window.shut_the_box_image,
                                     command=self.shut_the_box)
        tic_tac_toe_btn = tk.Button(buttons_frame, bg=BACKGROUND_COLOR, bd=0, image=self.window.tic_tac_toe_image,
                                    command=self.tic_tac_toe)
        numberle_btn = tk.Button(buttons_frame, bg=BACKGROUND_COLOR, bd=0, image=self.window.numberle_image,
                                 command=self.numberle)
        simon_btn = tk.Button(buttons_frame, bg=BACKGROUND_COLOR, bd=0, image=self.window.simon_image,
                              command=self.simon)

        shut_the_box_btn.grid(row=0, column=0, pady=10)
        tic_tac_toe_btn.grid(row=1, column=0, pady=10)
        numberle_btn.grid(row=2, column=0, pady=10)
        simon_btn.grid(row=0, column=1, pady=10, padx=25)

        return buttons_frame

    def create_menu_bar(self):
        # create a menubar
        menubar = Menu(self.window)
        self.window.config(menu=menubar)

        # create the file_menu
        file_menu = Menu(
            menubar,
            tearoff=0,
            fg="purple"
        )

        # add menu items to the File menu
        file_menu.add_command(label='Menu', command=self.upload_menu)

        # add Exit menu item
        file_menu.add_command(
            label='Exit',
            command=self.window.destroy
        )

        # add the File menu to the menubar
        menubar.add_cascade(
            label="Game",
            menu=file_menu
        )


    def upload_menu(self):
        self.clear()
        self.window.title("World Of Games")
        self.window.geometry('850x550')
        self.window.configure(bg=BACKGROUND_COLOR)

        self.window.columnconfigure(0, weight=4)

        self.game_frame = Frame(self.window, bg=BACKGROUND_COLOR)
        self.game_frame.grid(row=0, column=0)
        buttons_frame = self.create_buttons()
        title_frame = self.create_title_frame()
        title_frame.grid(row=1, column=0, pady=65)
        buttons_frame.grid(row=2, column=0, pady=25)
        self.create_menu_bar()

        self.window.iconbitmap('images/favicon.ico')

        self.window.mainloop()

    def clear(self):
        for widget in self.game_frame.winfo_children():
            widget.destroy()

    def shut_the_box(self):
        self.clear()
        ShutTheBox(window=self.game_frame)
        self.clear()
        self.upload_menu()

    def numberle(self):
        self.clear()
        Numberle(window=self.game_frame)
        self.clear()
        self.upload_menu()

    def simon(self):
        self.clear()
        Simon(window=self.game_frame)
        self.clear()
        self.upload_menu()

    def tic_tac_toe(self):
        self.clear()
        TicTacToe(window=self.game_frame)
        self.clear()
        self.upload_menu()


Intro()
