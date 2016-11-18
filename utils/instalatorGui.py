"""Just Instalator Gui"""
import Tkinter as tk
import ttk as ttk
import tkFileDialog


class Core(tk.Tk):
    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)

        tk.Tk.wm_title(self, "Output initializer")

        container = tk.Frame(self)

        container.pack(side="top", fill="both", expand=True)
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)

        menu = tk.Menu(self)
        self.config(menu=menu)
        file = tk.Menu(menu)
        file.add_command(label="Open")
        file.add_command(label="Exit")

        help = tk.Menu(menu)
        help.add_command(label="Help")

        menu.add_cascade(label="File", menu=file)
        menu.add_cascade(label="Help", menu=help)

        self.frames = {}

        for F in (MainPage, PageOne):
            page_name = F.__name__
            frame = F(parent=container, controller=self)
            self.frames[page_name] = frame
            frame.grid(row=0, column=0, sticky="nsew")

        self.show_frame("MainPage")

    def show_frame(self, cont):
        frame = self.frames[cont]
        frame.tkraise()

    def quit(self):
        tk.Tk.destroy()


class MainPage(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)

        # labels
        lb_abaqus_dir = ttk.Label(self, text="Path to abaqus directory")
        lb_plugin_dir = ttk.Label(self, text="Path to your plugin directory")

        # entries
        entry_abaqus_dir = ttk.Entry(self)
        entry_plugin_dir = ttk.Entry(self)

        lb_abaqus_dir.grid(row=0, padx=20, pady=20).grid(row=1)
        entry_1.grid(row=0, column=1)
        entry_2.grid(row=1, column=1)




class PageOne(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)

        label_1 = ttk.Label(self, text="COS TAM")
        label_2 = ttk.Label(self, text="COS TAM 2")

        entry_1 = ttk.Entry(self)
        entry_2 = ttk.Entry(self)

        label_1.grid(row=0, padx=20, pady=20)
        label_2.grid(row=1)
        entry_1.grid(row=0, column=1)
        entry_2.grid(row=1, column=1)




def run_gui():
    app = Core()
    app.minsize(width=400,height=400)
    app.mainloop()

if __name__ == '__main__':
    run_gui()