import json

from face import FaceRecognition
from prediction import Prediction
from audio import Interaction


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
    currentFloor = 1  # TODO: receive from arduino
    floors = {-1, 0, 1, 2, 3, 4, 5, 6}  # TODO: in the future check if the desired floor is valid

    # Recognize the face and identify the user
    while user is None:
        face_recognition = FaceRecognition()
        user = face_recognition.run_recognition()
        print("User: " + str(user))

    # Make prediction
    prediction = Prediction(str(user))
    prediction.get_actions_from_source(currentFloor)
    print("Prediction: " + str(prediction.predict_floor()[0]))

    # Interact with de user
    desiredFloor = Interaction().interact()  # TODO: negative approach; user recognition interaction;
    print("Desired floor: " + str(desiredFloor))

    # Add interaction to database
    add_action(user, currentFloor, desiredFloor)
    print("Action added to the database: [" + str(currentFloor) + ", " + str(desiredFloor) + "]")
