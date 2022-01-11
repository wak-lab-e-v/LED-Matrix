import socket
import datetime
import random
from tkinter.constants import FALSE
import numpy as np
from pynput import keyboard
import socket
import urllib.request,io
import configparser
from pathlib import Path

import time


#read config for HOST
path = Path(__file__).parent.parent
# Returns a Pathlib object
print(path)
config = configparser.ConfigParser() 
config.read("{}\MatrixHost.ini".format(path))

HOST = config.get("Pixelserver","host")
print(HOST)

# monkeypatch: make requests only use ipv4
import requests.packages.urllib3.util.connection as urllib3_cn
def allowed_gai_family(): 
    return socket.AF_INET
urllib3_cn.allowed_gai_family = allowed_gai_family()

PORT = 1337

offset_x = 1
offset_y = 1

Display_Height = 33
Display_Width  = 60

BOX_SIZE = [3,13]
BLACK = [0,0,0] #defines the black color
COLOR = [255,255,255] #defines the color of the game elements
SOCKET_NUMBER = 1
output_array = []
socket_array = [socket.socket(socket.AF_INET, socket.SOCK_STREAM) for x in range(SOCKET_NUMBER)]

MAIN=False
remote_array = [[[0,0,0] for x in range(Display_Height)] for x in range(Display_Width)]

def sockets():
    """creates multiple socket connections"""
    global socket_array
    for i in range(SOCKET_NUMBER):
        socket_array[i].settimeout(0.5)
        socket_array[i].connect((HOST,PORT))

sockets()

def Putpixel(x,y,color):
    """sets the value for the desired pixel"""
    global output_array
    output_array.append([x,y,color])
    if(MAIN==False):
        remote_array[x][y] = color
        #print(remote_array)

def array_init():
    """resets the matrix with black"""  

    cmd=""  
    for x in range(Display_Width):
        for y in range(Display_Height):
            x1 = x + offset_x
            y1 = y + offset_y
            #print(x1, y1)
            if (x1 <= Display_Width) and (y1 <= Display_Height):
                #cmd = ("PX %d %d %d %d %d\n" % (x,y,r,g,b))
                cmd = cmd+ f"PX {x1} {y1} 0 0 0\n"
                #print(cmd)
    socket_array[0].send(cmd.encode())

def send():
    """sends the command via tcp to the Pixelserver"""
    global socket_array,output_array
    #reset the command
    cmd = ""
    i=0
    length = len(output_array)
    sock_error = False

    while (i<length):
        val = output_array[i]
        x1 = val[0] + offset_x
        y1 = val[1] + offset_y
        color = val[2]

        #print(val)
        cmd=cmd+f"PX {x1} {y1} {color[0]} {color[1]} {color[2]}\n"
        #print(cmd)
        i+=1
    try:
        print(cmd,len(cmd))
        socket_array[0].send(cmd.encode())
        time.sleep(1)
        #text = socket_array[0].recv(1024).decode()
        #print(text)
        #time.sleep(100000)
    except:
        #reconnect to the socket
        socket_array[0].close()
        socket_array[0] = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        socket_array[0].settimeout(0.5)
        try:
            socket_array[0].connect((HOST, PORT))
            socket_array[0].send(cmd.encode())
        except:
            print("socket error")
            sock_error = True
    
    if(not sock_error):
        output_array.clear()

def middle_line():
    """draws the middle line"""
    i = 0
    black = True
    start = int(Display_Width/2 -1)
    end = int(Display_Width/2 +1)
    for y in range(Display_Height):
        if(i % 2 == 0):
            i = 0
            black = not black
        
        if(black):
            for x in range(start,end):
                Putpixel(x,y,BLACK)
        else:
            for x in range(start,end):
                Putpixel(x,y,COLOR)
        
        i +=1


BALL_X = int(Display_Width/2)
BALL_Y = int(Display_Height/2)
BALLSIZE = 4
DIRECTION_X = 0
DIRECTION_Y = 0

SPEED = 0.000000001
START_TIME = datetime.datetime.now()

def ball_init():
    """initiates the ball movement"""
    global DIRECTION_X, DIRECTION_Y
    dir_x = random.randint(0,1)
    dir_y = random.randint(0,1)
    if(dir_x==0):
        DIRECTION_X = -1
    else:
        DIRECTION_X = 1
    
    if(dir_y==0):
        DIRECTION_Y = -1
    else:
        DIRECTION_Y = 1    

def ball_move():
    """moves the ball around"""
    global BALL_X,BALL_Y,DIRECTION_Y,DIRECTION_X,START_TIME
    now = datetime.datetime.now()
    start = START_TIME.second +SPEED
    #print(now.microsecond,start)
    if(now.second >= start): # only move every x microseconds
        START_TIME = now
        for y in range(BALL_Y-DIRECTION_Y,BALL_Y+BALLSIZE-DIRECTION_Y):
            for x in range(BALL_X-DIRECTION_X, BALL_X+BALLSIZE-DIRECTION_X):
                Putpixel(x,y,BLACK)
        for x in range(BALL_X,BALL_X+BALLSIZE):
            for y in range(BALL_Y,BALL_Y+BALLSIZE):
                if(x==BALL_X and y==BALL_Y
                or x==BALL_X+BALLSIZE-1 and y==BALL_Y+BALLSIZE-1
                or x==BALL_X and y==BALL_Y+BALLSIZE-1
                or x==BALL_X+BALLSIZE-1 and y==BALL_Y):
                    continue
                Putpixel(x,y,COLOR)
        
        if(BALL_Y+BALLSIZE >= Display_Height or BALL_Y <= 0): #change movement direction if border is hit
            DIRECTION_Y = DIRECTION_Y * (-1)
        if(BALL_X+BALLSIZE >= Display_Width or BALL_X <= 0): #change movement direction if border is hit
            DIRECTION_X = DIRECTION_X * (-1)
                
        BALL_X += DIRECTION_X
        BALL_Y += DIRECTION_Y

LEFT = 10
RIGHT = 10
#Create the left and right pixelbox
def pong():
    """main function for pong"""
    global output_array
    middle_line()
    ball_move()
    if(MAIN):
        send()
    else:
        output_array.clear()


def right(direction):
    """moves the right box"""
    global RIGHT
    if (direction==0):
        RIGHT -= 1
    elif(direction==1):
        RIGHT += 1

    #right
    if(RIGHT > Display_Height - BOX_SIZE[1]):
        RIGHT = Display_Height - BOX_SIZE[1]
    elif(RIGHT < 0):
        RIGHT = 0
    
    x_start = Display_Width-BOX_SIZE[0]
    x_end = Display_Width
    y_end = BOX_SIZE[1]+RIGHT
    #draw right box
    for x in range(x_start, x_end):
        for y in range(RIGHT, y_end):
            Putpixel(x,y,COLOR)
        for y in range(RIGHT):
            Putpixel(x,y,BLACK)
        for y in range(y_end, Display_Height):
            Putpixel(x,y,BLACK)

def left(direction):
    """moves the left box"""
    global LEFT
    if(direction==0):
        LEFT -= 1
    elif(direction==1):
        LEFT += 1
    
    #check if left is too high
    if(LEFT > Display_Height - BOX_SIZE[1]):
        LEFT = Display_Height - BOX_SIZE[1]
    elif(LEFT < 0):
        LEFT = 0
    
    y_end = BOX_SIZE[1]+LEFT
    
    #draw left box
    for x in range(BOX_SIZE[0]):
        for y in range(LEFT, y_end):
            Putpixel(x,y,COLOR)
        for y in range(LEFT):
            Putpixel(x,y,BLACK)
        for y in range(y_end, Display_Height):
            Putpixel(x,y,BLACK)
     
def on_press(key):
    """listens for key-presses"""
    try:
        #print('alphanumeric key {0} pressed'.format(
        #    key))
        
        if(str(key) == 'Key.up'):
            right(0)
        elif(str(key) == 'Key.down'):
            right(1)

        if(key.char == 'w'):
            left(0)
        elif(key.char == 's'):
            left(1)  

    except AttributeError:
        pass

#msg = "Message from Server {}".format(msgFromServer[0])

listener = keyboard.Listener(
    on_press=on_press)
listener.start()

def pong_init():
    ball_init()
    array_init()

if __name__ == "__main__":
    pong_init()
    MAIN = True
    while True:
        pong()
