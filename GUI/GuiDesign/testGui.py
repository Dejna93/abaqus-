from Tkinter import *
import ttk
# from abaqus import *
# from abaqusConstants import *
#from django import forms

#execfile("abaqusCommands.py")
import abaqusCommands
import actualAbaqusCommands

import os
dir_path = os.path.dirname(os.path.realpath(__file__))


def testFunction():
    class GuiApplication:
        def __init__(self):
            self.master = Tk()

            self.rounding_float_value = 0.0
            self.previous_rounding_value = StringVar()
            self.previous_rounding_value.set("0.0")

            self.v = IntVar()

            self.abaqus = actualAbaqusCommands.ActualAbaqusCommands()
            # self.abaqus = abaqusCommands.AbaqusCommands()

            self.sphericalIndenterImage = PhotoImage(file=dir_path+"/"+"leonardo-da-vinci.ppm")
            self.vickersIndenterImage = PhotoImage(file=dir_path+"/"+"marco-polo.ppm")
            self.berkovichIndenterImage = PhotoImage(file=dir_path+"/"+"Plato-raphael.ppm")
            Radiobutton(self.master, text="steel", variable=self.v, value=1, command=self.steel).pack(anchor=W)
            Radiobutton(self.master, text="titanium", variable=self.v, value=2, command=self.titanium).pack(anchor=W)

            self.frame = Frame(self.master)
            self.frame.pack()

            self.indenterLabel = ttk.Label(self.frame, text="Please select one of the indenters available below:")
            self.indenterLabel.pack()
            self.indenters = ('spherical', 'Vickers', 'Berkovich')
            self.indenterComboBox = ttk.Combobox(self.frame, values=self.indenters, textvariable=self.indenters)
            self.indenterImageLabel = ttk.Label(self.frame, image=self.sphericalIndenterImage)
            self.indenterComboBox.current(newindex=0)
            self.indenterComboBox.bind("<<ComboboxSelected>>", self.update_gui_on_selected_indenter)
            self.indenterComboBox.pack()

            self.roundingValue = StringVar()
            self.roundingValue.set("0.0")
            self.roundingValue.trace("w", lambda name, index, mode, roundingValue=self.roundingValue: self.on_rounding_input(roundingValue))

            self.roundingEntry = ttk.Entry(self.master, textvariable=self.roundingValue)
            self.indenterRoundingLabel = ttk.Label(self.frame, text="rounding radius:")
            self.indenterImageLabel.image = self.sphericalIndenterImage
            self.indenterImageLabel.pack()

            self.button = Button(self.frame, text="done", command=self.close_window)
            self.button.pack()



            mainloop()

        def on_rounding_input(self, rounding_value):
            try:
                self.rounding_float_value = float(rounding_value.get())
                print(self.rounding_float_value)
                self.previous_rounding_value.set(rounding_value.get())
            except:
                rounding_value.set(self.previous_rounding_value.get())







        def close_window(self):
            self.abaqus.setindenter(self.indenterComboBox.get(), self.rounding_float_value)
            #print(self.indenterComboBox.get())

            self.master.destroy()



        def update_gui_on_selected_indenter(self, event):
            if self.indenterComboBox.get() == 'spherical':
                self.button.pack_forget()
                self.button.grid_forget()
                self.indenterRoundingLabel.pack_forget()
                self.indenterImageLabel.configure(image=self.sphericalIndenterImage)
                self.button.pack()
            elif self.indenterComboBox.get() == "Vickers":
                self.button.pack_forget()
                self.button.grid_forget()
                self.indenterRoundingLabel.pack()
                self.roundingEntry.pack()
                self.indenterImageLabel.configure(image=self.vickersIndenterImage)
                self.button.pack()
            elif self.indenterComboBox.get() == "Berkovich":
                self.button.pack_forget()
                self.button.grid_forget()
                self.indenterRoundingLabel.pack()
                self.roundingEntry.pack()
                self.indenterImageLabel.configure(image=self.berkovichIndenterImage)
                self.button.pack()

        def steel(self):
            pass
            # mdb.models['Model-1'].Material('AISI 1005 Steel')
            # mdb.models['Model-1'].materials['AISI 1005 Steel'].Density(table=((7872,),))
            # mdb.models['Model-1'].materials['AISI 1005 Steel'].Elastic(table=((200E9, 0.29),))

        def titanium(self):
            pass
            # mdb.models['Model-1'].Material('Titanium')
            # mdb.models['Model-1'].materials['Titanium'].Density(table=((4500,),))
            # mdb.models['Model-1'].materials['Titanium'].Elastic(table=((200E9, 0.3),))
    app = GuiApplication()





    class AbaqusCommands:
        def __init__(self):
            pass

        def setIndenter(self, indenter):
            if indenter == 'spherical':
                pass

            elif indenter == 'Vickers':
                pass

            elif indenter == 'Berkovich':
                pass

        # Materials = [
        #     ("Steel", "mode"),
        #     ("Titanium", "mode"),
        #     ("GOLD", "mode"),
        # ]
        #
        # v = Tkinter.StringVar()
        # v.set("L")
        #
        # for text, mode in Materials:
        #     b = Tkinter.Radiobutton(top, text=text,
        #                             variable=v, value=mode)
        #     b.pack(anchor=Tkinter.W)

        #
        # mdb.models['Model-1'].Material('Titanium')
        # mdb.models['Model-1'].materials['Titanium'].Density(table=((4500, ), ))
        # mdb.models['Model-1'].materials['Titanium'].Elastic(table=((200E9, 0.3), ))
        #
        # mdb.models['Model-1'].Material('AISI 1005 Steel')
        # mdb.models['Model-1'].materials['AISI 1005 Steel'].Density(table=((7872, ), ))
        # mdb.models['Model-1'].materials['AISI 1005 Steel'].Elastic(table=((200E9, 0.29), ))
        #
        # mdb.models['Model-1'].Material('Gold')
        # mdb.models['Model-1'].materials['Gold'].Density(table=((19320, ), ))
        # mdb.models['Model-1'].materials['Gold'].Elastic(table=((77.2E9, 0.42), ))




if __name__ == '__main__':
    testFunction()



