"""Just Instalator Gui"""
import Tkinter as tk
import os
import threading
import tkFileDialog

import time

from manage_plugins import AbaqusInstalator
from settings import config

manage_plugin = AbaqusInstalator()


class ThreadedTask(threading.Thread):
    def __init__(self, queue):
        threading.Thread.__init__(self)
        self.queue = queue

    def run(self):
        time.sleep(5)  # Simulate long running process
        self.queue.put("Task finished")


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

        ### Location frame ###
        # labels frame
        self.frame_dialog_dir = tk.LabelFrame(self, text="Location", height=100, padx=10, pady=10)
        self.frame_dialog_dir.grid(row=0, column=0, sticky='we')

        # entries
        self._v_abaqus_dir = tk.StringVar()
        self._v_plugin_dir = tk.StringVar()

        self.entry_abaqus_dir = tk.Entry(self.frame_dialog_dir, width=25, textvariable=self._v_abaqus_dir)
        self.entry_abaqus_dir.grid(row=0, column=1, sticky=tk.W)
        self._v_abaqus_dir.set(config.ABAQUS_DIR)
        self.entry_plugin_dir = tk.Entry(self.frame_dialog_dir, width=25, textvariable=self._v_plugin_dir)
        self.entry_plugin_dir.grid(row=1, column=1, sticky=tk.W)
        self._v_plugin_dir.set(config.PROJECT_PLUGIN)

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

        ### Option frame ###
        # labels frame
        self.frame_options = tk.LabelFrame(self, text="Options", height=100, padx=10, pady=10)
        self.frame_options.grid(row=1, column=0, sticky='we')

        # buttons
        self.button_install_libs = tk.Button(self.frame_options, text="Install Libs in Abaqus", width=25,
                                             command=lambda: self.set_location(entry=self.entry_abaqus_dir))
        self.button_install_libs.grid(row=0, column=0, sticky=tk.W, padx=5, pady=5)

        self.button_collect_libs = tk.Button(self.frame_options, text="Collect necessary libs", width=25,
                                             command=lambda: manage_plugin.collect_libs())
        self.button_collect_libs.grid(row=0, column=1, sticky=tk.W, padx=5, pady=5)

        self.buttonrequirements = tk.Button(self.frame_options, text="Create requirements file", width=25,
                                            command=lambda: self.save_requirements())
        self.buttonrequirements.grid(row=1, column=1, sticky=tk.W, padx=5, pady=5)

        self.button_install_plugin = tk.Button(self.frame_options, text="Install your plugin", width=25,
                                               command=lambda: manage_plugin.copy_files(
                                                   config.PROJECT_PLUGIN, config.ABAQUS_LIBS_DIR, flat=False))
        self.button_install_plugin.grid(row=1, column=0, sticky=tk.W, padx=5, pady=5)

        self.button_install_plugin = tk.Button(self.frame_options, text="TestButton", width=25,
                                               command=lambda: GuiThreader(name='Save paths', function=self.test_threading()))
        self.button_install_plugin.grid(row=3, column=0, sticky=tk.W, padx=5, pady=5)

        ### Python command frame ###
        # labels frame
        self.frame_python_command = tk.LabelFrame(self, text="PythonComand", height=100, padx=10, pady=10)
        self.frame_python_command.grid(row=3, column=0, sticky='we')

        # labels
        self.label_python_comand = tk.Label(self.frame_python_command,
                                            text=u'There you can write python command using Python from Abaqus')
        self.label_python_comand.grid(row=0, column=0, sticky='we')

        # button
        self.button_python_command = tk.Button(self.frame_python_command, text="Run it!",
                                               command=lambda: self.run_command())
        self.button_python_command.grid(row=1, column=1, sticky='w', padx=5, pady=5)

        # entry
        self._v_python_comand = tk.StringVar()
        self.entry_python_command = tk.Entry(self.frame_python_command, textvariable=self._v_python_comand, width=25)
        self.entry_python_command.grid(row=1, column=0, sticky='we')

        ### TextArea frame ###
        # labels frame
        self.frame_textarea = tk.LabelFrame(self, text="TextArea", height=100, padx=10, pady=10)
        self.frame_textarea.grid(row=4, column=0, sticky='we')

        # textarea
        self.text_console_output = tk.Text(self.frame_textarea, height=20, borderwidth=3, relief="sunken")
        self.text_console_output.grid(row=0, column=0, sticky='we')

        # scrollbar
        self.scrollbar_textarea = tk.Scrollbar(self.frame_textarea, command=self.text_console_output.yview)
        self.scrollbar_textarea.grid(row=0, column=1, sticky='nsew')
        self.text_console_output['yscrollcommand'] = self.scrollbar_textarea.set

    # return path to choosen directory

    def set_location(self, entry):
        entry.delete(0, tk.END)
        entry.insert(0, self.get_file_path())

    def save_requirements(self):
        self.text_console_output.delete('1.0', tk.END)  # clear textarea
        self.text_console_output.insert(tk.END, "Requirements:\n")
        req, errors = manage_plugin.create_requirements_file()
        self.text_console_output.insert(tk.END, req)
        with open(os.path.join('.', os.path.join('docs', 'requirements.txt')), 'w') as file:
            file.write(req)

    def test(self):
        self.text_console_output.delete('1.0', tk.END)  # clear textarea
        for output, errors, lib in manage_plugin.libs_install_test():
            self.text_console_output.insert(tk.END, "Installing library: %s" % lib)
            self.text_console_output.insert(tk.END, "Output from pip: %s\n" % output)
            self.text_console_output.insert(tk.END, "Errors: %s\n" % errors)

    def run_command(self):
        self.text_console_output.delete('1.0', tk.END)  # clear textarea
        output, errors = manage_plugin.python_command(self._v_python_comand.get())
        self.text_console_output.insert(tk.END, "Output: \n%s\n" % output)
        self.text_console_output.insert(tk.END, "Errors: \n%s\n" % errors)

    def update_settings(self, *args, **kwargs):
        config_vars = {
            'ABAQUS_DIR': self.entry_abaqus_dir.get(),
            'PROJECT_PLUGIN': self.entry_plugin_dir.get()
        }

        self.text_console_output.delete('1.0', tk.END)
        self.text_console_output.insert(tk.END, "Saved paths:\n")
        with open(config.CONFIG_PATH, 'w') as config_file:
            for key, value in config_vars.items():
                opt = key + "=" + value + '\n'
                config_file.write(opt)
                self.text_console_output.insert(tk.END, opt)


class PageOne(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)


def run_gui():
    app = Core()
    app.minsize(width=425, height=400)
    app.mainloop()


if __name__ == '__main__':
    run_gui()
