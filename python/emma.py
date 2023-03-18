import speech_recognition as sr
import pyttsx3

elevator_name=["EMMA"]
instructions = ["CANCEL", "TAKE"]
destinations = ["GROUND FLOOR", "FIRST", "SECOND", "THIRD", "FOURTH", "FIFTH"]


# Convert text to speech
def speak_text(engine, command):
    engine.say(command)
    engine.runAndWait()
    engine.stop()


def loop(sr, engine):
    sr.Recognizer()
    # wait for stimullus (message from face recognizer )
    while(True): # while stimmulus = true 
        interact(sr, engine, elevator_name) #Greetings
 
        #check for message from elevator saying he reached the destination and left -> stimullus = false

def wordInSpeech(keyword, speech):
    print(speech)
    if keyword in speech:  
        return True;
    else:
        return False
    

def getInstructionType(speech):
    print(speech)
    asked_instructions = []
    for ins in instructions:
        if ins in speech:
            asked_instructions.append(ins)
    return asked_instructions


def getDestination(speech):
    for word in speech.split("TAKE")[1]:
        if word in destinations:
            return word
    return "None"

def listenForCall(mic, engine, response, idle_response):
    with sr.Microphone() as source:
        called = False
        while not called:
            print("Start Greeting fase")
            audio = mic.listen(source)
            try:
                text = mic.recognize_google(audio, language='en-US')
                if wordInSpeech(elevator_name[0], text.upper()):
                    speak_text(engine, response)
                    called = True
                else:
                    print("EMMA not detected.")
            except sr.UnknownValueError:
                speak_text(engine, idle_response)
                print("Google Speech Recognition could not understand audio")

def interact(mic, engine):
    with sr.Microphone() as source:
        
        endedGreetings = False

        rideOnGoing = True

        listenForCall(mic, engine, response="Hello! Which floor would you like to go?", idle_response="Hey, if you're speaking i cant understand you")

        print("Start Instruction Fase")
        
        while rideOnGoing: #Esta variavel vai ser mudada por que controlar os temporizadores
            audio = mic.listen(source)
            try:
                text = mic.recognize_google(audio, language='en-US')
                print(text)

                
                givenInstructions = getInstructionType(text.upper());
                if len(givenInstructions) == 0:
                    speak_text(engine, "GUESS I DONT KNOW WHAT TO DO")
                else:
                    for ins in givenInstructions:
                        if ins == instructions[0]:
                            #TODO: NEEDS TO CHECK THE DESTINATION WAS THERE TO BEGIN WITH
                            # send signal to cancel the current destination
                            speak_text(engine, "Removing Destination")
                            pass
                        elif ins == instructions[1]:
                            speak_text(engine, "Adding new Destination")
                            newDestination = getDestination(text.upper())
                            #send signal about new destination
                            print(newDestination)
                            pass

            except sr.UnknownValueError:
                speak_text(engine, "Hey, if you're speaking i cant understand you")
                print("Google Speech Recognition could not understand audio")

            listenForCall(mic, engine, "yes?", "")



if __name__ == '__main__':
    r = sr.Recognizer()
    engine = pyttsx3.init()
    engine.setProperty('voice', engine.getProperty('voices')[1].id)
    interact(r, engine)

