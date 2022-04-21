import time
import pyttsx3
import speech_recognition as sr
from kivy.app import App
from kivy.uix.widget import Widget

# from kivy.properties import NumericProperty, ReferenceListProperty
# from kivy.vector import Vector
from kivy.uix.behaviors import DragBehavior

# from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.boxlayout import BoxLayout

# from kivy.uix.gridlayout import GridLayout

from kivy.uix.label import Label
from kivy.uix.button import Button


# Simple drag from a boxlayout onto a drop zone, animate the return if the drop zone is missed.
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


# class CustomBubbleButton(BubbleButton):
#     def add_text(self):
#         app = App.get_running_app()
#         index = app.root.text_input.cursor[0] - 1
#         if self.text != "⌫":
#             app.root.text_input.text = (
#                 app.root.text_input.text[: index + 1]
#                 + self.text
#                 + app.root.text_input.text[index + 1 :]
#             )
#             app.root.text_input.cursor = (index + 2, 0)
#         else:
#             app.root.text_input.text = (
#                 app.root.text_input.text[:index] + app.root.text_input.text[index + 1 :]
#             )
#             app.root.text_input.cursor = (index, 0)
#
#     pass
#
#
# class NumericKeyboard(Bubble):
#     def on_touch_up(self, touch):
#         app = App.get_running_app()
#         if not self.collide_point(*touch.pos) and not app.root.text_input.collide_point(
#             *touch.pos
#         ):
#             app.root.remove_widget(app.root.bubb)
#             app.root.text_input.focus = False
#             delattr(app.root, "bubb")
#
#     def __init__(self, **kwargs):
#         super(NumericKeyboard, self).__init__(**kwargs)
#         self.create_bubble_button()
#
#     def create_bubble_button(self):
#         numeric_keypad = ["7", "8", "9", "4", "5", "6", "1", "2", "3", ".", "0", "⌫"]
#         for x in numeric_keypad:
#             bubb_btn = CustomBubbleButton(text=str(x))
#             self.layout.add_widget(bubb_btn)
#
#
# class BubbleShowcase(FloatLayout):
#     def show_bubble(self, *l):
#         if not hasattr(self, "bubb"):
#             self.bubb = NumericKeyboard()
#             self.bubb.arrow_pos = "bottom_mid"
#             self.add_widget(self.bubb)
#


class ActionWidge(DragBehavior, Button):
    dragging = BooleanProperty(False)
    original_pos = ListProperty()
    after_delay = 0.2

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.delay_input = TextInput()
        self.delay_input.input_type = "number"
        self.delay_input.text = "0.3"

        self.delay_block = BoxLayout()
        self.delay_block.orientation = "vertical"
        label = Label()
        label.text = "After Delay Seconds"
        label.size_hint_y = 0.2
        self.delay_block.add_widget(label)
        self.delay_block.add_widget(self.delay_input)

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

    def set_settings(self, settings_layout: BoxLayout):
        newButton = Button()
        newButton.text = "Nothing to do here!\nI'm a base button!"
        settings_layout.add_widget(newButton)

    def __str__(self) -> str:
        return "Base Action Widge" + super().__str__()

    def get_class_name(self) -> str:
        return str(self.__class__).split(".")[-1]


# ------------------------------------------------------------------------------


class DriveWidge(ActionWidge):
    drive_speed: int
    duration: float

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.drive_speed = 0
        self.duration = 0

    def __str__(self) -> str:
        return f"{self.get_class_name()}: speed {self.drive_speed}: seconds {self.duration}: after_delay {self.after_delay}"

    def set_settings(self, settings_layout: BoxLayout):
        # VKeyboard.layout = "numeric"
        # player = VKeyboard()
        # player.type
        newButton = Button()
        newButton.text = "Nothing to do here!\nI'm a base button!"
        settings_layout.add_widget(TextInput())


# ------------------------------------------------------------------------------


class TurnWidge(ActionWidge):
    turn_speed: int
    duration: float

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.turn_speed = 0
        self.duration = 0

    def __str__(self) -> str:
        return f"{self.get_class_name()}: speed {self.turn_speed}: seconds {self.duration}: after_delay {self.after_delay}"


class HeadTiltWidge(ActionWidge):
    position: int
    duration: float

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.position = 0
        self.duration = 0

    def __str__(self) -> str:
        str(self.__class__).split(".")[-1][:-2]
        return f"{self.get_class_name()}: position {self.position}: seconds {self.duration}: after_delay {self.after_delay}"


# ------------------------------------------------------------------------------


class HeadTurnWidge(ActionWidge):
    position: int
    duration: float

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.position = 0
        self.duration = 0

    def __str__(self) -> str:
        str(self.__class__).split(".")[-1]
        return f"{self.get_class_name()}: position {self.position}: seconds {self.duration}: after_delay {self.after_delay}"


# ------------------------------------------------------------------------------


class WaistWidge(ActionWidge):
    position: int
    duration: float

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.position = 0
        self.duration = 0

    def __str__(self) -> str:
        str(self.__class__).split(".")[-1]
        return f"{self.get_class_name()}: speed {self.position}: seconds {self.duration}: after_delay {self.after_delay}"


# ------------------------------------------------------------------------------


class InputWidge(ActionWidge):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.input_widge = TextInput()
        self.input_widge.text = "nothing"
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
                        print("Words accepted!")
                        break
        else:
            return
            # while True:
            #     words = input()
            #     if self.input_widge.text.lower() in words:
            #         print("Words accepted!")
            #         break
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
        settings_layout.add_widget(self.inner_layout)

    def activate(self) -> None:
        print("Speaking")
        self.my_speaker.output(self.output_widge.text)
        time.sleep(float(self.delay_input.text))
