"""Just Instalator Gui"""
import Tkinter as tk
import os
import ttk as ttk
import tkFileDialog

import subprocess

from manage_plugins import AbaqusInstalator
from settings import config

setup = AbaqusInstalator()


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
        self.parent = parent


        ### Location frame###
        # labels frame
        self.frame_dialog_dir = tk.LabelFrame(self, text="Location", height=100, padx=10, pady=10)
        self.frame_dialog_dir.grid(row=0, column=0, sticky='we')

        # entries
        _v_abaqus_dir = tk.StringVar()
        _v_plugin_dir = tk.StringVar()

        self.entry_abaqus_dir = tk.Entry(self.frame_dialog_dir, width=25, textvariable=_v_abaqus_dir)
        self.entry_abaqus_dir.grid(row=0, column=1, sticky=tk.W)
        _v_abaqus_dir.set(config.ABAQUS_DIR)
        self.entry_plugin_dir = tk.Entry(self.frame_dialog_dir, width=25, textvariable=_v_plugin_dir)
        self.entry_plugin_dir.grid(row=1, column=1, sticky=tk.W)
        _v_plugin_dir.set(config.PROJECT_PLUGIN)
        # buttons
        self.button_abaqus_dir = tk.Button(self.frame_dialog_dir, text="Choose Abaqus directory", width=25,
                                      command=lambda: self.set_location(entry=self.entry_abaqus_dir))
        self.button_abaqus_dir.grid(row=0, column=0, sticky=tk.W, padx=5, pady=5)

        self.button_abaqus_dir = tk.Button(self.frame_dialog_dir, text="Choose Your plugin directory", width=25,
                                      command=lambda: self.set_location(entry=self.entry_plugin_dir))
        self.button_abaqus_dir.grid(row=1, column=0, sticky=tk.W, padx=5, pady=5)

        self.button_save_config = tk.Button(self.frame_dialog_dir, text="Save paths", width=25,
                                           command=lambda: self.update_settings())
        self.button_save_config.grid(row=2, sticky='we', padx=5, pady=5)

        ### Option frame###
        # labels frame
        self.frame_options = tk.LabelFrame(self, text="Options", height=100, padx=10, pady=10)
        self.frame_options.grid(row=1, column=0, sticky='we')

        # buttons
        self.button_install_libs = tk.Button(self.frame_options, text="Install Libs in Abaqus", width=25,
                                      command=lambda: self.set_location(entry=self.entry_abaqus_dir))
        self.button_install_libs.grid(row=0, column=0, sticky=tk.W, padx=5, pady=5)

        self.button_install_plugin = tk.Button(self.frame_options, text="Collect necessary libs", width=25,
                                          command=lambda: setup.collect_libs())
        self.button_install_plugin.grid(row=0, column=1, sticky=tk.W, padx=5, pady=5)

        self.button_install_plugin = tk.Button(self.frame_options, text="Install your plugin", width=25,
                                      command=lambda: setup.copy_files(
                                          config.PROJECT_PLUGIN, config.ABAQUS_LIBS_DIR, flat=False))
        self.button_install_plugin.grid(row=1, column=0, sticky=tk.W, padx=5, pady=5)

        ### Option frame###
        # labels frame
        self.frame_progress_bar = tk.LabelFrame(self, text="Options", height=100, padx=10, pady=10)
        self.frame_progress_bar.grid(row=3, column=0, sticky='we')

        # progressbar
        self.progress = ttk.Progressbar(self.frame_progress_bar, orient="horizontal", length=400, mode="determinate")
        self.progress.grid(row=3, column=0)



    # return path to choosen directory
    def get_file_path(self):
        return tkFileDialog.askdirectory(parent=self.parent, initialdi='.')

    def set_location(self, entry):
        entry.delete(0, tk.END)
        entry.insert(0, self.get_file_path())

    def progress_bar_start(self):
        self.progress["value"] = 0
        self.maxbytes = 50000
        self.progress["maximum"] = 50000
        self.read_bytes()

    def progress_bar_read_bytes(self):
        '''simulate reading 500 bytes; update progress bar'''
        self.bytes += 500
        self.progress["value"] = self.bytes
        if self.bytes < self.maxbytes:
            # read more bytes after 100 ms
            self.after(100, self.read_bytes)

    def update_settings(self, *args, **kwargs):
        config_vars = {
            'ABAQUS_DIR': self.entry_abaqus_dir.get(),
            'PROJECT_PLUGIN': self.entry_plugin_dir.get()
        }
        with open(config.CONFIG_PATH, 'w') as config_file:
            for key, value in config_vars.items():
                config_file.write(key + "=" + value + '\n')


class PageOne(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)



def run_gui():
    app = Core()
    app.minsize(width=425, height=400)
    app.mainloop()

if __name__ == '__main__':
    run_gui()