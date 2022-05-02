#!/usr/bin/env python3

from in_out import Listener, Speaker
from map_memory import Map
import time
from threading import Thread

from kivy.app import App
from kivy.core.image import Image
from kivy.uix.button import Button
from kivy.config import Config
from kivy.uix.widget import Widget
from kivy.core.window import Window
from kivy.properties import ObjectProperty
from kivy.clock import Clock
from kivy.uix.screenmanager import ScreenManager

actually_speak = False
actually_listen = False
actually_move = False

Commands_list = [
    "north",
    "south",
    "east",
    "west",
    "fight",
    "run",
]


class gameRobot:
    game_map: Map
    listener: Listener
    speaker: Speaker

    def __init__(self) -> None:
        print("Initialized main gameRobot")
        self.game_map = Map()
        # TODO: gui

    def perform_action(self):
        ...
        # TODO: probably check current game state
        # update gui
        # speak state and options to user
        # get input from user
        # perform action given input
        # Then return

    def run(self):
        ...


class MyScreenManager(ScreenManager):
    ...


class TangoGameApp(App):
    title = "Group 26 Tango"

    def build(self):
        return MyScreenManager()


if __name__ == "__main__":
    TangoGameApp().run()
