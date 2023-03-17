import json

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

    while user is None:
        face_recognition = FaceRecognition()
        user = face_recognition.run_recognition()
        print("User: " + str(user))

    prediction = Prediction(str(user))
    prediction.get_actions_from_source(source=1)
    print("Prediction: " + str(prediction.predict_floor()[0]))

    # add_action(user, src=1, dst=3)
