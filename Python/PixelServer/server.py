from flask import Flask, request, render_template
from skripte.pong import Pong
from skripte.lauftext import Lauftext


app = Flask(__name__)
lauftext_instance = Lauftext()
pong_instance = Pong()

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
    pong_instance.post()


if(__name__ == "__main__"):
    app.run(debug=True, host="0.0.0.0", port="80")
