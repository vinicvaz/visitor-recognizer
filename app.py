from flask import Flask, redirect, url_for, render_template
from flask_socketio import SocketIO

app = Flask(__name__, template_folder='templates')

app.config.update(
    SEND_FILE_MAX_AGE_DEFAULT=0
)


@app.route('/')
def home():
    return render_template("index.html")


if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0')
