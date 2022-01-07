import socket
import time
import tkinter as tk
from PIL import Image, ImageDraw, ImageTk
import codecs
import configparser
from pathlib import Path
import pong

path = Path(__file__).parent.parent
config = configparser.ConfigParser() 
config.read("{}/MatrixHost.ini".format(path))
HOST = config.get("Pixelserver","host")
PORT = 1337
width = 60
height = 33
multiply = 8
offset_x = 1
offset_y = 1
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.setsockopt(socket.IPPROTO_TCP, socket.TCP_NODELAY, 1)
sock.settimeout(1)
sock.connect((HOST, PORT))


class MyWidget(tk.Widget):
    def Timer(self):
        print("foo")
        self.after(1000, self.Timer)
        
class Window(tk.Frame):      
    def change_img(self):
        self.render =ImageTk.PhotoImage(getPicture())
        self.img.configure(image=self.render)
        self.img.image=self.render
        self.after(1000, self.change_img)

    def __init__(self, master=None):
        tk.Frame.__init__(self, master)
        self.master = master
        self.pack(fill=tk.BOTH, expand=1)
        #button= tk.Button(self, text= "Change", font= ('Helvetica 13 bold'),command=self.change_img)
        #button.pack(pady=15)
        #self.bind("<Return>", self.change_img)
        
        load = getPicture()
        self.render = ImageTk.PhotoImage(load)
        self.img = tk.Label(self, image=self.render)
        self.img.pack()
        #self.img.image = self.render
        #self.img.place(x=0, y=0)
        self.change_img()



def DrawLed(aImg, x,y, multi, color):
    draw = ImageDraw.Draw(aImg)
    r    = round(multi / 5)
    draw.ellipse((multi*x-r, multi*y-r, multi*x+r, multi*y+r), fill=color, outline=color)
    #aImg.putpixel((multi*x-1, multi*y), (color[0],0,0))
    #aImg.putpixel((multi*x+1, multi*y), (0,color[1],0))
    #aImg.putpixel((multi*x, multi*y+1), (0,0,color[2]))



def getPicture():
    img  = Image.new( mode = "RGB", size = (multiply*(width+1), multiply*(height+1)), color= (0,0,0))
    for y in range(height):
        for x in range(width):
            colors = pong.remote_array
            try:
                colors = colors[x][y]
                DrawLed(img, x,y, multiply, ("#{r:02X}{g:02X}{b:02X}".format(r=colors[0],g=colors[1],b=colors[2])))
            except:
                pass
    maxsize = (multiply*width, multiply*height)
    img = img.resize(maxsize)
    #img.save('img.png')
    return img

def start():
    root = tk.Tk()
    app = Window(root)
    root.wm_title("Matrix window")
    root.geometry("%dx%d" % (multiply*width, multiply*height))
    #root.geometry("1000x1000")
    root.mainloop()
if __name__ == '__main__':


    root = tk.Tk()
    app = Window(root)
    root.wm_title("Matrix window")
    root.geometry("%dx%d" % (multiply*width, multiply*height))
    #root.geometry("1000x1000")
    #root.mainloop()

    pong.pong_init()
    while True:
        pong.pong()
        root.update()





