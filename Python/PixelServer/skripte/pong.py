from flask import request, render_template

class Pong():

    def __init__(self):
        pass

    def post(self):
        command = str(request.form['command'])
        side = str(request.form['side'])

        if(command=="0"):
            #up
            pass
        elif(command=="1"):
            #down
            pass

        return render_template('/pong/ingame/index.html', side=side)
    
        