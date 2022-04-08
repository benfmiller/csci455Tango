from black import out
import speech_recognition as sr
import pyttsx3
import re
import csv
import string
import random
from pprint import pprint


class Listener:  # input
    microphone: sr.Microphone
    listener_rec: sr.Recognizer
    using_console = False

    def __init__(self, audio=True):
        if audio is True:
            with sr.Microphone() as source:
                self.speaker = source
                self.listener_rec = sr.Recognizer()
                print("Adjusting to ambient noise")
                self.listener_rec.adjust_for_ambient_noise(source, duration=2)
                self.listener_rec.energy_threshold = 3000
                self.listener_rec.dynamic_energy_threshold = True
        else:
            self.using_console = True

    def get_input(self):
        user_input = ""
        while user_input == "":
            if self.using_console is True:
                user_input = input("Human: ").lower()
            else:
                try:
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
        if self.using_console is False:
            self.engine.say(output)
            self.engine.runAndWait()
        print(f"Robot: {output}")


class DocumentNode:
    doc_line: str
    good_line: bool = True
    level: int
    inputs: list[str]
    outputs: list[str]
    child_nodes: list[any]
    parent_nodes: list[any]

    def __init__(self, document_line: str) -> None:
        self.doc_line = document_line
        self.child_nodes = []
        self.parent_nodes = []
        self.parse_line()

    def parse_line(self):
        line = self.doc_line.lower()
        if line[0] != "u":
            print(f"Error: line must start with 'u': {line}")
        if line[1] not in string.digits:
            line = "u0" + line[1:]
        try:
            self.level = int(line[1 : line.index(":")])
        except Exception as e:
            print(f"Illegal level in {self.doc_line}")
            self.good_line = False

        if line.count(":") != 2:
            print(f"Improper syntax, needs two ':' in {self.doc_line}")
            self.good_line = False
            return
        line = line[line.index(":") + 1 :]
        inputs = line[: line.index(":")]
        outputs = line[line.index(":") + 1 :]
        if "_" in line:
            if "$" not in line:
                print(f"Error: variable in input requires variable in output: {line}")
                self.good_line = False
                return
        self.parse_inputs(inputs)
        self.parse_outputs(outputs)

    def parse_inputs(self, inputs: str):
        inputs = inputs.strip()
        if inputs[0] not in "([":
            print(f"Error: bad inputs in {self.doc_line}")
            self.good_line = False
            return
        if inputs[0] == "(":
            assert inputs[-1] == ")"  # matching "()"
            inputs = inputs[1:-1]
            self.inputs = [inputs]
        elif inputs[0] == "[":
            assert inputs[-1] == "]"  # matching "()"
            inputs = inputs[1:-1]
            if "," not in inputs:
                csv_reader = csv.reader([inputs], delimiter=" ")
            else:
                csv_reader = csv.reader([inputs], delimiter=",")
            inputs_list = []
            for row in csv_reader:
                inputs_list = list(row)
                self.inputs = inputs_list
        else:
            print(f"Bad inputs format, need () or []: {self.doc_line}")
            self.good_line = False

    def parse_outputs(self, outputs: str):
        outputs = outputs.strip()
        if len(outputs) == 0:
            print(f"No outputs given: {self.doc_line}")
            self.good_line = False
            return
        if outputs[0] == "[":
            assert outputs[-1] == "]"  # matching "()"
            outputs = outputs[1:-1]
            if "," not in outputs:
                csv_reader = csv.reader([outputs], delimiter=" ")
            else:
                csv_reader = csv.reader([outputs], delimiter=",")
            outputs_list = []
            for row in csv_reader:
                outputs_list = list(row)
                self.outputs = outputs_list
        else:
            self.outputs = [outputs]

    def __repr__(self) -> str:
        return self.doc_line + ": " + len(self.child_nodes) + " child nodes"


class Document:
    contents: list[str]
    root_nodes: list[DocumentNode]
    variables: dict[str, list[str]]

    def __init__(self, document_file: str = "") -> None:
        if document_file == "":
            print("No file to read")
            self.contents = []
        else:
            with open(document_file) as f:
                self.contents = f.readlines()
        self.root_nodes = []
        self.variables = {}
        self.parse_contents()

    def parse_contents(self) -> None:
        """Parses all contents"""
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
        node_stack = []
        for line in self.contents:
            line_node = DocumentNode(line)
            if line_node.good_line is False:
                continue
            if len(self.root_nodes) == 0:
                if line_node.level != 0:
                    print(f"Error: First line level must be 0: {line}")
                    break
            if line_node.level == 0:
                self.root_nodes += [line_node]
                node_stack = []
            elif line_node.level > node_stack[-1].level + 1:
                print(
                    f"Error: skip in line level from {node_stack[-1]} to {line_node.level}: {line_node.doc_line}"
                )
            elif line_node.level == node_stack[-1].level + 1:
                node_stack[-1].child_nodes += [line_node]
            elif line_node.level == node_stack[-1].level:
                node_stack.pop()
                node_stack[-1].child_nodes += [line_node]
                # node_stack[-1].child_nodes += [line_node]
            else:
                while line_node.level != node_stack[-1]:
                    node_stack.pop()
                node_stack.pop()
                node_stack[-1].child_nodes += [line_node]
            node_stack += [line_node]


class DialogBot:
    listener: Listener
    speaker: Speaker
    document: Document
    active_nodes: list[DocumentNode]
    active_variables = {"_": False}
    variables: dict[str, str] = {}
    level: int

    def __init__(
        self, listener: Listener, speaker: Speaker, document: Document
    ) -> None:
        self.listener = listener
        self.speaker = speaker
        self.document = document

    def run(self) -> None:
        # TODO

        self.active_nodes = self.document.root_nodes
        if len(self.active_nodes) == 0:
            print("No root nodes from document!")
            return
        self.level = 0
        while True:
            # document root nodes are active
            # Get input, compare it to inputs in each active node
            # if it matches, we "speak" output
            # Deactivate parent parent nodes and current node, activate subnodes
            # Handle variables
            input_encountered = False
            _input = self.listener.get_input()
            if _input == "bye":
                self.speaker.output("Goodbye Gator")
                break
            for node in self.active_nodes:
                for input_option in node.inputs:
                    if "_" in input_option:
                        shortened_input = input_option[: input_option.index("_")]
                        if shortened_input in _input:
                            # We have a match!
                            index = _input.index(shortened_input)
                            after_underscore = _input[index + len(shortened_input) :]
                            print(after_underscore)
                            after_underscore_list = after_underscore.strip().split()
                            if len(after_underscore_list) == 0:
                                # no variable, so wasn't a true match
                                continue
                            variable = after_underscore_list[0]
                            self.set_variable(variable, node)
                            self.matched_node(node)
                            input_encountered = True
                            break

                        self.active_variables["_"] = True
                    else:
                        if input_option in _input:
                            # We have a match!
                            self.matched_node(node)
                            input_encountered = True
                            break
            if input_encountered == False:
                print("no input matched with dialog")

    def matched_node(self, node: DocumentNode):
        output_index = random.randint(0, len(node.outputs) - 1)
        output = node.outputs[output_index]
        for var_name, value in self.variables.items():
            if var_name in output:
                output = output.replace(var_name, value)
                break
        self.speaker.output(output)
        self.active_nodes = node.child_nodes

    def set_variable(self, variable: str, node: DocumentNode):
        for output in node.outputs:
            if "$" in output:
                after_dollar = output[output.index("$") :]
                assert (
                    len(after_dollar) > 0
                )  # There has to be a variable name to store into
                var_name = after_dollar.strip().split()[0]
                self.variables[var_name] = variable
                return
        print("Error: variable retrieved from input but no name to match")


if __name__ == "__main__":
    listener = Listener(audio=False)
    speaker = Speaker(audio=True)
    document = Document("dialog/test_file1.txt")
    dialog_bot = DialogBot(listener, speaker, document)
    dialog_bot.run()
