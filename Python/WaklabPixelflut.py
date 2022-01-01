import socket
import numpy as np
import PIL
from PIL import Image, ImageOps
import random
import math
import pytesseract
import urllib.request,io
import time
import configparser
 
# monkeypatch: make requests only use ipv4
import requests.packages.urllib3.util.connection as urllib3_cn
def allowed_gai_family(): return socket.AF_INET
urllib3_cn.allowed_gai_family = allowed_gai_family

from itertools import chain
#https://wiki.maglab.space/wiki/PixelCompetition
#https://www.youtube.com/user/jschlingensiepen/live
#https://wiki.maglab.space/wiki/PixelCompetition/Csharp

config = configparser.ConfigParser() 
config.read(r"..\..\MatrixHost.ini")

HOST = config['Pixelserver']['Host']

PORT = 1337
width = 60
height = 33

offset_x = 1
offset_y = 1

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
#sock.setsockopt(socket.IPPROTO_TCP, socket.TCP_NODELAY, 1)
sock.settimeout(0.1)
sock.connect((HOST, PORT))



def getPicture():
    cmd = "GM\n"
    sock.send(cmd.encode())
    time.sleep(0.5)
    Text=sock.recv(3*2*width*height).decode()
    print(Text)

def drawpixel(x,y, r, g, b):
    x1 = x + offset_x
    y1 = y + offset_y
    #print(x1, y1)
    if (x1 <= width) and (y1 <= height):
        #cmd = ("PX %d %d %d %d %d\n" % (x,y,r,g,b))
        cmd = "PX %d %d #%s%s%s\n" % (x1,y1,format(r, '02x') ,format(g, '02x') ,format(b, '02x'))
        #print(cmd)
        sock.send(cmd.encode())
        #Text=sock.recv(300).decode()
    #print(Text)
    
    #while Text:=sock.recv(1) != '\n':
    #    pass
     # Sinnlose antwort
    
def line(x1,y1, x2, y2):
    deltax = abs(x2-x1)
    deltay = abs(y2-y1)
    if deltay > deltax :
        delta = deltay
    else:
        delta = deltax
    for i in range(0, delta):
        x = x1+i*(x2-x1)/delta 
        y = y1+i*(y2-y1)/delta
        drawpixel(x,y, 0, 0, 255)
        
        
def linepic(x1,y1, x2, y2,pic):
    deltax = abs(x2-x1)
    deltay = abs(y2-y1)
    if deltay > deltax :
        delta = deltay 
    else:
        delta = deltax
    delta = int (delta /10)    
    for i in range(0, delta):
        x = x1+i*(x2-x1)/delta 
        y = y1+i*(y2-y1)/delta
        pushpicture(x,y,pic)        

def square(x1,y1, x2, y2):
    line(x1,y1,x1,y2)
    line(x1,y2,x2,y2)
    line(x2,y2,x2,y1)
    line(x2,y1,x1,y1)

def pushpicture(x,y,imgfile):
    img = Image.open(imgfile)    
    img = img.convert('RGBA')
    pushimage(x,y,img)
    
def pushimage(x,y,img):
    maxsize = (width, height)
    img = img.resize(maxsize);
    arr = np.array(img)
    cmd = ""
    for i in range (0, img.size[0]):
        for j in range(0,img.size[1]):
            x1 = i + x
            y1 = j + y
            if  arr[j][i][3]  > 0 :
                drawpixel(x1,y1, arr[j][i][0] , arr[j][i][1], arr[j][i][2])

def pushpicturerandom(x,y,imgfile):
    img = Image.open(imgfile)    
    img = img.convert('RGBA')
    pushimage(x,y,img)
    
def pushimagerandom(x,y,img):   
    maxsize = (width, height)
    img = img.resize(maxsize);
    arr = np.array(img)
    checkArr = np.zeros((img.size[0],img.size[1]))
    cmd = ""
    countdown = img.size[0]*img.size[1]
    n = 0
    while True:
        n = n + 1
        i1 = int(random.random()*img.size[0])
        j1 = int(random.random()*img.size[1])
        x1 = i1 + x
        y1 = j1 + y
        r = arr[j1][i1][0]
        g = arr[j1][i1][1]
        b = arr[j1][i1][2]
        if (checkArr[i1][j1] == 0):
            if (arr[j1][i1][3] > 0)  and ((r>0) or (b>0) or (g>0)):
                drawpixel(x1,y1, r,g, b)
            countdown = countdown - 1;
            if countdown == 0:
                break
        checkArr[i1][j1] = 1;  
#        

                
def pushgif(x,y,giffile):
    imageObject = Image.open(giffile)
    print(imageObject.is_animated)
    print(imageObject.n_frames)
    imageObject.seek(0)
    #im = copy.copy(imageObject)
    #im = im.convert('RGBA')
    #arr0 = np.array(im)
    arr0 = np.ones(shape=(imageObject.size[1],imageObject.size[0],4))
    #for j in range (0, imageObject.size[0]):
    #    for i in range(0,imageObject.size[1]):
    #        arr0[i][j][0] = 1
    #        arr0[i][j][1] = 1
    #        arr0[i][j][1] = 1
    for frame in range(0,imageObject.n_frames):
        imageObject.seek(frame)
        im = copy.copy(imageObject)
        im = im.convert('RGBA')
        arr1 = np.array(im)
        for j in range (0, imageObject.size[0]):
            for i in range(0,imageObject.size[1]):
                if (arr0[i][j][0] == arr1[i][j][0]) and (arr0[i][j][1] == arr1[i][j][1]) and (arr0[i][j][2] == arr1[i][j][2]):
                    arr1[i][j][3] = 0
        imo = Image.fromarray(arr1)    
        pushimage(x,y,imo)
        arr0 = np.array(im)
                
def pushpicturesnake(x,y,imgfile):
    img = Image.open(imgfile)    
    img = img.convert('RGBA')
    arr = np.array(img)
    cmd = ("ST %d %d\n" % (x,y))
    print(cmd)
    sock.send(cmd.encode())
    cmd = ""
    i = int(img.size[0]/2)
    j = int(img.size[1]/2)
    
        
def zufall(x,y,n):
    x1 = 0
    y1 = 0
    for i in range(0,n):
        x2=int(random.random()*x)
        y2=int(random.random()*y)
        line(x1,y1, x2, y2)
        x1 = x2;
        y1 = y2;
        
def zufall2(x,y,n):
    x1 = 0
    y1 = 0
    for i in range(0,n):
        x2=int(random.random()*x)
        y2=int(random.random()*y)
        linepic(x1+offset_x,y1+offset_y, x2+offset_x, y2+offset_y,'w2.png')  
        x1 = x2;
        y1 = y2;        

def CLR():
    for i in range(33):
        for j in range(60):
            #if i % 2 != 0:
            drawpixel(j,i, 0, 50, 00)
    


if __name__ == '__main__':
    delay = 0.03
    #drawpixel(1,33, 100, 100, 0)
    #getPicture()
    #CLR()
    
    #while True:
    #    for i in range(20,100,4):
    #        drawpixel(60,1, i, 0, 0)
    #        time.sleep(delay)
    #    for i in reversed(range(20,100,4)):
    #        drawpixel(60,1, i, 0, 0)
    #        time.sleep(delay)
    #    for i in range(20,100,4):
    #        drawpixel(60,1, 0, i, 0)
    #        time.sleep(delay)
    #    for i in reversed(range(20,100,4)):
    #        drawpixel(60,1, 0, i, 0)
    #        time.sleep(delay)
    #    for i in range(20,100,4):
    #        drawpixel(60,1, 0, 0, i)
    #        time.sleep(delay)
    #    for i in reversed(range(20,100,4)):
    #        drawpixel(60,1, 0, 0, i)
    #        time.sleep(delay)
            

        
    #for i in range(0,10):
    #    #sock.setblocking(0)
    #    welkome=sock.recv(1024)
    #    print(welkome[-6:-2])
    #    if welkome[-6:-2] == b'1080':
    #         breakp

    pushpicturerandom(0, 0, 'w2.png')

    
