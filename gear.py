from tkinter import *
import tkinter.font as tkFont
from PIL import ImageTk,Image
from tkinter import filedialog
import os 
import numpy as np
import tensorflow as tf
import matplotlib.pyplot as plt
import matplotlib.image as mpimg
from scipy import ndimage, misc
import numpy as np
import os
import cv2
import tkinter as tk
from math import log
class HoverButton(tk.Button):
    def __init__(self, master, **kw):
        tk.Button.__init__(self,master=master,**kw)
        self.defaultBackground = self["background"]
        self.bind("<Enter>", self.on_enter)
        self.bind("<Leave>", self.on_leave)
    def on_enter(self, e):
        self['background'] = self['activebackground']
    def on_leave(self, e):
        self['background'] = self.defaultBackground
def read_img(path):
    img=tf.io.read_file(path)
    img=tf.image.decode_jpeg(img,3)
    img=tf.image.convert_image_dtype(img,tf.float32)
    img=tf.image.resize(img,(224,224))
    img=tf.clip_by_value(img,0.0,1.0)
    return img
def start():
    global model_ss
    status = Label(frame5, text ="Model Initiation", anchor=W, bd=0, bg="black", fg="white")
    status.grid(row=2, sticky="w", padx=350, ipadx=500)
    model_ss=tf.keras.models.load_model(r'C:\MLCourse\CNN\3')   
def insert_image():
    status = Label(frame5, text ="Insert Image", anchor=W, bd=0, bg="black", fg="white")
    status.grid(row=2, sticky="w", padx=350, ipadx=500)
    root.filename=filedialog.askopenfilename(initialdir="/", title="Select Image", filetypes=(("jpeg files","*.jpg"),("all files","*.*"))) 
    global IMAGE
    IMAGE = root.filename
    my_img2=Image.open(IMAGE)
    my_img3 = my_img2.resize((400, 410),Image.ANTIALIAS)
    photo=ImageTk.PhotoImage(my_img3)
    my_img3=Label(frame3, image=photo, width =450, height=450, bg="#F5F5F5", borderwidth=5)
    my_img3.image=photo
    my_img3.grid(row =1, column=2, rowspan=3, sticky="new", ipady=0)
def inspect():
    status = Label(frame5, text ="Inspection Results", anchor=W, bd=0, bg="black", fg="white")
    status.grid(row=2, sticky="w", padx=350, ipadx=500)
    img=read_img(IMAGE)
    img=tf.expand_dims(img,0)
    pred=model_ss(img,training=False)
    if pred > 0.5:
        y =1
        sum =0
        my_label2 = Label(frame4, text = "Gear is damaged", font=helv34, fg="red")
        my_label2.grid(row=1, column=3,  sticky="w")
        sum = sum + (y*log(pred) + (1-y)*log(1-pred))
        c = (-1)*sum
        acc= '%2.2f' % (pred)
        acc2=float(acc) * 100
        mylabel3 = Label(frame4, text = str(acc2)+"%", font=helv34, fg="red")
        mylabel3.grid(row=2, column=3, sticky="w")
        c2= '%2.2f' % c
        c3=float(c2) * 100
        mylabel4 = Label(frame4, text = str(c3)+"%", font=helv34, fg="red")
        mylabel4.grid(row=3, column=3, sticky="w")
        my_label21 = Label(frame4, text = "Helical", font=helv34, fg="red")
        my_label21.grid(row=1, column=5,  sticky="w")
        my_label31 = Label(frame4, text = "Automotive/Transmission", font=helv34, fg="red")
        my_label31.grid(row=2, column=5,  sticky="w")
        my_label51 = Label(frame4, text = "Stainless-Steel", font=helv34, fg="red")
        my_label51.grid(row=3, column=5,  sticky="w")
    else:
        y =0
        sum =0
        my_label2 = Label(frame4, text = "Gear is in healthy condition", font=helv34, fg="red")
        my_label2.grid(row=1, column=3,  sticky="w")
        sum = sum + (y*log(pred) + (1-y)*log(1-pred))
        c = (-1)*sum
        acc= '%2.2f' % (1-pred)
        acc2=float(acc) * 100
        mylabel3 = Label(frame4, text = str(acc2)+"%", font=helv34, fg="red")
        mylabel3.grid(row=2, column=3, sticky="w")
        c2= '%2.2f' % c
        c3=float(c2) * 100
        mylabel4 = Label(frame4, text = str(c3)+"%", font=helv34, fg="red")
        mylabel4.grid(row=3, column=3, sticky="w")
        my_label21 = Label(frame4, text = "Helical", font=helv34, fg="red")
        my_label21.grid(row=1, column=5,  sticky="w")
        my_label31 = Label(frame4, text = "Automotive/Transmission", font=helv34, fg="red")
        my_label31.grid(row=2, column=5,  sticky="w")
        my_label51 = Label(frame4, text = "Stainless-Steel", font=helv34, fg="red")
        my_label51.grid(row=3, column=5,  sticky="w")                    
def donothing():
    return
root = tk.Tk()
root.geometry('{}x{}'.format(800,600))
root.title("Gears Inspector")
root.iconbitmap(r"C:\MLCourse\CNN\GUI\icon.ico")
root.configure(background='#F5F5F5')
root.resizable(False, False)
root.grid_rowconfigure(1, weight=1)
root.grid_columnconfigure(0, weight=1)
menubar = Menu(root)
filemenu = Menu(menubar, tearoff=0)
filemenu.add_command(label="New Inspection", command=donothing)
filemenu.add_command(label="Open", command=donothing)
filemenu.add_command(label="Save", command=donothing)
filemenu.add_separator()
filemenu.add_command(label="Exit", command=root.destroy)
menubar.add_cascade(label="File", menu=filemenu)
reportmenu = Menu(menubar, tearoff=0)
reportmenu.add_command(label="Create a new report", command=donothing)
reportmenu.add_command(label="Load a report", command=donothing)
reportmenu.add_command(label="Window", command=donothing)
menubar.add_cascade(label="Report", menu=reportmenu)
editmenu = Menu(menubar, tearoff=0)
editmenu.add_command(label="Style", command=donothing)
editmenu.add_command(label="Fonts", command=donothing)
editmenu.add_command(label="Window", command=donothing)
menubar.add_cascade(label="Edit", menu=editmenu)
viewmenu = Menu(menubar, tearoff=0)
viewmenu.add_command(label="Zoom", command=donothing)
viewmenu.add_command(label="Zoom fit", command=donothing)
menubar.add_cascade(label="View", menu=viewmenu)
helpmenu = Menu(menubar, tearoff=0)
helpmenu.add_command(label="Help index", command=donothing)
helpmenu.add_command(label="About...", command=donothing)
menubar.add_cascade(label="Help", menu=helpmenu)
root.config(menu=menubar)
frame1 = tk.Frame(root, bg="black", width=800, height=200, pady =3)
frame1.grid(row=0, columnspan=3,sticky="ew")
frame12= tk.Frame(root, bg="black", width=800, height=1, pady =3)
frame12.grid(row=0, columnspan=3,sticky="s")
frame2 = tk.Frame(root, bg="#F5F5F5", width=400, height = 400)
frame2.grid(row=1,sticky="nw", ipadx=56, columnspan=3, ipady=96)
frame2.grid_rowconfigure(0, weight=1)
frame2.grid_columnconfigure(1, weight=1)
frame3 = tk.Frame(root, bg="#F5F5F5", width=500, height = 330)
frame3.grid(row=1, column=2, sticky="en")
frame31 = tk.Frame(root, bg="black", width=1, height = 550)
frame31.grid(row=1,column=1, pady=30)
frame4 = tk.Frame(root, bg="#F5F5F5", width=500, height = 150)
frame4.grid(row=2, sticky="ne", ipadx=115, columnspan=3)
frame5= tk.Frame(root, bg="black", width=800, height=20, pady =3)
frame5.grid(row=3, columnspan=3, sticky="s")
frame6= tk.Frame(root, bg="black", width=3, height=800)
frame6.grid(row=0, column=4, rowspan=4, sticky="ne")
frame7= tk.Frame(root, bg="black", width=3, height=800)
frame7.grid(row=0, column=0, rowspan=4, sticky="nw")
my_img = ImageTk.PhotoImage(Image.open(r'C:\MLCourse\CNN\GUI\icon2.png'))
my_img1=Label(frame1, image=my_img, width =50, height=50, bg="black")
helv35 = tkFont.Font(family="Lucida Console", size=30, weight="bold")
mylabel=Label(frame1, text="Gears Inspector", font=helv35, fg="white",pady=2, bg="black")
my_img1.grid(row =0, column=0)
mylabel.grid(row=0, column= 1)
my_img2=Image.open(r'C:\MLCourse\CNN\GUI\start12.png')
my_img3 = my_img2.resize((120, 90),Image.ANTIALIAS)
login_btn1=ImageTk.PhotoImage(my_img3)
my_img4=Image.open(r'C:\MLCourse\CNN\GUI\INSERT12.png')
my_img5 = my_img4.resize((120, 90),Image.ANTIALIAS)
login_btn2=ImageTk.PhotoImage(my_img5)
my_img6=Image.open(r'C:\MLCourse\CNN\GUI\INSPECT12.png')
my_img7 = my_img6.resize((120, 90),Image.ANTIALIAS)
login_btn3=ImageTk.PhotoImage(my_img7)
my_img8=Image.open(r'C:\MLCourse\CNN\GUI\EXIT12.png')
my_img9 = my_img8.resize((120, 90),Image.ANTIALIAS)
login_btn4=ImageTk.PhotoImage(my_img9)
helv36 = tkFont.Font(family="Time", size=10, weight="bold")
mybutton1 = HoverButton(frame2, image=login_btn1, command=start, fg="black", font=helv36, padx=30, pady=10, width = 105, height=50, borderwidth=0, activebackground="#F7EA89")
mybutton2 = Button(frame2, image=login_btn2, width = 105, height=50, padx=30, pady=10, command=insert_image, fg="black", font=helv36, borderwidth=0) #activebackground="#FFA500"
mybutton3 = Button(frame2, image=login_btn3, padx=30, pady=10, command=inspect, fg="black", font=helv36, width = 105, height=50, borderwidth=0)
mybutton4 = Button(frame2, image=login_btn4, padx = 30, pady = 10, command=root.destroy, fg="black", font=helv36,  width = 105, height=50, borderwidth=0)
mybutton1.grid(row=0, column=2, sticky="e", pady=10)
mybutton2.grid(row=2, column=2, sticky="e", pady=10)
mybutton3.grid(row=3, column=2, sticky="e", pady=10)
mybutton4.grid(row=5, column=2, sticky="e", pady=40)
helv32 = tkFont.Font(family="Time", size=15, weight="bold")
label2= Label(frame3, text="Inspected Gear", font=helv32, pady=10, fg="Black", bg="#F5F5F5")
label2.grid(row=0, column=1, columnspan=3, ipadx=200)
helv33 = tkFont.Font(family="Time", size=13, weight="bold", underline=True)
label3= Label(frame4, text="Inspection Details", font=helv33, padx=3, pady=1, fg="black", bg="#F5F5F5")
label3.grid(row=0, column = 4)
helv34 = tkFont.Font(family="Time", size=11, weight="bold")
label4= Label(frame4, text="Gear Status:", font=helv34, pady=5, fg="black", bg="#F5F5F5")
label4.grid(row=1, column=2, ipadx=10, sticky="e")
label6= Label(frame4, text="Model Accuracy:", font=helv34, pady=5, fg="black", bg="#F5F5F5")
label6.grid(row=2, column = 2, ipadx=10, sticky="e")
label8= Label(frame4, text="Model Loss:", font=helv34, pady=5, padx=4, fg="black", bg="#F5F5F5")
label8.grid(row=3, ipadx=10, column=2, sticky="e")
label41= Label(frame4, text="Gear Type:", font=helv34, pady=5, fg="black", bg="#F5F5F5")
label41.grid(row=1, column=4, ipadx=10, sticky="e")
label61= Label(frame4, text="Service Type:", font=helv34, pady=5, fg="black", bg="#F5F5F5")
label61.grid(row=2, column = 4, ipadx=10, sticky="e")
label81= Label(frame4, text="Material:", font=helv34, pady=5, padx=4, fg="black", bg="#F5F5F5")
label81.grid(row=3, ipadx=10, column=4, sticky="e")
label7= Entry(frame4, font=helv34, fg="red", bg="#F5F5F5", borderwidth=0)
label7.grid(row=1, column=3)
label9= Entry(frame4, font=helv34, fg="red", bg="#F5F5F5", borderwidth=0)
label9.grid(row=2, column=3)
label10= Entry(frame4,font=helv34, fg="red", bg="#F5F5F5", borderwidth=0)
label10.grid(row=3, column=3) 
label71= Entry(frame4, font=helv34, fg="red", bg="#F5F5F5", borderwidth=0)
label71.grid(row=1, column=5)
label91= Entry(frame4, font=helv34, fg="red", bg="#F5F5F5", borderwidth=0)
label91.grid(row=2, column=5)
label11= Entry(frame4,font=helv34, fg="red", bg="#F5F5F5", borderwidth=0)
label11.grid(row=3, column=5) 
root.mainloop()