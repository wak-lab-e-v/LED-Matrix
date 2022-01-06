import socket
import datetime
import random
import numpy as np
from pynput import keyboard
import socket
import urllib.request,io
import configparser
from pathlib import Path

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

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.settimeout(None)
sock.connect((HOST, PORT))

Display_Height = 33
Display_Width  = 60

BOX_SIZE = [3,13]
BLACK = [None,None,None,True] #defines the black color
COLOR = [255,255,255,True] #defines the color of the game elements

output_array = []

def Putpixel(x,y,rgb):
    global output_array
    old = output_array[x][y]
    if(old[0]!=rgb[0]
       or old[1] != rgb[1]
       or old[2] != rgb[2]):
        output_array[x][y] = rgb
        print("changed!")

def array_init():
    global output_array
    output_array = [[[0,0,0,False] for x in range(Display_Height)] for x in range(Display_Width)]
    cmd = ""
    
    for x in range(Display_Width):
        for y in range(Display_Height):
            x1 = x + offset_x
            y1 = y + offset_y
            #print(x1, y1)
            if (x1 <= Display_Width) and (y1 <= Display_Height):
                #cmd = ("PX %d %d %d %d %d\n" % (x,y,r,g,b))
                cmd = cmd+ "PX {x_val} {y_val} #{r:02X}{g:02X}{b:02X}\n".format(x_val = x1,y_val = y1, r=0, g=0, b=0)
                #print(cmd)
    sock.send(cmd.encode())
    #print(output_array)

def send():
    cmd = ""
    i=1
    for x in range(Display_Width):
        for y in range(Display_Height):
            """if(i%30==0):
                i=0
                sock.send(cmd.encode())
                cmd = """""
            x1 = x + offset_x
            y1 = y + offset_y
            #print(x1, y1)
            rgb = output_array[x][y]
            #print(rgb)
            if(rgb[3] == True):
                if(rgb == BLACK):
                    cmd = cmd+ "PX {x_val} {y_val} #{r:02X}{g:02X}{b:02X}\n".format(x_val = x1,y_val = y1, r=0, g=0, b=0)
                    output_array[x][y] = [BLACK[0],BLACK[1],BLACK[2],False]
                elif (x1 <= Display_Width) and (y1 <= Display_Height):
                    #cmd = ("PX %d %d %d %d %d\n" % (x,y,r,g,b))
                    cmd = cmd+ "PX {x_val} {y_val} #{r:02X}{g:02X}{b:02X}\n".format(x_val = x1,y_val = y1, r=rgb[0], g=rgb[1], b=rgb[2])
                    output_array[x][y] = [COLOR[0],COLOR[1],COLOR[2],False]

    sock.send(cmd.encode())
    #Text=sock.recv(30).decode()
    #print(Text)

#msgFromServer = UDPClientSocket.recvfrom(bufferSize)

def middle_line():
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

SPEED = 1000
START_TIME = datetime.datetime.now()

def ball_init():
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
    global BALL_X,BALL_Y,DIRECTION_Y,DIRECTION_X,START_TIME
    now = datetime.datetime.now()
    if(now.microsecond > START_TIME.microsecond + SPEED):
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
        
        if(BALL_Y+BALLSIZE == Display_Height or BALL_Y == 0):
            DIRECTION_Y = DIRECTION_Y * (-1)
        if(BALL_X+BALLSIZE == Display_Width or BALL_X == 0):
            DIRECTION_X = DIRECTION_X * (-1)
                
        BALL_X += DIRECTION_X
        BALL_Y += DIRECTION_Y

LEFT = 10
RIGHT = 10
#Create the left and right pixelbox
def pong():
    global LEFT, RIGHT
    #left
    
    #check if left is too high
    if(LEFT > Display_Height - BOX_SIZE[1]):
        LEFT = Display_Height - BOX_SIZE[1]
    elif(LEFT < 0):
        LEFT = 0
    
    y_end = BOX_SIZE[1]+LEFT
    
    for x in range(BOX_SIZE[0]):
        for y in range(LEFT, y_end):
            Putpixel(x,y,COLOR)
        for y in range(LEFT):
            Putpixel(x,y,BLACK)
        for y in range(y_end, Display_Height):
            Putpixel(x,y,BLACK)
        
    
    #right
    if(RIGHT > Display_Height - BOX_SIZE[1]):
        RIGHT = Display_Height - BOX_SIZE[1]
    elif(RIGHT < 0):
        RIGHT = 0
    
    x_start = Display_Width-BOX_SIZE[0]
    x_end = Display_Width
    y_end = BOX_SIZE[1]+RIGHT
    for x in range(x_start, x_end):
        for y in range(RIGHT, y_end):
            Putpixel(x,y,COLOR)
        for y in range(RIGHT):
            Putpixel(x,y,BLACK)
        for y in range(y_end, Display_Height):
            Putpixel(x,y,BLACK)
 
    middle_line()
    #ball_move()
    
    send()

def right(direction):
    global RIGHT
    if (direction==0):
        RIGHT -= 1
    elif(direction==1):
        RIGHT += 1

def left(direction):
    global LEFT
    if(direction==0):
        LEFT -= 1
    elif(direction==1):
        LEFT += 1
     
def on_press(key):
    try:
        #print('alphanumeric key {0} pressed'.format(
        #    key))
        
        if(str(key) == 'Key.up'):
            right(0)
        elif(str(key) == 'Key.down'):
            right(1)

        if(key.char == 'w'):
            print("up")
            left(0)
        elif(key.char == 's'):
            print("down")
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
    while True:
        pong()
