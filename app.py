'''
from flask import Flask, request, jsonify, render_template
import numpy as np
import cv2, os
from ultralytics import YOLO
from werkzeug.utils import secure_filename

app = Flask(__name__)

app.config['MODEL_PATH'] = "static/best.pt"
app.config['UPLOAD_FOLDER'] = "static/uploads"
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024
ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg'])


model = YOLO(app.config['MODEL_PATH'])

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def runNeuralNetwork(filename):
    img = cv2.imread(filename)
    #img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    #img = cv2.resize(img, (256, 256))

    
    pred = model(img)
    # pred = model(img)
    print(pred[0].boxes.cls.shape[0])
    if pred[0].boxes.cls.shape[0] > 0:
        return "drn"
    else:
        return "no drn"


@app.route('/', methods=['GET'])
def displayLandingPage():
    return render_template("index.html")

@app.route('/upload', methods=['POST'])
def classifyImage():
    if request.method == 'POST':
        resText = ''
        if 'image' not in request.files:
            resText = "Error uploading image"
        else:
            file = request.files['image']
            
            if file and allowed_file(file.filename) and file.filename != '':
                filename = os.path.join(app.config['UPLOAD_FOLDER'], secure_filename(file.filename))
                file.save(filename)
                resText = runNeuralNetwork(filename)
            else:
                resText = "Error uploading image"
        
        response = jsonify({'resText' : resText})
        response.headers.add('Access-Control-Allow-Origin', '*')
        return response


if __name__ == "__main__":
    app.run(port=5000)

'''

from flask import Flask, request, jsonify, render_template
import cv2
import os
from ultralytics import YOLO
from werkzeug.utils import secure_filename

app = Flask(__name__)

app.config['MODEL_PATH'] = "static/best.pt"
app.config['UPLOAD_FOLDER'] = "static/uploads"
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}

model = YOLO(app.config['MODEL_PATH'])

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def detect_Drone(image_path):
    img = cv2.imread(image_path)
    pred = model(img)
    if pred[0].boxes.cls.shape[0] > 0:
        return f"{pred[0].boxes.cls.shape[0]} Drones detected!"
    else:
        return "No Drone detected."

@app.route('/')
def display_landing_page():
    return render_template("index.html")

@app.route('/upload', methods=['POST'])
def classify_image():
    if 'image' not in request.files:
        return jsonify({'resText': 'Error uploading image'}), 400

    file = request.files['image']
    if file.filename == '' or not allowed_file(file.filename):
        return jsonify({'resText': 'Invalid file format'}), 400

    filename = os.path.join(app.config['UPLOAD_FOLDER'], secure_filename(file.filename))
    file.save(filename)

    result = detect_Drone(filename)

    return jsonify({'resText': result}), 200

if __name__ == "__main__":
    app.run(port=5000)



