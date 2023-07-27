from flask import Flask, render_template, request, url_for, flash, redirect, Response
import cv2
from markupsafe import escape
from utils import gen_frames, gen_image
import os

app = Flask(__name__)
basedir = os.path.dirname(os.path.abspath(__file__))

# Connect the web cam
camera = cv2.VideoCapture(0)

# Connect the camera and let user take a picture
# TODO: Pass the insurance as optional argument, so the user does not have to reenter it on picture retake.
@app.get('/')
def index():
    return render_template("index.html")

@app.get('/<insurance>')
def indexInsurance(insurance):
    return render_template("index.html", insurance=insurance)

# Save the picture & process the input & render the confirmation page
@app.post('/')
def processImage():
    # Record a frame
    frame = gen_image(camera)
    # Turn off the camera
    # camera.release() # Keep the camera on, up until the database submition
    # Save the frame
    snapshot_location = os.path.join(basedir, './static/snapshot.jpg')
    cv2.imwrite(snapshot_location, frame)
    # Extract insurance number
    insurance_number = request.form['insurance-number']
    # Render template
    return render_template('confirm.html', insurance=insurance_number)



# Stream the webcam
@app.route('/video_feed')
def video_feed():
    # Supply the frames as a response
    return Response(gen_frames(camera), mimetype='multipart/x-mixed-replace; boundary=frame')
