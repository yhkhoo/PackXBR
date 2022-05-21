import tkinter as tk
import tkinter.ttk as ttk
from tkinter import N, E, S, W


def multipleChoice(root, options, values, variable, grid):
    if not len(options) == len(values) == len(grid):
        raise Exception("multipleChoice options and values must be the same length")

    for i in range(len(values)):
        ttk.Radiobutton(root, value=values[i], text=options[i], variable=variable). \
            grid(column=grid[i][0], row=grid[i][1], padx=30, sticky=W + E)


# In win10 normal buttons don't change color on hover.
# https://stackoverflow.com/a/49896477/8133370
class HoverButton(tk.Button):
    def __init__(self, master, **kw):
        tk.Button.__init__(self, master=master, **kw)
        self.defaultBackground = self["background"]
        self.bind("<Enter>", self.on_enter)
        self.bind("<Leave>", self.on_leave)

    def on_enter(self, e):
        self['background'] = self['activebackground']

    def on_leave(self, e):
        self['background'] = self.defaultBackground


def darkTitle(root):
    def minim():
        root.overrideredirect(False)
        root.wm_state("iconic")
        root.overrideredirect(True)

    # turns off default windows titlebar
    root.overrideredirect(True)
    # make a frame for the new title bar
    title_bar = tk.Frame(root, relief='flat', borderwidth=0, bg="#262626")
    title_bar.pack(expand=1, fill=tk.X)
    # canvas for the main area of the window
    window = tk.Canvas(root, bg="#464646", borderwidth=0, highlightthickness=0)
    window.pack(expand=1, fill=tk.BOTH)

    # title
    tk.Label(title_bar, text=" PackXBR", bg="#262626", borderwidth=0, highlightthickness=0,
             fg="#B8BABD", font=("Arial", 10)). \
        pack(side=tk.LEFT)
    # close button
    HoverButton(title_bar, text=' ✕ ', command=root.destroy,
                bg="#262626", highlightbackground="#E81123", activebackground="#E81123",
                borderwidth=0, highlightthickness=0, fg="#B8BABD", activeforeground="#B8BABD",
                takefocus=False, font=("Arial", 10)). \
        pack(side=tk.RIGHT)
    # minimize button
    HoverButton(title_bar, text=' – ', command=minim,
                bg="#262626", highlightbackground="#2E3033", activebackground="#2E3033",
                borderwidth=0, highlightthickness=0, fg="#B8BABD", activeforeground="#B8BABD",
                takefocus=False, font=("Arial", 10)). \
        pack(side=tk.RIGHT)

    # bind title bar motion to the move window function
    def get_pos(event):
        xwin = root.winfo_x()
        ywin = root.winfo_y()
        startx = event.x_root
        starty = event.y_root

        ywin = ywin - starty
        xwin = xwin - startx

        def move_window(event):
            root.geometry('+{0}+{1}'.format(event.x_root + xwin, event.y_root + ywin))

        title_bar.bind('<B1-Motion>', move_window)

    title_bar.bind('<Button-1>', get_pos)

    return window
