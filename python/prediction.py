import json


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
        f.close()

        for item in database:
            if item["_id"] == self.user_id:
                self.user = item
                print("User: ", item)
                break

    def get_actions(self):
        self.actions = self.user["actions"]

    def get_actions_from_source(self, src):
        self.source = []
        for item in self.actions:
            if item["source"] == src:
                self.source.append(item)
                print("Action appended: ", item)

    def predict_floor(self):
        predictions = []
        sort = sorted(self.source, key=lambda number: number["nr_travels"], reverse=True)
        for i, predict in enumerate(sort):
            if predict["nr_travels"] > 2:
                predictions.append(predict["destination"])
                print("Prediciton appended: ", predict["destination"])
        return predictions
