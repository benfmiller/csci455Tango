import speech_recognition as sr
import pyttsx3
import re


class Listener:
    microphone: sr.Microphone
    listener: sr.Recognizer
    using_console = False

    def __init__(self, audio=True):
        if audio is True:
            with sr.Microphone() as source:
                self.speaker = source
                self.listener = sr.Recognizer()
                print("Adjusting to ambient noise")
                self.listener.adjust_for_ambient_noise(source, duration=2)
                self.listener.energy_threshold = 3000
                self.listener.dynamic_energy_threshold = True
        else:
            self.using_console = True

    def get_input(self):
        user_input = ""
        while user_input == "":
            if self.using_console is True:
                user_input = input("Human: ").lower()
            try:
                print("listening")
                audio = self.listener.listen(self.microphone)
                print("Got audio")
                words = self.listener.recognize_google(audio)
                if isinstance(words, str):
                    words = words.lower()
                user_input = words
            except sr.UnknownValueError:
                print("Unrecognized word")
        print(f'User Input: "{user_input}"')
        return user_input


class Speaker:
    engine: pyttsx3.Engine
    using_console = False

    def __init__(self, audio=True) -> None:
        if audio is True:
            voices = self.engine.getProperty("voices")
            self.engine = pyttsx3.init()
            # TODO
            # i corresponds with the voice type
            # we'll need to figure out which voice to use and the rate
            i = 10
            self.engine.setProperty("voice", voices[i].id)
            print(f'Using voice: {self.engine.getProperty("voice")}')
            self.engine.setProperty("rate", 150)
        else:
            self.using_console = True

    def output(self, output: str):
        if self.using_console is True:
            self.engine.say(output)
            self.engine.runAndWait()
        print(f"Robot: {output}")


class DocumentNode:
    string: str

    def __init__(self, document_line: str) -> None:
        self.string = document_line


class Document:
    contents: list[str]
    root_node: DocumentNode

    def __init__(self, document_file: str = "") -> None:
        if document_file == "":
            print("No file to read")
            self.contents = []
        else:
            with open(document_file) as f:
                self.contents = f.readlines()
        self.parse_contents()

    def parse_contents(self) -> None:
        # TODO:
        lines_builder = []
        for line in self.contents:
            line = line.strip()
            if len(line) > 0:
                if line[0] == "#":
                    continue
                lines_builder += [line]

        print(lines_builder)


class DialogBot:
    listener: Listener
    speaker: Speaker
    document: Document

    def __init__(
        self, listener: Listener, speaker: Speaker, document: Document
    ) -> None:
        pass
        self.listener = listener
        self.speaker = speaker
        self.document = document

    def run(self) -> None:
        # TODO
        pass


if __name__ == "__main__":
    listener = Listener(audio=False)
    speaker = Speaker(audio=False)
    document = Document("dialog/test_file1.txt")
    dialog_bot = DialogBot(listener, speaker, document)
    dialog_bot.run()
