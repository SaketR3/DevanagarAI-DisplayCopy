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

model = load_model('mnist.h5')

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
        
        
@app.route('/save', methods=['GET', 'POST'])
def save():
    conn = psycopg2.connect(database="paintmyown", user="nidhin")
    cur = conn.cursor()
    cur.execute("SELECT id, name, data, canvas_image from files")
    files = cur.fetchall()
    conn.close()
    return render_template("dp_save.html", files = files )

@app.route('/process', methods=['POST']) 
def process(): 
    #img = request.get_json()
    #json_data = "{\"image\":\"iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAQAAAC1HAwCAAAAC0lEQVR42mNkYAAAAAYAAjCB0C8AAAAASUVORK5CYII=\"}"
    json_data = ""
    json_data = "\"" + str(request) + "\""
    image_data = json.loads(json_data)
    image_encoded = image_data[0].encode('ascii')
    image_decoded = base64.b64decode(image_encoded)
    image_array = np.frombuffer(image_decoded, dtype=np.uint8)
    image_new = Image.fromarray(image_array)
    img = image_new.resize((28,28))
    img_array = np.array(img)
    img_array = img_array.reshape(1, 28, 28, 1)
    img_array = img_array / 255.0
    res = model.predict([img_array])[0]
    digit, acc = np.argmax(res), max(res)
    #return jsonify(result=digit)
    return str("" + str(digit) + " " + str(acc))


if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
