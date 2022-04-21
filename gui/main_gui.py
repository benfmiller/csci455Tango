#!/usr/bin/env python3


import time
from kivy.app import App
from kivy.uix.widget import Widget

# from kivy.properties import NumericProperty, ReferenceListProperty
# from kivy.vector import Vector
from kivy.uix.behaviors import DragBehavior

# from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.boxlayout import BoxLayout

# from kivy.uix.gridlayout import GridLayout

# from kivy.uix.label import Label
from kivy.uix.button import Button


# Simple drag from a boxlayout onto a drop zone, animate the return if the drop zone is missed.
from kivy.properties import BooleanProperty, ListProperty
from kivy.animation import Animation
from kivy.uix.vkeyboard import VKeyboard
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.bubble import Bubble, BubbleButton

from kivy.uix.textinput import TextInput
from kivy.config import Config

Config.set("kivy", "keyboard_mode", "systemandmulti")

# 1. Motors with speed, time and direction.
# 2. Motors turn robot left, or right for x amount of seconds.
# 3. Head tilt both directions
# 4. Head pan both directions
# 5. Waist turn both directions
# 6. A wait for human speech input
# 7. Talking, be able to type in what sentence you want to say and the robot says it.

num_placeholders = 8
categories = {
    "drive": [],
    "turn": [],
    "head_tilt": [],
    "head_turn": [],
    "waist_turn": [],
    "input": [],
    "speak": [],
}
actually_speak = False
actually_listen = False
actually_move = False


class Speaker:  # output
    engine: pyttsx3.Engine
    using_console = False

    def __init__(self, audio=True) -> None:
        if audio is True:
            self.engine = pyttsx3.init()
            voices = self.engine.getProperty("voices")
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
#             bubb_btn = CustomBubbleButton(text=str(x), font_name="arial-unicode-ms.ttf")
#             self.layout.add_widget(bubb_btn)


class ReturnButton(Button):
    def on_touch_down(self, touch):
        if self.collide_point(*touch.pos):
            print("Returning to Main Screen")
            app = App.get_running_app()
            app.root.current = "mainScreen"
        return super().on_touch_down(touch)


class ClearButton(Button):
    def on_touch_down(self, touch):
        if self.collide_point(*touch.pos):
            print("Clearing placeholders")
            app = App.get_running_app()
            num = len(app.root.ids.placeHolderLayout.children)
            for button in app.root.ids.placeHolderLayout.children:
                button.reset()
                button.text = str(num)
                num -= 1
        return super().on_touch_down(touch)


class ActivateButton(Button):
    running = False

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        # self.bind(on_press=self.callback)

    def on_touch_down(self, touch):
        if self.collide_point(*touch.pos) and not self.running:
            self.running = True
            print("\n********Activating setup********!")
            # time.sleep(0.05)

            app = App.get_running_app()
            # num = len(app.root.ids.placeHolderLayout.children)
            num = 1
            for button in app.root.ids.placeHolderLayout.children[::-1]:
                print(f"Running box {num}: category {button.action}")
                # temp_background = button.background_normal
                # button.background_normal = ""
                # button.background_color = (1.0, 1.0, 0.0, 1.0)
                if button.action is not None:
                    button.action.activate()
                # time.sleep(0.5)
                # button.background_color = (1.0, 1.0, 1.0, 1.0)
                # button.background_normal = temp_background
                num += 1
            print("********Activation Done********\n")
            self.running = False
        return super().on_touch_down(touch)


class ActionWidge(DragBehavior, Button):
    dragging = BooleanProperty(False)
    original_pos = ListProperty()
    after_delay = 0.2

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
        str(self.__class__).split(".")[-1]
        return f"{self.get_class_name()}: position {self.position}: seconds {self.duration}: after_delay {self.after_delay}"


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


class InputWidge(ActionWidge):
    input_string: str

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.input_string = "Nothing"

    def __str__(self) -> str:
        str(self.__class__).split(".")[-1]
        return f"{self.get_class_name()}: Wait for string '{self.input_string}': after_delay {self.after_delay}"


class OutputWidge(ActionWidge):
    output_string: str

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.output_string = "I have nothing to say"

    def __str__(self) -> str:
        str(self.__class__).split(".")[-1]
        return f"{self.get_class_name()}: Will say '{self.output_string}': after_delay {self.after_delay}"

    def set_settings(self, settings_layout: BoxLayout):
        # VKeyboard.layout = "numeric"
        # player = VKeyboard()
        # player.type
        newButton = Button()
        newButton.text = "Nothing to do here!\nI'm a base button!"
        settings_layout.add_widget(TextInput())

    def activate(self) -> None:
        # TODO: speak self.output_string
        return super().activate()


class PlaceHolderButton(Button):
    action = None

    def on_touch_down(self, touch):
        if self.collide_point(*touch.pos):
            print("I've been touched!")
            app = App.get_running_app()
            self.set_settings_screen()
            app.root.current = "settingsScreen"
        return super().on_touch_down(touch)

    def set_settings_screen(self):
        # TODO:
        app = App.get_running_app()
        settings_layout = app.root.ids.settingsLayout
        for widge in list(settings_layout.children):
            settings_layout.remove_widget(widge)

        if self.action is None:
            newButton = Button()
            newButton.text = "Nothing to do here!"
            settings_layout.add_widget(newButton)
        else:
            self.action.set_settings(settings_layout)

    def set_action(self, actionWidge: ActionWidge):
        self.action = actionWidge

        # TODO: add action images
        self.text = actionWidge.text
        # print(self.background_normal)
        # print(type(self.background_normal))
        self.background_normal = actionWidge.background_normal

    def reset(self):
        self.action = None
        self.attributes = None
        self.background_normal = "atlas://data/images/defaulttheme/button"


class TangoApp(App):
    title = "Group 26 Tango"

    def build(self):
        return super().build()


if __name__ == "__main__":
    TangoApp().run()
