from PIL import Image, ImageDraw, ImageSequence, ImageEnhance
import cv2 
import math
import socket
import time
import numpy as np
import os

Display_Height = 33
Display_Width  = 60

Mode =  5;


serverAddressPort   = ("10.10.22.57", 21324)


w,h = Display_Width, Display_Height
t = (w*h,3)
OutputArray = np.zeros(t,dtype=np.uint8)

GammaTable = np.array([((i / 255.0) ** 2.6) * 32.0+0.5 # gamma 2.6
    for i in np.arange(0, 256)]).astype("uint8")

#print(bytesToSend)

# Create a UDP socket at client side

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

def SendUDP(aMode, array):
    offset = 0
    while True:
        if Mode == 4:
            bytesToSend         = b'\x04\x02'
            UDP_Leds = 480
        else:
            bytesToSend         = b'\x05\x02'
            UDP_Leds = 700
            
        bytesToSend  += offset.to_bytes(2,'big')
        segment      = array[offset:offset+UDP_Leds]
        offset       += UDP_Leds
        
        ledCount = len(segment)
        if (ledCount == 0):
            break;

        for color in segment:
            #print(color)
            if Mode == 4:
                bytesToSend += color[0].tobytes() + color[1].tobytes() + color[2].tobytes()
            else:
                bytesToSend += color[0].tobytes() + color[1].tobytes()
        #print(len(bytesToSend))
        UDPClientSocket.sendto(bytesToSend, serverAddressPort)


def one_word(r,g,b):
    r1 = r if(r < 0x3f) else 0x3f
    g1 = g if(g < 0x3f) else 0x3f
    b1 = b if(b < 0x3f) else 0x3f

    code = ((r1 & 0x3e) <<10) | ((g1 & 0x3f)<<5) | ((b1 & 0x3e)>>1)
    return [ (code  >> 8) & 0xff, code & 0xff, 0]

def Putpixel(x,y,aColor):
    if Mode == 4:
        color = [GammaTable[aColor[0]], GammaTable[aColor[1]], GammaTable[aColor[2]]]  ## RGB
    else:
        color = one_word(GammaTable[aColor[0]], GammaTable[aColor[1]], GammaTable[aColor[2]])  ## RGB
    Zeile, Spalte = PixelDecoder(x, y)
    #print(Spalte,Zeile)
    OutputArray[Zeile * Display_Width + Spalte] = color;
    

def Black():
    for i in range (0, Display_Width ):
        for j in range(0,Display_Height):
            #print(i,j)
            Putpixel(i,j,[0,0,0])
    SendUDP(Mode, OutputArray)

def White():
    for i in range (0, Display_Width ):
        for j in range(0,Display_Height):
            #print(i,j)
            Putpixel(i,j,[150,150,150])
    SendUDP(Mode, OutputArray)
    
if __name__ == "__main__":
    UDPClientSocket = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM) #SOCK_DGRAM) #SOCK_STREAM)
    White()
    
