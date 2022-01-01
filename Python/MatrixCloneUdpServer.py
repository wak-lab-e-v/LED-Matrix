import socket
import time
import numpy as np
import tkinter as tk
from PIL import Image, ImageTk
import codecs

from threading import Thread, Event

UDP_IP_ADDRESS = '127.0.0.1'
UDP_PORT_NO = 21324

bufferSize  = 2048
ADDR        = (UDP_IP_ADDRESS, UDP_PORT_NO)

width = 60
height = 33
multiply = 8
offset_x = 1
offset_y = 1

MatrixBuffer = np.zeros(shape=(width,height,3), dtype=int)


class Window(tk.Frame):      
    def change_img(self):
        self.render =ImageTk.PhotoImage(self.DrawBuffer(MatrixBuffer))
        self.img.configure(image=self.render)
        self.img.image=self.render
        self.after(70, self.change_img)

    def __init__(self, master=None):
        tk.Frame.__init__(self, master)
        self.master = master
        self.pack(fill=tk.BOTH, expand=1)
        #button= tk.Button(self, text= "Change", font= ('Helvetica 13 bold'),command=self.change_img)
        #button.pack(pady=15)
        #self.bind("<Return>", self.change_img)
        
        load = self.DrawBuffer(MatrixBuffer)
        self.render = ImageTk.PhotoImage(load)
        self.img = tk.Label(self, image=self.render)
        self.img.pack()
        #self.img.image = self.render
        #self.img.place(x=0, y=0)
        self.change_img()
        
    def DrawBuffer(self, Buffer):
        #print(Buffer.shape)
        Bwidth, Bheight,_ = Buffer.shape
        img  = Image.new( mode = "RGB", size = (multiply*(width+1), multiply*(height+1)), color= (0,0,0))
        for j in range(Bheight):
            for i in range(Bwidth):
                color = Buffer[i][j]
                y = j + 1
                x = i + 1 
                img.putpixel((multiply*x, multiply*y), (color[0], color[1], color[2]) )
                img.putpixel((multiply*x+1, multiply*y), (color[0], color[1], color[2]) )
                img.putpixel((multiply*x-1, multiply*y), (color[0], color[1], color[2]) )
                img.putpixel((multiply*x, multiply*y-1), (color[0], color[1], color[2]) )
                img.putpixel((multiply*x, multiply*y+1), (color[0], color[1], color[2]) )
        return img



#while True:
#    data, addr = serverSock.recvfrom(1024)
#    print "Message: ", data




def getPicture():
##    cmd = "GM\n"
##    try:
##        Text=sock.recv(10) # socket.setblocking
##    except socket.timeout:
##        pass
##    sock.send(cmd.encode())
##    time.sleep(0.5)
##    Text=sock.recv(3*2*width*height).decode()
    img  = Image.new( mode = "RGB", size = (multiply*width, multiply*height), color= (0,0,0))
##    try:
##        bytesObj = codecs.decode(Text, 'hex_codec')
##    except:
##        print(Text)
    index = 0
    #print(bytesObj)

    #maxsize = (multiply*width, multiply*height)
    #img = img.resize(maxsize);
    return img


def accept_incoming_connections():
    """Sets up handling for incoming clients."""
    while not stop.isSet():
        print("Wait for Client")
        try:
          client_msg, client_address = UDPServerSocket.recvfrom(bufferSize)  
          print("%s:%s has connected." % client_address)
        except:
          stop.set()
        msg2Matrix(client_msg)

def Decode4(msg):
    gain = 6
    offset = (msg[2] << 8) + msg[3]
    for i in range(int((len(msg)-4)/3)):
        color = (msg[i*3+4]*gain, msg[i*3+5]*gain, msg[i*3+6]*gain)
        index = i+offset
        Zeile = int(index/width)
        if (Zeile % 2) == 0:
            MatrixBuffer[index % width][Zeile] = color
        else:
            MatrixBuffer[(width-1)-(index % width)][Zeile] = color
    
def Decode5(msg):
    offset = (msg[2] << 8) + msg[3]
    #print(len(msg))
    for i in range(int((len(msg)-4)/2)):
        color16 = (msg[i*2+4] << 8) + msg[i*2+5]
        color = ((color16 >> 8) & 0xF8, (color16 >> 3) & 0xFC, (color16 << 3) & 0xF8)
        index = i+offset
        Zeile = int(index/width)
        if (Zeile % 2) == 0:
            MatrixBuffer[index % width][Zeile] = color
        else:
            MatrixBuffer[(width-1)-(index % width)][Zeile] = color
        
    
        
def msg2Matrix(msg):
    if len(msg) > 4:
        Type = msg[0]
        if (Type == 5):
            Decode5(msg)
        if (Type == 4):  # WLED UDP Realtime Control ,Protokoll 4 DNRGB
            Decode4(msg)
        
    
if __name__ == '__main__':
    root = tk.Tk()
    app = Window(root)
    root.wm_title("Matrix window")
    root.geometry("%dx%d" % (multiply*width, multiply*height))
    #root.geometry("1000x1000")

    UDPServerSocket = socket.socket(socket.AF_INET, type=socket.SOCK_DGRAM)
    UDPServerSocket.bind(ADDR)
    stop = Event()
    print("Waiting for connection...")
    try: 
        receive_thread = Thread(target=accept_incoming_connections)
        receive_thread.start()
        #receive_thread.join()
        root.mainloop()
    except (KeyboardInterrupt, SystemExit):
        print('\n! Received keyboard interrupt, quitting threads.\n'  )
        stop.set()
    UDPServerSocket.close()





