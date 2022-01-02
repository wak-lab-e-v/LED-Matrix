import PixelMatrix
from math import sin

# Additive Farbmischung
Weiss = (255, 255, 255)
Rot   = (255, 0, 0)
Gruen = (0, 255, 0)
Blau  = (0, 0, 255)

# Wir erzeugen eine Instanz Namens ,,Matrix``
# der Klasse PixelMatrix() aus der PixelMatrix Bibliothek
# Dies übernimmt für uns alles, was wir zum Pixeln brauchen.
# Wir müssen uns nun nur noch um das setzen der Pixel kümmern
Matrix = PixelMatrix.PixelMatrix()

x = 0
y = 15
for i in range(60):
    Matrix.Putpixel(i,y+round(sin(i/10)*15), Weiss)


