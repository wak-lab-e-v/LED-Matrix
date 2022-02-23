from flask import Flask, request, render_template
from skripte.pong import Pong
from skripte.lauftext import Lauftext
import matrix_handler

app = Flask(__name__)

Display_Height = 33
Display_Width  = 60
Pixelflut = matrix_handler.Matrix(width=Display_Width,height=Display_Height)

lauftext_instance = Lauftext(Pixelflut)
pong_instance = Pong(Pixelflut)

@app.route('/')
def main():
    return render_template('/main/index.html')

@app.route('/lauftext')
def lauftext():
    return lauftext_instance.normal()

@app.route('/lauftext', methods=['POST'])
def lauftext_post():
    return lauftext_instance.post()

@app.route('/pong')
def pong():
    return render_template('/pong/index.html')

@app.route('/pong/ingame', methods=['POST'])
def pong_ingame():
    return pong_instance.receive_post()

if(__name__ == "__main__"):
    app.run(debug=True, host="0.0.0.0", port="80")
