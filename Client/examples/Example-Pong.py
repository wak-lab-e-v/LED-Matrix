import PixelMatrix
from math import sin, cos, pi, trunc
from time import sleep, time
import numpy as np
from pathlib import Path
import keyboard
import configparser
from functools import wraps, lru_cache
import serial
from random import random

config = configparser.ConfigParser() 
configpath = Path(__file__).parent.parent/"MatrixHost.ini"
print(configpath)
config.read(configpath)
HOST = config.get("Pixelserver","Host")
UDP_HOST = config.get("WLED Server","Host")

# Additive Farbmischung
# aus Rot, Grün und Blauanteil
Weiss = (255, 255, 255)
Rot   = (255, 0, 0)
Gruen = (67, 143, 73)
Blau  = (0, 0, 255)
Lila  = (200,100,200)

def crc16_(data: bytes):
    xor_in = 0x0000  # initial value
    xor_out = 0x0000  # final XOR value
    poly = 0x1021  # generator polinom (normal form)

    reg = xor_in
    for octet in data:
        # reflect in
        for i in range(8):
            topbit = reg & 0x8000
            if octet & (0x80 >> i):
                topbit ^= 0x8000
            reg <<= 1
            if topbit:
                reg ^= poly
        reg &= 0xFFFF
        # reflect out
    return reg ^ xor_out

def findPort():
    # Find first available EiBotBoard by searching USB ports.
    # Return serial port object.
    try:
        from serial.tools.list_ports import comports
    except ImportError:
        return None
    if comports:
        try:
            com_ports_list = list(comports())
        except TypeError: # https://github.com/evil-mad/plotink/issues/38
            return None
        serial_portname = None
        for port in com_ports_list:
                print(str(port[2]))
                if port[2].startswith("USB VID:PID=0403:6001"): #FDTI 
                    serial_portname = port[0]  # Success; EBB found by VID/PID match.
                    break  # stop searching-- we are done.
        if serial_portname is None:
            for port in com_ports_list:
                #inkex.errormsg(gettext.gettext(str(port[1])))
                print(port[1])
                if port[1].startswith("USB-SERIAL CH340") or port[1].startswith("USB Serial"): # Nano
                    serial_portname = port[0]  # Success; EBB found by name match.
                    break  # stop searching-- we are done.

        return serial_portname

    

#Score
class Score():
    left = 0
    right = 0

    def resetScore(self):
        self.left = 0
        self.right = 0

LEFT = 0
RIGHT = 1
POINTS_TO_WIN = 7

class ScoreDigits():
    ZERO ="###\n# #\n###"
    ONE =" ##\n# #\n  #"
    TWO = "## \n # \n ##"
    THREE = "###\n  #\n###"
    FOUR = "# #\n###\n  #"
    FIVE = " ##\n # \n## "
    SIX = "#  \n## \n## "
    SEVEN = "###\n  #\n # "

    def returnString(self, value:int)-> str:
        if value == 0:
            return self.ZERO
        elif value == 1:
            return self.ONE
        elif value == 2:
            return self.TWO
        elif value == 3:
            return self.THREE
        elif value == 4:
            return self.FOUR
        elif value == 5:
            return self.FIVE
        elif value == 6:
            return self.SIX
        elif value == 7:
            return self.SEVEN
        
        raise ValueError("Digit is unsupported yet!")

def GRAD() -> float:
    return pi/180; 

def Paddel(aArray : np.ndarray, x,y):
    for j in range(1,5):
        aArray[x+0][j+y] = Weiss
        aArray[x+1][j+y] = Weiss
        
def Ball(aArray : np.ndarray, x:int,y:int):
    #print(x,y)
    aArray[x][y] = Weiss
    aArray[x][y+1] = Weiss
    aArray[x+1][y] = Weiss
    aArray[x+1][y+1] = Weiss


@lru_cache(maxsize=None) 
def RotateX(x,y,a) ->float:
  return x*cos(a*pi/180)#-y*sin(a*pi/180);

@lru_cache(maxsize=None)     
def RotateY(x,y,a) -> float:
  return x*sin(a*pi/180)#+y*cos(a*pi/180);

class Letters():
    L = "#    \n#    \n#    \n#    \n#####"
    I = "  #  \n  #  \n  #  \n  #  \n  #  "
    N = "#   #\n##  #\n# # #\n#  ##\n#   #"
    K = "#  # \n# #  \n##   \n# #  \n#  # "
    S = "#####\n#    \n#####\n    #\n#####"
    G = "#####\n#    \n# ###\n#   #\n#####"
    E = "#####\n#    \n###  \n#    \n#####"
    W = "#   #\n#   #\n# # #\n## ##\n#   #"
    T = "#####\n  #  \n  #  \n  #  \n  #  "
    R = "###  \n#  # \n###  \n# #  \n#  # "
    C = "#####\n#    \n#    \n#    \n#####"
    H = "#   #\n#   #\n#####\n#   #\n#   #"
    A = "  #  \n # # \n ### \n # # \n # # "
    P = " ### \n # # \n ### \n #   \n #   "
    O = "#####\n#   #\n#   #\n#   #\n#####"
    MINUS = "     \n     \n ### \n     \n     "
    EXCLAMATION = "  #  \n  #  \n  #  \n     \n  #  "

    def returnString(self, value: str):
        value = value.upper()
        if(value == "L"):
            return self.L
        if(value == "I"):
            return self.I
        if(value == "N"):
            return self.N
        if(value == "K"):
            return self.K
        if(value == "S"):
            return self.S
        if(value == "G"):
            return self.G
        if(value == "E"):
            return self.E
        if(value == "W"):
            return self.W
        if(value == "T"):
            return self.T
        if(value == "R"):
            return self.R
        if(value == "C"):
            return self.C
        if(value == "H"):
            return self.H
        if(value == "!"):
            return self.EXCLAMATION
        if(value == "A"):
            return self.A
        if(value == "P"):
            return self.P
        if(value == "O"):
            return self.O
        if(value == "-"):
            return self.MINUS

        raise ValueError("Input not supported!")

letters = Letters()

def gameOverScreen(score : Score, matrix:PixelMatrix.UdpPixelMatrix):
    """zeigt am Ende des Spiels den Gewinner an"""
    game_over_array = np.zeros(shape=(Matrix.Width,Matrix.Height,3), dtype=np.uint8)
    text = "Rechts gewinnt!"
    #links:
    if score.left == POINTS_TO_WIN:
        text = "Links gewinnt!"
    text = text.split(" ")

    for j in range(len(text)):
        for i in range(0, len(text[j])):
            current_letter = letters.returnString(text[j][i]).split("\n")
            for y in range(5):
                for x in range(5):
                    if current_letter[y][x] == "#":
                        game_over_array[3+6*i+x][5+j*6+y] = Gruen

    matrix.NdArray(game_over_array)
    sleep(5)
    score.resetScore()

def gameStartScreen(matrix:PixelMatrix.UdpPixelMatrix):
    """zeigt den normalen Startschirm an"""
    start_array = np.zeros(shape=(Matrix.Width,Matrix.Height,3), dtype=np.uint8)
    text = "Wak-pong!"

    for j in range(len(text)):
        current_letter = letters.returnString(text[j]).split("\n")
        for y in range(5):
            for x in range(5):
                if current_letter[y][x] == "#":
                    start_array[4+6*j+x][13+y] = Gruen

    matrix.NdArray(start_array)
    #TODO: add function to wait for movement of paddle
    sleep(5)
    

def scoredPoint(score: Score, side:int) -> bool:
    """Fügt einen Punkt zur jeweiligen Seite hinzu
    Gibt Wahr zurück, wenn eine Seite gewonnen hat"""
    if side == LEFT:
        score.left += 1
        if score.left == POINTS_TO_WIN:
            return True
    elif side == RIGHT:
        score.right += 1
        if score.right == POINTS_TO_WIN:
            return True
    return False

digits = ScoreDigits()

def scoreDisplay(score:Score, aArray:np.ndarray):
    """zeigt den aktuellen Score oben mittig an"""
    #links:
    data = digits.returnString(score.left).split("\n")
    help_x = x_middle-5
    for y in range(0,3):
        for x in range(0,3):
            if data[y][x] == "#":
                aArray[help_x+x][y+1] = Weiss
    
    #rechts:
    data = digits.returnString(score.right).split("\n")
    help_x = x_middle+3
    for y in range(0,3):
        for x in range(0,3):
            if data[y][x] == "#":
                aArray[help_x+x][y+1] = Weiss


def ReflektionY(Winkel):
    Einheitswinkel = Winkel
    while Einheitswinkel > 270:
        Einheitswinkel -= 360
    while Einheitswinkel < -90:
        Einheitswinkel += 360
    if (Einheitswinkel > 90):
        Einheitswinkel -=180
        Einheitswinkel *= -1*(1+((random()-0.5)/4))
        print(Einheitswinkel)
    else:
        Einheitswinkel +=180
        Einheitswinkel *= -1*(1+((random()-0.5)/4))
        print(Einheitswinkel)
    return Einheitswinkel

def Flieg(aArray : np.ndarray ,Von, Speed, Winkel):
    x = Von[0]+RotateX(Speed,0,Winkel)
    y = Von[1]+RotateY(Speed,0,Winkel)

    scored = [False,None]

    if x > Matrix.Width-2:
        #pruefe, ob Ball gegen Paddel läuft
        if (aArray[Matrix.Width-1,int(y)] == Weiss).all() or (aArray[Matrix.Width-1,int(y+1)] == Weiss).all():
            Winkel = ReflektionY(Winkel)  #180 - Winkel*1.1
        else:
            scored = [True, LEFT]
    if x < 2:
        #pruefe, ob Ball gegen Paddel läuft
        if (aArray[1,int(y)] == Weiss).all() or (aArray[1,int(y+1)] == Weiss).all():
            Winkel = ReflektionY(Winkel) # 0 - (Winkel*1.1-180)
        else:
            scored = [True, RIGHT]
    if y > Matrix.Height-2:
        #pruefe, ob Ball gegen die Decke
        Winkel = -90 - (Winkel-90)
    if y < 2:
        #pruefe, ob Ball gegen den Boden
        Winkel = 90 - (Winkel+90)
        
    #print(Winkel)
    x = Von[0]+RotateX(Speed,0,Winkel)
    y = Von[1]+RotateY(Speed,0,Winkel)

    return [x, y], Winkel, scored    

# Wir erzeugen eine Instanz Namens ,,Matrix``
# der Klasse PixelMatrix() aus der PixelMatrix Bibliothek
# Dies übernimmt für uns alles, was wir zum Pixeln brauchen.
# Wir müssen uns nun nur noch um das setzen der Pixel kümmern
Matrix = PixelMatrix.UdpPixelMatrix(UDP_HOST)
#Matrix = PixelMatrix.PixelMatrix(HOST)

Background = np.zeros(shape=(Matrix.Width,Matrix.Height,3), dtype=np.uint8)
for i in range(1,round(Matrix.Height/2)):
    Background[round(Matrix.Width/2)][i*2] = Weiss
Matrix.NdArray(Background)
Spielfeld = np.copy(Background)
sleep(1.6)
x = 30
y = 16

x_middle = int(Matrix.Width/2)
y_middle = int(Matrix.Height/2)
score = Score()

class Position():

    def __init__(self):
        self.resetPosition(random() > 0.5)

    def resetPosition(self, Dir = False):
        if Dir:
            self.position = [x_middle +10, y_middle-1]
        else:
            self.position = [x_middle-10, y_middle-1]
        self.angle = -30 + 60*random()
        if Dir:
            self.angle += 180

class PaddelData():
    left = y_middle-3
    right = y_middle-3

    def resetPaddel(self):
        self.left = y_middle-3
        self.right = y_middle-3

SerPosLinks = 0
SerPosRechts = 0
SerPosLinksOffset = 0
SerPosRechtsOffset = 0

def SerPos(serial):
    global SerPosLinks
    global SerPosRechts
    global SerPosLinksOffset
    global SerPosRechtsOffset
    while(len(data := ser.read(1)) > 0):
        if (len(data) > 0) and (data[0] == 0xAD):
            data = ser.read(4)
            if len(data) == 4:
                Paket = bytes(b'\xad' + bytearray(data[:2]))
                myCrc16 = crc16_(Paket)
                if myCrc16 == int.from_bytes(data[2:4], "little"):
                    SerPosLinks = SerPosLinksOffset + (data[0] >> 1)
                    SerPosRechts = SerPosRechtsOffset + (data[1] >> 1)
                    if (SerPosLinks > 28):
                        SerPosLinksOffset = SerPosLinksOffset - (SerPosLinks - 28)
                        SerPosLinks = SerPosLinksOffset + (data[0] >> 1)

                    if (SerPosLinks < 0):
                        SerPosLinksOffset = SerPosLinksOffset - (SerPosLinks)
                        SerPosLinks = SerPosLinksOffset + (data[0] >> 1)

                    if (SerPosRechts > 28):
                        SerPosRechtsOffset = SerPosRechtsOffset - (SerPosRechts - 28)
                        SerPosRechts = SerPosRechtsOffset + (data[1] >> 1)

                    if (SerPosRechts < 0):
                        SerPosRechtsOffset = SerPosRechtsOffset - (SerPosRechts)
                        SerPosRechts = SerPosRechtsOffset + (data[1] >> 1)
                        
                    print(' '.join('{:02x}'.format(x) for x in data[0:2]))
                    print(SerPosLinks, SerPosRechts, SerPosLinksOffset, SerPosRechtsOffset)
    

if __name__ == '__main__':
    paddel = PaddelData()
    position_class = Position()
    if (port := findPort()):
        ser = serial.Serial()
        ser.port = port
        ser.baudrate = 38400
        ser.timeout = 0.015
        ser.open()
        sleep(0.15)
        ser.flushInput()
        sleep(3.15)
        ser.write('X'.encode('cp1252')) # deaktivieren wenn möglich den 433MHz Sender
        

    #for i in range(1,1000):
    lastSend = time()
    while 1:
        if (port == None):
            if keyboard.is_pressed("p"):
                if paddel.right > 0:
                    paddel.right -= 1
            if keyboard.is_pressed("l"):
                if paddel.right < Matrix.Height-5:
                    paddel.right += 1

            if keyboard.is_pressed("q"):
                if paddel.left > 0:
                    paddel.left -= 1
            if keyboard.is_pressed("a"):
                if paddel.left < Matrix.Height-5:
                    paddel.left += 1
        else:
            SerPos(ser)
            paddel.left = SerPosLinks
            paddel.right = SerPosRechts
            
        sleep(0.04)
        delay = time() - lastSend
        if (delay > 0.080) :
            
            lastSend = time()
                
            Spielfeld = np.copy(Background)
            scoreDisplay(score, Spielfeld)
            Paddel(Spielfeld,0,paddel.left)
            Paddel(Spielfeld,Matrix.Width-2,paddel.right)
        
            Ball(Spielfeld,trunc(position_class.position[0]),trunc(position_class.position[1]))
            position_class.position, position_class.angle, scored = Flieg(Spielfeld, position_class.position, 1, position_class.angle)
            if scored[0]:
                #pruefe, ob Spiel zu Ende ist
                if(scoredPoint(score ,scored[1])):
                    #beende Spiel
                    gameOverScreen(score, Matrix)
                    gameStartScreen(Matrix)
                    position_class.resetPosition()
                    paddel.resetPaddel()
                else:
                    #resette Spielfeld für naechsten Turn
                    position_class.resetPosition(scored[1] != LEFT)
                    paddel.resetPaddel()
                    
            else:
                Matrix.NdArray(Spielfeld)
       
        
        


