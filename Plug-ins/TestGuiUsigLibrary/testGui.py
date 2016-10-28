from Tkinter import *
from abaqus import *
from abaqusConstants import *
#from django import forms





def testFunction():
    def close_window():
        master.destroy()

    def steel():
        pass
        mdb.models['Model-1'].Material('AISI 1005 Steel')
        mdb.models['Model-1'].materials['AISI 1005 Steel'].Density(table=((7872,),))
        mdb.models['Model-1'].materials['AISI 1005 Steel'].Elastic(table=((200E9, 0.29),))

    def titanium():
        pass
        mdb.models['Model-1'].Material('Titanium')
        mdb.models['Model-1'].materials['Titanium'].Density(table=((4500,),))
        mdb.models['Model-1'].materials['Titanium'].Elastic(table=((200E9, 0.3),))

    master = Tk()

    v = IntVar()

    Radiobutton(master, text="steel", variable=v, value=1, command=steel).pack(anchor=W)

    Radiobutton(master, text="titanium", variable=v, value=2, command=titanium).pack(anchor=W)

    frame = Frame(master)
    frame.pack()
    button = Button(frame, text="test-close", command=close_window)
    button.pack()

    mainloop()



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




# if __name__ == '__main__':
#     testFunction()



