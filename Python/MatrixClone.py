import socket
import time
import tkinter as tk
from PIL import Image, ImageDraw, ImageTk
import codecs
import configparser
from pathlib import Path

path = Path(__file__).parent
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
    cmd = "GM\n"
    try:
        Text=sock.recv(10) # socket.setblocking
    except socket.timeout:
        pass
    sock.send(cmd.encode())
    time.sleep(0.5)
    Text=sock.recv(3*2*width*height).decode()
    img  = Image.new( mode = "RGB", size = (multiply*(width+1), multiply*(height+1)), color= (0,0,0))
    try:
        bytesObj = codecs.decode(Text, 'hex_codec')
    except:
        bytesObj = codecs.decode('00', 'hex_codec')
        print(Text)
        Text=sock.recv(3*2*width*height).decode()
    index = 0
    if len(bytesObj) >= 3*width*height: 
        for y in range(1,height+1):
            for x in range(1,width+1):
                DrawLed(img, x,y, multiply, (bytesObj[index], bytesObj[index+1], bytesObj[index+2]))
                index = index + 3
    maxsize = (multiply*width, multiply*height)
    img = img.resize(maxsize)
    #img.save('img.png')
    return img

    
if __name__ == '__main__':


    root = tk.Tk()
    app = Window(root)
    root.wm_title("Matrix window")
    root.geometry("%dx%d" % (multiply*width, multiply*height))
    #root.geometry("1000x1000")
    root.mainloop()





