import face_recognition
import cv2
from datetime import datetime, timedelta
import numpy as np
import face_handler as face_handler
from face_handler import *


def main_loop():

    # Start video capture, 0 is default for webcam.
    cap = cv2.VideoCapture(0)

    number_of_faces_since_save = 0

    while True:

        ret, frame = cap.read()

        # Resize image to 1/4 for faster processing
        small_frame = cv2.resize(frame, (0, 0), fx=0.25, fy=0.25)

        # Convert color OpenCV uses BGR and face_recognition RGB
        rgb_small_frame = cv2.cvtColor(small_frame, cv2.COLOR_BGR2RGB)

        face_locations = face_recognition.face_locations(rgb_small_frame)
        face_encodings = face_recognition.face_encodings(
            rgb_small_frame, face_locations)

        face_labels = check_have_seen(
            face_locations, face_encodings, small_frame)

        draw_bbox(face_locations, face_labels, frame)

        draw_visitors_data(frame)

        cv2.imshow('Video', frame)

        # Press Q to stop
        if cv2.waitKey(1) & 0xFF == ord('q'):
            save_faces(face_locations, number_of_faces_since_save, quit=True)
            break

        number_of_faces_since_save = save_faces(
            face_locations, number_of_faces_since_save)


if __name__ == "__main__":
    load_known_faces()
    main_loop()
