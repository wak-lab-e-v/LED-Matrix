import socket
import time
import numpy as np
from PIL import Image, ImageSequence
from threading import Thread, Event
from functools import wraps, lru_cache

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

                
class UdpPixelMatrix():
    def __init__(self, UDPserver='127.0.0.1', Port = 21324, Mode = 5, Autosend = True, Dim = (DefaultWidth, DefaultWidth)):
        self.serverAddressPort = (UDPserver, Port)
        self.lastSend = int(round(time.time() * 1000))
        self.Height = Dim[1]
        self.Width  = Dim[0]
        if Dim[0] == 56:
            self.PixelDecoder = self.PixelDecoderChaos
        else:
            self.PixelDecoder = self.PixelDecoderSnake
            
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
            
    @lru_cache(maxsize=None)
    def PixelDecoderSnake(self, x, y):
        if (y == 0):
            y = 1
        if (x == 0):
            x = 1
            
        Zeile  = y-1  # von oben nach unten wie auch in den Bildern
        if ((Zeile % 2) == 0):
            Spalte = x-1
        else:
            Spalte = (self.Width-1) - (x-1)
        return Zeile * self.Width + Spalte
    
    @lru_cache(maxsize=None)
    def PixelDecoderChaos(self, x, y):
        if (y == 0):
            y = 1
        if (x == 0):
            x = 1
        x = x-1
        y = y-1
        segment = int(x / 8)
        if y % 2 == 0:
            x2 = x
        else:
            x2 = 7-x
        return 255+(segment*256)-(x2%8)-(y*8)  

    def cyclic_send(self):
        while not self.stop.isSet():
            try:
                self.Send()
            except:
                self.stop.set()
                
    def Send(self):
        offset = 0
        delay = time.time() - self.lastSend
        if (delay < 0.140) and (delay > 0):
            while (time.time() - self.lastSend) < 0.140:
                time.sleep(0.04)
        delay = time.time() - self.lastSend
        self.lastSend = time.time()
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
            
    @lru_cache(maxsize=None)
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
        offset = self.PixelDecoder(x, y)

        self.OutputArray[offset] = color;

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
    def NdArray(self, aArray : np.ndarray):
        for i in range (1, self.Width+1 ):
            for j in range(1,self.Height+1):
                #print(i,j)
                self.Putpixel(i,j,aArray[i-1][j-1])
                
    def Picture(self, aFilename, x=1,y=1):
        frame = Image.open(aFilename)
        imagesize = frame.size
        size = (self.Width - x, self.Height - y)
        size = (min(size[0],imagesize[0]), min(size[1],imagesize[1]))
        im = frame.copy()
        im.thumbnail(size)
        im = im.convert('RGBA')
        arr = np.array(im)
        for i in range (0, im.size[0]):
            for j in range(0,im.size[1]):
                self.Putpixel(x+i,y+j,arr[j,i])

    def AnimateGif(self, filename, x=1,y=1):
        img = Image.open(filename)
        for i,frame in enumerate(ImageSequence.Iterator(img)):
            imagesize = frame.size
            size = (self.Width - x, self.Height - y)
            size = (min(size[0],imagesize[0]), min(size[1],imagesize[1]))
            im = frame.copy()
            im.thumbnail(size)
            im = im.convert('RGBA')
            arr = np.array(im)
            for i in range (0, im.size[0]):
                for j in range(0,im.size[1]):
                    self.Putpixel(x+i,y+j,arr[j,i])
            time.sleep(frame.info['duration']/1000)
 

class PixelMatrix():
    def __init__(self, Pixelserver='127.0.0.1', Port = 1337, Dim = (DefaultWidth, DefaultWidth)):
        self.serverAddressPort = (Pixelserver, Port)
        print('Connected to', Pixelserver, Port) 
        self.lastSend = int(round(time.time() * 1000))
        self.Height = Dim[1]
        self.Width  = Dim[0]

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
            #cmd = "PX 20 20 #FFFFFF\n"
            #cmd = 'HELP\n'
            self.ClientSocket.send(cmd.encode())
            self.ClientSocket.recv
            #print(self.ClientSocket.recv(180).decode())

    def Getpixel(self,x,y):
        if (x>0) and (y>0) and (x <= self.Width) and (y <= self.Height):
            cmd = "GP %d %d\n" % (x,y)
            self.ClientSocket.recv
            self.ClientSocket.send(cmd.encode())
            answer = self.ClientSocket.recv(6).decode().split()
            print(answer)
            if (len(answer) >= 6):
                #color = bytes.fromhex(answer[3][1:])
                return tuple(int(answer[3]),int(answer[4]),int(answer[5]))
            return None
        
    def Black(self):
        for i in range (1, self.Width+1 ):
            for j in range(1,self.Height+1):
                self.Putpixel(i,j,(0,0,0))
    def White(self):
        for i in range (1, self.Width+1 ):
            for j in range(1,self.Height+1):
                #print(i,j)
                self.Putpixel(i,j,[255,255,255])
    
    def NdArray(self, aArray : np.ndarray):
        for i in range (1, self.Width+1 ):
            for j in range(1,self.Height+1):
                #print(i,j)
                self.Putpixel(i,j,aArray[i-1][j-1])
                
    def Picture(self, aFilename, x=1,y=1):
        frame = Image.open(aFilename)
        imagesize = frame.size
        size = (self.Width - x, self.Height - y)
        size = (min(size[0],imagesize[0]), min(size[1],imagesize[1]))
        im = frame.copy()
        im.thumbnail(size)
        im = im.convert('RGBA')
        arr = np.array(im)
        for i in range (0, im.size[0]):
            for j in range(0,im.size[1]):
                self.Putpixel(x+i,y+j,arr[j,i])
                

    def AnimateGif(self, filename, x=1,y=1):
        img = Image.open(filename)
        for i,frame in enumerate(ImageSequence.Iterator(img)):
            imagesize = frame.size
            size = (self.Width - x, self.Height - y)
            size = (min(size[0],imagesize[0]), min(size[1],imagesize[1]))
            im = frame.copy()
            im.thumbnail(size)
            im = im.convert('RGBA')
            arr = np.array(im)
            for i in range (0, im.size[0]):
                for j in range(0,im.size[1]):
                    self.Putpixel(x+i,y+j,arr[j,i])
            time.sleep(frame.info['duration']/1000)

if __name__ == "__main__":
    pass
    #Matrix = UdpPixelMatrix()
    #xImage = MxImage('Fox-Face2.png')
    #Matrix.White()
##    #Matrix.Send()
##    time.sleep(1)
##    Matrix.Black()
##    #Matrix.Send()
##
##    import configparser
##    config = configparser.ConfigParser() 
##    config.read(r"..\..\..\MatrixHost.ini")
##    HOST = config.get("Pixelserver","Host")
##    UDP_HOST = config.get("WLED Server","Host")
##
##    Matrix = UdpPixelMatrix(UDP_HOST)
##    #Matrix = PixelMatrix(HOST)
##    Matrix.White()
##    #Matrix.Send()
##    time.sleep(1)
##    Matrix.Black()
##    #Matrix.Send()
