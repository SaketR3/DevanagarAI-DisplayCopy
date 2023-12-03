import os
import sys
import json
from flask import Flask, render_template, request, redirect, url_for
import psycopg2
from keras.models import load_model
from PIL import ImageGrab, Image
import numpy as np
import json
import base64

# CHANGE THIS TO YOUR OWN ABSOLUTE PATH TO 'AIDAN.H5'
# To figure out the path, right-click 'aidan.h5' and then click 'Copy Path'
# After copy/pasting it, change all the back-slashes to forward-slashes
# (Change all of the \ to /)
model = load_model('C:/Users/sredd/OneDrive/Documents/GitHub/Group16-FA23/aidan.h5')

devanagari_characters = [
    "क", "ख", "ग", "घ", "ङ",
    "च", "छ", "ज", "झ", "ञ",
    "ट", "ठ", "ड", "ढ", "ण",
    "त", "थ", "द", "ध", "न",
    "प", "फ", "ब", "भ", "म",
    "य", "र", "ल", "व", "श",
    "ष", "स", "ह", "क्ष",
    "त्र", "त्त", "०", "१", "२", "३",
    "४", "५", "६", "७", "८", "९"
]

dict = {
  "क": "ka",
  "ख": "kha",
  "ग": "ga",
  "घ": "gha",
  "ङ": "kna",
  "च": "cha",
  "छ": "chha",
  "ज": "ja",
  "झ": "jha",
  "ञ": "yna",
  "ट": "taa",
  "ठ": "thaa",
  "ड": "da",
  "ढ": "dha",
  "ण": "adna",
  "त": "ta",
  "थ": "tha",
  "द": "da",
  "ध": "dha",
  "न": "na",
  "प": "pa",
  "फ": "pha",
  "ब": "ba",
  "भ": "bha",
  "म": "ma",
  "य": "ya",
  "र": "ra",
  "ल": "la",
  "व": "va",
  "श": "sha",
  "ष": "shaa",
  "स": "sa",
  "ह": "ha",
  "क्ष": "chhya",
  "त्र": "tra",
  "त्त": "gya",
  "०": "0",
  "१": "1",
  "२": "2",
  "३": "3",
  "४": "4",
  "५": "5",
  "६": "6",
  "७": "7",
  "८": "8",
  "९": "9",
}

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def paintapp():
    if request.method == 'GET':
        return render_template("paint.html")
    if request.method == 'POST':
        filename = request.form['save_fname']
        data = request.form['save_cdata']
        canvas_image = request.form['save_image']
        conn = psycopg2.connect(database="paintmyown", user = "nidhin")
        cur = conn.cursor()
        cur.execute("INSERT INTO files (name, data, canvas_image) VALUES (%s, %s, %s)", [filename, data, canvas_image])
        conn.commit()
        conn.close()
        return redirect(url_for('save'))        

@app.route('/process', methods=['POST']) 
def process(): 
    #img = request.get_json()
    #json_data = "{\"image\":\"iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAQAAAC1HAwCAAAAC0lEQVR42mNkYAAAAAYAAjCB0C8AAAAASUVORK5CYII=\"}"
    #json_data = ""
    #json_data = "\"" + str(request.json) + "\""
    #request_json = request.json
    #dictionary = request_json['data']
    #image_data = json.loads(json_data)
    #image_encoded = image_data[0].encode('ascii')
    #image_decoded = base64.b64decode(image_encoded)
    #image_array = np.frombuffer(image_decoded, dtype=np.uint8)
    #image_new = Image.fromarray(image_array)
    #return jsonify(result=digit)
    #return str("\"" + str(request) + "\"")

    """
    img = im.resize((28,28))
    img = img.convert('L')
    img_array = np.array(img)
    img_array = img_array.reshape(1, 28, 28, 1)
    img_array = img_array / 255.0
    """

    im = ImageGrab.grab(bbox = (750, 210, 1400, 890))
    #im.show()
    img = im.resize((32,32))
    img = img.convert('L')
    img_array = np.array(img)
    img_array = img_array.reshape(1, 32, 32, 1)
    img_array = img_array / 255.0
    res = model.predict([img_array])[0]
    letter, acc = np.argmax(res), max(res)
    return_array = [devanagari_characters[letter], dict.get(devanagari_characters[letter]), str(round(acc*100, 2))]
    return return_array

@app.route('/about', methods=['GET'])
def about_page():
    return render_template("about.html")

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
