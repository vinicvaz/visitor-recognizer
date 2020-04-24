from flask import Flask, redirect, url_for, render_template, redirect, flash
from flask_socketio import SocketIO
import base64
import numpy as np
import cv2
from Recognizer import *
import face_handler as face_handler
from face_handler import *
from engineio.payload import Payload
from Forms import *
from flask_bootstrap import Bootstrap
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
from flask_fontawesome import FontAwesome

## Basic Configuration ##
app = Flask(__name__, template_folder='templates')
app.config['SECRET_KEY'] = 'secret!'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite://///home/vinicius/Área de Trabalho/Codes/visitor-recognizer/database.db'
Bootstrap(app)
db = SQLAlchemy(app)
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'
app.config.update(
    SEND_FILE_MAX_AGE_DEFAULT=0
)

from models import * 

socketio = SocketIO(app)
Payload.max_decode_packets = 5
recognizer = 0

## Routes ##
@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

# Logout Route
@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('home'))

# Login route
@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()

    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user:
            if check_password_hash(user.password, form.password.data):
                login_user(user, remember=True)
                return redirect(url_for('stream'))

            else:
                flash('Invalid username or password')
        else:
             flash('Invalid username or password')

    return render_template('login.html', form=form)


# Register Route
@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterForm()

    if form.validate_on_submit():
        if form.password.data == form.password2.data:
            hashed_password = generate_password_hash(
                form.password.data, method='sha256')
            user = User.query.filter_by(username=form.username.data).first()
            email = User.query.filter_by(email=form.email.data).first()
            if (user!=None and email!=None):
                flash("User and email already exists.")
            elif (user==None and email!=None):
                flash("Email already exists.")
            elif (user!=None and email==None):
                flash("User already exists.")
            else:
                new_user = User(
                    username=form.username.data,
                    email=form.email.data,
                    password=hashed_password
                )
                db.session.add(new_user)
                db.session.commit()
        
                return redirect(url_for('login'))
        elif form.password.data!=form.password2.data:
            flash("Passwords must match.")

    return render_template('register.html', form=form)


# Stream route
@app.route('/stream')
@login_required
def stream():
    return render_template("index.html", name=current_user.username)


@app.route('/home')
def home():
    if(current_user.is_authenticated and current_user.is_active):
        return render_template("home.html", name=current_user.username)
    else:
        return render_template("home.html", name=None)


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

@app.route('/teste')
def teste():
    return render_template('navbar.html')


if __name__ == "__main__":
    socketio.run(app, debug=True, port=5000)
