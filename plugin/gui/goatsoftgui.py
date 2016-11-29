import Tkinter as tk
import ttk as ttk
import tkFileDialog

FONT = ("Times New Roman", 8)


class Core(tk.Tk):
    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)

        tk.Tk.wm_title(self, "Output initializer")

        container = tk.Frame(self)

        container.pack(side="top", fill="both", expand=True)
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)
        self.frames = {}

        for F in (StartPage, PageOne):
            page_name = F.__name__
            frame = F(parent=container, controller=self)
            self.frames[page_name] = frame
            frame.grid(row=0, column=0, sticky="nsew")

        self.show_frame("StartPage")

    def show_frame(self, cont):
        frame = self.frames[cont]
        frame.tkraise()

    def quit(self):
        tk.Tk.destroy()


class StartPage(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.parent = parent
        button1 = ttk.Button(self, text="OK", command=lambda: controller.show_frame("PageOne"))
        button1.grid(row=1, column=1)
        button2 = ttk.Button(self, text="Quit", command=lambda: StartPage.quit(self))
        button2.grid(row=1, column=2)

class PageOne(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.parent = parent

        # 'private' variables
        _i = 0
        _j = 0

        # frames
        self.frame_increments = tk.LabelFrame(self, text="Increments", height=100, padx=10, pady=10)
        self.frame_increments.grid(row=0, column=0, sticky='we')
        self.frame_select_increments = tk.LabelFrame(self, text="Select increments", height=100, padx=10, pady=10)
        self.frame_select_increments.grid(row=1, column=0, sticky='we')

        self.frame_elements = tk.LabelFrame(self, text="Elements", height=100, padx=10, pady=10)
        self.frame_elements.grid(row=0, column=1, sticky='we')
        self.frame_select_elements = tk.LabelFrame(self, text="Select elements", height=100, padx=10, pady=10)
        self.frame_select_elements.grid(row=1, column=1, sticky='we')

        self.frame_output_request = tk.LabelFrame(self, text="Output request", height=100, padx=10, pady=10)
        self.frame_output_request.grid(row=2, column=0, sticky='we')
        self.frame_steps = tk.LabelFrame(self, text="Steps", height=100, padx=10, pady=10)
        self.frame_steps.grid(row=2, column=1, sticky='we')

        self.frame_materials = tk.LabelFrame(self, text="Materials", height=100, padx=10, pady=10)
        self.frame_materials.grid(row=2, column=0, sticky='we')
        self.frame_select_grains = tk.LabelFrame(self, text="Selcet grains", height=100, padx=10, pady=10)
        self.frame_select_grains.grid(row=2, column=1, sticky='we')

        ### Increments ###
        # radio buttons
        self.radio_increments = {}
        _radio_buttons = ((u"All increments", 0), (u"Selected", 0), (u"Range", 0))
        _i = 0
        for radio in _radio_buttons:
            self.radio_increments[radio[0]] = tk.Radiobutton(self.frame_increments, text=radio[0], value=radio[1])
            self.radio_increments[radio[0]].grid(row=0, column=_i, columnspan=2, sticky='we')
            _i += 2

        # entries
        self.entires_increments = {}
        _entires = ((u"Set max", (1, 2)), (u"Min", (1, 4)), (u"Max", (2, 4)))
        _i = 3
        for entry in _entires:
                self.entires_increments[entry[0]] = self.make_entry(
                    self.frame_increments, text=entry[0], row=entry[1][0], col=entry[1][1], width=6)

        ### Elements ###
        # radio buttons
        self.radio_elements = {}
        _radio_buttons = ((u"All increments", 0), (u"Selected", 0), (u"Range", 0))
        _i = 0
        for radio in _radio_buttons:
            print(radio[0])
            self.radio_elements[radio[0]] = tk.Radiobutton(self.frame_elements, text=radio[0])
            self.radio_elements[radio[0]].grid(row=0, column=_i, columnspan=2, sticky='we')
            _i += 2

        # entries
        self.entires_elements = {}
        _entires = ((u"Set max", (1, 2)), (u"Min", (1, 4)), (u"Max", (2, 4)))
        _i = 3
        for entry in _entires:
            self.entires_elements[entry[0]] = self.make_entry(
                self.frame_elements, text=entry[0], row=entry[1][0], col=entry[1][1], width=6)

        print self.radio_elements["All increments"].get()

    def make_entry(self, frame, text, row, col, width=25, **e_options):
        """
        :param col: grid column
        :param row: grid row
        :param frame: parent frame/label_frame
        :param text: print by label
        :param e_options: dict of entry options
        :return: tuple (label and entry)
        """
        label = tk.Label(frame, text=text, width=10)
        label.grid(row=row, column=col, sticky='e')
        entry = tk.Entry(frame, width=width, **e_options)
        entry.insert(0, row)
        entry.bind("<KeyPress>", lambda event: self.entry_integer_validator(event, max_len=width))
        entry.grid(row=row, column=col + 1, sticky='e')
        return (label, entry)

    # custom validator
    def entry_integer_validator(self, event, max_len):
        if event.char in '0123456789':
            pass
        elif event.widget.get().count('.') == 0 and event.char == '.':
            pass
        elif event.keysym == "BackSpace" or event.keysym == 'Delete':
            pass
        else:
            return 'break'

        if len(event.widget.get()) < max_len:
            pass
        elif len(event.widget.get()) == max_len and event.keysym == "BackSpace" or event.keysym == 'Delete':
            pass
        else:
            return 'break'

    def get_increments(self):
        pass

    def get_elements(self):
        pass


def run_gui():
    app = Core()
    app.minsize(width=400, height=400)
    app.mainloop()

if __name__ == '__main__':
    run_gui()