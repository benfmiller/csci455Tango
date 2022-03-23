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
            "read": self.robot.turnWaistRight,
            "red": self.robot.turnWaistRight,
            "blue": self.robot.turnWaistLeft,
            "apple": self.robot.turnHeadRight,
            "orange": self.robot.turnHeadLeft,
            "mango": self.robot.tiltHeadUp,
            "banana": self.robot.tiltHeadDown,
        }

    def getWords(self) -> str:
        with sr.Microphone() as source:
            # print(source)
            r = sr.Recognizer()
            r.adjust_for_ambient_noise(source)
            r.dyanmic_energythreshhold = 3000

            try:
                print("listening")
                audio = r.listen(source)
                print("Got audio")
                words: str = r.recognize_google(audio)
                words = words.lower()
                print(words)
                return words

            except sr.UnknownValueError:
                print("Unrecognized word")
                return ""

    def run(self):
        while True:
            """
            words = self.getWords()
            print("heard commands: " + words)
            if words in self.commands.keys():
                self.commands.get(words)()
            else:
                word_list = words.split()
                for w in word_list:
                    try:
                        self.commands.get(w)()
                    except Exception as e:
                        print("Don't know that command")
            # Above works iff multi word commands are the only thing in 'words'
            # Below is in progress to handle more cases
            """
            words = self.getWords()
            word_list = words.split()
            print(word_list)
            while len(word_list) > 0:
                try:
                    first = word_list.pop(0)
                    if first in self.commands.keys():
                        self.commands.get(first)()
                    else:
                        second = word_list[0]
                        poss_command = first + " " + second
                        if poss_command in self.commands.keys():
                            self.commands.get(poss_command)()
                except Exception as e:
                    print(e)
                    break


with Tango() as tango:
    voice = VoiceControl(tango)
    voice.run()
