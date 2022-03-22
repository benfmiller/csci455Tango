import speech_recognition as sr
from Robot import Tango
from functools import partial


# for index, name in enumerate(sr.Microphone.list_microphone_names()):
#     print(
#         'Microphone with name "{1}" found for `Microphone(device_index={0})`'.format(
#             index, name
#         )
#     )


class VoiceControl:
    def __init__(self, robot: Tango) -> None:
        self.robot = robot

        self.commands = {
            "stop": self.robot.stop,
            "forward": partial(self.robot.forward, duration=0.2),
            "backward": partial(self.robot.backward, duration=0.2),
            "right": self.robot.turnRight,
            "left": self.robot.turnLeft,
            "neutral": self.robot.neutral,
        }

    def getWords(self):
        with sr.Microphone() as source:
            print(source)
            r = sr.Recognizer()
            r.adjust_for_ambient_noise(source)
            r.dyanmic_energythreshhold = 3000

            try:
                print("listening")
                audio = r.listen(source)
                print("Got audio")
                words = r.recognize_google(audio)
                print(words)
                return words

            except sr.UnknownValueError:
                print("Unrecognized word")
                return "Unrecognized word"

    def run(self):
        while True:
            words = self.getWords()
            word_list = words.split()
            for w in word_list:
                try:
                    self.commands.get(w)
                except Exception as e:
                    print("Don't know that command")


with Tango() as tango:
    voice = VoiceControl(tango)
    voice.run()
