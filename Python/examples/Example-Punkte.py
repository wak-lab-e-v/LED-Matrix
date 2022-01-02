import PixelMatrix

Weiss = (255, 255, 255)
Rot   = (255, 0, 0)
Gruen = (0, 255, 0)
Blau  = (0, 0, 255)

# Wir erzeugen eine Instanz Namens ,,Matrix``
# der Klasse PixelMatrix() aus der PixelMatrix Bibliothek
# Dies übernimmt für uns alles, was wir zum Pixeln brauchen.
# Wir müssen uns nun nur noch um das setzen der Pixel kümmern
Matrix = PixelMatrix.PixelMatrix()

x = 10
y = 10
Matrix.Putpixel(x,y, Weiss)

x = 10
y = 11
Matrix.Putpixel(x,y, Rot)

x = 10
y = 12
Matrix.Putpixel(x,y, Gruen)

x = 10
y = 13
Matrix.Putpixel(x,y, Blau)
