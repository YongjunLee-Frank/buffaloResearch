import matplotlib.pyplot as plt

import PySimpleGUI as sg
import cv2
import numpy as np
#import arduino_laser # frank
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

#rover = arduino_laser.controller() # frank
speed = 50

l_hue = 0
l_sat = 0
l_value=250

u_hue = 255
u_sat = 255
u_value=255

k_val = 2


green = [0, 255, 255]
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
    
def on_change_k(val):
    global k_val
    val = int(val)
    k_val = val
    
#def fwd():# frank
#    global speed
#    rover.setspeed(speed)
#    rover.setaction(speed,1)
#def rvs():
#    global speed
#    rover.setspeed(speed)
#    rover.setaction(speed,2)
#def lft():
#    global speed
#    rover.setspeed(speed)
#   rover.setaction(speed,3)
#def rgt():
#    global speed
#    rover.setspeed(speed)
#    rover.setaction(speed,4)
#def stp():
#    rover.setspeed(0)
#    rover.setaction(0,5)# frank

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
    [
        sg.Text('K', justification='center', font = ("Arial", 15), size = (20, 1)),
        sg.Slider((1, 5), k_val, 1, orientation='h', size=(30, 15), key='K', enable_events = True)
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

    
    global k_val
    coords = [0,0]
    sg.theme('LightGreen')

    # define the window layout
    layout = [
      [sg.Text('Walk The RoverV1', size=(100, 1), justification='center')],
      [sg.Image(filename='', key='-IMAGE-'), sg.Image(filename='', key='-MASK-'), sg.Image(filename='', key='-RES-')],
      [sg.Text('X', justification='center'),sg.Text('', justification='center', key = '-X-')],
      [sg.Text('Y', justification='center'),sg.Text('', justification='center', key = '-Y-')],
      [sg.Column(sliders_box)],
      #[sg.Text('Color', justification='center', key = 'COLOR', background_color = green)],
      [sg.Button('Exit', size=(10, 1))]
    ]

    # create the window and show it without the plot
    window = sg.Window('OpenCV Integration', layout, location=(0, 0))

    #cap = cv2.VideoCapture(0) # frank

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

#        if rover.start==False : # frank
#            rover.startR()# frank
        
        event, values = window.read(timeout=20)
#        if event == 'Exit' or event == sg.WIN_CLOSED:# frank
#            rover.stopR()# frank
#            break# frank

        #ret, frame = cap.read() # remove : get frame from PI camera # frank
        frame = cv2.resize(frame, (200, 200))
        
        img = cv2.cvtColor(frame,cv2.COLOR_BGR2RGB)
        hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
        
        lower1 = np.array([l_hue, l_sat, l_value])
        upper1 = np.array([u_hue, u_sat, u_value])
        
        lower1 = np.array([l_hue, l_sat, l_value])
        upper1 = np.array([u_hue, u_sat, u_value])
        lower_mask = cv2.inRange(hsv, lower1, upper1)
        result = cv2.bitwise_and(frame, frame, mask=lower_mask)
        plt.imshow(img)
        
        twoDimage = img.reshape((-1,3))
        twoDimage = np.float32(twoDimage)
        
        criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 10, 1.0)
        attempts = 10
        
        ret,label,center=cv2.kmeans(twoDimage,k_val,None,criteria,attempts,cv2.KMEANS_PP_CENTERS)
        center = np.uint8(center)
        res = center[label.flatten()]
        result_image = res.reshape((img.shape))

        plt.axis('off')
        plt.imshow(result_image)
        
        
        
        
        #Get the coordnates for circle based on result window color selection
        #Y, X = np.where(np.all(result==ret,axis=2))
        
        X = center[0][0]
        Y = center[0][1] 
        
        if X > 0 and Y > 0:
            coords = [X,Y]
        else:
            coords = [0,0]
        print(center)

        cv2.circle(frame, (X,Y), 20, (255, 0, 0), 2, cv2.LINE_AA)
        window['-X-'].update(coords[0])
        window['-Y-'].update(coords[1])
        
        cv2.circle(result_image, (X,Y), 20, (255, 0, 0), 2, cv2.LINE_AA)
        window['-X-'].update(coords[0])
        window['-Y-'].update(coords[1])

        #
        
         #Get the list of past coordnates
        if len(pastLoc) < 20:
            if coords[0] > 0 and coords[1] > 0:
                pastLoc.append([coords[0], coords[1]])
        else:
            if coords[0] > 0 and coords[1] > 0:
                del pastLoc[0]
                pastLoc.append([coords[0], coords[1]])
        
        #print(pastLoc, "\n")
        
#        if coords[0] > 50 and coords[0] < 150 and coords[1] < 100:# frank
#            rvs()# frank
#        elif coords[0] > 50 and coords[0] < 150 and coords[1] >= 100:# frank
#            fwd()# frank
#        elif coords[0] > 150 and coords[0] < 200:# frank
#            lft()# frank
#        elif coords[0] > 0 and coords[0] < 50:# frank
#            rgt()# frank
#        else: # frank
#            stp() # frank
        
        mask = cv2.resize(lower_mask, (200, 200))

        imgbytes = cv2.imencode('.png', frame)[1].tobytes()
        imgbytes2 = cv2.imencode('.png', result_image)[1].tobytes()
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
        elif event == 'K':
            on_change_k(values['K'])
        elif event == 'R':
            on_change_r(values['R'])
            #window['COLOR'].update(background_color = 'red')
        elif event == 'G':
            on_change_g(values['G'])
        elif event == 'B':
            on_change_b(values['B'])
        
            
    window.close()


main()
