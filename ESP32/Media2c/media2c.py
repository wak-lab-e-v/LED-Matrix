
from PIL import ImageDraw, ImageSequence, ImageEnhance
from PIL import Image as PilImage
import cv2
import numpy as np
from tkinter import *
from tkinter import filedialog
import os
Display_Width  = 56
Display_Height = 32

gain = 0.75
STARTFRAME = 4
MAXFRAME = 168

w,h = Display_Width, Display_Height
t = (w*h,3)
OutputArray = np.zeros(t,dtype=np.uint8)

GammaTable = np.array([((i / 255.0) ** 2.6) * 32.0+0.5 # gamma 2.6
    for i in np.arange(0, 256)]).astype("uint8")



def PixelDecoderSnake(x, y):
    Zeile  = y  # von oben nach unten wie auch in den Bildern
    if ((Zeile % 2) == 0):
        Spalte = x
    else:
        Spalte = (Display_Width-1) - x
    return Zeile * Display_Width + Spalte

def PixelDecoderChaos(x, y):
    segment = int(x / 8)
    if y % 2 == 0:
        x2 = x
    else:
        x2 = 7-x
    return 255+(segment*256)-(x2%8)-(y*8)  

def Putpixel(x,y,aColor):
    color = [GammaTable[aColor[0]], GammaTable[aColor[1]], GammaTable[aColor[2]]]  ## RGB
    offset = PixelDecoder(x, y)
    #print(Spalte,Zeile)
    OutputArray[offset] = color;

def NpArray2h(aArray):
    offset = 0
    laenge = 0
    print()
    with open('default.h','w') as f:
        f.write('const unsigned char myGraphic[%i] PROGMEM = {\n' % (len(aArray)*3))
        while 1:
            if offset+10 < len(aArray):
                array_alpha = bytearray(aArray[offset:offset+10])
                f.write(' ,'.join('0x{:02x}'.format(x) for x in array_alpha)+',\n')
            else:
                array_alpha =  bytearray(aArray[offset:])
                f.write(' ,'.join('0x{:02x}'.format(x) for x in array_alpha))
            
            laenge += len(array_alpha)
            offset+=10
            if offset >=  len(aArray):
                break
        f.write('};\n')

def NumpyArrayOut(im):
    for i in range (0, im.shape[1]):
        for j in range(0,im.shape[0]):
            Putpixel(i,j,im[j,i])
    
    return OutputArray

def ExportIMG(Image, index):
    OUT = cv2.cvtColor(Image, cv2.COLOR_BGR2RGB)
    cv2.imwrite('./split/%d.png'%index,OUT)

def Image2C(filename):
    frame = PilImage.open(filename)
    enhancer = ImageEnhance.Brightness(frame)
    im_pil = enhancer.enhance(gain)
    #im.thumbnail((Display_Width, Display_Height))
    maxsize = (Display_Width, Display_Height)
    im = im_pil.convert('RGBA')
    im = cv2.resize(np.array(im),maxsize,interpolation=cv2.INTER_LINEAR)#INTER_AREA)

    NumpyArrayOut(im)

    #array1 = np.vstack([OutputArray, OutputArray])
    NpArray2h(OutputArray)
    print(OutputArray)


    

def Gif2C(filename):
    size = 0
    img = PilImage.open(filename)
    for i,frame in enumerate(ImageSequence.Iterator(img)):
        if (i+1)>= STARTFRAME:
            frm = frame.convert('RGBA') 
            enhancer = ImageEnhance.Brightness(frm)
            im_pil = enhancer.enhance(gain)
            im = im_pil.copy()
            im.thumbnail((Display_Width, Display_Height))
            im = im.convert('RGBA')
            arr = np.array(im)
            if size == 0:
                array1 = np.copy(NumpyArrayOut(arr))
            else:
                array1 = np.vstack([array1,NumpyArrayOut(arr)])
            size += 1
            if size >= MAXFRAME:
                    break
    NpArray2h(array1)
   
def Mp42C(filename):
    size = 0
    i = 0
    video = cv2.VideoCapture(filename)
    while True:
        ret,frame = video.read()
        if ret:
            i+=1
            if i>= STARTFRAME:
                maxsize = (Display_Width, Display_Height) 
                im = cv2.resize(frame,maxsize,interpolation=cv2.INTER_AREA)
                im = cv2.cvtColor(im, cv2.COLOR_BGR2RGB)
                frame = PilImage.fromarray(im)
                enhancer = ImageEnhance.Brightness(frame)
                im_pil = enhancer.enhance(gain)
                im = im_pil.copy()
                im = im.convert('RGBA')
                arr = np.array(im)
                if size == 0:
                    array1 = np.copy(NumpyArrayOut(arr))
                else:
                    array1 = np.vstack([array1,NumpyArrayOut(arr)])
                size += 1
                if size >= MAXFRAME:
                    break
                
        else:
            break
    NpArray2h(array1)


    

if __name__ == "__main__":
    if Display_Width == 56:
        PixelDecoder = PixelDecoderChaos
    else:
        PixelDecoder = PixelDecoderSnake
    
    fenster = Tk()
    fenster.filename = ""
    fenster.filename = filedialog.askopenfilename(initialdir = "./", title = "Picture", filetypes =(("all files","*"),("Bitmap files","*.bmp")))
    print('Input:  ',fenster.filename)
    vPath = fenster.filename
    fenster.destroy()

    Name = os.path.splitext(vPath)[0]
    Ext  = os.path.splitext(vPath)[1]
    Datei = vPath
    print(Ext)
    print(Datei)
    if (Ext in ['.png', '.jpg', '.bmp']) and not os.path.split(Datei)[1].startswith('.'):
        Image2C(Datei)
    if (Ext in ['.avi', '.mkv', '.mp4']):
        Mp42C(Datei)
    if (Ext in ['.gif']):
        Gif2C(Datei)
    #if (Ext in ['.gif']):
    #    AnimateGif(Datei)



