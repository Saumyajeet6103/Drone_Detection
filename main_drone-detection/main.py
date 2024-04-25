from flask import Flask, request, jsonify, render_template
import cv2
import os
from ultralytics import YOLO
from werkzeug.utils import secure_filename

app = Flask(__name__)

app.config['IMAGE_MODEL_PATH'] = "static/image_model.pt"
app.config['VIDEO_MODEL_PATH'] = "static/video_model.pt"
app.config['UPLOAD_FOLDER'] = "static/uploads"
app.config['MAX_CONTENT_LENGTH'] = 20 * 1024 * 1024
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'mp4', 'avi', 'mkv'}

image_model = YOLO(app.config['IMAGE_MODEL_PATH'])
video_model = YOLO(app.config['VIDEO_MODEL_PATH'])

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def detect_drone(image_path):
    img = cv2.imread(image_path)
    pred = image_model(img)
    if pred[0].boxes.cls.shape[0] > 0:
        return f"{pred[0].boxes.cls.shape[0]} drones detected!"
    else:
        return "No drone detected."

@app.route('/')
def display_landing_page():
    return render_template("img.html")

@app.route('/video')
def display_video_page():
    return render_template("video.html")

@app.route('/upload', methods=['POST'])
def classify_image():
    if 'image' not in request.files:
        return jsonify({'resText': 'Error uploading image'}), 400

    file = request.files['image']
    if file.filename == '' or not allowed_file(file.filename):
        return jsonify({'resText': 'Invalid file format'}), 400

    filename = os.path.join(app.config['UPLOAD_FOLDER'], secure_filename(file.filename))
    file.save(filename)

    result = detect_drone(filename)

    return jsonify({'resText': result}), 200

def detect_drone_in_video(video_path):
    cap = cv2.VideoCapture(video_path)
    if not cap.isOpened():
        return "Error opening video file"

    frame_count = 0
    drone_count = 0

    while True:
        ret, frame = cap.read()
        if not ret:
            break

        # Perform drone detection on each frame
        pred = video_model(frame)
        drone_count += pred[0].boxes.cls.shape[0]
        frame_count += 1

    cap.release()

    if drone_count > 0:
        return f"{drone_count} drones detected in {frame_count} frames"
    else:
        return "No drone detected"

@app.route('/uploadvideo', methods=['POST'])
def classify_video():
    if 'video' not in request.files:
        return jsonify({'resText': 'Error uploading video'}), 400

    file = request.files['video']
    if file.filename == '' or not allowed_file(file.filename):
        return jsonify({'resText': 'Invalid file format'}), 400

    filename = os.path.join(app.config['UPLOAD_FOLDER'], secure_filename(file.filename))
    file.save(filename)

    result = detect_drone_in_video(filename)

    return jsonify({'resText': result}), 200

if __name__ == "__main__":
    app.run()
