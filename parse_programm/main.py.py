import tkinter as tk

from constants import PROGRAMM_NAME, WINDOW_SIZE
from frames import Menu


class App(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title(PROGRAMM_NAME)
        self.geometry(WINDOW_SIZE)
        self.menu = Menu()
        self.mainloop()


if __name__ == '__main__':
    app = App()
