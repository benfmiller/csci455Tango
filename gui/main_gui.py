#!/usr/bin/env python3


import time
from kivy.app import App
from kivy.uix.button import Button
from kivy.config import Config
from action_widgets import ActionWidge
from kivy.core.window import Window

Window.maximize()

Config.set("kivy", "keyboard_mode", "systemanddock")
Config.write()
# Config.set("graphics", "width", "200")
# Config.set("graphics", "height", "200")

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
            app.root.ids.settingsTitle.text = ""
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

if actually_move:
    from robot import Tango

    root_robot = Tango()
else:
    root_robot = None
