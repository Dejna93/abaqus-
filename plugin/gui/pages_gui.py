import Tkinter as tk
import os
import tkFileDialog

from plugin.odb_scripts.source import test

from plugin.settings import config
from plugin.settings import global_vars_storage


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
        entry.insert(0, int(row))
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

        ### vars ###
        self.is_acticve3D = False

        ### frames ###
        self.frame_first_part = tk.LabelFrame(self, text="Increments and elements", height=100, padx=10, pady=10)
        self.frame_first_part.grid(row=0, column=0, columnspan=2, sticky="we")

        self.frame_first_part_set_inc = tk.LabelFrame(self.frame_first_part, height=25)
        self.frame_first_part.grid(row=0, column=0, sticky='we')

        self.frame_first_part_set_el = tk.LabelFrame(self.frame_first_part, height=25)
        self.frame_first_part.grid(row=0, column=1,  sticky='we')

        self.frame_first_part_range_inc = tk.LabelFrame(self.frame_first_part, height=25)
        self.frame_first_part.grid(row=1, column=0, sticky='we')

        self.frame_first_part_range_el = tk.LabelFrame(self.frame_first_part, height=25)
        self.frame_first_part.grid(row=0, column=1,  sticky='we')

        self.frame_output_request = tk.LabelFrame(self, text="Outputs", height=25)
        self.frame_output_request.grid(row=1, column=1, columnspan=2, sticky='we')

        self.frame_materials = tk.LabelFrame(self, text="Materials")
        self.frame_materials.grid(row=2, column=1, sticky='we')
        ##############

        _names = (u"All", u"Set", u"Range")

        self.label_increments = tk.Label(self.frame_first_part, text=u"Increments")
        self.label_increments.grid(row=0, column=0, sticky='we')

        self.label_elements = tk.Label(self.frame_first_part, text=u"Elements")
        self.label_elements.grid(row=0, column=1, sticky='we')

        ### listboxes ###
        self.listbox_increments = tk.Listbox(self.frame_first_part, height=3)
        self.listbox_increments.grid(row=1, column=0, sticky='we')
        self.create_listbox_values(self.listbox_increments, _names, exportselection=0)

        self.listbox_elements = tk.Listbox(self.frame_first_part, height=3)
        self.listbox_elements.grid(row=1, column=1, sticky='we')
        self.create_listbox_values(self.listbox_elements, _names, exportselection=0)

        self.listbox_increments_selceted = tk.Listbox(self.frame_first_part, exportselection=0, selectmode=tk.EXTENDED)
        self.listbox_elements_selceted = tk.Listbox(self.frame_first_part, exportselection=0, selectmode=tk.EXTENDED)

        self.listbox_output_2D = tk.Listbox(self.frame_output_request, exportselection=0, selectmode=tk.EXTENDED)
        _names = global_vars_storage.vars2D
        self.create_listbox_values(self.listbox_output_2D, _names, width=15, height=10)
        self.listbox_output_2D.grid(row=0, column=1)

        self.listbox_output_3D = tk.Listbox(self.frame_output_request, exportselection=0, selectmode=tk.EXTENDED)
        _names = global_vars_storage.vars3D
        self.create_listbox_values(self.listbox_output_3D, _names, width=15, height=10)

        self.listbox_grains = tk.Listbox(self.frame_materials, exportselection=0, selectmode=tk.EXTENDED)

        ##################
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

        self.entry_inc_max.bind('<Return>', lambda event: self.show_selection_lb("increments"))
        self.entry_el_max.bind('<Return>', lambda event: self.show_selection_lb("elements"))

        self.entry_step, self.label_step = self.create_entry_integer(
            self.frame_output_request, "Step", 0, 2, 10)

        self.entry_name_grain, self.label_add_grain = self.create_entry(self.frame_materials, "Part name", 0, 0, 25)
        # last part of gui
        self.entry_add_grain = tk.Entry(self.frame_materials)
        ###############

        ### buttons ###
        self.button_add_grain = tk.Button(
            self.frame_materials, text="Add grain", command=lambda: self.add_grain())

        self.button_remove_grain = tk.Button(
            self.frame_materials, text="Remove grain", command=lambda: self.remove_grain())

        self.button_test = tk.Button(self, text="Test czy cokolwiek dziala", command=lambda: test())
        self.button_test.grid(row=5, column=1, columnspan=2, sticky="we")

        ##############

        ### selections ###
        self.list_increments_sel = []
        self.list_elements_sel = []
        ##################

        ### optmemnu ###
        _names = ["2D", "3D"]
        self.variable_opt_menu = tk.StringVar(self.frame_output_request)
        self.variable_opt_menu.set(_names[0])  # default value

        self.menu_output = tk.OptionMenu(
            self.frame_output_request, self.variable_opt_menu, *_names, command=lambda opt: self.show_output_request())
        self.menu_output.grid(row=0, column=0, sticky="wnse")

        _names = ["All grain in one file",
                  "All grain in order M1, M2, Mx",
                  "Selected grain"]
        self.variable_material_menu = tk.StringVar(self.frame_materials)
        self.variable_material_menu.set(_names[0])  # default value

        self.menu_materials = tk.OptionMenu(
            self.frame_materials, self.variable_material_menu, *_names, command=lambda mat: self.show_grains())
        self.menu_materials.grid(row=1, column=0, columnspan=2, sticky="wnse")
        #################

    def show_first_part_inc(self):
        increments = self.listbox_increments.get(self.listbox_increments.curselection())
        if increments == u"Set":
            self.frame_first_part_range_inc.grid_remove()
            self.frame_first_part_set_inc.grid(row=2, column=0, sticky='we')
            self.show_selection_lb("increments")
        elif increments == u"Range":
            self.frame_first_part_set_inc.grid_remove()
            self.frame_first_part_range_inc.grid(row=2, column=0, sticky='we')
            self.listbox_increments_selceted.grid_remove()
        else:
            self.frame_first_part_set_inc.grid_remove()
            self.frame_first_part_range_inc.grid_remove()
            self.listbox_increments_selceted.grid_remove()

    def show_first_part_el(self):
        elements = self.listbox_elements.get(self.listbox_elements.curselection())
        if elements == u"Set":
            self.frame_first_part_range_el.grid_remove()
            self.frame_first_part_set_el.grid(row=2, column=1, sticky='we')
            self.show_selection_lb("elements")
        elif elements == u"Range":
            self.frame_first_part_set_el.grid_remove()
            self.frame_first_part_range_el.grid(row=2, column=1, sticky='we')
            self.listbox_elements_selceted.grid_remove()

        else:
            self.frame_first_part_set_el.grid_remove()
            self.frame_first_part_range_el.grid_remove()
            self.listbox_elements_selceted.grid_remove()

    def show_selection_lb(self, part):
        if part == "increments":
            self.listbox_increments_selceted.grid(row=4, column=0)
            self.listbox_increments_selceted.delete(0, tk.END)
            counter = self.entry_inc_max.get()
            if counter:
                for i in range(int(counter)):
                    self.listbox_increments_selceted.insert(i, "element %s" % i)

        if part == "elements":
            self.listbox_elements_selceted.grid(row=4, column=1)
            self.listbox_elements_selceted.delete(0, tk.END)
            counter = self.entry_el_max.get()
            if counter:
                for i in range(int(counter)):
                    self.listbox_elements_selceted.insert(i, "element %s" % i)

    def show_output_request(self):
        part = self.variable_opt_menu.get()
        if part == "2D":
            self.listbox_output_3D.grid_remove()
            self.listbox_output_2D.grid(row=0, column=1)
            self.is_acticve3D = False

        if part == "3D":
            self.listbox_output_2D.grid_remove()
            self.listbox_output_3D.grid(row=0, column=1)
            self.is_acticve3D = True

    def show_grains(self):
        if self.variable_material_menu.get() == "Selected grain":
            # showing widgets
            self.entry_add_grain.grid(row=1, column=1, sticky="we")
            self.entry_add_grain.grid(row=2, column=0, columnspan=2, sticky="we")
            self.button_add_grain.grid(row=3, column=0, sticky="we")
            self.button_remove_grain.grid(row=3, column=1, sticky="we")
            self.listbox_grains.grid(row=4, column=0, columnspan=2, sticky="wesne")
        else:
            self.entry_add_grain.grid_remove()
            self.button_add_grain.grid_remove()
            self.button_remove_grain.grid_remove()
            self.entry_add_grain.grid_remove()
            self.listbox_grains.grid_remove()

    def add_grain(self):
        name = self.entry_add_grain.get()
        self.listbox_grains.insert(tk.END, name)

    def remove_grain(self):
        names = self.listbox_grains.curselection()
        for i in names:
            self.listbox_grains.delete(i)


class OptionPage(Page):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.parent = parent
        self.controller = controller

        self.button_save_location = tk.Button(self, text="SaveLocation", command=lambda: self.get_file_path())
        self.button_save_location.grid(row=4, column=0, columnspan=2, sticky="we")

        self.entry_odb_path = tk.Entry(self)
        self.entry_odb_path.grid(row=1, column=0,  sticky="we")

    def get_file_path(self):
        path = tkFileDialog.askopenfilename(parent=self.parent, filetypes=[("ODB files", "*.odb")])
        self.entry_odb_path.insert(tk.END, path)
        config.odb_fullpath = path
        config.odb_path, config.odb_name = os.path.split(path)

        self.controller.show_frame("StartPage")
