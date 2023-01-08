import tkinter as tk

def listbox_event(event):
    object = event.widget
    # print(type(object.curselection()))
    print(object.curselection())
    index = object.curselection()
    mylabel.configure(text=object.get(index))

root = tk.Tk()
root.title('my window')
root.geometry('200x180')

mylabel = tk.Label(root)
mylabel.pack()

mylistbox = tk.Listbox(root)
for i in ['apple','banana','orange','lemon','tomato','apple','banana','orange','lemon','tomato','apple','banana','orange','lemon','tomato','apple','banana','orange','lemon','tomato']:
    mylistbox.insert(tk.END, i)
mylistbox.bind("<<ListboxSelect>>", listbox_event)
mylistbox.pack()

root.mainloop()