from flask import Flask, redirect, url_for, render_template
from flask_socketio import SocketIO
import base64
import numpy as np
import cv2
from main import main_loop

app = Flask(__name__, template_folder='templates')

app.config.update(
    SEND_FILE_MAX_AGE_DEFAULT=0
)

app.config['SECRET_KEY'] = 'secret!'
socketio = SocketIO(app)

# Stream route
@app.route('/')
def handle_message():
    return render_template("index.html")

# Get data from socket and decode as np.array
@socketio.on('event')
def handle_event(data):

    data_splitted = data.split(',')[1]
    data_encodded = data_splitted.encode()
    data_decoded = base64.decodebytes(data_encodded)

    img_buffer = np.frombuffer(data_decoded, np.uint8)

    if len(img_buffer) > 0:
        image = cv2.imdecode(img_buffer, cv2.COLOR_BGR2RGB)


if __name__ == "__main__":
    socketio.run(app, debug=True)
