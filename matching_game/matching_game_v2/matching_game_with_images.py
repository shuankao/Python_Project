import tkinter as tk
import tkinter.messagebox
import random
from PIL import Image,ImageTk
from pathlib import Path
import os
import time
import sys

root = tk.Tk()
root.title("Matching Game")
root.geometry('1000x700')

button_list = []
image_list = []
image_list_double = []
photo_list = []
first_guess_pos = -1
count = 0
start_time = 0
finished_time = 0
record = sys.maxsize

# create card buttons and store them in button_list
def build_but():
    # global card_back
    for i in range(12):
        button_list.append(tk.Button(root,image = card_back,state = "disabled",width = 180, height = 180, command = lambda i=i: button_click(i)))
        button_list[i].grid(row = int(i/4),column = i%4)

# the image of the back of card is set as default image when buttons are built
# 'path' variable stores the directory(parent of file) where the .py is
path = Path(__file__).parent / "./images/card_back.jpg"
image = Image.open(path)
img = image.resize((180,180))
card_back = ImageTk.PhotoImage(img)

# create a start button
def go_click():
    global start_time
    for item in button_list:
        if item['state'] != "disabled":
            return
    for item in button_list:
        item['state'] = 'normal'
    start_time = time.time()


but_go = tk.Button(root,text = "Go", height = 2, width = 8, fg = "white", bg = "black", command = lambda:go_click())
but_go.grid(row = 4,column = 1,pady = 20)

# shuffle images everytime this function is called
# maintain opened images with image_list (which will later be combined with .getdata() to compare images)
def shuffle():
    for i in range(10):
        # 'basepath' variable stores the name of the directory where this .py is
        basepath = os.path.dirname(__file__)
        filepath = os.path.realpath(os.path.join(basepath,'images','image'+str(i+1)+'.png'))
        image = Image.open(filepath)
        img = image.resize((180,180))
        image_list.append(img)

    random.shuffle(image_list)

    # the first 6 elements of shuffled image_list will be copied once to create pairs of images
    for i in range(6):
        for j in range(2):
            image_list_double.append(image_list[i])

    random.shuffle(image_list_double)

# convert opened images into the data type which can be handled by tk.Button()
def change_to_photo():
    for i in range(12):
        photo_list.append(ImageTk.PhotoImage(image_list_double[i]))

# check if game is finished
def check_finished():
    for item in button_list:
        if(item['state'] != 'disabled'):
            return False
    return True
        
# action invoked by button click
def button_click(i):
    # global variables cannot be used before assignment in function
    # so declare global var in function to allow global var to be seen in local function
    global count,first_guess_pos,finished_time
    if count < 2:
        button_list[i]["image"] = photo_list[i]
        if count == 0: 
            first_guess_pos = i 
        count += 1    
    if count == 2:
        # see if the two images are the same
        # print(list(image_list_double[first_guess_pos].getdata()))
        # print(image_list_double[i].getdata())
        if list(image_list_double[first_guess_pos].getdata()) == list(image_list_double[i].getdata()):
            button_list[i]["state"] = "disabled"
            button_list[first_guess_pos]["state"] = "disabled"
        else:
            tk.messagebox.showinfo("Error","Incorrect!")
            button_list[first_guess_pos]["image"] = card_back
            button_list[i]["image"] = card_back
        first_guess_pos = -1
        count = 0 
    if check_finished():
        finished_time = time.time()
        time_span = finished_time-start_time
        formatted_time = "{:.2f}".format(time_span)
        tk.messagebox.showinfo("Congratulations!","Game is finished!\nTime spent: "+formatted_time)
        update_record(time_span)
        reset()
        

def update_record(time_span):
    global record
    if  time_span < record:
        if record != sys.maxsize:
            tk.messagebox.showinfo("Congratulations!","You broke the record!")
        record = time_span
        formatted_time = "{:.2f}".format(record)
        record_text = tk.Label(root,text = "Current Record:\n\n"+ formatted_time)
        record_text.grid(row = 0,column = 4,padx = 20)
    

record_text = tk.Label(root,text = "Current Record:\n\n")
record_text.grid(row = 0,column = 4,padx = 20)



# create Restart button
but_reset = tk.Button(root,text = "Reset",height = 2, width = 15,fg = "white", bg = "black", command = lambda:reset())
but_reset.grid(row = 4,column = 2,pady = 20)

# reset everything when Restart button clicked
def reset():
    global count
    button_list.clear()
    image_list.clear()
    image_list_double.clear()
    photo_list.clear()
    build_but()
    shuffle()
    change_to_photo()
    first_guess_pos = -1
    count = 0
    


# build 12 cards and ready for click
build_but()
shuffle()
change_to_photo()

tk.mainloop()

# for testing
# def click():
#     pass
# but = tk.Button(root, image = image_list[0],width = 100, height = 100,command = click())
# but.grid(row = 1,column = 1)