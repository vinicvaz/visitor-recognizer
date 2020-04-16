from flask import Flask, redirect, url_for, render_template
from flask_socketio import SocketIO
import base64
from io import BytesIO
import numpy as np
from PIL import Image
import io
import cv2

app = Flask(__name__, template_folder='templates')

app.config.update(
    SEND_FILE_MAX_AGE_DEFAULT=0
)

app.config['SECRET_KEY'] = 'secret!'
socketio = SocketIO(app)


@app.route('/')
def handle_message():
    return render_template("index.html")

# Function to get data from socket and decode (have to add np array converter)
@socketio.on('event')
def handle_event(data):

    data_splitted = data.split(',')[1]
    data_encodded = data_splitted.encode()
    data_decoded = base64.decodebytes(data_encodded)

    with open('test.jpg', 'wb') as f:
        f.write(data_decoded)


if __name__ == "__main__":
    socketio.run(app, debug=True)
