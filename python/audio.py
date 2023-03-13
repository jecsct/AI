import speech_recognition as sr
import pyttsx3

# Initialize the recognizer
r = sr.Recognizer()


# Function to convert text to speech
def speak_text(command):
    engine = pyttsx3.init()
    engine.say(command)
    engine.runAndWait()
    engine.stop()


SENTENCES = [
    "take me to the minus one floor",
    "take me to the -1 floor",
    "take me to the first floor",
    "take me to the 1st floor",
    "take me to the second floor",
    "take me to the 2nd floor",
    "take me to the third floor",
    "take me to the 3rd floor",
    "take me to the fourth floor",
    "take me to the 4th floor",
    "take me to the fifth floor",
    "take me to the 5th floor",
    "take me to the sixth floor"
    "take me to the 6th floor",
]

# Exception handling to handle exceptions at the runtime
try:
    # use the microphone as source for input.
    with sr.Microphone() as source:
        r.adjust_for_ambient_noise(source, duration=0.2)

        # listens for the user's input
        audio = r.listen(source)
        first = r.recognize_google(audio).lower()

        for sentence in SENTENCES:
            if sentence == first:
                speak_text("Did you say " + first)

                audio = r.listen(source)
                response = r.recognize_google(audio).lower()

                if response == "yes":
                    floor = sentence.split(" ")[4:]
                    speak_text("Okay " + ''.join(floor) + ", here we go!")

except sr.RequestError as e:
    print("Could not request results; {0}".format(e))

except sr.UnknownValueError:
    print("unknown error occurred")
