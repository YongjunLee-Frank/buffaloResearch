import time
import requests
from PIL import Image, ImageTk, ImageFile
from io import BytesIO
from guizero import App, Picture, Box, Text, PushButton
import cv2

ImageFile.LOAD_TRUNCATED_IMAGES = True




# this button start to listen camera data from PI side
def get_video():
    video.value = "PiCamera.jpg"
    #while True:
    #    video = Picture(video_box, image = "PiCamera.jpg", width = 250, height = 250)


#DECLARE GLOBAL VARIABLES
count = 0
videoShow = True


#ENABLE BUTTONS ONCE START IS PRESSED
def start_buttons():
    #enable direction, and stop btn, disable start btn
    foward.enable()
    back.enable()
    left.enable()
    right.enable()
    stop_btn.enable()
    start.disable()

#DISABLE BUTTONS ONCE STOP IS PRESSED
def stop_buttons():
    #Disable all but start btn
    foward.disable()
    back.disable()
    left.disable()
    right.disable()
    gas.disable()
    break_.disable()
    stop_btn.disable()
    start.enable()

#DEFINE START, STOP, BREAK, and GAS
def start_r():
    welcome_message.value = "ON"
    start_buttons()

def gas_r():
    global count
    #Increase speed value
    count += 1
    #update speed display
    momentum.value = str(count)
    
    #Dont allow speed past 10
    if count >= 10:
        count = 10
        momentum.value = str(count)
    #Update speed values    
    rover.setspeed(count)
        
def break_r(): 
    global count
    #Decrease speed value
    count -= 1
    #update speed display
    momentum.value = str(count)
    
    #Dont allow speed below 0
    if count <= 0:
        count = 0
        momentum.value = str(count)
    #Update speed values    
    rover.setspeed(count)
    
def stop():
    global count
    welcome_message.value = "OFF"
    #set count to zero
    count = count - count
    #Update speed display
    momentum.value = str(count)
    #disable buttons
    stop_buttons()
    #Update speed values and stop engine
    rover.setspeed(count)
    rover.stopR()

#FUNCTIONS FOR CONTROL OF ROBOT DIRECTION
def foward_move():
    #Enable break and gas
    gas.enable()
    break_.enable()
    #Update gear display
    welcome_message.value = "FORWARD"
    #Set rover gear value
    rover.setaction(count,1) #error line

def back_move():
    #Enable break and gas
    gas.enable()
    break_.enable()
    #Update gear display
    welcome_message.value = "BACK"
    #Set rover gear value
    rover.setaction(count,2)    

    
def left_move():
    #Enable break and gas
    gas.enable()
    break_.enable()
    #Update gear display
    welcome_message.value = "LEFT"
    #Set rover gear value
    rover.setaction(count,3)
    
def right_move():
    #Enable break and gas
    gas.enable()
    break_.enable()
    #Update gear display
    welcome_message.value = "RIGHT"
    #Set rover gear value
    rover.setaction(count,4)

#TOGGLE VIDEO DISPLAY FUNCTION
def show_video():
    global videoShow
    if videoShow == False:
        #enable video
        video.visible = True
        #Update flag
        videoShow = True
    else:
        #disable video
        video.visible = False
        #Update flag
        videoShow = False
         
        
#DISPLAY THE GUI FORM FOR THE CONTROLLER
app = App(title = "Rover GUI", width = 925, height = 500, bg = "#ef9637")


#ADD GIU WIDGET CODE HERE
#DISPLAYS CURRENT GEAR OF ROVER
welcome_message = Text(app, text = "OFF", font = "Times New Roman", size = 35, color = "red")

#DISPLAYS SPEED OF ROVER
momentum = Text(app, text = str(count), font = "Times New Roman", size = 30)

#BOX FOR HOLDING ALL GUI WIDGETS
container = Box(app, layout = "grid")

#ALL INSIDE CONTAINER GRID

#BOX FOR HOLDING THE VIDEO
space_boxLeft       = Box(container, grid = [0,1,1,2], height = "fill", width = "25")
video_box           = Box(container, grid = [1,1],     height = 275,    width = 250)
video_btn_box       = Box(container, grid = [1,2])
video_get_btn_box   = Box(container, grid = [1,3])
space_boxMiddle     = Box(container, grid = [2,1],     height = "10",   width = "300")

#BOX HOLDING ALL THE BUTTONS
buttons_box    = Box(container, grid = [3,1], layout = "grid")
space_boxRight = Box(container, grid = [4,1], height = "fill", width = "25")

#OBJECTS IN BOXES
#DISPLAYS THE VIDEO
video = Picture(video_box, image = "PiCamera.jpg", width = 250, height = 250)



#DISPLAYS THE TOGGLE BUTTON FOR VIDEO
showVideoBtn = PushButton(video_btn_box,     command = show_video, text = "Show Video", width = 8, height = 1, align = "left")
getVideoBtn  = PushButton(video_get_btn_box, command = get_video,  text = "Get Video",  width = 8, height = 1, align = "left")

#DISPLAYS THE CONTROLLER

start    = PushButton(buttons_box, command = start_r, text = "start", grid = [0,0], width = 3, height = 3)
stop_btn = PushButton(buttons_box, command = stop,    text = "stop",  grid = [0,1], width = 3, height = 3, enabled = False)
gas      = PushButton(buttons_box, command = gas_r,   text = "gas",   grid = [1,1], width = 3, height = 3, enabled = False)
break_   = PushButton(buttons_box, command = break_r, text = "break", grid = [2,1], width = 3, height = 3, enabled = False)

#direction btns
foward = PushButton(buttons_box, command = foward_move, text = "^", grid = [1,2], width = 3, height = 3, enabled = False)
left   = PushButton(buttons_box, command = left_move,   text = "<", grid = [0,3], width = 3, height = 3, enabled = False)
back   = PushButton(buttons_box, command = back_move,   text = "v", grid = [1,3], width = 3, height = 3, enabled = False)
right  = PushButton(buttons_box, command = right_move,  text = ">", grid = [2,3], width = 3, height = 3, enabled = False)


#CHANGE VALUES OF CERITAN PROPERTIES OF OBJECTS
foward.bg = "white"
back.bg   = "white"
left.bg   = "white"
right.bg  = "white"
start.bg  = "white"
gas.bg    = "white"
break_.bg = "white"
stop_btn.bg = "white"
showVideoBtn.bg = "white"
stop_btn.text_color = "red"

#END OF CONTAINER

#Repeat app to get image data
app.repeat(10, get_video)

#DISPLAY GUI
app.display()



