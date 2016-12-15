import Tkinter as tk
import ttk as ttk
import tkFileDialog

from plugin.settings import config


class Page(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.parent = parent

    def create_listbox_values(self, widget, values, **widget_options):
        widget.config(widget_options)
        for value in values:
            widget.insert(tk.END, value)

        widget.select_set(0)

    def create_entry(self, frame, text, row, col, width=25, **e_options):
        """
        :param col: grid column
        :param row: grid row
        :param frame: parent frame/label_frame
        :param text: print by label
        :param e_options: dict of entry options
        :return: tuple (label and entry)
        """
        label = tk.Label(frame, text=text, width=width)
        label.grid(row=row, column=col, sticky='e')
        entry = tk.Entry(frame, width=width, **e_options)
        entry.grid(row=row, column=col + 1, sticky='e')
        return entry, label

    def create_entry_integer(self, frame, text, row, col, width=25, **e_options):
        entry, label = self.create_entry(frame, text, row, col, width=width, **e_options)
        entry.bind("<KeyPress>", lambda event: self.entry_integer_validator(event, max_len=width))
        entry.insert(0, row)
        return entry, label

    # custom validator
    def entry_integer_validator(self, event, max_len):
        keysym_tuple = ("BackSpace", 'Delete', "Tab")
        if event.char in '0123456789':
            pass
        elif event.widget.get().count('.') == 0 and event.char == '.':
            pass
        elif event.keysym in keysym_tuple:
            pass
        else:
            return 'break'

        if len(event.widget.get()) < max_len:
            pass
        elif len(event.widget.get()) == max_len and event.keysym in keysym_tuple:
            pass
        else:
            return 'break'


class StartPage(Page):
    def __init__(self, parent, controller):
        Page.__init__(self, parent, controller)

        ### frames ###
        self.frame_first_part = tk.LabelFrame(self, text="Increments and elements", height=100, padx=10, pady=10)
        self.frame_first_part.grid(row=0, column=0, columnspan=2, sticky="we")

        self.frame_increments_sel = tk.LabelFrame(self, text="Increments", height=100, padx=10, pady=10)
        self.frame_elements_sel = tk.LabelFrame(self, text="Selections", height=100, padx=10, pady=10)

        self.frame_first_part_set_inc = tk.LabelFrame(self.frame_first_part, height=25)
        self.frame_first_part.grid(row=0, column=0, sticky='we')

        self.frame_first_part_set_el = tk.LabelFrame(self.frame_first_part, height=25)
        self.frame_first_part.grid(row=0, column=1,  sticky='we')

        self.frame_first_part_range_inc = tk.LabelFrame(self.frame_first_part, height=25)
        self.frame_first_part.grid(row=1, column=0, sticky='we')

        self.frame_first_part_range_el = tk.LabelFrame(self.frame_first_part, height=25)
        self.frame_first_part.grid(row=0, column=1,  sticky='we')
        ##############

        _names = (u"All", u"Set", u"Range")

        self.label_increments = tk.Label(self.frame_first_part, text=u"Increments")
        self.label_increments.grid(row=0, column=0, sticky='we')

        self.label_elements = tk.Label(self.frame_first_part, text=u"Elements")
        self.label_elements.grid(row=0, column=1, sticky='we')

        self.listbox_increments = tk.Listbox(self.frame_first_part, height=3)
        self.listbox_increments.grid(row=1, column=0, sticky='we')
        self.create_listbox_values(self.listbox_increments, _names, exportselection=0)

        self.listbox_elements = tk.Listbox(self.frame_first_part, height=3)
        self.listbox_elements.grid(row=1, column=1, sticky='we')
        self.create_listbox_values(self.listbox_elements, _names, exportselection=0)

        ### listboxex commands ###
        self.listbox_increments.bind('<<ListboxSelect>>', lambda event: self.show_first_part_inc())
        self.listbox_elements.bind('<<ListboxSelect>>', lambda event: self.show_first_part_el())
        ##########################

        ### entires ###
        self.entry_inc_max, self.label_inc_max = self.create_entry_integer(
            self.frame_first_part_set_inc, u"Max", 0, 0, 3)
        self.entry_inc_max.insert(0, 1)


        self.entry_inc_start, self.label_inc_start = self.create_entry_integer(
            self.frame_first_part_range_inc, u"Start", 0, 0, 3)
        self.entry_inc_end, self.label_inc_end = self.create_entry_integer(
            self.frame_first_part_range_inc, u"End", 1, 0, 3)

        self.entry_el_max, self.label_el_max = self.create_entry_integer(
            self.frame_first_part_set_el, u"Max", 0, 0, 3)
        self.entry_el_max.insert(0, 1)

        self.entry_el_start, self.label_el_start = self.create_entry_integer(
            self.frame_first_part_range_el, u"Start", 0, 0, 3)

        self.entry_el_end, self.label_el_end = self.create_entry_integer(
            self.frame_first_part_range_el, u"End", 1, 0, 3)

        self.entry_inc_max.bind('<Return>', lambda event: self.show_selections("increments"))
        self.entry_el_max.bind('<Return>', lambda event: self.show_selections("elements"))
        ###############

        ### selections ###
        self.list_increments_sel = []
        self.list_elements_sel = []
        ##################

    def show_first_part_inc(self):
        increments = self.listbox_increments.get(self.listbox_increments.curselection())
        if increments == u"Set":
            self.frame_first_part_range_inc.grid_remove()
            self.frame_first_part_set_inc.grid(row=2, column=0, sticky='we')
            self.show_selections("increments")
        elif increments == u"Range":
            self.frame_first_part_set_inc.grid_remove()
            self.frame_first_part_range_inc.grid(row=2, column=0, sticky='we')
            self.frame_increments_sel.grid_remove()

        else:
            self.frame_first_part_set_inc.grid_remove()
            self.frame_first_part_range_inc.grid_remove()
            self.frame_increments_sel.grid_remove()

    def show_first_part_el(self):
        elements = self.listbox_elements.get(self.listbox_elements.curselection())
        if elements == u"Set":
            self.frame_first_part_range_el.grid_remove()
            self.frame_first_part_set_el.grid(row=2, column=1, sticky='we')
            self.show_selections("elements")
        elif elements == u"Range":
            self.frame_first_part_set_el.grid_remove()
            self.frame_first_part_range_el.grid(row=2, column=1, sticky='we')
            self.frame_elements_sel.grid_remove()
        else:
            self.frame_first_part_set_el.grid_remove()
            self.frame_first_part_range_el.grid_remove()
            self.frame_elements_sel.grid_remove()

    def show_selections(self, part):
        if part == "increments":
            # clearing frame #
            if self.list_increments_sel:
                self.frame_increments_sel.grid_remove()
                for i in self.list_increments_sel:
                    i.grid_remove()
            self.list_increments_sel[:] = []
            ###########################

            self.frame_increments_sel.grid(row=1, column=1, sticky='nwe')
            counter = int(self.entry_inc_max.get())
            for i in range(counter):
                self.list_increments_sel.append(tk.Checkbutton(self.frame_increments_sel, text=i))
                self.list_increments_sel[i].grid(row=i)

        if part == "elements":
            # clearing frame #
            self.frame_elements_sel.grid_remove()
            if self.list_elements_sel:
                for i in self.list_elements_sel:
                    i.grid_remove()
                self.list_elements_sel[:] = []
            ###########################
            self.frame_elements_sel.grid(row=1, column=2, sticky='nwe')
            counter = int(self.entry_el_max.get())
            for i in range(counter):
                self.list_elements_sel.append(tk.Checkbutton(self.frame_elements_sel, text=i))
                self.list_elements_sel[i].grid(row=i)


class OptionPage(Page):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.parent = parent
