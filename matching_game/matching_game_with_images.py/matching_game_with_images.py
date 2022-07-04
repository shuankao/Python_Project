import tkinter as tk
import tkinter.messagebox
import random
from PIL import Image,ImageTk

root = tk.Tk()
root.title("Matching Game")
root.geometry('500x400')

button_list = []
image_list = []
image_list_double = []
photo_list = []
first_guess_pos = -1
count = 0

# create card buttons and store them in button_list
def build_but():
    # global card_back
    for i in range(12):
        button_list.append(tk.Button(root,image = card_back,width = 100, height = 100, command = lambda i=i: button_click(i)))
        button_list[i].grid(row = int(i/4),column = i%4)

# the image of the back of card is set as default image when buttons are built
image = Image.open('./images/card_back.jpg')
img = image.resize((100,100))
card_back = ImageTk.PhotoImage(img)


# shuffle images everytime this function is called
# maintain opened images with image_list (which will later be combined with .getdata() to compare images)
def shuffle():
    for i in range(10):
        image = Image.open('./images/image'+str(i+1)+'.png')
        img = image.resize((100,100))
        image_list.append(img)

    # the first 6 elements of shuffled image_list will be copied once to create pairs of images
    for i in range(6):
        for j in range(2):
            image_list_double.append(image_list[i])

    random.shuffle(image_list_double)

# convert opened images into the data type which can be handled by tk.Button()
def change_to_photo():
    for i in range(12):
        photo_list.append(ImageTk.PhotoImage(image_list_double[i]))

# action invoked by button click
def button_click(i):
    # global variables cannot be used before assignment in function
    # so declare global var in function to allow global var to be seen in local function
    global count,first_guess_pos
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

# create Restart button
but_restart = tk.Button(root,text = "Restart",height = 1, width = 5, command = lambda:restart())
but_restart.grid(row = 4,column = 1, pady = 20)

# reset everything when Restart button clicked
def restart():
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