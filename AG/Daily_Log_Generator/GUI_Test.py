from tkinter import *
from tkinter import messagebox
from tkinter import filedialog


window = Tk()
window.title("Welcome to Madison's app")

# Sets default window size
window.geometry('350x200')

# Creates a text label
lbl = Label(window, text="Enter text here: ", font=("Arial Bold", 10), fg="blue")
lbl.grid(column=0, row=0)

# Create an input box
txt = Entry(window, width=10)
txt.grid(column=1, row=0)
txt.focus()  # set focus to this widget

# function to handle button click event
def clicked():
    res = "Welcome to " + txt.get()
    lbl.configure(text=res)
    messagebox.showerror('Message title', 'Message content')

# Creates a button
btn = Button(window, text="Click Me", bg="orange", fg="red", command=clicked)
btn.grid(column=2, row=0)

# Adds a file dialog
file = filedialog.askopenfilename()

window.mainloop()

# https://likegeeks.com/python-gui-examples-tkinter-tutorial/
