import socket
import time
import numpy as np
from PIL import Image
from threading import Thread, Event


#serverAddressPort   = ("192.168.188.114", 21324)
#serverAddressPort   = ("192.168.188.115", 21324)
#serverAddressPort   = ("192.168.178.39", 21324)
#serverAddressPort   = ("192.168.178.39", 21324)
#serverAddressPort   = ("192.168.179.35", 21324)
#serverAddressPort   = ('127.0.0.1', 21324)

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

DefaultWidth  = 60
DefaultHeight = 33

class MxImage():
    def __init__(self, aImage):
        if isinstance(aImage, str):
            img = self.LoadImage(aImage)
        else:
            if isinstance(aImage, numpy.ndarray):
                img = Image.fromarray(aImage)
                img = img.convert('RGBA')
            else:
                img = aImage # PIL.Image.Image
        self.Sprite = np.array(img)
        self.Height = DefaultHeight
        self.Width  = DefaultWidth
        self.Background = np.ones(shape=(self.Width,self.Height,4))
        self.Foreground = np.zeros(shape=(self.Width,self.Height,4))       
        #arr1 = np.array(im)

    def LoadImage(self, imgfile):
        img = Image.open(imgfile)
        return img.convert('RGBA')

    def Position(x,y):
        dim = np.shape(self.Sprite)
        for i in range (0, dim[0]):
            for j in range(0,dim[1]):
                x1 = i + x
                y1 = j + y
                if  arr[j][i][3]  > 0 :
                    drawpixel(x1,y1, arr[j][i][0] , arr[j][i][1], arr[j][i][2])        
        


##        for j in range (0, imageObject.size[0]):
##            for i in range(0,imageObject.size[1]):
##                if (arr0[i][j][0] == arr1[i][j][0]) and (arr0[i][j][1] == arr1[i][j][1]) and (arr0[i][j][2] == arr1[i][j][2]):
##                    arr1[i][j][3] = 0
##        imo = Image.fromarray(arr1)
##
##
##        def pushpicture(x,y,imgfile):
##    img = Image.open(imgfile)    
##    img = img.convert('RGBA')
##    pushimage(x,y,img)
##    
##def pushimage(x,y,img):
##    maxsize = (width, height)
##    if (img.size[0] > width) or (img.size[1] > height):
##        img = img.resize(maxsize);
##    arr = np.array(img)
##    cmd = ""
##    for i in range (0, img.size[0]):
##        for j in range(0,img.size[1]):
##            x1 = i + x
##            y1 = j + y
##            if  arr[j][i][3]  > 0 :
##                drawpixel(x1,y1, arr[j][i][0] , arr[j][i][1], arr[j][i][2])
##

                

class UdpPixelMatrix():
    def __init__(self, UDPserver='127.0.0.1', Port = 21324, Mode = 5, Autosend = True):
        self.serverAddressPort = (UDPserver, Port)
        self.lastSend = int(round(time.time() * 1000))
        self.Height = DefaultHeight
        self.Width  = DefaultWidth
        self.OutputArray = np.zeros((self.Height*self.Width,3),dtype=np.uint8)
        self.Mode =  Mode;
        self.MaxLight = 0x3f
        self.GammaTable = np.array([((i / 255.0) ** 2.6) * self.MaxLight+0.5 # gamma 2.6
            for i in np.arange(0, 256)]).astype("uint8")
        self.UDPClientSocket = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM)
        if Autosend:
            self.stop = Event()
            send_thread = Thread(target=self.cyclic_send)
            send_thread.start()

    def PixelDecoder(self, x, y):
        if (y == 0):
            y = 1
        if (x == 0):
            x = 1
            
        Zeile  = y-1  # von oben nach unten wie auch in den Bildern
        if ((Zeile % 2) == 0):
            Spalte = x-1
        else:
            Spalte = (self.Width-1) - (x-1)
        return Zeile, Spalte

    def cyclic_send(self):
        while not self.stop.isSet():
            try:
                self.Send()
            except:
                self.stop.set()
                
    def Send(self):
        offset = 0
        while int(round(time.time() * 1000)) < self.lastSend + 140:
            time.sleep(0.04)
        lastSend = int(round(time.time() * 1000))
        while True:
            if self.Mode == 4:
                bytesToSend         = b'\x04\x02'
                UDP_Leds = 480
            else:
                bytesToSend         = b'\x05\x02'
                UDP_Leds = 700
                
            bytesToSend  += offset.to_bytes(2,'big')
            segment      = self.OutputArray[offset:offset+UDP_Leds]
            offset       += UDP_Leds
            
            ledCount = len(segment)
            if (ledCount == 0):
                break;

            for color in segment:
                if self.Mode == 4:
                    bytesToSend += color[0].tobytes() + color[1].tobytes() + color[2].tobytes()
                else:
                    bytesToSend += color[0].tobytes() + color[1].tobytes()
            self.UDPClientSocket.sendto(bytesToSend, self.serverAddressPort)

    def Color16(self,r,g,b):
        r1 = r if(r < 0x3f) else 0x3f
        g1 = g if(g < 0x3f) else 0x3f
        b1 = b if(b < 0x3f) else 0x3f

        code = ((r1 & 0x3e) <<10) | ((g1 & 0x3f)<<5) | ((b1 & 0x3e)>>1)
        return [ (code  >> 8) & 0xff, code & 0xff, 0]

    def drawpixel(x,y, aColor):
        self.Putpixel(x,y,aColor)
        
    def Setpixel(self,x,y,aColor):
        self.Putpixel(x,y,aColor)

    def Putpixel(self,x,y,aColor):
        if self.Mode == 4:
            color = [self.GammaTable[aColor[0]], self.GammaTable[aColor[1]], self.GammaTable[aColor[2]]]  ## RGB
        else:
            color = self.Color16(self.GammaTable[aColor[0]], self.GammaTable[aColor[1]], self.GammaTable[aColor[2]])  ## RGB
        Zeile, Spalte = self.PixelDecoder(x, y)

        self.OutputArray[Zeile * self.Width + Spalte] = color;

    def Black(self):
        for i in range (1, self.Width+1 ):
            for j in range(1,self.Height+1):
                #print(i,j)
                self.Putpixel(i,j,[0,0,0])
    def White(self):
        for i in range (1, self.Width+1 ):
            for j in range(1,self.Height+1):
                #print(i,j)
                self.Putpixel(i,j,[255,255,255])

class PixelMatrix():
    def __init__(self, Pixelserver='127.0.0.1', Port = 1337):
        self.serverAddressPort = (Pixelserver, Port)
        print('Connected to', Pixelserver, Port) 
        self.lastSend = int(round(time.time() * 1000))
        self.Height = DefaultHeight
        self.Width  = DefaultWidth

        self.ClientSocket = socket.socket(family=socket.AF_INET, type=socket.SOCK_STREAM)
        self.ClientSocket.settimeout(0.1)
        self.ClientSocket.connect(self.serverAddressPort) # TCP

    def drawpixel(x,y, aColor):
        self.Putpixel(x,y,aColor)
    def Setpixel(self,x,y,aColor):
        self.Putpixel(x,y,aColor)

    def Putpixel(self,x,y,aColor):
        if (x>0) and (y>0) and (x <= self.Width) and (y <= self.Height):
            cmd = "PX %d %d #%s%s%s\n" % (x,y,format(aColor[0], '02x') ,format(aColor[1], '02x') ,format(aColor[2], '02x'))
            #cmd=f"PX {x} {y} {aColor[0]} {aColor[1]} {aColor[2]}\n"
            #print(cmd)
            self.ClientSocket.send(cmd.encode())

    def Black(self):
        for i in range (1, self.Width+1 ):
            for j in range(1,self.Height+1):
                self.Putpixel(i,j,(0,0,0))
    def White(self):
        for i in range (1, self.Width+1 ):
            for j in range(1,self.Height+1):
                #print(i,j)
                self.Putpixel(i,j,[255,255,255])

if __name__ == "__main__":
    Matrix = UdpPixelMatrix()

    xImage = MxImage('pac.png')
    
    Matrix.White()
    #Matrix.Send()
    time.sleep(1)
    Matrix.Black()
    #Matrix.Send()

    import configparser
    config = configparser.ConfigParser() 
    config.read(r"..\..\..\MatrixHost.ini")
    HOST = config.get("Pixelserver","Host")
    UDP_HOST = config.get("WLED Server","Host")

    #Matrix = UdpPixelMatrix(UDP_HOST)
    Matrix = PixelMatrix(HOST)
    Matrix.White()
    #Matrix.Send()
    time.sleep(1)
    Matrix.Black()
    #Matrix.Send()
