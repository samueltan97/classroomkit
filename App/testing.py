import matplotlib.pyplot as mpl
from tkinter import *

def doThing():
    names = ("John", "Jane", "Bob")
    values = ("10", "20", "50")
    # Given names of students and corresponding frequency of attendance, graphs
    # number of times they were present.
    mpl.bar(names,values)
    mpl.ylabel("Classes Attended")
    mpl.xlabel("Student")
    mpl.show()
    # Given dates and corresponding number of students present, graphs the number
    # of people at any given date
    mpl.bar(names, values)
    mpl.ylabel("Students Attended")
    mpl.xlabel("Class Dates")
    mpl.show()
def doThing2():


    root = Tk()

    height = 5
    width = 5
    for i in range(height):  # Rows
        for j in range(width):  # Columns
            b = Label(root, text="Place")
            b.grid(row=i, column=j)

    mainloop()
def doThing3():
    root = Tk()
    names = ("Bpb", "John", "Mary", "Madeline")
    dates = ("11/1", "11/2", "11/3", "11/4")
    i = 1
    j = 1
    for name in names:
        btn_column = Button(root, text=name)
        btn_column.grid(row=0, column=j)
        j += 1
    for date in dates:
        btn_row = Label(root, text=date)
        btn_row.grid(row = i, column = 0)
        i += 1
    root.mainloop()
def doThing4():
    root = Tk()
    # use width x height + x_offset + y_offset (no spaces!)

    root.title('listbox with scrollbar')
    # create the listbox (height/width in char)
    listbox = Listbox(root, width=100, height=6)
    listbox.grid(row=0, column=0)
    # create a vertical scrollbar to the right of the listbox
    #yscroll = Scrollbar(command=listbox.yview, orient=VERTICAL)
    #yscroll.grid(row=0, column=1, sticky='ns')
    #listbox.configure(yscrollcommand=yscroll.set)


    # create a vertical scrollbar to the right of the listbox
    xscroll = Scrollbar(command=listbox.xview, orient=HORIZONTAL)
    xscroll.grid(row=1, column=0, sticky='ns')
    listbox.configure(xscrollcommand=xscroll.set)
    # now load the listbox with data
    friend_list = [
        'Stew', 'Tom', 'Jen', 'Adam', 'Ethel', 'Barb', 'Tiny',
        'Tim', 'Pete', 'Sue', 'Egon', 'Swen', 'Albert']
    for item in friend_list:
        # insert each new item to the end of the listbox
        listbox.insert('end', item)
    # optionally scroll to the bottom of the listbox
    lines = len(friend_list)
    listbox.yview_scroll(lines, 'units')
    root.mainloop()

global v
def doThing5():
    global v
    master = Tk()

    v = IntVar()

    Radiobutton(master, text="One", variable=v, value=1).pack(anchor=W)
    Radiobutton(master, text="Two", variable=v, value=2).pack(anchor=W)
    Button(master, text="value?", command = getV).pack(anchor=S)
    mainloop()

def getV():
    global v
    print(v.get())

doThing5()

