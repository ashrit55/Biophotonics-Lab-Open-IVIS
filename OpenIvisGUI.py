# IVIS  System
# Developed by HMC Biophotonics Lab tea'
# Environment: Python on Raspberry PI
# Libraries used: Neopixel (Adafruit), PiCamera (native), tkinter for GUI

# This is the template code the GUI and controls for the LEDS
# and the camera systems.
# The system is currently configured for 3 LEDs
# More LEDs can be added, Additional button controls to switch on/off the
# LED should be added.

#Libraries
import time
import board
import neopixel
from rpi_ws281x import PixelStrip, Color
#from picamera import PiCamera
from picamera2 import Picamera2, Preview
from time import sleep

import tkinter as tk  
from tkinter import *
from tkinter import filedialog

from PIL import Image, ImageTk



#camera = PiCamera()  #Initialize the Camera Object
# Set initial switch condition  to  off for all LEDs
led1Switch = False # On/off Status of LED 1
led2Switch = False # On/off Status of LED 2
led3Switch = False # On/off Status of LED 3
led4Switch = False # On/off Status of LED 4
ledaSwitch = False # On/off Status of all LEDs
imageWin   = None # Window to dsiplay images
currColor =   (255,255,255)  #default color is white
img_count = 0 # count of pictures taken
image_dir = "/home/pi/" #directory to store images
max_images = 5 # Number of images per session

# The Neopixel strip is connected to GPIO Pin D18

pixel_pin = board.D18

# The number of NeoPixels in the strip
num_pixels = 4
freq =  800000 # frequency in hertz
bright = 1.0  # default brightness value, 1 = full brightness

# Initialize the neopixel object with the following parameters:
# Pin : Digital 18, Neo Pixels count (3), brightness (1=max), auto-write = false(we want to control LED display through show instruction)
#  order = Green, Red, Blue White (GRBW), bpp = bytes per pixel (3)

#Variables for camera settings
#Shutter Speed
shut_speed = 1000
zoom_factor = 100

sav_as_format = 0 #default is PNG 0 - PNG, 1- YUV


pixels = neopixel.NeoPixel(pixel_pin, num_pixels, brightness=bright, auto_write=False, pixel_order=neopixel.GRBW, bpp=3)

# This function sets the pixel passes as a parameter to the global variable currColor

def rainon(pix):
global currColor
pixels[pix] =  currColor
pixels.show()

# This function shuts off the pixel passes as a parameter

def rainoff(pix):
pixels[pix] =  (0,0,0)
pixels.show()

# Function for the camera control. When the camera button is
# clicked, it sets the camera in preview mode, captures
# the picture, and displays the picture in the label control

def takePicture():
global img_count
global max_images
global image_dir
global sav_as_format
 
# we can take 5 pictures per session. If there  are not than 5 pics, we over-write
# starting with the first

img_count = img_count + 1
if img_count > max_images:
img_count = 1

canvas = tk.Canvas(win, width = 400, height = 300)
canvas.pack()

picam2 = Picamera2()  #Initialize the Camera Object

# preview_config = picam2.create_preview_configuration(main={"size": (800, 600)})
# picam2.configure(preview_config)   #Configure the picture frame

speeds = [10,100,10000,100000,1000000]
picam2.set_controls({"ExposureTime": speeds[img_count - 1], "AnalogueGain": 1.0})
picam2.start_preview(Preview.QTGL)
picam2.start()
time.sleep(2)
# picam2.set_controls({"AfMode":1,"AfTrigger":0})
picam2.zoom = (zoom_factor/100, zoom_factor/100, .5, .5)  

# save image as YUV or PNG
if sav_as_format == 0:
picam2.capture_file(image_dir + "image%s.png" % img_count, format = 'png')
else:
picam2.capture_file(image_dir + "image%s.data" % img_count, 'yuv')
picam2.stop_preview()
picam2.close()

# camera.start_preview()
# camera.capture('/home/pi/Desktop/image%s.jpg' % img_count)
# camera.stop_preview()
sleep(3) # too long?
img = Image.open(image_dir + 'image%s.png' % img_count)
img = img.resize((300,200), Image.ANTIALIAS)
new_img = ImageTk.PhotoImage(img)
#img = ImageTk.PhotoImage(Image.open('/home/pi/Desktop/image.jpg'))
#img = img.resize(50,50)
label1.configure(image=new_img)
label1.image = new_img
label1.pack()

# GUI Setup
win = tk.Tk()  
win.title("In Vivo Application") # Application Title  
win.geometry("500x500")

frame = Frame(win, width=200, height=200)
frame.pack()
frame.place(anchor='center', relx=.1, rely=.1)

# display the default picture
img = ImageTk.PhotoImage(Image.open(image_dir + 'mouse'))

label1 = tk.Label(image=img)
# Position image
label1.place(x=10, y=10)
label1.pack()

# functions for button clicks
 
#function for camera settings



def cam_settings():
format_option = IntVar()  
def save_text():
global shut_speed
global zoom_factor
global sav_as_format
shut_speed = speedtxt.get()
zoom_factor = zoomsli.get()
sav_as_format = format_option.get()
CamSetWin.destroy()

# shut_speed = int(shut_speed.get())

CamSetWin = Toplevel(win)
CamSetWin.geometry("300x520")
CamSetWin.title("Camera Settings")

#Variables to store settings

#Shutter Speed
def save_img_dir():
global image_dir

CamSetWin.directory = filedialog.askdirectory()
image_dir = CamSetWin.directory

speed = Label(CamSetWin, text="Shutter Speed")
speedtxt = Entry(CamSetWin)
speedtxt.insert(0, shut_speed)
speedtxt.place(x=500, y=10)
speedtxt.pack()
speed.place(x=20,y=10)
speed.pack()

submitss = Button(CamSetWin,text ="Save Camera Parameters",command=save_text)
# shut_speed = submitss

#Camera Zoom
zoomlab = Label(CamSetWin, text="Zoom")
zoomsli = Scale(CamSetWin, from_ = 0.25, to = 100, orient = VERTICAL)
zoomlab.pack()
zoomsli.pack()

#YUV or PNG
save_text = Label(CamSetWin, text = "Choose format to save: ")


R1 = Radiobutton(CamSetWin, text = "PNG", variable = format_option, value = 0)
R2 = Radiobutton(CamSetWin, text = "YUV", variable = format_option, value = 1)

save_text.pack()
R1.pack()
R2.pack()


#Folder Save

save_file = Button(CamSetWin, text = "Choose folder to save images", command = save_img_dir)
save_file.pack()


submitss.pack()

# Smile button click


def current_settings():
global sav_as_format
global image_dir
disp_format = ""
CurrSetWin = Toplevel(win)
CurrSetWin.geometry("300x520")
CurrSetWin.title("Display Settings")
speedisp = Label(CurrSetWin, text="Shutter Speed is: " + str(shut_speed))
speedisp.place(x=2000,y=60)
speedisp.pack()

zoomdisp = Label(CurrSetWin, text = "Camera Zoom is: " + str(zoom_factor))
zoomdisp.pack()
if sav_as_format == 0:
disp_format = "PNG"
else:
disp_format = "YUV"

curr_format = Label(CurrSetWin, text = "Current Save format is: " + disp_format)
curr_format.pack()

curr_dir = Label(CurrSetWin, text = "Current Save Directory is: " + image_dir)
curr_dir.pack()



def click():
#imageWin = Toplevel(win)
#mageWin.geometry("300x520")
#imageWin.title("Snap Picture")

#camera = picamera.Picamera()
#camera.start_preview()



takePicture()

# LED1 button click
# If on,  call function to switch off LED and change text
# If off, call function to switch  on LED and change text

def fled1():
global led1Switch
if led1Switch:
led1Switch = False
rainoff(0)
led1["text"] = "LED1 On"
else:
led1Switch =  True
rainon(0)
led1["text"] = "LED1 Off"
# LED2 button click
# If on,  call function to switch off LED and change text
# If off, call function to switch  on LED and change text

def fled2():
        global led2Switch
        if led2Switch:
                led2Switch = False
                rainoff(1)
                led2["text"] = "LED2 On"
        else:
                led2Switch =  True
                rainon(1)
                led2["text"] = "LED2 Off"
# LED3 button click
# If on,  call function to switch off LED and change text
# If off, call function to switch  on LED and change text

def fled3():
        global led3Switch
        if led3Switch:
                led3Switch = False
                rainoff(2)
                led3["text"] = "LED3 On"
        else:
                led3Switch =  True
                rainon(2)
                led3["text"] = "LED3 Off"
               
# LED4 button click
# If on,  call function to switch off LED and change text
# If off, call function to switch  on LED and change text

def fled4():
        global led4Switch
        if led4Switch:
                led4Switch = False
                rainoff(2)
                led4["text"] = "LED4 On"
        else:
                led4Switch =  True
                rainon(2)
                led4["text"] = "LED4 Off"

# All LEDs button click
# If on,  call function to switch off LED and change text
# If off, call function to switch  on LED and change text

def fleda():
global ledaSwitch
if ledaSwitch:
ledaSwitch = False
for i in range(num_pixels):
rainoff(i)
leda["text"] = "All LEDs On"
else:
ledaSwitch =  True
for i in range(num_pixels):
rainon(i)
leda["text"] = "All LEDs Off"

# Color Selection buttons
# When a button is clicked, the global variable is set to the
# corresponding color

def fblue():
global currColor
currColor =  (0,0,255)

def fred():
        global currColor
        currColor =  (0,255,0)

def fgreen():
        global currColor
        currColor =  (255,0,0)

def fwhite():
        global currColor
        currColor =  (255,255,255)
       
def update_preview():
picam2 = Picamera2()
picam2.capture_file(image_dir + "image%s.png" % img_count)
image = Image.open(image_dir + "image%s.png" % img_count)
image_resized = image.resize((400, 500), Image.ANITALIAS)
img = ImageTk.PhotoImage(image=image_resized)

label.configure(image=img)
label.img = img
window.after(10, update_preview)

def ShowImg():
global iamge_dir
global img_count
# Define in the images popup window
imageWin = Toplevel(win)
imageWin.geometry("700x750")
imageWin.title("Capture")

# set up space for preview
update_preview



# set up the space for the first image

img1 = Label(imageWin, text="image 1")
img1.place(x=10,y=10)
img1.pack()

# placeholder for the 2nd image

img2 = Label(imageWin, text="image 2")
img2.place(x=10,y=20)
img2.pack()

#placeholder for the 3rd image

img3 = Label(imageWin, text="image 3")
img3.place(x=10,y=30)
img3.pack()

# place holder for the 4th image

img4 = Label(imageWin, text="image 4")
img4.place(x=10,y=40)
img4.pack()

# placeholder for the 5th image
img5 = Label(imageWin, text="image 5")
img5.place(x=50,y=50)
img5.pack()

# if the first picture ws taken, show it. Otherwise, show the mouse
if img_count > 0:
imgP = Image.open(image_dir + 'image1.png' )
else:
imgP = Image.open(image_dir + 'no-image')

imgP = imgP.resize((100,100), Image.ANTIALIAS)
new_imgP = ImageTk.PhotoImage(imgP)
img1.configure(image=new_imgP)
img1.image = new_imgP
img1.pack()

# if the second picture ws taken, show it. Otherwise, show the mouse
if img_count > 1:
imgP = Image.open(image_dir + 'image2.png')
else:
imgP = Image.open(image_dir + 'no-image')

imgP = imgP.resize((100,100), Image.ANTIALIAS)
new_imgP = ImageTk.PhotoImage(imgP)
img2.configure(image=new_imgP)
img2.image = new_imgP
img2.pack()

# if the third picture ws taken, show it. Otherwise, show the mouse
if img_count > 2:
imgP = Image.open(image_dir + 'image3.png' )
else:
imgP = Image.open(image_dir + 'no-image')

imgP = imgP.resize((100,100), Image.ANTIALIAS)
new_imgP = ImageTk.PhotoImage(imgP)
img3.configure(image=new_imgP)
img3.image = new_imgP
img3.pack()

# if the fourth picture ws taken, show it. Otherwise, show the mouse
if img_count > 3:
imgP = Image.open(image_dir + 'image4.png')
else:
imgP = Image.open(image_dir + 'no-image')

imgP = imgP.resize((100,100), Image.ANTIALIAS)
new_imgP = ImageTk.PhotoImage(imgP)
img4.configure(image=new_imgP)
img4.image = new_imgP
img4.pack()

# if the fifth picture ws taken, show it. Otherwise, show the mouse
if img_count > 4:
imgP = Image.open(image_dir + 'image5.png' )
else:
imgP = Image.open(image_dir + 'no-image')

imgP = imgP.resize((100,100), Image.ANTIALIAS)
new_imgP = ImageTk.PhotoImage(imgP)
img5.configure(image=new_imgP)
img5.image = new_imgP
img5.pack()

currentset = tk.Button(win, text = "Current Settings",  command = current_settings)
action = tk.Button(win, text = "Smile", command = click)
led1   = tk.Button(win, text = "LED1 On", command = fled1)
led2   = tk.Button(win, text = "LED2 On", command = fled2)
led3   = tk.Button(win, text = "LED3 On", command = fled3)
led4   = tk.Button(win, text = "LED4 On", command = fled4)
leda   = tk.Button(win, text = "All LEDs On", command = fleda)
blue   = tk.Button(win, text = "Blue", command = fblue)
red    = tk.Button(win, text = "Red", command = fred)
green  = tk.Button(win, text = "Green", command = fgreen)
white   = tk.Button(win, text = "White", command = fwhite)
show = tk.Button(win, text= "Show Imges", command = ShowImg)
Camsettin  = tk.Button(win, text = "Camera Settings", command = cam_settings)

action.pack()
led1.pack()
led2.pack()
led3.pack()
led4.pack()
leda.pack()
currentset.pack()

# Position the color buttons at the bottom
 
blue.pack(side = LEFT)
red.pack(side = LEFT)
green.pack(side = LEFT)
white.pack(side = LEFT)
show.pack(side = RIGHT)
Camsettin.pack(side = RIGHT)
win.mainloop()

