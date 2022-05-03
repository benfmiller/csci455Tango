import speech_recognition as sr
import pyttsx3


class Listener:  # input
    microphone: sr.Microphone
    listener_rec: sr.Recognizer
    using_console = False

    def __init__(self, audio=True):
        if audio is True:
            pass
        else:
            self.using_console = True

    def get_input(self):
        user_input = ""
        while user_input == "":
            if self.using_console is True:
                user_input = input("Human: ").lower()
            else:
                try:
                    with sr.Microphone() as source:
                        self.microphone = source
                        self.listener_rec = sr.Recognizer()
                        print("Adjusting to ambient noise")
                        self.listener_rec.adjust_for_ambient_noise(source, duration=0.1)
                        self.listener_rec.energy_threshold = 3000
                        self.listener_rec.dynamic_energy_threshold = True
                        print("listening")
                        audio = self.listener_rec.listen(self.microphone)
                        print("Got audio")
                        words = self.listener_rec.recognize_google(audio)
                        if isinstance(words, str):
                            words = words.lower()
                        user_input = words
                except sr.UnknownValueError:
                    print("Unrecognized word")
        print(f'User Input: "{user_input}"')
        return user_input


class Speaker:  # output
    engine: pyttsx3.Engine
    using_console = False

    def __init__(self, audio=True) -> None:
        if audio is True:
            self.engine = pyttsx3.init()
            voices = self.engine.getProperty("voices")
            # i corresponds with the voice type
            # we'll need to figure out which voice to use and the rate
            i = 11
            self.engine.setProperty("voice", voices[i].id)
            print(f'Using voice: {self.engine.getProperty("voice")}')
            self.engine.setProperty("rate", 200)
        else:
            self.using_console = True

    def output(self, output: str):
        if self.using_console is False:
            self.engine.say(output)
            self.engine.runAndWait()
        print(f"Robot: {output}")
