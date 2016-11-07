import Tkinter as tk
import ttk as ttk
import tkFileDialog

FONT = ("Times New Roman", 8)


class Capp(tk.Tk):
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

        for F in (StartPage, PageOne, MainPage):
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
        tk.Frame.__init__(self,parent)
        self.parent = parent
        button1 = ttk.Button(self, text="OK", command=lambda: controller.show_frame("MainPage"))
        button1.grid(row=1, column=1)
        button2 = ttk.Button(self, text="Quit", command=lambda: StartPage.quit(self))
        button2.grid(row=1, column=2)


class MainPage(tk.Frame):
    def __init__(self, parent , controller):
        tk.Frame.__init__(self, parent)
        self.parent = parent
        self.grid(row=0, column=0, sticky=tk.NSEW)
        self.file_opt = options = {}

        labelFrame_1 = tk.LabelFrame(self, text=u"Specify Output directory", height="200", padx=10, pady=10)
        labelFrame_1.pack(fill="both", padx=5, pady=5)

        label_1 = tk.Label(labelFrame_1, text=u"Text file path", bg="white")
        label_1.pack(side=tk.LEFT, padx=20)

        self.entry_1 = tk.Entry(labelFrame_1, bd=2, width=50)
        self.entry_1.pack(side=tk.LEFT, fill=tk.X, padx=20)

########################################################################################################################

        labelFrame_2 = tk.LabelFrame(self, text="Operations", height=100, padx=10, pady=10)
        labelFrame_2.pack(fill="both", padx=5, pady=5)

        radiobutton_inc = tk.Radiobutton(labelFrame_2, padx=10, pady=10).grid(row=0, column=0)
        radio_labels_inc = tk.Label(labelFrame_2, text=u"All elements", bg="white").grid(row=0, column=1)

        radiobutton_inc_2 = tk.Radiobutton(labelFrame_2, padx=10, pady=10).grid(row=1, column=0)
        radio_labels_inc_2 = tk.Label(labelFrame_2, text=u'Selected', bg="white").grid(row=1, column=1)
        entry_inc_2 = tk.Entry(labelFrame_2, bd=2, width=4).grid(row=1, column=6)
        entry_labels_inc_2 = tk.Label(labelFrame_2, text=u'Set max', bg="white").grid(row=1, column=5)

        radiobutton_inc_3 = tk.Radiobutton(labelFrame_2, padx=10, pady=10).grid(row=3, column=0)
        radio_labels_inc_3 = tk.Label(labelFrame_2, text=u'Selected', bg="white").grid(row=3, column=1)
        entry_inc_3 = tk.Entry(labelFrame_2, bd=2, width=4).grid(row=3, column=4)
        entry_labels_inc_3 = tk.Label(labelFrame_2, text=u'Set max', bg="white").grid(row=3, column=5)
        entry_inc_4 = tk.Entry(labelFrame_2, bd=2, width=4).grid(row=3, column=6)
        entry_labels_inc_4 = tk.Label(labelFrame_2, text=u'Set max', bg="white").grid(row=3, column=5)

########################################################################################################################

        labelFrame_3 = tk.LabelFrame(self, text="Elements", height=100, padx=10, pady=10)
        labelFrame_3.pack(fill="both", padx=5, pady=5)

        radiobutton_inc = tk.Radiobutton(labelFrame_3, padx=10, pady=10).grid(row=0, column=0)
        radio_labels_inc = tk.Label(labelFrame_3, text=u"All elements", bg="white").grid(row=0, column=1)

        radiobutton_inc_2 = tk.Radiobutton(labelFrame_3, padx=10, pady=10).grid(row=1, column=0)
        radio_labels_inc_2 = tk.Label(labelFrame_3, text=u'Selected', bg="white").grid(row=1, column=1)
        entry_inc_2 = tk.Entry(labelFrame_3, bd=2, width=4).grid(row=1, column=6)
        entry_labels_inc_2 = tk.Label(labelFrame_3, text=u'Set max', bg="white").grid(row=1, column=5)

        radiobutton_inc_3 = tk.Radiobutton(labelFrame_3, padx=10, pady=10).grid(row=3, column=0)
        radio_labels_inc_3 = tk.Label(labelFrame_3, text=u'Selected', bg="white").grid(row=3, column=1)
        entry_inc_3 = tk.Entry(labelFrame_3, bd=2, width=4).grid(row=3, column=4)
        entry_labels_inc_3 = tk.Label(labelFrame_3, text=u'Set max', bg="white").grid(row=3, column=5)
        entry_inc_4 = tk.Entry(labelFrame_3, bd=2, width=4).grid(row=3, column=6)
        entry_labels_inc_4 = tk.Label(labelFrame_3, text=u'Set max', bg="white").grid(row=3, column=5)

########################################################################################################################

        labelFrame_4 = tk.LabelFrame(self, text="Output request", height=100, padx=10, pady=10)
        labelFrame_4.pack(fill="both", padx=5, pady=5)
        radiobutton_out = tk.Radiobutton(labelFrame_4, padx=10, pady=10).grid(row=0, column=0)
        radio_labels_inc_2 = tk.Label(labelFrame_4, text=u'2D', bg="white").grid(row=0, column=1)

        radiobutton_out = tk.Radiobutton(labelFrame_4, padx=10, pady=10).grid(row=0, column=2)
        radio_labels_inc_2 = tk.Label(labelFrame_4, text=u'3D', bg="white").grid(row=0, column=3)
        radio_labels_inc_2 = tk.Label(labelFrame_4, text=u'3D', bg="white").grid(row=0, column=3)
        names2D = ['S', 'PEEQ', 'EVOL', 'SDV121', 'U']
        names3D = ['S', 'T', 'D']

        list2d = tk.Listbox(labelFrame_4)
        for name in names2D:
            list2d.insert(tk.END, name)
        list2d.grid(row=1, column=0)

        list3d = tk.Listbox(labelFrame_4)
        for name in names3D:
            list3d.insert(tk.END, name)
        list3d.grid(row=1, column=2)

    def set_entry(self, text):
        self.entry_1.delete(0, tk.END)
        self.entry_1.insert(0, text)

    def check_filepath(self,controller):

        if(self.filename):
            controller.show_frame("STLPage")

    def opennew(self):
        print "opening"


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
    app = Capp()
    app.minsize(width=400,height=400)
    app.mainloop()

if __name__ == '__main__':
    run_gui()