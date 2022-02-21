import configparser
from pathlib import Path
import os
from sys import platform
import socket
from tkinter import X
from PIL import Image, ImageFont, ImageDraw
import time

offset_x = 1
offset_y = 1

class Matrix():

    def __init__(self,width:int, height:int):
        self.width = width
        self.height = height
        configpath = Path(__file__).parent.parent/"MatrixHost.ini"
        #if platform == "linux" or platform == "linux2":
            # linux
        #    config.read(r"../../MatrixHost.ini")
        #elif platform == "darwin":
            # OS X
        if platform == "win32":
            # Windows...
            configpath = os.path.normpath(configpath)

        print(configpath)

        #path = Path(__file__).parent
        config = configparser.ConfigParser() 
        config.read(configpath)
        #config.read("{}/MatrixHost.ini".format(path))
        self.HOST = config.get("Pixelserver","host")
        self.PORT = 1337
        print(self.HOST,self.PORT)
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.settimeout(1)
        self.socket.connect((self.HOST, self.PORT))
    
    def create_message_matrix(self,message_string:str,color):
        font = ImageFont.truetype('arialbd.ttf', 12) #load the font
        size = font.getsize(message_string)  #calc the size of text in pixels
        image = Image.new('1', size, 1)  #create a b/w image
        draw = ImageDraw.Draw(image)
        draw.text((0, 0), message_string, font=font) #render the text to the bitmap
        
        print(size)
        x_threshhold = 2
        y_threshhold = 9
        x_offset = 0
        while True:
            return_array = [[[0,0,0] for x in range(self.height)] for x in range(self.width)]
            for rownum in range(size[1]): 
            #scan the bitmap:
            # print ' ' for black pixel and 
            # print '#' for white one
                i = 0
                #print(x_offset)
                for colnum in range(x_offset,min(self.width-x_threshhold+x_offset,size[0])):
                    try:
                        if not (image.getpixel((colnum, rownum))): return_array[i+x_threshhold][rownum+y_threshhold]=color
                    except:
                        print(colnum)
                        break
                    i+=1
            
            self.send_to_matrix(return_array)
                #print(''.join(line))
            if(size[0]-x_offset < self.width-x_threshhold):
                break
            x_offset+=1
            time.sleep(0.5)
 
    def send_to_matrix(self, pixelarray):
        cmd = ""
        for x in range(self.width):
            for y in range(self.height):
                #element: [x,y,[r,g,b]]
                color = pixelarray[x][y]
                cmd = cmd + f"PX {x+offset_x} {y+offset_y} {color[0]} {color[1]} {color[2]}\n"
        #print(cmd)
        try:
            #print(cmd,len(cmd))
            self.socket.send(cmd.encode())
            return True
        except:
            #reconnect to the socket
            self.socket.close()
            self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.socket.settimeout(1)
            try:
                self.socket.connect((self.HOST, self.PORT))
                self.socket.send(cmd.encode())
                return True
            except:
                print("socket error")
                #sock_error = True
                return False

    def send_message(self, message:str,requested_color):
        self.create_message_matrix(message,requested_color)

    def send_pong(self,command):
        try:
            #print(cmd,len(cmd))
            self.socket.send(command.encode())
            return True
        except:
            #reconnect to the socket
            self.socket.close()
            self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.socket.settimeout(1)
            try:
                self.socket.connect((self.HOST, self.PORT))
                self.socket.send(command.encode())
                return True
            except:
                print("socket error")
                #sock_error = True
                return False
