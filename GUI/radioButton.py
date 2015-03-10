from Tkinter import *

def sel():
	selection = "You selected the option " + str(var.get())
	label.config(text = selection)
	print str(var.get())

root = Tk()
var = IntVar()
for n in range(1,10):
	R1 = Radiobutton(root, text="Option "+str(n), variable=var, value=n)
	R1.pack( anchor = W )
b = Button(root, text="get", width=10, command=sel)
b.pack()

label = Label(root)
label.pack()
root.mainloop()