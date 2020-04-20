import face_recognition
import cv2
from datetime import datetime, timedelta
import numpy as np
import pickle

known_face_encodings = []
known_face_metadata = []


def load_known_faces():
    global known_face_encodings
    global known_face_metadata

    try:
        with open("faces_file.dat", "rb") as faces_file:
            print('cai aq')
            known_face_encodings, known_face_metadata = pickle.load(
                faces_file)
            print('Known faces lodaded')
    except FileNotFoundError as err:
        print('No file found, creating a new one')
        pass


def lookup_known_faces(face_encoding):
    metadata = None

    # If has no faces return
    if len(known_face_encodings) == 0:
        return metadata

    # Else, compare using euclidean distance (lower value, higher similarity)
    face_distances = face_recognition.face_distance(
        known_face_encodings, face_encoding)
    best_match_index = np.argmin(face_distances)

    # Threshold at 0.65
    if face_distances[best_match_index] < 0.65:
        metadata = known_face_metadata[best_match_index]
        metadata["last_seen"] = datetime.now()
        metadata["seen_frames"] += 1

        # If not seen in the last X minutes, is a new visit
        if datetime.now() - metadata["first_seen_this_interaction"] > timedelta(minutes=30):
            metadata["first_seen_this_interaction"] = datetime.now()
            metadata["seen_count"] += 1
    return metadata


def register_new_face(face_encoding, face_image):
    print("Recording new face")

    # Add new face to the known face data
    known_face_encodings.append(face_encoding)

    known_face_metadata.append({
        "first_seen": datetime.now(),
        "first_seen_this_interaction": datetime.now(),
        "last_seen": datetime.now(),
        "seen_count": 1,
        "seen_frames": 1,
        "face_image": face_image,
    })


def check_have_seen(face_locations, face_encodings, small_frame):
    face_labels = []
    for location, encoding in zip(face_locations, face_encodings):
        metadata = lookup_known_faces(encoding)

        if metadata is not None:
            time_at_door = datetime.now(
            ) - metadata['first_seen_this_interaction']
            face_label = f"Time: {int(time_at_door.total_seconds())}s"
        else:
            face_label = "New visitor!"

            top, right, bottom, left = location
            face_image = small_frame[top:bottom, left:right]
            face_image = cv2.resize(face_image, (150, 150))
            register_new_face(encoding, face_image)

        face_labels.append(face_label)
    return face_labels


def draw_bbox(face_locations, face_labels, frame):

    for(top, right, bottom, left), face_label in zip(face_locations, face_labels):
        # Return to normal size since we divided by 4
        top *= 4
        right *= 4
        bottom *= 4
        left *= 4

        print(left, bottom, right, top)
        # Draw bbox on face
        cv2.rectangle(frame, (left, top), (right, bottom), (0, 0, 255), 2)
        # Draw label
        cv2.rectangle(frame, (left, bottom - 35),
                      (right, bottom), (0, 0, 255), cv2.FILLED)
        cv2.putText(frame, face_label, (left + 6, bottom - 6),
                    cv2.FONT_HERSHEY_DUPLEX, 0.8, (255, 255, 255), 1)


def draw_visitors_data(frame):
    number_of_recent_visitors = 0

    for metadata in known_face_metadata:
        # If we have seen this person in the last minute, draw their image
        if (datetime.now() - metadata['last_seen'] < timedelta(seconds=10)) and (metadata['seen_frames'] > 5):
            # Position offset to display face image
            x_position = number_of_recent_visitors * 150
            frame[30:180, x_position:x_position+150] = metadata['face_image']
            number_of_recent_visitors += 1

            visits = metadata['seen_count']
            visit_label = f"{visits} visits"
            if visits == 1:
                visit_label = 'First Visit'

            cv2.putText(frame, visit_label, (x_position + 10, 170),
                        cv2.FONT_HERSHEY_DUPLEX, 0.6, (255, 255, 255), 1)

    if number_of_recent_visitors > 0:
        cv2.putText(frame, "Visitors:", (5, 18),
                    cv2.FONT_HERSHEY_DUPLEX, 0.8, (0, 0, 0), 1)


def save_faces(face_locations, number_of_faces_since_save, quit=False):

    if((len(face_locations) > 0 and number_of_faces_since_save > 100) or quit == True):
        print('saving')

        with open("faces_file.dat", "wb") as faces_file:
            face_data = [known_face_encodings, known_face_metadata]
            pickle.dump(face_data, faces_file)
            print('Known faces saved')

        number_of_faces_since_save = 0
        return number_of_faces_since_save
    else:
        number_of_faces_since_save += 1
        return number_of_faces_since_save
