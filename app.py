from flask import Flask, redirect, url_for, render_template
from flask_socketio import SocketIO
import base64
import numpy as np
import cv2
from Recognizer import *
import face_handler as face_handler
from face_handler import *
from engineio.payload import Payload


# Basic Config
app = Flask(__name__, template_folder='templates')
app.config.update(
    SEND_FILE_MAX_AGE_DEFAULT=0
)
app.config['SECRET_KEY'] = 'secret!'

# Socket
socketio = SocketIO(app)
Payload.max_decode_packets = 5

recognizer = 0

# Login route
@app.route('/login')
def home():
    return render_template('login.html')


@app.route('/register')
def register():
    return render_template('register.html')

# Stream route
@app.route('/')
def handle_message():
    return render_template("index.html")


# Starter socket that sends an ack to client if load faces is succefull
@socketio.on('start')
def handle_start(data):
    global recognizer

    recognizer = Recognizer(user=1)
    return 'loaded'

# Get data from socket and decode as np.array
@socketio.on('event')
def handle_event(data):
    global recognizer

    data_splitted = data.split(',')[1]
    data_encodded = data_splitted.encode()
    data_decoded = base64.decodebytes(data_encodded)

    img_buffer = np.frombuffer(data_decoded, np.uint8)

    if len(img_buffer) > 0 and recognizer != 0:
        frame = cv2.imdecode(img_buffer, cv2.COLOR_BGR2RGB)
        recognizer.get_results(frame)

        return recognizer.results
    return 0


if __name__ == "__main__":
    socketio.run(app, debug=True)
