import asyncio

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
    return floor_str, floor_dict.get(floor_str)


class Audio:

    def __init__(self, event):
        self.event = event

    mic = sr.Recognizer()
    engine = pyttsx3.init()
    destination_floor = None
    engine.setProperty('voice', engine.getProperty('voices'))
    destinations = [-1, 0, 1, 2, 3, 4, 5, 6]
    sentPrediction = False

    def speak_text(self, speech):
        self.engine.say(speech)
        self.engine.runAndWait()
        self.engine.stop()

    def wait_for_response(self, source, prediction, current_floor):
        while True:
            audio = self.mic.listen(source)
            try:
                if self.event.is_set():
                    return
                elif prediction is not None and self.sentPrediction is False:
                    self.speak_text("Hello! Would you like to go to floor " + str(prediction) + "?")
                    self.destination_floor = (prediction, prediction)
                    self.sentPrediction = True
                    return
                else:
                    self.speak_text("Which floor would you like to go?")
                    self.destination_floor = convert_floor_string_to_num(self.mic.recognize_google(audio, language='en-US').lower())
                    if self.destination_floor[1] in self.destinations and self.destination_floor[1] is not current_floor:
                        self.speak_text("Do you want to go to the " + self.destination_floor[0] + " floor?")
                        return
                    else:
                        self.speak_text("Provided invalid floor. Please try again.")
            except sr.UnknownValueError:
                self.speak_text("I cannot understand you")

    def wait_for_confirmation(self, source):
        while True:
            audio = self.mic.listen(source)
            try:
                if self.event.is_set():
                    return True
                text = self.mic.recognize_google(audio, language='en-US')
                if text.lower() == "no":
                    return False
                elif text.lower() == "yes":
                    self.speak_text(str(self.destination_floor[0]) + " floor, here we go!")
                    print("Final destination: " + str(self.destination_floor[1]))
                    return True
                else:
                    self.speak_text("Provided action not valid. Please say yes or no.")
            except sr.UnknownValueError:
                self.speak_text("I cannot understand you")

    def interact(self, prediction, current_floor):
        with sr.Microphone() as source:
            self.mic.adjust_for_ambient_noise(source, duration=0.2)

            while True:
                print("Listening for instruction...")
                self.wait_for_response(source, prediction, current_floor)

                if self.event.is_set():
                    break

                print("Listening for confirmation...")
                if self.wait_for_confirmation(source):
                    return self.destination_floor[1]
