#!/usr/bin/env python3

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
    def on_touch_down(self, touch):
        if self.collide_point(*touch.pos):
            print("\n********Activating setup********!")
            app = App.get_running_app()
            # num = len(app.root.ids.placeHolderLayout.children)
            num = 1
            for button in app.root.ids.placeHolderLayout.children[::-1]:
                print(f"Running box {num}: category {button.action}")
                if button.action is not None:
                    button.action.activate()
                num += 1
            print("********Activation Done********\n")
        return super().on_touch_down(touch)


class ActionWidge(DragBehavior, Button):
    dragging = BooleanProperty(False)
    original_pos = ListProperty()

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
        return f"{self.get_class_name()}: speed {self.drive_speed}: seconds {self.duration}"


class TurnWidge(ActionWidge):
    turn_speed: int
    duration: float

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.turn_speed = 0
        self.duration = 0

    def __str__(self) -> str:
        return (
            f"{self.get_class_name()}: speed {self.turn_speed}: seconds {self.duration}"
        )


class HeadTiltWidge(ActionWidge):
    position: int
    duration: float

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.position = 0
        self.duration = 0

    def __str__(self) -> str:
        str(self.__class__).split(".")[-1]
        return f"{self.get_class_name()}: position {self.position}: seconds {self.duration}"


class HeadTurnWidge(ActionWidge):
    position: int
    duration: float

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.position = 0
        self.duration = 0

    def __str__(self) -> str:
        str(self.__class__).split(".")[-1]
        return f"{self.get_class_name()}: position {self.position}: seconds {self.duration}"


class WaistWidge(ActionWidge):
    position: int
    duration: float

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.position = 0
        self.duration = 0

    def __str__(self) -> str:
        str(self.__class__).split(".")[-1]
        return (
            f"{self.get_class_name()}: speed {self.position}: seconds {self.duration}"
        )


class InputWidge(ActionWidge):
    input_string: str

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.input_string = "Nothing"

    def __str__(self) -> str:
        str(self.__class__).split(".")[-1]
        return f"{self.get_class_name()}: Wait for string '{self.input_string}'"


class OutputWidge(ActionWidge):
    output_string: str

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.output_string = "I have nothing to say"

    def __str__(self) -> str:
        str(self.__class__).split(".")[-1]
        return f"{self.get_class_name()}: Will say '{self.output_string}'"


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
    def build(self):
        return super().build()


if __name__ == "__main__":
    TangoApp().run()
