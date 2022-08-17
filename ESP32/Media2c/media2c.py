
from PIL import ImageDraw, ImageSequence, ImageEnhance
from PIL import Image as PilImage
import cv2
import numpy as np
from tkinter import *
from tkinter import filedialog
Display_Width  = 60
Display_Height = 33

gain = 2.5


w,h = Display_Width, Display_Height
t = (w*h,3)
OutputArray = np.zeros(t,dtype=np.uint8)

GammaTable = np.array([((i / 255.0) ** 2.6) * 32.0+0.5 # gamma 2.6
    for i in np.arange(0, 256)]).astype("uint8")

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
    color = [GammaTable[aColor[0]], GammaTable[aColor[1]], GammaTable[aColor[2]]]  ## RGB
    Zeile, Spalte = PixelDecoder(x, y)
    #print(Spalte,Zeile)
    OutputArray[Zeile * Display_Width + Spalte] = color;

    
def Image2C(filename):
    frame = PilImage.open(filename)
    enhancer = ImageEnhance.Brightness(frame)
    im_pil = enhancer.enhance(gain)
    #im.thumbnail((Display_Width, Display_Height))
    maxsize = (Display_Width, Display_Height)
    im = im_pil.convert('RGBA')
    im = cv2.resize(np.array(im),maxsize,interpolation=cv2.INTER_LINEAR)#INTER_AREA)

    for i in range (0, im.shape[1]):
        for j in range(0,im.shape[0]):
            Putpixel(i,j,im[j,i])
   
    offset = 0
    laenge = 0
    with open('output.h','w') as f:
        f.write('const unsigned char myGraphic[5940] PROGMEM = {\n')
        while 1:
            if offset+10 < len(OutputArray):
                array_alpha = bytearray(OutputArray[offset:offset+10])
            else:
                array_alpha =  bytearray(OutputArray[offset:])
            laenge += len(array_alpha)
            f.write(' ,'.join('0x{:02x}'.format(x) for x in array_alpha)+',\n')
            offset+=10
            if offset >=  len(OutputArray):
                f.write('['+str(laenge)+']')
                break
        f.write('};\n')

if __name__ == "__main__":
    fenster = Tk()
    fenster.filename = ""
    fenster.filename = filedialog.askopenfilename(initialdir = "./", title = "Picture", filetypes =(("all files","*"),("Bitmap files","*.bmp")))
    print('Input:  ',fenster.filename)
    vPath = fenster.filename
    fenster.destroy()
    Image2C(vPath)
