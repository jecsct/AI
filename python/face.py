import string
import random

import face_recognition  # dlib-19.22.99-cp39-cp39-win_amd64.whl
import os
import cv2  # opencv-python
import numpy as np
from PIL import Image

known_faces = []
known_names = []


def random_id():
    characters = string.ascii_letters + string.digits
    person_id = ''.join(random.choices(characters, k=12))
    return person_id


def encode_faces():
    for image in os.listdir('faces'):
        img = face_recognition.load_image_file(f"faces/{image}")
        try:
            face = face_recognition.face_encodings(img)[0]
            known_faces.append(face)
            known_names.append(image)
        except IndexError:
            print("No face found in the provided image")
            print("Removing corrupt image from database")
            os.remove("faces/" + image)


def run_recognition():
    video_capture = cv2.VideoCapture(0)
    ret, frame = video_capture.read()
    name = None

    # Only process every other frame of video to save time
    # Resize frame of video to 1/4 size for faster face recognition processing
    small_frame = cv2.resize(frame, (0, 0), fx=0.25, fy=0.25)

    # Convert the image from BGR color (which OpenCV uses) to RGB color (which face_recognition uses)
    rgb_small_frame = small_frame[:, :, ::-1]

    # Find all the faces and face encodings in the current frame of video
    locations = face_recognition.face_locations(rgb_small_frame)
    faces = face_recognition.face_encodings(rgb_small_frame, locations)

    if len(known_faces) > 0:
        for face_encoding in faces:
            # See if the face is a match for the known face(s)
            matches = face_recognition.compare_faces(known_faces, face_encoding)

            # Calculate the shortest distance to face
            face_distances = face_recognition.face_distance(known_faces, face_encoding)

            best_match = np.argmin(face_distances)
            if matches[best_match]:
                name = known_names[best_match]
                break

    if name is None:
        print("Face not recognized")
        print("Saving image to the database")
        face = np.array(small_frame)
        image = Image.fromarray(face)
        image.save("faces/" + random_id() + ".jpg")
    else:
        print("Face recognized")
        print("Hello " + name)


if __name__ == '__main__':
    encode_faces()
    run_recognition()
