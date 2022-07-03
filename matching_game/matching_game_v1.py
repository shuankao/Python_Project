import tkinter as tk
from tkinter import messagebox
import random


root = tk.Tk()
root.title("Matching Game")
root.geometry('400x350')

button_list = []
match_list = [1,1,2,2,3,3,4,4,5,5,6,6]
random.shuffle(match_list)

first_guess_pos = -1
count = 0

def button_click(i):
    # global variables cannot be used before assignment in function
    # so declare global in function to allow global var to be seen in local function
    global count,first_guess_pos
    if count < 2:
        button_list[i]["text"] = match_list[i]
        if count == 0: 
            first_guess_pos = i 
        count += 1    
    if count == 2:
        if match_list[first_guess_pos] == match_list[i]:
            button_list[i]["state"] = "disabled"
            button_list[first_guess_pos]["state"] = "disabled"
        else:
            tk.messagebox.showinfo("Error","Incorrect!")
            button_list[first_guess_pos]["text"] = " "
            button_list[i]["text"] = " "
        first_guess_pos = -1
        count = 0    

def build_but():
    for i in range(len(match_list)):
        button_list.append(tk.Button(root,text = " ", state = "active", height = 5, width = 10, command = lambda i=i: button_click(i)))
        button_list[i].grid(row = int(i/4),column = i%4)

build_but()

def restart():
    global count
    button_list.clear()
    build_but()
    random.shuffle(match_list)
    first_guess_pos = -1
    count = 0
but_restart = tk.Button(root,text = "Restart",height = 1, width = 5, command = lambda:restart())
but_restart.grid(row = 4,column = 1, pady = 20)

tk.mainloop()
