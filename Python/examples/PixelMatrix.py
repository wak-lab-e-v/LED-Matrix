import socket
import time
import numpy as np
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

class PixelMatrix():
    def __init__(self, UDPserver='127.0.0.1', Port = 21324, Mode = 5, Autosend = True):
        self.serverAddressPort = (UDPserver, Port)
        self.lastSend = int(round(time.time() * 1000))
        self.Height = 33
        self.Width  = 60
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
        Zeile  = y  # von oben nach unten wie auch in den Bildern
        if ((Zeile % 2) == 0):
            Spalte = x
        else:
            Spalte = (self.Width-1) - x
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
        for i in range (0, self.Width ):
            for j in range(0,self.Height):
                #print(i,j)
                self.Putpixel(i,j,[0,0,0])
    def White(self):
        for i in range (0, self.Width ):
            for j in range(0,self.Height):
                #print(i,j)
                self.Putpixel(i,j,[255,255,255])

if __name__ == "__main__":
    Matrix = PixelMatrix()
    Matrix.White()
    #Matrix.Send()
    time.sleep(1)
    Matrix.Black()
    #Matrix.Send()