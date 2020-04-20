import face_recognition
import cv2
from datetime import datetime, timedelta
import numpy as np
import face_handler as face_handler
from face_handler import *


class Recognizer:

    def __init__(self, user=None):

        self.user = user
        self.known_face_encodings = []
        self.known_face_metadata = []
        self.number_of_faces_since_save = 0
        self.file = "faces_file{}.dat".format(self.user)
        self.save = False
        self.results = None

        self.load_known_faces()

        print('Recognizer Started for User {}, loading faces'.format(self.user))

    def load_known_faces(self):

        try:
            with open("faces_file{}.dat".format(self.user), "rb") as faces_file:
                self.known_face_encodings, self.known_face_metadata = pickle.load(
                    faces_file)
                print('Known faces lodaded')
        except FileNotFoundError as err:
            print('No file found, creating a new one')
            pass

    def get_results(self, frame):
        # Resize image to 1/4 for faster processing
        small_frame = cv2.resize(frame, (0, 0), fx=0.25, fy=0.25)

        # Convert color OpenCV uses BGR and face_recognition RGB
        rgb_small_frame = cv2.cvtColor(small_frame, cv2.COLOR_BGR2RGB)

        face_locations = face_recognition.face_locations(rgb_small_frame)
        face_encodings = face_recognition.face_encodings(
            rgb_small_frame, face_locations)

        # Check if have seen
        face_labels = self.check_have_seen(
            face_locations, face_encodings, small_frame)

        results = self.get_bbox(face_locations, face_labels, frame)

        self.save_faces(face_locations)
        self.results = results

    def get_bbox(self, face_locations, face_labels, frame):
        boxes = []
        for(top, right, bottom, left), face_label in zip(face_locations, face_labels):
            # Return to normal size since we divided by 4
            top *= 4  # y2
            right *= 4  # x2
            bottom *= 4  # y1
            left *= 4  # x1

            #print(left, bottom, right, top)

            info_dict = {
                # x1, y1, x2, y2
                "boxes": [left, top, right, bottom],
                "label": face_label
            }
            boxes.append(info_dict)
        return boxes

    def check_have_seen(self, face_locations, face_encodings, small_frame):
        face_labels = []
        for location, encoding in zip(face_locations, face_encodings):
            metadata = self.lookup_known_faces(encoding)

            if metadata is not None:
                time_at_door = datetime.now(
                ) - metadata['first_seen_this_interaction']
                face_label = f"Time: {int(time_at_door.total_seconds())}s"
            else:
                face_label = "New visitor!"

                top, right, bottom, left = location
                face_image = small_frame[top:bottom, left:right]
                face_image = cv2.resize(face_image, (150, 150))
                self.register_new_face(encoding, face_image)

            face_labels.append(face_label)
        return face_labels

    def lookup_known_faces(self, face_encoding):
        metadata = None

        # If has no faces return
        if len(self.known_face_encodings) == 0:
            return metadata

        # Else, compare using euclidean distance (lower value, higher similarity)
        face_distances = face_recognition.face_distance(
            self.known_face_encodings, face_encoding)
        best_match_index = np.argmin(face_distances)

        # Threshold at 0.65
        if face_distances[best_match_index] < 0.65:
            metadata = self.known_face_metadata[best_match_index]
            metadata["last_seen"] = datetime.now()
            metadata["seen_frames"] += 1

            # If not seen in the last X minutes, is a new visit
            if datetime.now() - metadata["first_seen_this_interaction"] > timedelta(minutes=30):
                metadata["first_seen_this_interaction"] = datetime.now()
                metadata["seen_count"] += 1
        return metadata

    def register_new_face(self, face_encoding, face_image):
        print("Recording new face")

        # Add new face to the known face data
        self.known_face_encodings.append(face_encoding)

        self.known_face_metadata.append({
            "first_seen": datetime.now(),
            "first_seen_this_interaction": datetime.now(),
            "last_seen": datetime.now(),
            "seen_count": 1,
            "seen_frames": 1,
            "face_image": face_image,
        })

        self.save = True

    def save_faces(self, face_locations, quit=False):

        if((len(face_locations) > 0 and self.number_of_faces_since_save > 100) or self.save == True):
            print('saving')

            with open(self.file, "wb") as faces_file:
                face_data = [self.known_face_encodings,
                             self.known_face_metadata]
                pickle.dump(face_data, faces_file)
                print('Known faces saved')
                self.save = False

            self.number_of_faces_since_save = 0
        else:
            self.number_of_faces_since_save += 1
