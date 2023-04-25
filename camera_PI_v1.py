import cv2
import io
import socket
import struct
import time
import pickle
import numpy as np


client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# client_socket.connect(('0.tcp.ngrok.io', 19194))
client_socket.connect(('10.36.162.52', 8485))

img_counter = 0
cam = cv2.VideoCapture(0)
cam.set(cv2.CAP_PROP_FRAME_WIDTH,320)
cam.set(cv2.CAP_PROP_FRAME_HEIGHT,240)

#encode to jpeg format
#encode param image quality 0 to 100. default:95
#if you want to shrink data size, choose low image quality.
encode_param=[int(cv2.IMWRITE_JPEG_QUALITY),90]

while True:
    ret, frame = cam.read()
    #
    #frame = imutils.resize(frame, width=320)
    #
    frame = cv2.flip(frame,180)
    result, image = cv2.imencode('.jpg', frame, encode_param)
    data = pickle.dumps(image, 0)
    size = len(data)

    if img_counter%2==0:
        client_socket.sendall(struct.pack(">L", size) + data) # > big-endian L long unsigned
        #cv2.imshow('client',frame)
        
    img_counter += 1

    # press q to quit
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
    

cam.release()
