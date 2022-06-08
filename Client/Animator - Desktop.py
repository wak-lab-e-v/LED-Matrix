from PIL import Image, ImageDraw, ImageSequence, ImageEnhance
import cv2 
import math
import socket
import time
import numpy as np
import os

Display_Height = 33
Display_Width  = 60

Mode =  5

gain = 2.5

#serverAddressPort   = ("192.168.188.114", 21324)
#serverAddressPort   = ("192.168.188.115", 21324)
#serverAddressPort   = ("192.168.178.39", 21324)
#serverAddressPort   = ("192.168.178.39", 21324)
#serverAddressPort   = ("192.168.179.35", 21324)
serverAddressPort   = ("10.10.22.57", 21324)
serverAddressPort   = ("192.168.1.226", 21324) # WAKLAB OPenWRT

#serverAddressPort   = ("127.0.0.1", 21324)


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
    
def Desktop():
    import pyautogui
    frame = pyautogui.screenshot()
    maxsize = (Display_Width, Display_Height)
    # Crop
    #frame = frame[30:250, 100:230]
    #frame = frame.crop((350, 300, 1550, 700))
    im = cv2.resize(np.array(frame),maxsize,interpolation=cv2.INTER_LANCZOS4  ) #INTER_AREA)


##    frm = np.array(frame)
##    x_step = frame.size[0] / Display_Width
##    y_step = frame.size[1] / Display_Height
##    
##    im = np.zeros(shape=(Display_Height, Display_Width,3))  
##    for i in range (0, frame.size[0]):
##        for j in range(0, frame.size[1]):
##            x = int(i/x_step)
##            y = int(j/y_step)
##            if np.sum(im[y,x]) < np.sum(frm[j,i]):
##                im[y,x] = frm[j,i]
            
            
            
    #sp = np.array_split(im, 10, axis=0)
    #print(sp, len(sp), len(sp[0]), sp[0][0].shape)
    
    #im = cv2.cvtColor(np.array(frame), cv2.COLOR_BGR2RGB)
    for i in range (0, im.shape[1]):
        for j in range(0,im.shape[0]):
            Putpixel(i,j,im[j,i])
    SendUDP(Mode, OutputArray)
    time.sleep(0.06)
    
def ShowPicture(filename):
    frame = Image.open(filename)
    enhancer = ImageEnhance.Brightness(frame)
    im_pil = enhancer.enhance(gain)
    im = im_pil.copy()
    im.thumbnail((Display_Width, Display_Height))
    im = im.convert('RGBA')
    arr = np.array(im)
    for i in range (0, im.size[0]):
        for j in range(0,im.size[1]):
            #print(i,j)
            Putpixel(i,j,arr[j,i])
    SendUDP(Mode, OutputArray)   
    time.sleep(1.5)

def AnimateGif(filename):
    img = Image.open(filename)
    for i in range(5):
        for i,frame in enumerate(ImageSequence.Iterator(img)):
            im = frame.copy()
            im.thumbnail((Display_Width, Display_Height))
            im = im.convert('RGBA')
            arr = np.array(im)
            for i in range (0, im.size[0]):
                for j in range(0,im.size[1]):
                    #print(i,j)
                    Putpixel(i,j,arr[j,i])
            SendUDP(Mode, OutputArray)
            time.sleep(frame.info['duration']/1000)

def AnimateMp4(filename):
     video = cv2.VideoCapture(filename)
     while True:
        ret,frame = video.read() 
        if ret: 
            maxsize = (Display_Width, Display_Height) 
            im = cv2.resize(frame,maxsize,interpolation=cv2.INTER_AREA)
            im = cv2.cvtColor(im, cv2.COLOR_BGR2RGB)
            #im    = imRes.convert('RGB')
            #arr = np.array(im)
            #print(im.shape)
            for i in range (0, im.shape[1]):
                for j in range(0,im.shape[0]):
                    #print(i,j)
                    Putpixel(i,j,im[j,i])
            SendUDP(Mode, OutputArray)
            time.sleep(0.025)
        else:
            break
            


    
# Send to server using created UDP socket
def Lauflicht():
    while True:
        for i in range(0,60):
            Adress              = i
            GRB                 = [0,50,0]
            bytesToSend         = b'\x04\x02'
            bytesToSend         = bytesToSend + Adress.to_bytes(2,'big')
            bytesToSend         = bytesToSend + bytes(GRB)
            UDPClientSocket.sendto(bytesToSend, serverAddressPort)
            time.sleep(0.04)
            GRB                 = [0,0,0]
            bytesToSend         = b'\x04\x02'
            bytesToSend         = bytesToSend + Adress.to_bytes(2,'big')
            bytesToSend         = bytesToSend + b'\x00\x00\x00'
            UDPClientSocket.sendto(bytesToSend, serverAddressPort)
            time.sleep(0.04)
            #print(bytesToSend)
        
 
def PlayDir(aPath):
    dirList = os.listdir(aPath)
    result = ""
    for Dir in dirList:  
        Datei = os.path.join(aPath, Dir)  #Dir ist wieder os.path.basename(Datei)
        if not (os.path.isdir(Datei)):
            Name = os.path.splitext(Dir)[0]
            Ext  = os.path.splitext(Dir)[1]
            print(Datei)
            if (Ext in ['.png', '.jpg', '.bmp']):
                ShowPicture(Datei)
            if (Ext in ['.avi', '.mkv', '.mp4']):
                AnimateMp4(Datei)
            if (Ext in ['.gif']):
                AnimateGif(Datei)
            Black()
                

def Webcam():
    # get the webcam:
    import cv2
    cap = cv2.VideoCapture(0)
    maxsize = (Display_Width, Display_Height)
    while(cap.isOpened()):
        try:
            ret, frame = cap.read()
            img = cv2.resize(frame,maxsize,interpolation=cv2.INTER_AREA)
            img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
            
            im_pil = Image.fromarray(img)
            # For reversing the operation:
            # im_np = np.asarray(im_pil)
            enhancer = ImageEnhance.Brightness(im_pil)
            im_pil = enhancer.enhance(gain)
            im = im_pil.copy()
            #im.thumbnail((Display_Width, Display_Height))
            im = im.convert('RGBA')
            
            arr = np.array(im)
            for i in range (0, im.size[0]):
                for j in range(0,im.size[1]):
                    #print(i,j)
                    Putpixel(i,j,arr[j,i])
            SendUDP(Mode, OutputArray)   
            
        except KeyboardInterrupt:
            print('Hello user you have pressed ctrl-c button.')
            break
    cap.release()
           
            
    

#msgFromServer = UDPClientSocket.recvfrom(bufferSize)

 

#msg = "Message from Server {}".format(msgFromServer[0])

if __name__ == "__main__":
    UDPClientSocket = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM) #SOCK_DGRAM) #SOCK_STREAM)
    Black()
	#Webcam()
    while True:
        #AnimateGif("Katze.gif")
        #AnimateMp4("2021-08-08 02-03-54.mkv")
        #ShowPicture("Katze.png")
        Desktop()
        #PlayDir('./')
