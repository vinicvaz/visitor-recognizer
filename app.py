from flask import Flask, redirect, url_for, render_template
from flask_socketio import SocketIO
import base64
import numpy as np
import cv2
from Recognizer import *
import face_handler as face_handler
from face_handler import *


# Basic Config
app = Flask(__name__, template_folder='templates')
app.config.update(
    SEND_FILE_MAX_AGE_DEFAULT=0
)
app.config['SECRET_KEY'] = 'secret!'

# Socket
socketio = SocketIO(app)


recognizer = None

# Stream route
@app.route('/')
def handle_message():
    return render_template("index.html")

# Starter socket that sends an ack to client if load faces is succefull
@socketio.on('start')
def handle_start(data):
    recognizer = Recognizer(user='1')
    return 'loaded'

# Get data from socket and decode as np.array
@socketio.on('event')
def handle_event(data):

    data_splitted = data.split(',')[1]
    data_encodded = data_splitted.encode()
    data_decoded = base64.decodebytes(data_encodded)

    img_buffer = np.frombuffer(data_decoded, np.uint8)

    if len(img_buffer) > 0:
        frame = cv2.imdecode(img_buffer, cv2.COLOR_BGR2RGB)


if __name__ == "__main__":
    socketio.run(app)
