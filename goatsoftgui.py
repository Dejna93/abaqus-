import Tkinter as tk
import tkMessageBox

from plugin.gui.pages_gui import StartPage
from plugin.odb_scripts.source import odb_reader
from plugin.settings import config
from plugin.settings import global_vars_storage

try:
    from concurrent.futures import ThreadPoolExecutor, ProcessPoolExecutor, wait
    import matplotlib
except ImportError:
    tkMessageBox.showerror(
        title="Library import error",
        message="You have to install necessary librarys\n"
                "Please read 'Readme.txt'",
    )
    pass


class Core(tk.Tk):
    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)

        tk.Tk.wm_title(self, "Output initializer")

        self.container = tk.Frame(self)

        self.container.pack(side="top", fill="both", expand=True)
        self.container.grid_rowconfigure(0, weight=1)
        self.container.grid_columnconfigure(0, weight=1)
        self.frames = {}

        for F in (StartPage,):
            page_name = F.__name__
            frame = F(parent=self.container, controller=self)
            self.frames[page_name] = frame
            frame.grid(row=0, column=0, sticky="nsew")

        self.show_frame("StartPage")

    def show_frame(self, cont):
        frame = self.frames[cont]
        frame.tkraise()

    def show_refreshed_frame(self, cont):
        frame = self.frames[cont]
        frame.refresh()
        frame.tkraise()

    def quit(self):
        print("Closed GoatSoft")
        try:
            print "Cleaning"
            del global_vars_storage
            del odb_reader

        except Exception:
            pass

        finally:
            tk.Tk.destroy(self)


def start_app():
    app = Core()
    app.minsize(width=config.window_width, height=config.window_height)
    app.protocol("WM_DELETE_WINDOW", app.quit)
    app.mainloop()


if __name__ == '__main__':
    start_app()
