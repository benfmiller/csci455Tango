import speech_recognition as sr
import pyttsx3
import re
import csv
import string


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
    doc_line: str
    good_line: bool = True

    def __init__(self, document_line: str) -> None:
        self.doc_line = document_line
        self.parse_line()

    def parse_line(self):
        line = self.doc_line
        if line[0] != "u":
            print(f"Error: line must start with 'u': {line}")
        if line[1] not in string.digits:
            line = "u0" + line[1:]
        # TODO:


class Document:
    contents: list[str]
    root_nodes: list[DocumentNode]
    variables: dict[str, list[str]] = {}

    def __init__(self, document_file: str = "") -> None:
        if document_file == "":
            print("No file to read")
            self.contents = []
        else:
            with open(document_file) as f:
                self.contents = f.readlines()
        self.parse_contents()

    def parse_contents(self) -> None:
        lines_builder = []
        for line in self.contents:
            line = line.strip()
            if len(line) > 0:
                if line[0] == "#":
                    continue
                if line[0] == "~":
                    variable, value = self.parse_var_line(line)
                    if variable is not None and value is not None:
                        self.variables[variable] = value
                    continue
                lines_builder += [line]
        lines_builder_var_parsed = []
        for line in lines_builder:
            if "~" in line:
                for variable, value in self.variables.items():
                    if variable in line:
                        line = line.replace(variable, "[" + ",".join(value) + "]")
                if "([" in line and "])" in line:
                    line = line.replace("([", "[")
                    line = line.replace("])", "]")

                if "~" in line:
                    print(f"Error: unmatches variables in {line}")
                else:
                    lines_builder_var_parsed += [line]
            else:
                lines_builder_var_parsed += [line]
        self.contents = lines_builder_var_parsed
        self.build_tree()

    def parse_var_line(self, line: str) -> tuple[str, list[str]]:
        variable = line[0 : line.index(":")]
        var_val = line[line.index(":") + 1 :]
        var_val = var_val.strip()
        var_val = var_val[1:-1]
        csv_reader = csv.reader([var_val], delimiter=" ")
        var_val_list = []
        for row in csv_reader:
            var_val_list = list(row)
        return (variable, var_val_list)

    def build_tree(self) -> None:
        # TODO:
        last_level = 0

        for line in self.contents:
            line_node = DocumentNode(line)
            if line_node.good_line is False:
                continue

            # if int(line[1]) == last_level +1:

        _ = [print(x) for x in self.contents]


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
