import time
from kivy.core.image import Image
import pyttsx3
import speech_recognition as sr
from kivy.app import App
from kivy.uix.widget import Widget
from kivy.uix.behaviors import DragBehavior
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.button import Button
import kivy.uix.button
from kivy.properties import BooleanProperty, ListProperty
from kivy.animation import Animation
from kivy.uix.vkeyboard import VKeyboard
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.bubble import Bubble, BubbleButton
from kivy.uix.textinput import TextInput
from kivy.core.window import Window

actually_speak = False
actually_listen = False
actually_move = False

if actually_move:
    from robot import Tango

    root_robot = Tango()
    time.sleep(0.2)
    root_robot.forward()
    time.sleep(0.05)
    root_robot.stop()
    time.sleep(0.2)
    root_robot.neutral()

else:
    root_robot = None


class Speaker:  # output
    engine: pyttsx3.Engine
    using_console = False

    def __init__(self) -> None:
        if actually_speak is True:
            self.engine = pyttsx3.init()
            voices = self.engine.getProperty("voices")
            # i corresponds with the voice type
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


class ActionWidge(DragBehavior, Button):
    dragging = BooleanProperty(False)
    original_pos = ListProperty()
    after_delay = 0.2

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.delay_input = TextInput()
        self.delay_input.input_type = "number"
        self.delay_input.text = "0.3"
        # self.delay_input.size_hint_y = 0.4

        self.delay_block = BoxLayout()
        self.delay_block.orientation = "vertical"
        label = Label()
        label.text = "After Delay Seconds"
        label.size_hint_y = 0.2
        # image_button = ImageButton("./assets/settingsICONS/delayICON.png")
        # image_button.size_hint_min_y = 0.3
        self.delay_block.add_widget(label)
        self.delay_block.add_widget(self.delay_input)
        # self.delay_block.add_widget(image_button)

    def on_touch_down(self, touch):
        if self.collide_point(*touch.pos):
            print("on touch down")
            self.original_pos = self.pos
        return super().on_touch_down(touch)

    def on_touch_move(self, touch):
        if touch.grab_current is self:
            self.opacity = 0.4
            self.dragging = True
        return super().on_touch_move(touch)

    def collide_widget(self, wid):
        if abs(self.center_x - wid.center_x) < wid.width / 2:
            if self.top < wid.y:
                return False
            if self.y > wid.top:
                return False
            return True
        return False

    def on_touch_up(self, touch):
        app = App.get_running_app()
        # print(app.root.ids)
        if self.dragging:
            self.opacity = 1
            self.dragging = False
            for place_widge in app.root.ids.placeHolderLayout.children:
                if self.collide_widget(place_widge):
                    place_widge.set_action(self)
            anim = Animation(pos=self.original_pos, duration=0.0)
            anim.start(self)
            return super().on_touch_up(touch)

    def activate(self) -> None:
        print("Base Button Activated")

    def set_settings_title(self):
        app = App.get_running_app()
        app.root.ids.settingsTitleText.text = self.get_class_name()
        app.root.ids.settingsTitleImage.background_normal = self.background_normal
        app.root.ids.settingsTitleImage.background_color = (1, 1, 1, 1)

    def set_settings(self, settings_layout: BoxLayout):
        self.set_settings_title()
        newButton = Button()
        newButton.text = "Nothing to do here!\nI'm a base button!"
        settings_layout.add_widget(newButton)

    def __str__(self) -> str:
        return "Base Action Widge" + super().__str__()

    def get_class_name(self) -> str:
        return str(str(self.__class__).split(".")[-1])[:-2]


# ------------------------------------------------------------------------------


class DriveWidge(ActionWidge):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.speed_widge = TextInput()
        self.speed_widge.input_type = "number"
        self.speed_widge.text = "0"
        self.duration_widge = TextInput()
        self.duration_widge.input_type = "number"
        self.duration_widge.text = "2"
        self.inner_layout = self.build_settings()

    def __str__(self) -> str:
        str(self.__class__).split(".")[-1]
        return f"{self.get_class_name()}: speed {self.speed_widge.text}: seconds {self.duration_widge.text}: after_delay {self.delay_input.text}"

    def build_settings(self):
        inner_layout = BoxLayout()

        block1 = BoxLayout()
        block1.orientation = "vertical"
        block1.size_hint_x = 0.3
        label = Label()
        label.text = "Speed [-3, 3] int"
        label.size_hint_y = 0.2

        block1.add_widget(label)
        block1.add_widget(self.speed_widge)

        block2 = BoxLayout()
        block2.orientation = "vertical"
        block2.size_hint_x = 0.3
        label = Label()
        label.text = "Duration Seconds float"
        label.size_hint_y = 0.2

        block2.add_widget(label)
        block2.add_widget(self.duration_widge)

        inner_layout.add_widget(block1)
        inner_layout.add_widget(block2)
        self.delay_block.size_hint_x = 0.3
        inner_layout.add_widget(self.delay_block)
        return inner_layout

    def set_settings(self, settings_layout: BoxLayout):
        self.set_settings_title()
        settings_layout.add_widget(self.inner_layout)

    def activate(self) -> None:
        print("Driving")
        if actually_move:
            position = int(self.speed_widge.text)
            while position < 0:
                root_robot.forward()
                time.sleep(0.05)
                position += 1
            while position > 0:
                root_robot.backward()
                time.sleep(0.05)
                position -= 1
        time.sleep(float(self.duration_widge.text))
        if actually_move:
            root_robot.stop()
        time.sleep(float(self.delay_input.text))


# ------------------------------------------------------------------------------


class TurnWidge(ActionWidge):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.speed_widge = TextInput()
        self.speed_widge.input_type = "number"
        self.speed_widge.text = "0"
        self.duration_widge = TextInput()
        self.duration_widge.input_type = "number"
        self.duration_widge.text = "2"
        self.inner_layout = self.build_settings()

    def __str__(self) -> str:
        str(self.__class__).split(".")[-1]
        return f"{self.get_class_name()}: speed {self.speed_widge.text}: seconds {self.duration_widge.text}: after_delay {self.delay_input.text}"

    def build_settings(self):
        inner_layout = BoxLayout()

        block1 = BoxLayout()
        block1.orientation = "vertical"
        block1.size_hint_x = 0.3
        label = Label()
        label.text = "Speed [-3, 3] int"
        label.size_hint_y = 0.2

        block1.add_widget(label)
        block1.add_widget(self.speed_widge)

        block2 = BoxLayout()
        block2.orientation = "vertical"
        block2.size_hint_x = 0.3
        label = Label()
        label.text = "Duration Seconds float"
        label.size_hint_y = 0.2

        block2.add_widget(label)
        block2.add_widget(self.duration_widge)

        inner_layout.add_widget(block1)
        inner_layout.add_widget(block2)
        self.delay_block.size_hint_x = 0.3
        inner_layout.add_widget(self.delay_block)
        return inner_layout

    def set_settings(self, settings_layout: BoxLayout):
        self.set_settings_title()
        settings_layout.add_widget(self.inner_layout)

    def activate(self) -> None:
        print("Turning")
        if actually_move:
            position = int(self.speed_widge.text)
            while position < 0:
                root_robot.turnRight()
                time.sleep(0.05)
                position += 1
            while position > 0:
                root_robot.turnLeft()
                time.sleep(0.05)
                position -= 1
        time.sleep(float(self.duration_widge.text))
        if actually_move:
            root_robot.stop()
        time.sleep(float(self.delay_input.text))


# ------------------------------------------------------------------------------


class HeadTiltWidge(ActionWidge):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.position_widge = TextInput()
        self.position_widge.input_type = "number"
        self.position_widge.text = "0"
        self.duration_widge = TextInput()
        self.duration_widge.input_type = "number"
        self.duration_widge.text = "1"
        self.inner_layout = self.build_settings()

    def __str__(self) -> str:
        str(self.__class__).split(".")[-1]
        return f"{self.get_class_name()}: position {self.position_widge.text}: seconds {self.duration_widge.text}: after_delay {self.delay_input.text}"

    def build_settings(self):
        inner_layout = BoxLayout()

        block1 = BoxLayout()
        block1.orientation = "vertical"
        block1.size_hint_x = 0.3
        label = Label()
        label.text = "Position [-2, 2] int"
        label.size_hint_y = 0.2

        block1.add_widget(label)
        block1.add_widget(self.position_widge)

        block2 = BoxLayout()
        block2.orientation = "vertical"
        block2.size_hint_x = 0.3
        label = Label()
        label.text = "Duration Seconds float\nLeave at 0 to stay in position"
        label.size_hint_y = 0.2

        block2.add_widget(label)
        block2.add_widget(self.duration_widge)

        inner_layout.add_widget(block1)
        inner_layout.add_widget(block2)
        self.delay_block.size_hint_x = 0.3
        inner_layout.add_widget(self.delay_block)
        return inner_layout

    def set_settings(self, settings_layout: BoxLayout):
        self.set_settings_title()
        settings_layout.add_widget(self.inner_layout)

    def activate(self) -> None:
        print("Tilting Head")
        if actually_move:
            position = int(self.position_widge.text)
            while position < 0:
                root_robot.tiltHeadDown()
                time.sleep(0.05)
                position += 1
            while position > 0:
                root_robot.tiltHeadUp()
                time.sleep(0.05)
                position -= 1
        time.sleep(float(self.duration_widge.text))
        if self.delay_input.text == "0" and actually_move:
            root_robot.neutral()
        time.sleep(float(self.delay_input.text))


# ------------------------------------------------------------------------------


class HeadTurnWidge(ActionWidge):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.position_widge = TextInput()
        self.position_widge.input_type = "number"
        self.position_widge.text = "0"
        self.duration_widge = TextInput()
        self.duration_widge.input_type = "number"
        self.duration_widge.text = "1"
        self.inner_layout = self.build_settings()

    def __str__(self) -> str:
        str(self.__class__).split(".")[-1]
        return f"{self.get_class_name()}: position {self.position_widge.text}: seconds {self.duration_widge.text}: after_delay {self.delay_input.text}"

    def build_settings(self):
        inner_layout = BoxLayout()

        block1 = BoxLayout()
        block1.orientation = "vertical"
        block1.size_hint_x = 0.3
        label = Label()
        label.text = "Position [-2, 2] int"
        label.size_hint_y = 0.2

        block1.add_widget(label)
        block1.add_widget(self.position_widge)

        block2 = BoxLayout()
        block2.orientation = "vertical"
        block2.size_hint_x = 0.3
        label = Label()
        label.text = "Duration Seconds float\nLeave at 0 to stay in position"
        label.size_hint_y = 0.2

        block2.add_widget(label)
        block2.add_widget(self.duration_widge)

        inner_layout.add_widget(block1)
        inner_layout.add_widget(block2)
        self.delay_block.size_hint_x = 0.3
        inner_layout.add_widget(self.delay_block)
        return inner_layout

    def set_settings(self, settings_layout: BoxLayout):
        self.set_settings_title()
        settings_layout.add_widget(self.inner_layout)

    def activate(self) -> None:
        print("Turning Head")
        if actually_move:
            position = int(self.position_widge.text)
            while position < 0:
                root_robot.turnHeadLeft()
                time.sleep(0.05)
                position += 1
            while position > 0:
                root_robot.turnHeadRight()
                time.sleep(0.05)
                position -= 1
        time.sleep(float(self.duration_widge.text))
        if self.delay_input.text == "0" and actually_move:
            root_robot.neutral()
        time.sleep(float(self.delay_input.text))


# ------------------------------------------------------------------------------


class WaistWidge(ActionWidge):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.position_widge = TextInput()
        self.position_widge.input_type = "number"
        self.position_widge.text = "0"
        self.duration_widge = TextInput()
        self.duration_widge.input_type = "number"
        self.duration_widge.text = "1"
        self.inner_layout = self.build_settings()

    def __str__(self) -> str:
        str(self.__class__).split(".")[-1]
        return f"{self.get_class_name()}: position {self.position_widge.text}: seconds {self.duration_widge.text}: after_delay {self.delay_input.text}"

    def build_settings(self):
        inner_layout = BoxLayout()

        block1 = BoxLayout()
        block1.orientation = "vertical"
        block1.size_hint_x = 0.3
        label = Label()
        label.text = "Position [-1, 1] int"
        label.size_hint_y = 0.2

        block1.add_widget(label)
        block1.add_widget(self.position_widge)

        block2 = BoxLayout()
        block2.orientation = "vertical"
        block2.size_hint_x = 0.3
        label = Label()
        label.text = "Duration Seconds float\nLeave at 0 to stay in position"
        label.size_hint_y = 0.2

        block2.add_widget(label)
        block2.add_widget(self.duration_widge)

        inner_layout.add_widget(block1)
        inner_layout.add_widget(block2)
        self.delay_block.size_hint_x = 0.3
        inner_layout.add_widget(self.delay_block)
        return inner_layout

    def set_settings(self, settings_layout: BoxLayout):
        self.set_settings_title()
        settings_layout.add_widget(self.inner_layout)

    def activate(self) -> None:
        print("Moving waist")
        if actually_move:
            position = int(self.position_widge.text)
            if position == -1:
                root_robot.turnWaistLeft()
            elif position == 1:
                root_robot.turnWaistRight()
        time.sleep(float(self.duration_widge.text))
        if self.delay_input.text == "0" and actually_move:
            root_robot.neutral()
        time.sleep(float(self.delay_input.text))


# ------------------------------------------------------------------------------


class InputWidge(ActionWidge):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.input_widge = TextInput()
        self.input_widge.text = "continue"
        self.inner_layout = self.build_settings()

    def __str__(self) -> str:
        str(self.__class__).split(".")[-1]
        return f"{self.get_class_name()}: Listening for '{self.input_widge.text}': after_delay {self.delay_input.text}"

    def build_settings(self):
        inner_layout = BoxLayout()

        block = BoxLayout()
        block.size_hint_x = 0.6
        block.orientation = "vertical"
        label = Label()
        label.text = "Input text to speak"
        label.size_hint_y = 0.2
        block.add_widget(label)
        block.add_widget(self.input_widge)

        inner_layout.add_widget(block)
        self.delay_block.size_hint_x = 0.4
        inner_layout.add_widget(self.delay_block)
        return inner_layout

    def set_settings(self, settings_layout: BoxLayout):
        self.set_settings_title()
        settings_layout.add_widget(self.inner_layout)

    def activate(self) -> None:
        print("Listening")
        if actually_listen:
            with sr.Microphone() as source:
                r = sr.Recognizer()
                r.adjust_for_ambient_noise(source)
                r.energy_threshold = 3000
                r.dynamic_energy_threshold = True
                words = ""
                while True:
                    try:
                        print("listening")
                        audio = r.listen(source)
                        print("Got audio")
                        words = r.recognize_google(audio)
                        print(words)
                    except sr.UnknownValueError:
                        print("Don't know that word")
                    if self.input_widge.text.lower() in words:
                        break
        else:
            print("command line input not working?")
            # while True:
            #     words = input()
            #     if self.input_widge.text.lower() in words:
            #         print("Words accepted!")
            #         break
        print("Words accepted!")
        time.sleep(float(self.delay_input.text))


# ------------------------------------------------------------------------------


class OutputWidge(ActionWidge):
    my_speaker = Speaker()

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.output_widge = TextInput()
        self.output_widge.text = "I have nothing to say"
        self.inner_layout = self.build_settings()

    def __str__(self) -> str:
        str(self.__class__).split(".")[-1]
        return f"{self.get_class_name()}: Will say '{self.output_widge.text}': after_delay {self.delay_input.text}"

    def build_settings(self):
        # VKeyboard.layout = "numeric"
        # player = VKeyboard()
        # player.type
        inner_layout = BoxLayout()

        block = BoxLayout()
        block.size_hint_x = 0.6
        block.orientation = "vertical"
        label = Label()
        label.text = "Input text to speak"
        label.size_hint_y = 0.2
        block.add_widget(label)
        block.add_widget(self.output_widge)

        inner_layout.add_widget(block)
        self.delay_block.size_hint_x = 0.4
        inner_layout.add_widget(self.delay_block)
        return inner_layout

    def set_settings(self, settings_layout: BoxLayout):
        self.set_settings_title()
        settings_layout.add_widget(self.inner_layout)

    def activate(self) -> None:
        print("Speaking")
        self.my_speaker.output(self.output_widge.text)
        time.sleep(float(self.delay_input.text))
