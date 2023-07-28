from flask import Flask, render_template, request, url_for, flash, redirect, Response
import cv2
from markupsafe import escape
from utils import gen_frames, gen_image
import os

app = Flask(__name__)
basedir = os.path.dirname(os.path.abspath(__file__))

# Connect the web cam
camera = cv2.VideoCapture(0)

# Data dictionary
driver_data_dict = {
    "insurance": "102",
    "state": "ON",
    "license-number": "123",
    "expiry-date": "02/25",
    "birth-day": "21.02.1980",
    "license-class": "G",
}


# Connect the camera and let user take a picture
@app.get("/")
def index():
    return render_template("index.html")


@app.get("/<insurance>")
def indexInsurance(insurance):
    return render_template("index.html", insurance=insurance)


# Save the picture & process the input & render the confirmation page
@app.post("/")
def processImage():
    # Record a frame
    frame = gen_image(camera)
    # Turn off the camera
    # camera.release() # Keep the camera on, while the app is runing (for simplicity)
    # Save the frame
    snapshot_location = os.path.join(basedir, "./static/snapshot.jpg")
    cv2.imwrite(snapshot_location, frame)
    # Extract insurance number
    driver_data_dict["insurance"] = request.form["insurance-number"]
    # TODO: Extract the data from image here, record it into driver_data_dict
    # Render template
    return render_template("confirm.html", driver=driver_data_dict)

@app.post("/confirmed")
def confirmed():
    data_dict = request.form
    # TODO: Write the data to the database here
    return render_template('sent.html', data_dict=data_dict)

# Stream the webcam
@app.route("/video_feed")
def video_feed():
    # Supply the frames as a response
    return Response(
        gen_frames(camera), mimetype="multipart/x-mixed-replace; boundary=frame"
    )
