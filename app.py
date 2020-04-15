from flask import Flask, redirect, url_for, render_template
from flask_socketio import SocketIO

app = Flask(__name__, template_folder='templates')

app.config.update(
    SEND_FILE_MAX_AGE_DEFAULT=0
)

app.config['SECRET_KEY'] = 'secret!'
socketio = SocketIO(app)


@app.route('/')
def handle_message():
    return render_template("index.html")


@socketio.on('event')
def handle_event(data):
    image = data['data']
    print(image)


if __name__ == "__main__":
    socketio.run(app, debug=True)
