import math
import socket
import datetime
import random
import numpy as np
from pynput import keyboard

Display_Height = 33
Display_Width  = 60

Mode =  4

BOX_SIZE = [3,13]

#serverAddressPort   = ("192.168.188.114", 21324)
#serverAddressPort   = ("192.168.188.115", 21324)
serverAddressPort   = ("192.168.179.35", 21324)

##Value     Description     Max. LEDs
##1     WARLS   255
##2     DRGB    490
##3     DRGBW   367
##4     DNRGB   489/packet
##0     WLED Notifier   -
#https://github-wiki-see.page/m/Aircoookie/WLED/wiki/UDP-Realtime-Control
# DNRGB
# 2     Start index high byte
# 3     Start index low byte
# 4 + n*3   Red Value
# 5 + n*3   Green Value
# 6 + n*3   Blue Value

w,h = Display_Width, Display_Height
t = (w*h,3)
OutputArray = np.zeros(t,dtype=np.uint8)

GammaTable = np.array([((i / 255.0) ** 2.6) * 255.0+0.5 # gamma 2.6
    for i in np.arange(0, 256)]).astype("uint8")

    
##GammaTable = [  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,
##    0,  0,  0,  0,  0,  0,  0,  0,  1,  1,  1,  1,  1,  1,  1,  1,
##    1,  1,  1,  1,  2,  2,  2,  2,  2,  2,  2,  2,  3,  3,  3,  3,
##    3,  3,  4,  4,  4,  4,  5,  5,  5,  5,  5,  6,  6,  6,  6,  7,
##    7,  7,  8,  8,  8,  9,  9,  9, 10, 10, 10, 11, 11, 11, 12, 12,
##   13, 13, 13, 14, 14, 15, 15, 16, 16, 17, 17, 18, 18, 19, 19, 20,
##   20, 21, 21, 22, 22, 23, 24, 24, 25, 25, 26, 27, 27, 28, 29, 29,
##   30, 31, 31, 32, 33, 34, 34, 35, 36, 37, 38, 38, 39, 40, 41, 42,
##   42, 43, 44, 45, 46, 47, 48, 49, 50, 51, 52, 53, 54, 55, 56, 57,
##   58, 59, 60, 61, 62, 63, 64, 65, 66, 68, 69, 70, 71, 72, 73, 75,
##   76, 77, 78, 80, 81, 82, 84, 85, 86, 88, 89, 90, 92, 93, 94, 96,
##   97, 99,100,102,103,105,106,108,109,111,112,114,115,117,119,120,
##  122,124,125,127,129,130,132,134,136,137,139,141,143,145,146,148,
##  150,152,154,156,158,160,162,164,166,168,170,172,174,176,178,180,
##  182,184,186,188,191,193,195,197,199,202,204,206,209,211,213,215,
##  218,220,223,225,227,230,232,235,237,240,242,245,247,250,252,255]

#print(bytesToSend)

# Create a UDP socket at client side

def SendUDP(aMode, array):
    offset = 0
    while True:
        if Mode == 4:
            bytesToSend         = b'\x04\x02'
            UDP_Leds = 489
        else:
            bytesToSend         = b'\x05\x02'
            UDP_Leds = 734
            
        bytesToSend  += offset.to_bytes(2,'big')
        segment      = array[offset:offset+UDP_Leds]
        offset       += UDP_Leds
        
        ledCount = len(segment)
        if (ledCount == 0):
            break

        for color in segment:
            #print(color)
            if Mode == 4:
                bytesToSend += color[0].tobytes() + color[1].tobytes() + color[2].tobytes()
            else:
                bytesToSend += color[0].tobytes() + color[1].tobytes()
        #print(len(bytesToSend))
        UDPClientSocket.sendto(bytesToSend, serverAddressPort)


def one_word(r,g,b):
    r1 = r if(r < 0x1f) else 0x1f
    g1 = g if(g < 0x1f) else 0x1f
    b1 = b if(b < 0x1f) else 0x1f

    code = ((r1 & 0x1f) <<11) | ((g1 & 0x3f)<<5) | (b1 & 0x1f)
    return [ (code  >> 8) & 0xff, code & 0xff, 0]

def PixelDecoder(x, y):
    if Display_Width <= Display_Width:
        Zeile  = y  # von oben nach unten wie auch in den Bildern
        if ((Zeile % 2) == 0):
            Spalte = x
        else:
            Spalte = (Display_Width-1) - x
    else:
        Zeile  = y if (x < Display_Width) else y + Display_Height # von oben nach unten wie auch in den Bildern
        if ((Zeile % 2) != 0):
            Spalte = x % Display_Width
        else:
            Spalte = (Display_Width-1) - (x % Display_Width)
    return Zeile, Spalte

def Putpixel(x,y,aColor):
    if Mode == 4:
        color = [GammaTable[aColor[0]], GammaTable[aColor[1]], GammaTable[aColor[2]]]  ## RGB
    else:
        color = one_word(GammaTable[aColor[0]], GammaTable[aColor[1]], GammaTable[aColor[2]])  ## RGB
    Zeile, Spalte = PixelDecoder(x, y)
    #print(Spalte,Zeile)
    OutputArray[Zeile * Display_Width + Spalte] = color
    

def Black():
    for i in range (0, Display_Width ):
        for j in range(0,Display_Height):
            #print(i,j)
            Putpixel(i,j,[0,0,0])

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
    dir = random.randint(0,1)
    if(dir==0):
        DIRECTION_X = -1
        DIRECTION_Y = -1
    else:
        DIRECTION_X = 1
        DIRECTION_Y = 1     

def ball_move():
    global BALL_X,BALL_Y,DIRECTION_Y,DIRECTION_X,START_TIME
    now = datetime.datetime.now()
    if(now.microsecond > START_TIME.microsecond + SPEED):
        START_TIME = now
        for y in range(BALL_Y-DIRECTION_Y,BALL_Y-DIRECTION_Y+BALLSIZE):
            for x in range(BALL_X-DIRECTION_X, BALL_X-DIRECTION_X+BALLSIZE):
                Putpixel(x,y,BLACK)
        for x in range(BALL_X,BALL_X+BALLSIZE):
            for y in range(BALL_Y,BALL_Y+BALLSIZE):
                if(x==BALL_X and y==BALL_Y
                or x==BALL_X+BALLSIZE-DIRECTION_X and y==BALL_Y+BALLSIZE-DIRECTION_Y
                or x==BALL_X and y==BALL_Y+BALLSIZE-DIRECTION_Y
                or x==BALL_X+BALLSIZE-DIRECTION_X and y==BALL_Y):
                    continue
                Putpixel(x,y,COLOR)
        
        if(BALL_Y+BALLSIZE == Display_Height):
            DIRECTION_Y = DIRECTION_Y * (-1)
        if(BALL_X+BALLSIZE == Display_Width):
            DIRECTION_X = DIRECTION_X * (-1)
                
        BALL_X += DIRECTION_X
        BALL_Y += DIRECTION_Y
    

BLACK = [0,0,0] #defines the black color
COLOR = [255,255,255] #defines the color of the game elements

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
    ball_move()
    
    SendUDP(Mode, OutputArray)

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
            left(0)
        elif(key.char == 's'):
            left(1)  

    except AttributeError:
        pass

#msg = "Message from Server {}".format(msgFromServer[0])

listener = keyboard.Listener(
    on_press=on_press)
listener.start()

if __name__ == "__main__":
    UDPClientSocket = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM)
    Black()
    ball_init()
    while True:
        pong()
