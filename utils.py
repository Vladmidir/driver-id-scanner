import cv2

def gen_frames(camera): 
    '''ctrl+c, ctrl+v'd this functing from here: https://towardsdatascience.com/video-streaming-in-web-browsers-with-opencv-flask-93a38846fe00'''
    while True:
        success, frame = camera.read()  # read the camera frame
        if not success:
            break
        else:
            ret, buffer = cv2.imencode('.jpg', frame)
            frame = buffer.tobytes()
            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')  # concat frame one by one and show result
            
def gen_image(camera):
    '''Return the latest frame from the camera'''
    success, frame = camera.read()  # read the camera frame
    if not success:
        return None
    else:
        return frame