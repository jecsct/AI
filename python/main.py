import json
import os
import threading
import serial

from audio_text import Audio
from face import FaceRecognition
from prediction import Prediction

result = None
user = None
prediction = None
current_floor = None

ser = serial.Serial('COM4', 9600, timeout=1)
# ser = serial.Serial('/dev/ttyACM0', 9600, timeout=1)

floors = ["-1", "0", "1", "2", "3", "4", "5", "6"]


def get_current_floor():
    ser.reset_input_buffer()
    while True:
        if ser.in_waiting > 0:
            line = ser.readline().decode('utf-8').rstrip()
            if line[0:3] == "SRC":
                if line[3:] in floors:
                    curr = int(line[3:])
                    print("Current floor received: ", curr)
                    return curr


def add_action(user_id, src, dst):
    if os.stat("database/database.json").st_size != 0:
        with open('database/database.json', 'r') as f:
            json_data = json.load(f)
        f.close()
        for usr in json_data:
            if usr["_id"] == user_id and usr["_id"] != "None":
                for action in usr["actions"]:
                    if action["source"] == src and action["destination"] == dst:
                        action["nr_travels"] += 1
                        break

                else:
                    usr["actions"].append({
                        'source': src,
                        'destination': dst,
                        'nr_travels': 1
                    })
                break
    else:
        json_data = ([{
            "_id": str(user_id),
            "actions": [
                {
                    "source": src,
                    "destination": dst,
                    "nr_travels": 1
                }
            ]
        }])

    with open('database/database.json', 'w') as f:
        json.dump(json_data, f, indent=4)
    f.close()


def wait_for_manual_response(name, event):
    print("Waiting for manual response")
    global result
    ser.reset_input_buffer()
    while True:
        if event.is_set():
            return
        elif ser.in_waiting > 0:
            line = ser.readline().decode('utf-8').rstrip()
            if line[0:3] == "DST":
                if line[3:] in floors:
                    result = int(line[3:])
                    print("Manual input received: ", result)
                    event.set()
                    break


def wait_for_verbal_response(name, event):
    print("Waiting for verbal response")
    global result, user, prediction, current_floor

    # Recognize the face and identify the user
    while user is None:
        face_recognition = FaceRecognition()
        user = face_recognition.run_recognition()
        print("User: " + str(user))

    # Make prediction
    if os.stat("database/database.json").st_size != 0:
        prediction = Prediction(str(user))
        prediction.get_actions_from_source(current_floor)
        try:
            prediction = prediction.predict_floor()[0]
            print("Prediction: " + str(prediction))
        except IndexError:
            prediction = None
            print("No prediction for current location.")

    # Interact with de user
    result = Audio(event).interact(prediction, current_floor)
    print("Desired floor: " + str(result))

    event.set()


def run():
    global current_floor
    # Get arduino input
    current_floor = get_current_floor()

    event = threading.Event()

    # Wait for manual input
    t1 = threading.Thread(target=wait_for_manual_response, args=("Manual", event))
    t2 = threading.Thread(target=wait_for_verbal_response, args=("Verbal", event))
    t1.start()
    t2.start()

    event.wait()

    # Add interaction to database
    add_action(str(user), int(current_floor), int(result))

    print("Action added to the database: [" + str(current_floor) + ", " + str(result) + "]")
    t2.join()
    t1.join()
    print("LEFT T2")
