#!/usr/bin/env python3

from in_out import Listener, Speaker
from map_memory import Map

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
        self.
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
