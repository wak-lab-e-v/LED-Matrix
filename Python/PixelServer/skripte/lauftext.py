from flask import request, render_template
from datetime import datetime
import matrix_handler

class Lauftext():
    app = None
    def __init__(self,matrix):
        self.entries = []
        self.history_length = 5

        self.pixelflut = matrix
    
        self.standard_colors = { "red":[255,0,0],
                            "green":[0,255,0],
                            "blue":[0,0,255],
                            "yellow":[255,255,0],
                            "orange":[255,128,0],
                            "purple":[255,0,255]}

    def normal(self,entry=""):
        return render_template('/lauftext/index.html', entry=entry, last_entries=self.entries)

    #@app.route('/lauftext', methods=['POST'])
    def post(self):
        text = str(request.form['text'])

        collected_input = text.split(" ", 1)
        if(len(collected_input)>1):
            retrieved_text = collected_input[1]
            color_tag = collected_input[0]
            #not using the new match feature from Python 3.10, since not everybody has it installed
            if( color_tag == "red" 
                or color_tag == "Red" 
                or color_tag == "rot" 
                or color_tag == "Rot" 
                or color_tag == "ROT" 
                or color_tag == "RED"):
                color = self.standard_colors["red"]
            elif(  color_tag == "green" 
                    or color_tag == "Green" 
                    or color_tag == "grün" 
                    or color_tag == "Grün" 
                    or color_tag == "GREEN" 
                    or color_tag == "grun" 
                    or color_tag == "GRÜN"):
                color = self.standard_colors["green"]
            elif(   color_tag == "blue" 
                    or color_tag == "Blue" 
                    or color_tag == "blau" 
                    or color_tag == "Blau" 
                    or color_tag == "BLUE" 
                    or color_tag == "BLAU"):
                color = self.standard_colors["blue"]
            elif(   color_tag == "yellow" 
                    or color_tag == "Yellow" 
                    or color_tag == "gelb" 
                    or color_tag == "Gelb" 
                    or color_tag == "YELLOW" 
                    or color_tag == "GELB"):
                color = self.standard_colors["yellow"]
            elif(   color_tag == "orange" 
                    or color_tag == "Orange" 
                    or color_tag == "ORANGE"):
                color = self.standard_colors["orange"]
            elif(   color_tag == "purple" 
                    or color_tag == "Purple" 
                    or color_tag == "lila" 
                    or color_tag == "Lila" 
                    or color_tag == "Pink"
                    or color_tag == "pink"
                    or color_tag == "PINK"   
                    or color_tag == "PURPLE" 
                    or color_tag == "LILA"):
                color = self.standard_colors["purple"]
            else:
                color = [255,255,255]
                #add non color value to displayed text
                retrieved_text = color_tag +" "+ retrieved_text
        else:
            color = [255,255,255]
            retrieved_text = collected_input[0]

        self.pixelflut.send_message(retrieved_text,color)
        
        now = datetime.now()
        modified_text = '"' + retrieved_text + '" ' + "um " + now.strftime("%H:%M:%S Uhr am %d.%m.%Y")
        #modify the main list
        self.entries.insert(0,modified_text)
        #remove last item, if list is too long
        if(len(self.entries)>self.history_length):
            self.entries.pop(-1)
            
            
        return self.normal(entry=retrieved_text)

