import face_recognition
import cv2
from datetime import datetime, timedelta
import numpy as np
import face_handler as face_handler
from face_handler import *


class Recognizer:

    def __init__(self, user=None):

        self.user = user
        self.known_face_encodings = None
        self.known_face_metadata = None

        self.load_known_faces()

        print('Recognizer Started for User {}, loading faces'.format(self.user))

    def load_known_faces(self):

        print('to aq')
        try:
            with open("faces_file.dat"+self.user, "rb") as faces_file:
                self.known_face_encodings, self.known_face_metadata = pickle.load(
                    faces_file)
                print('Known faces lodaded')
        except FileNotFoundError as err:
            print('No file found, creating a new one')
            pass
