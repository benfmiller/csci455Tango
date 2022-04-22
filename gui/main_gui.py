#!/usr/bin/env python3


import time
from threading import Thread

from kivy.app import App
from kivy.core.image import Image
from kivy.uix.button import Button
from kivy.config import Config
from kivy.uix.widget import Widget
from action_widgets import ActionWidge, root_robot
from kivy.core.window import Window
from kivy.properties import ObjectProperty
from kivy.clock import Clock
from kivy.uix.screenmanager import ScreenManager


if root_robot is not None:
    Window.maximize()
    Config.set("kivy", "keyboard_mode", "systemanddock")
    Config.write()

# Config.set("graphics", "width", "200")
# Config.set("graphics", "height", "200")

num_placeholders = 8


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


def set_activate_screen():
    app = App.get_running_app()
    activate_layout = app.root.ids.activateWidgetLayout
    for widge in list(activate_layout.children):
        activate_layout.remove_widget(widge)
    new_widge_list = list(app.root.ids.placeHolderLayout.children)[::-1]
    placeholder_layout = app.root.ids.placeHolderLayout
    for widge in list(app.root.ids.placeHolderLayout.children):
        placeholder_layout.remove_widget(widge)
    for widge in new_widge_list:
        activate_layout.add_widget(widge)


def set_main_placeholders_back():
    app = App.get_running_app()
    placeholder_layout = app.root.ids.placeHolderLayout
    for widge in list(placeholder_layout.children):
        placeholder_layout.remove_widget(widge)
    new_widge_list = list(app.root.ids.activateWidgetLayout.children)[::-1]
    activate_layout = app.root.ids.activateWidgetLayout
    for widge in list(activate_layout.children):
        activate_layout.remove_widget(widge)
    for widge in new_widge_list:
        placeholder_layout.add_widget(widge)


def activate_thread():
    app = App.get_running_app()
    Clock.schedule_interval(app.root.ids.activateAnimation.update, 1.0 / 60.0)
    num = 1
    # TODO: set animation
    app.root.ids.backToMainScreen.disabled = True
    for button in app.root.ids.activateWidgetLayout.children[::-1]:
        print(f"Running box {num}: category {button.action}")
        button.background_color = (1.0, 1.0, 0.2, 1.0)
        if button.action is not None:
            button.action.activate()
        time.sleep(0.5)
        button.background_color = (1.0, 1.0, 1.0, 1.0)
        num += 1
    app.root.ids.backToMainScreen.disabled = False
    if root_robot is not None:
        print("Neutralizing robot")
        root_robot.neutral()
        time.sleep(0.05)
        root_robot.neutral()
        time.sleep(0.05)
        root_robot.neutral()
        time.sleep(0.05)
        root_robot.forward()
        time.sleep(0.05)
        root_robot.stop()
        time.sleep(0.05)
        root_robot.backward()
        time.sleep(0.05)
        root_robot.stop()
        print("********Done Neutralizing********\n")


class ActivateButton(Button):
    last_ran = time.time()
    running = False

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        # self.bind(on_press=self.callback)

    def on_touch_down(self, touch):
        if self.collide_point(*touch.pos) and time.time() - self.last_ran > 1:
            print("\n********Activating setup********!")
            app = App.get_running_app()
            set_activate_screen()
            app.root.current = "activateScreen"
            Thread(target=activate_thread).start()
            print("********Activation Done********\n")
            self.last_ran = time.time()
        return super().on_touch_down(touch)


class AnimatingImage(Button):
    time = 0.0
    rate = 0.2
    frame = 1

    def update(self, dt):
        self.time += dt
        if self.time > self.rate:
            self.time -= self.rate
            self.source = "atlas://robot/frame" + str(self.frame)
            # self.background_normal = "hello.jpeg"
            self.frame = self.frame + 1
            if self.frame > 4:
                self.frame = 1
        print("Hey!")


class AnimationScreen(Widget):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.robot = AnimatingImage()
        self.robot.background_normal = "atlas://robot/frame1"
        # self.background_normal = self.robot.source
        self.add_widget(self.robot)

    def update(self, dt):
        self.robot.update(dt)


class ReturnScreenButton(Button):
    def on_touch_down(self, touch):
        if self.collide_point(*touch.pos) and not self.disabled:
            app = App.get_running_app()
            set_main_placeholders_back()
            app.root.current = "mainScreen"
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
        app = App.get_running_app()
        settings_layout = app.root.ids.settingsLayout
        for widge in list(settings_layout.children):
            settings_layout.remove_widget(widge)

        if self.action is None:
            newButton = Button()
            newButton.text = "Nothing to do here!"
            app.root.ids.settingsTitleText.text = ""
            app.root.ids.settingsTitleImage.background_normal = ""
            app.root.ids.settingsTitleImage.background_color = (0, 0, 0, 0)
            settings_layout.add_widget(newButton)
        else:
            self.action.set_settings(settings_layout)

    def set_action(self, actionWidge: ActionWidge):
        self.action = actionWidge
        self.text = actionWidge.text
        self.background_normal = actionWidge.background_normal

    def reset(self):
        self.action = None
        self.attributes = None
        self.background_normal = "atlas://data/images/defaulttheme/button"


class MyScreenManager(ScreenManager):
    ...


class TangoApp(App):
    title = "Group 26 Tango"

    def build(self):
        return MyScreenManager()


if __name__ == "__main__":
    TangoApp().run()
