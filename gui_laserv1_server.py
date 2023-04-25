import PySimpleGUI as sg
import cv2
import numpy as np
#import arduino_laser
import time
import math
import socket # new library - frank 
import pickle # new library - frank
import struct # new library - frank

# this is new global valuable - frank
HOST=''   # frank
PORT=8485 # frank

s=socket.socket(socket.AF_INET,socket.SOCK_STREAM)# frank
print('Socket created')# frank

s.bind((HOST,PORT))# frank
print('Socket bind complete')# frank
s.listen(0)# frank
print('Socket now listening')# frank

# this is new global valuable - frank

# rover = arduino_laser.controller()
speed = 50

l_hue = 0
l_sat = 80
l_value=250

u_hue = 255
u_sat = 255
u_value=255


#green = [0, 255, 255]
pastLoc = []

def on_change_lh(val):
    global l_hue
    val = int(val)
    l_hue=val

def on_change_ls(val):
    global l_sat
    val = int(val)
    l_sat=val

def on_change_lv(val):
    global  l_value
    val = int(val)
    l_value=val    
    
def on_change_uh(val):
    global u_hue
    val = int(val)
    u_hue=val

def on_change_us(val):
    global u_sat
    val = int(val)
    u_sat=val

def on_change_uv(val):
    global  u_value
    val = int(val)
    u_value=val
    
def on_change_r(val):
    global green
    val = int(val)
    green[2]=val
    
def on_change_g(val):
    global green
    val = int(val)
    green[1]=val
    
def on_change_b(val):
    global green
    val = int(val)
    green[0]=val
    
#def fwd():
#    global window
#    global speed
#    rover.setspeed(speed)
#    rover.setaction(speed,1)
#    window['Dir'].update("Forward")
#def rvs():
#    global window
#    global speed
#    rover.setspeed(speed)
#    rover.setaction(speed,2)
#    window['Dir'].update("Reverse")

#def lft():
#    global window
#    global speed
#    rover.setspeed(speed + 50)
#    rover.setaction(speed + 50,3)
#    window['Dir'].update("Left")

#def rgt():
#    global window
#    global speed
#    rover.setspeed(speed + 50)
#    rover.setaction(speed + 50,4)
#    window['Dir'].update("Right")

#def stp():
#    global window
#    rover.setspeed(0)
#    rover.setaction(0,5)
    
#def startRover():
#    global window
#    if rover.start==False :
#        rover.startR()
#        window['Status'].update("ON")
        
        
#def stopRover():
#    global window
#    if rover.start==True :
#        rover.stopR()
#        window['Status'].update("OFF")

print("Success")

sliders_box = [
    [
        sg.Text('Low_Hue', justification='center', font = ("Arial", 15), size = (20, 1)),
        sg.Slider((0, 255), l_hue, 1, orientation='h', size=(30, 15), key='Low_Hue', enable_events = True)
    ],
    [
        sg.Text('Low_Saturation', justification='center', font = ("Arial", 15), size = (20, 1)),
        sg.Slider((0, 255),l_sat, 1, orientation='h', size=(30, 15), key='Low_Saturation', enable_events = True)
    ],
    [
        sg.Text('Low_Value', justification='center', font = ("Arial", 15), size = (20, 1)),
        sg.Slider((0, 255), l_value, 1, orientation='h', size=(30, 15), key='Low_Value', enable_events = True)
    ],
    
    [
        sg.Text('Upper_Hue', justification='center', font = ("Arial", 15), size = (20, 1)),
        sg.Slider((0, 255), u_hue, 1, orientation='h', size=(30, 15), key='Upper_Hue', enable_events = True)
    ],
    [
        sg.Text('Upper_Saturation', justification='center', font = ("Arial", 15), size = (20, 1)),
        sg.Slider((0, 255), u_sat, 1, orientation='h', size=(30, 15), key='Upper_Saturation', enable_events = True)
    ],
    [
        sg.Text('Upper_Value', justification='center', font = ("Arial", 15), size = (20, 1)),
        sg.Slider((0, 255), u_value, 1, orientation='h', size=(30, 15), key='Upper_Value', enable_events = True)
    ],
    #[
        #sg.Text('R', justification='center', font = ("Arial", 15), size = (20, 1), key = 'Rt', background_color = 'red'),
        #sg.Slider((0, 255), green[2], 1, orientation='h', size=(30, 15), key='R', enable_events = True)
    #],
    #[
        #sg.Text('G', justification='center', font = ("Arial", 15), size = (20, 1), background_color = 'green'),
        #sg.Slider((0, 255), green[1], 1, orientation='h', size=(30, 15), key='G', enable_events = True)
    #],
    #[
        #sg.Text('B', justification='center', font = ("Arial", 15), size = (20, 1), background_color = 'blue'),
        #sg.Slider((0, 255), green[0], 1, orientation='h', size=(30, 15), key='B', enable_events = True)
    #],
]

def main():
    conn,addr=s.accept()
    data = b""                                     # new line # frank
    payload_size = struct.calcsize(">L")           # new line # frank
    print("payload_size: {}".format(payload_size)) # new line # frank

    global window
    coords = [0,0]
    sg.theme('LightGreen')

    # define the window layout
    layout = [
      [sg.Text('Walk The RoverV1', size=(100, 1), justification='center')],
      [sg.Image(filename='', key='-IMAGE-'), sg.Image(filename='', key='-MASK-'), sg.Image(filename='', key='-RES-')],
      [sg.Text('X', justification='center'),sg.Text('', justification='center', key = '-X-'), sg.Text('Direction: ', justification='center'), sg.Text('', justification='center', key = 'Dir')],
      [sg.Text('Y', justification='center'),sg.Text('', justification='center', key = '-Y-'), sg.Text('Engine Status: ', justification='center'), sg.Text('OFF', key = 'Status')],
      [sg.Column(sliders_box)],
      [sg.Button('Start', size=(10, 1)), sg.Button('Stop', size=(10, 1))],
      #[sg.Text('Color', justification='center', key = 'COLOR', background_color = green)],
      [sg.Button('Exit', size=(10, 1))]
    ]

    # create the window and show it without the plot
    window = sg.Window('OpenCV Integration', layout, location=(0, 0))

#    cap = cv2.VideoCapture(0)

    while True:
        # get image from PI camera - frank
        while len(data) < payload_size:
            data += conn.recv(4096)
            if not data:
                cv2.destroyAllWindows()
                conn,addr=s.accept()
                continue
        # receive image row data form client socket
        packed_msg_size = data[:payload_size]
        data = data[payload_size:]
        msg_size = struct.unpack(">L", packed_msg_size)[0]
        #print (payload_size, packed_msg_size, msg_size)
        while len(data) < msg_size:
            data += conn.recv(4096)
        frame_data = data[:msg_size]
        data = data[msg_size:]
        # unpack image using pickle
        frame=pickle.loads(frame_data, fix_imports=True, encoding="bytes")
        frame = cv2.imdecode(frame, cv2.IMREAD_COLOR)
        
        # get image from PI camera - frank


        event, values = window.read(timeout=20)
#        if event == 'Exit' or event == sg.WIN_CLOSED:
#            rover.stopR()
#            break

        #ret, frame = cap.read()
        frame = cv2.resize(frame, (200, 200))
        
        hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
        
        lower1 = np.array([l_hue, l_sat, l_value])
        upper1 = np.array([u_hue, u_sat, u_value])
        
        lower1 = np.array([l_hue, l_sat, l_value])
        upper1 = np.array([u_hue, u_sat, u_value])
        
        lower_mask = cv2.inRange(hsv, lower1, upper1)
        
        result = cv2.bitwise_and(frame, frame, mask=lower_mask)
        
        #Get the coordnates for circle based on result window color selection
        #Y, X = np.where(np.all(result==green,axis=2))

        #use min max function to get x y value. laser_camera.py
        
        (minVal, maxVal, minLoc, maxLoc) = cv2.minMaxLoc(lower_mask)
        X = maxLoc[0]
        Y = maxLoc[1]
        
        Xstr = str(maxLoc[0])
        Ystr = str(maxLoc[1])
        
        if X > 0 and Y > 0:
            coords = [X,Y]
        else:
            coords = [0,0]

        cv2.circle(frame, maxLoc, 20, (255, 0, 0), 2, cv2.LINE_AA)
        window['-X-'].update(maxLoc[0])
        window['-Y-'].update(maxLoc[1])

        #
        
         #Get the list of past coordnates
        if len(pastLoc) < 20:
            if coords[0] > 0 and coords[1] > 0:
                pastLoc.append([coords[0], coords[1]])
        else:
            if coords[0] > 0 and coords[1] > 0:
                del pastLoc[0]
                pastLoc.append([coords[0], coords[1]])
        
        print(pastLoc, "\n")
        
        #control the rovers movement based on where the laser point is
#        if coords[0] > 50 and coords[0] < 150 and coords[1] < 50:
#            rvs()
#        elif coords[0] > 50 and coords[0] < 150 and coords[1] >= 50:
#            fwd()
#        elif coords[0] > 150 and coords[0] < 200:
#            lft()
#        elif coords[0] > 0 and coords[0] < 50:
#            rgt()
#        else:
#            stp()
        
        mask = cv2.resize(lower_mask, (200, 200))

        imgbytes = cv2.imencode('.png', frame)[1].tobytes()
        imgbytes2 = cv2.imencode('.png', mask)[1].tobytes()
        imgbytes3 = cv2.imencode('.png', result)[1].tobytes()
        window['-IMAGE-'].update(data=imgbytes)
        window['-MASK-'].update(data=imgbytes2)
        window['-RES-'].update(data=imgbytes3)
        
        
        if event == 'Low_Hue':
            on_change_lh(values['Low_Hue'])
        elif event == 'Low_Saturation':
            on_change_ls(values['Low_Saturation'])
        elif event == 'Low_Value':
            on_change_lv(values['Low_Value'])
        elif event == 'Upper_Hue':
            on_change_uh(values['Upper_Hue'])
        elif event == 'Upper_Saturation':
            on_change_us(values['Upper_Saturation'])
        elif event == 'Upper_Value':
            on_change_uv(values['Upper_Value'])
        elif event == 'Start':
             startRover()
        elif event == 'Stop':
             stopRover()
        
        #elif event == 'R':
            #on_change_r(values['R'])
            #window['COLOR'].update(background_color = 'red')
        #elif event == 'G':
            #on_change_g(values['G'])
        #elif event == 'B':
            #on_change_b(values['B'])
        
            
    window.close()


main()
