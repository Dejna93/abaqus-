from plugin.gui.pages_gui import OptionPage
from plugin.gui.pages_gui import StartPage
import Tkinter as tk

from plugin.settings import config


class Core(tk.Tk):
    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)

        tk.Tk.wm_title(self, "Output initializer")

        container = tk.Frame(self)

        container.pack(side="top", fill="both", expand=True)
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)
        self.frames = {}

        for F in (StartPage, OptionPage):
            page_name = F.__name__
            frame = F(parent=container, controller=self)
            self.frames[page_name] = frame
            frame.grid(row=0, column=0, sticky="nsew")

        self.show_frame("OptionPage")

    def show_frame(self, cont):
        frame = self.frames[cont]
        frame.tkraise()

    def quit(self):
        tk.Tk.destroy()


def run_gui():
    app = Core()
    app.minsize(width=config.window_width, height=config.window_height)
    app.mainloop()

if __name__ == '__main__':
    run_gui()