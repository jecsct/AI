import speech_recognition as sr
import pyttsx3


def convert_floor_string_to_num(floor_str):
    floor_dict = {
        "-1": -1,
        "minus one": -1,
        "0": 0,
        "zero": 0,
        "1st": 1,
        "first": 1,
        "second": 2,
        "2nd": 2,
        "3rd": 3,
        "third": 3,
        "4th": 4,
        "fourth": 4
    }
    return floor_dict.get(floor_str)


class Audio:

    def __init__(self, event):
        self.event = event

    mic = sr.Recognizer()
    engine = pyttsx3.init()
    floor = None
    engine.setProperty('voice', engine.getProperty('voices'))
    destinations = [-1, 0, 1, 2, 3, 4, 5, 6]
    sentPrediction = False

    def wait_for_response(self, prediction, current_floor):
        while True:
            if self.event.is_set():
                return
            if prediction is not None and self.sentPrediction is False:
                print("Hello! Would you like to go to " + str(prediction) + " floor?")
                self.floor = prediction
                self.sentPrediction = True
                return
            else:
                self.floor = input("Which floor would you like to go? ")
                try:
                    if int(self.floor) in self.destinations and int(self.floor) is not current_floor:
                        print("Do you want to go to the " + self.floor + " floor? ")
                        return
                    else:
                        print("Provided floor not valid. Please try again.")
                except ValueError:
                    print("Provided floor not valid. Please try again")

    def wait_for_confirmation(self):
        while True:
            response = input()
            if self.event.is_set():
                break
            if response == "no":
                return False
            elif response == "yes":
                print(str(self.floor) + " floor, here we go!")
                return True
            else:
                print("Provided action not valid. Please type yes or no.")

    def interact(self, prediction, current_floor):
        while True:
            print("Waiting for instruction...")
            self.wait_for_response(prediction, current_floor)

            if self.event.is_set():
                break

            print("Waiting for confirmation...")
            if self.wait_for_confirmation():
                return self.floor
