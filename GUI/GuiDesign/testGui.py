from Tkinter import *
import ttk
# from abaqus import *
# from abaqusConstants import *
#from django import forms





def testFunction():
    class GuiApplication:
        def __init__(self):
            self.master = Tk()

            self.v = IntVar()

            self.sphericalIndenterImage = PhotoImage(file="leonardo-da-vinci.ppm")
            self.vickersIndenterImage = PhotoImage(file="marco-polo.ppm")
            self.berkovichIndenterImage = PhotoImage(file="Plato-raphael.ppm")
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
            self.indenterComboBox.bind("<<ComboboxSelected>>", self.changeIndenterImage)
            self.indenterComboBox.pack()
            self.indenterImageLabel.image = self.sphericalIndenterImage
            self.indenterImageLabel.pack()

            self.button = Button(self.frame, text="test-close", command=self.close_window)
            self.button.pack()

            mainloop()

        def close_window(self):
            self.master.destroy()



        def changeIndenterImage(self, event):
            if self.indenterComboBox.get() == 'spherical':
                self.indenterImageLabel.configure(image=self.sphericalIndenterImage)
            elif self.indenterComboBox.get() == "Vickers":
                self.indenterImageLabel.configure(image=self.vickersIndenterImage)
            elif self.indenterComboBox.get() == "Berkovich":
                self.indenterImageLabel.configure(image=self.berkovichIndenterImage)


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



