import json


def add_action(user_id, src, dst):
    with open('database/database.json', 'r') as f:
        json_data = json.load(f)

    for user in json_data:
        if user["_id"] == user_id:
            for action in user["actions"]:
                if action["source"] == src and action["destination"] == dst:
                    action["nr_travels"] += 1
                    break

            else:
                user["actions"].append({
                    'source': src,
                    'destination': dst,
                    'nr_travels': 1
                })
            break

    with open('database/database.json', 'w') as f:
        json.dump(json_data, f, indent=4)


class Prediction:
    user = None
    actions = None
    source = []

    def __init__(self, user_id):
        self.user_id = user_id
        self.get_user()
        try:
            self.get_actions()
        except TypeError:
            print("User not found")
            exit()

    def get_user(self):
        with open('database/database.json', 'r') as f:
            database = json.load(f)

        for item in database:
            if item["_id"] == self.user_id:
                self.user = item

    def get_actions(self):
        self.actions = self.user["actions"]

    def get_specific_actions(self, source):
        for item in self.actions:
            if item["source"] == source:
                self.source.append(item)

    def predict_floor(self):
        predictions = []
        sort = sorted(self.source, key=lambda number: number["nr_travels"], reverse=True)
        for i, predict in enumerate(sort):
            print("Prediction " + str(i+1) + ": " + str(predict["destination"]))
            predictions.append(predict["destination"])
        return predictions


if __name__ == '__main__':
    prediction = Prediction(user_id="343196631498")
    prediction.get_specific_actions(source=1)
    print(prediction.predict_floor())
    # add_action(user_id="343196631498", src=1, dst=3)
