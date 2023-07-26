from flask import Flask, render_template, request, url_for, flash, Response
import cv2
from markupsafe import escape
from utils import gen_frames

app = Flask(__name__)

# Connect the web cam
camera = cv2.VideoCapture(0)

@app.get('/')
def index():
    return render_template("index.html")

@app.route('/video_feed')
def video_feed():
    # Supply the frames as a response
    return Response(gen_frames(camera), mimetype='multipart/x-mixed-replace; boundary=frame')