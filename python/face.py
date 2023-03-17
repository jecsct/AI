import json
import string
import random
import face_recognition  # dlib-19.22.99-cp39-cp39-win_amd64.whl
import os
import cv2  # opencv-python
import numpy as np
from PIL import Image


def random_id():
    characters = string.digits
    person_id = ''.join(random.choices(characters, k=12))
    return person_id


def save_on_database(user_id):
    with open('database/database.json', 'r') as f:
        json_data = json.load(f)

    new_item = {
        "_id": user_id,
        "actions": []
    }

    json_data.append(new_item)

    with open('database/database.json', 'w') as f:
        json.dump(json_data, f, indent=4)


def remove_from_database(user_id):
    with open('database/database.json', 'r') as f:
        json_data = json.load(f)

    for i, item in enumerate(json_data):
        if item["_id"] == user_id:
            del json_data[i]
            break
    with open('database/database.json', 'w') as f:
        json.dump(json_data, f, indent=4)


class FaceRecognition:
    known_faces = []
    known_names = []
    face_recognized = False

    def __init__(self):
        self.encode_faces()

    def encode_faces(self):
        try:
            for image in os.listdir('faces'):
                img = face_recognition.load_image_file(f"faces/{image}")
                face = face_recognition.face_encodings(img)[0]
                self.known_faces.append(face)
                self.known_names.append(image)
        except IndexError:
            print("No face found in the provided image")
            print("Removing corrupt image from database")
            os.remove("faces/" + image)
            remove_from_database(image.split(".jpg")[0])

    def run_recognition(self):
        video_capture = cv2.VideoCapture(0)
        ret, frame = video_capture.read()
        name = None

        # Convert the image from BGR color (which OpenCV uses) to RGB color (which face_recognition uses)
        rgb_small_frame = cv2.cvtColor(frame, cv2.COLOR_RGB2BGR)

        # Find all the faces and face encodings in the current frame of video
        locations = face_recognition.face_locations(rgb_small_frame)
        faces = face_recognition.face_encodings(rgb_small_frame, locations)

        if len(self.known_faces) > 0:
            for face in faces:
                # See if the face is a match for the known face(s)
                matches = face_recognition.compare_faces(self.known_faces, face)

                # Calculate the shortest distance to face
                distances = face_recognition.face_distance(self.known_faces, face)

                best_match = np.argmin(distances)
                if matches[best_match]:
                    name = self.known_names[best_match]
                    break

        if name is None:
            print("Face not recognized")
            print("Saving image to the database")
            face = np.array(frame)
            image = Image.fromarray(face)
            user_id = random_id()
            image.save("faces/" + user_id + ".jpg")
            save_on_database(user_id)
        else:
            print("Face recognized")
            return name.split(".")[0]
