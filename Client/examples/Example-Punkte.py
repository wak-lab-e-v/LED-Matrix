import PixelMatrix
import configparser
config = configparser.ConfigParser() 
config.read(r"../../../MatrixHost.ini")
HOST = config.get("Pixelserver","Host")
UDP_HOST = "192.168.178.43" #config.get("WLED Server","Host")

# Additive Farbmischung
# aus Rot, Grün und Blauanteil
Weiss = (255, 255, 255)
Rot   = (255, 0, 0)
Gruen = (0, 255, 0)
Blau  = (0, 0, 255)
Lila  = (200,100,200)

# Wir erzeugen eine Instanz Namens ,,Matrix``
# der Klasse PixelMatrix() aus der PixelMatrix Bibliothek
# Dies übernimmt für uns alles, was wir zum Pixeln brauchen.
# Wir müssen uns nun nur noch um das setzen der Pixel kümmern
Matrix = PixelMatrix.UdpPixelMatrix(UDP_HOST)
#Matrix = PixelMatrix.PixelMatrix(HOST)
Matrix.White()


Matrix.Putpixel(1,1, Lila)
#Matrix.Putpixel(1,1,Rot)

#print(Matrix.Getpixel(2,12))

##for i in range(60):
##    for j in range(32):
##        Matrix.Putpixel(i,j,Rot)
##
##from math import sin, cos
##x = 30
##y = 16
##for i in range(1,59):        
##   Matrix.Putpixel(x+round(cos(i/9)*15),y+round(sin(i/9)*15), Blau)


##x = 10
##y = 20
##Matrix.Putpixel(x,y, Weiss)
##
##x = 10
##y = 11
##Matrix.Putpixel(x,y, Rot)
##
##x = 10
##y = 12
##Matrix.Putpixel(x,y, Gruen)
##
##x = 10
##y = 13
##Matrix.Putpixel(x,y, Blau)
