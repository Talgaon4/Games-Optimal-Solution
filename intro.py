from tkinter import *
from tkinter import messagebox
from GUI import GUI

BACKGROUND_COLOR = "#2B2B2B"
OPEN_CARD_COLOR = '#E4DCAD'
CLOSE_CARD_COLOR = '#D36B00'


class Intro:

    def __init__(self):
        self.window = Tk()
        self.window.title("Shut The Box")
        self.window.config(padx=30, pady=30, bg=BACKGROUND_COLOR)
        self.canvas = Canvas(width=400, height=270)
        self.create_title()
        self.create_how_2_play_btn()
        self.create_show_statics_btn()
        self.create_start_btn()
        self.window.mainloop()

    def create_title(self):
        self.canvas.create_rectangle(15, 0, 420, 70, fill=OPEN_CARD_COLOR)
        self.canvas.create_text(200, 35, text="Shut The Box", font=("Ariel", 30))
        self.canvas.grid(row=0, column=0)
        self.canvas.config(bg=BACKGROUND_COLOR, highlightthickness=0)

    def create_how_2_play_btn(self):
        how_2_play_btn = Button(text="How to Play", highlightthickness=0, command=self.display_how_2_play)
        how_2_play_btn.place(x=175, y=180)

    def display_how_2_play(self):
        with open("data/rules.txt", encoding='utf-8') as rules_file:
            lines = rules_file.read()
        how_2_play_box = messagebox.showinfo(title="How to play", message=f"{lines}")

    def create_show_statics_btn(self):
        show_statics_btn = Button(text="Statics", highlightthickness=0, command=self.display_statics)
        show_statics_btn.place(x=192, y=220)

    def display_statics(self):
        pass

    def create_start_btn(self):
        start_btn = Button(text="Start Game", highlightthickness=0, command=self.start_game)
        start_btn.place(x=180, y=140)

    def start_game(self):
        for widget in self.window.winfo_children():
            widget.destroy()
        game = GUI()
