import speech_recognition as sr  # SpeechRecognition
import pyttsx3


# Convert text to speech
def speak_text(command):
    engine = pyttsx3.init()
    engine.say(command)
    engine.runAndWait()
    engine.stop()


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


def get_floor(sentence):
    floor = sentence.split(" ")[4:]
    floor.remove("floor")
    return ' '.join(floor)


class Interaction:

    SENTENCES = [
        "take me to the minus one floor", "take me to the -1 floor",
        "take me to the zero floor", "take me to the 0 floor",
        "take me to the first floor", "take me to the 1st floor",
        "take me to the second floor", "take me to the 2nd floor",
        "take me to the third floor", "take me to the 3rd floor",
        "take me to the fourth floor", "take me to the 4th floor",
        "take me to the fifth floor", "take me to the 5th floor",
        "take me to the sixth floor" "take me to the 6th floor",
    ]

    def interact(self):
        r = sr.Recognizer()
        try:
            # use the microphone as source for input.
            with sr.Microphone() as source:
                speak_text("Hello! I can't recognize you. Which floor would you like to go?")
                r.adjust_for_ambient_noise(source, duration=0.2)

                # listens for the user's input
                audio = r.listen(source)
                first = r.recognize_google(audio).lower()

                for sentence in self.SENTENCES:
                    if sentence == first:
                        speak_text("Did you say " + first)

                        audio = r.listen(source)
                        response = r.recognize_google(audio).lower()

                        if response == "yes":
                            floor = get_floor(sentence)
                            speak_text("Okay " + floor + "floor, here we go!")
                            return convert_floor_string_to_num(floor)

        except sr.RequestError as e:
            print("Could not request results; {0}".format(e))

        except sr.UnknownValueError:
            print("unknown error occurred")
