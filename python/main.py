import json

from audio_text import Audio
from face import FaceRecognition
from prediction import Prediction


def add_action(user_id, src, dst):
    with open('database/database.json', 'r') as f:
        json_data = json.load(f)

    for usr in json_data:
        if usr["_id"] == user_id:
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

    with open('database/database.json', 'w') as f:
        json.dump(json_data, f, indent=4)


if __name__ == '__main__':
    user = None
    current_floor = 1  # TODO: receive from arduino

    # Recognize the face and identify the user
    while user is None:
        face_recognition = FaceRecognition()
        user = face_recognition.run_recognition()
        print("User: " + str(user))

    # Make prediction
    prediction = Prediction(str(user))
    prediction.get_actions_from_source(current_floor)
    try:
        prediction = prediction.predict_floor()[0]
        print("Prediction: " + str(prediction))
    except IndexError:
        prediction = None
        print("No prediction for current location.")

    # Interact with de user
    desired_floor = Audio().interact(prediction, current_floor)
    print("Desired floor: " + str(desired_floor))

    # Add interaction to database
    add_action(user, current_floor, int(desired_floor))
    print("Action added to the database: [" + str(current_floor) + ", " + str(desired_floor) + "]")
