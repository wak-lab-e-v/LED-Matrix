import PixelMatrix
from math import sin, cos
from time import sleep

# Additive Farbmischung
Weiss = (255, 255, 255)
Rot   = (255, 0, 0)
Gruen = (0, 255, 0)
Blau  = (0, 0, 255)
Lila  = (200,100,200)

# Wir erzeugen eine Instanz Namens ,,Matrix``
# der Klasse PixelMatrix() aus der PixelMatrix Bibliothek
# Dies übernimmt für uns alles, was wir zum Pixeln brauchen.
# Wir müssen uns nun nur noch um das setzen der Pixel kümmern
Matrix = PixelMatrix.PixelMatrix()

x = 30
y = 15
for i in range(60):
    Matrix.Putpixel(x+round(cos(i/9)*15),y+round(sin(i/9)*15), Lila)
    sleep(0.5)


