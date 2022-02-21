from flask import request, render_template
import matrix_handler

class Pong():

    def __init__(self,matrix: matrix_handler.Matrix):
        self.pixelflut = matrix

    def send_command(self,command: str):
        self.pixelflut.send_pong(command)

    def receive_post(self):
        command = str(request.form['command'])
        side = str(request.form['side'])
    
        if(command=="0"):
            #up
            if(side=="helle"):
                pass
            elif(side=="dunkle"):
                
                pass
            pass
        elif(command=="1"):
            #down
            if(side=="helle"):
                pass
            elif(side=="dunkle"):
                pass
            pass

        return render_template('/pong/ingame/index.html', side=side)
    
        