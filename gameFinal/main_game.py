#!/usr/bin/env python3

import random
from in_out import Listener, Speaker
from map_memory import Map, EasyEnemy, StrongEnemy, Enemy
import time
from threading import Thread
from robot_handler import RobotHandler

from kivy.app import App
from kivy.core.image import Image
from kivy.uix.button import Button
from kivy.config import Config
from kivy.uix.widget import Widget
from kivy.core.window import Window
from kivy.properties import ObjectProperty
from kivy.clock import Clock
from kivy.uix.screenmanager import ScreenManager

starting_health = 100
damage_range = [20, 40]
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


class StartButton(Button):
    def on_touch_down(self, touch):
        if self.collide_point(*touch.pos):
            print("Starting Game!")
            app = App.get_running_app()
            app.root.current = "startScreen"  # type: ignore
            Thread(target=app.start_game).start()  # type: ignore
        return super().on_touch_down(touch)


class TangoGameApp(App):
    title = "Group 26 Tango"
    health: int
    has_key: bool
    only_move: bool
    move_number: int

    game_map: Map
    listener: Listener
    speaker: Speaker

    def __init__(self) -> None:
        super().__init__()
        print("Initialized main gameRobot")
        self.game_map = Map()
        self.robot_handler = RobotHandler(actually_move=actually_move)
        self.speaker = Speaker(audio=actually_speak)
        self.listener = Listener(audio=actually_listen)
        self.health = starting_health
        self.has_key = False
        self.only_move = True
        self.move_number = 1

    def perform_action(self):
        ...

    def start_game(self):
        print("Running")
        while True:
            self.game_loop()

    def game_loop(self):
        # TODO
        # update gui
        # speak state and options to user
        # get input from user
        # perform action given input
        # Then return
        if self.only_move:
            input_options = self.game_map.get_input_options(only_move=True)
        else:
            input_options = self.game_map.get_input_options(only_move=False)
        if "fight" in input_options:
            self.fight_mode()
        else:
            ...
        self.move_number += 1
        if self.health <= 0:
            self.speaker.output("We died. Game Over")
            app = App.get_running_app()
            app.root.current = "deathScreen"  # type: ignore
            self.robot_handler.death()

    def fight_mode(self):
        self.speaker.output("Fight!")
        time.sleep(0.1)
        if isinstance(self.game_map.current_node, EasyEnemy):
            app = App.get_running_app()
            app.root.current = "easyEnemyScreen"  # type: ignore
            enemy_string = f"The enemy is weak. {int(self.game_map.current_node.health)} health points left"
        else:
            app = App.get_running_app()
            app.root.current = "strongEnemyScreen"  # type: ignore
            enemy_string = f"The enemy is strong. {int(self.game_map.current_node.health)} health points left"  # type: ignore
        self.speaker.output(f"We have {int(self.health)} health points left")
        time.sleep(0.1)
        self.speaker.output(enemy_string)
        time.sleep(0.1)
        input_string = ""
        while "fight" not in input_string and "run" not in input_string:
            self.speaker.output("Would you like to fight or run?")
            input_string = self.listener.get_input()
        if "fight" in input_string:
            self.perform_fight()
        else:
            self.perform_run()

    def perform_fight(self):
        self.speaker.output("Fight!")
        app = App.get_running_app()
        app.root.current = "fightScreen"  # type: ignore
        self.robot_handler.fight()
        # TODO: handle damage
        enemy_node: Enemy = self.game_map.current_node  # type: ignore
        damage_dealt = random.randint(damage_range[0], damage_range[1])
        enemy_node.health -= damage_dealt
        self.speaker.output(f"Dealt {damage_dealt} damage.")
        if enemy_node.health <= 0:
            self.speaker.output("Enemy is dead! We win!")
            if isinstance(enemy_node, StrongEnemy):
                if enemy_node.has_key:
                    self.speaker.output("We got the key!")
                    self.has_key = True
            return

        damage_took = random.randint(damage_range[0], damage_range[1])
        self.health -= damage_took
        self.speaker.output(f"Took {damage_took} damage.")
        time.sleep(0.1)
        self.speaker.output(f"New health is {self.health}.")

    def perform_run(self):
        self.speaker.output("Run!")
        if self.game_map.attempt_run():
            app = App.get_running_app()
            app.root.current = "runScreen"  # type: ignore
            self.speaker.output("We successfully escaped")
            self.speaker.output(
                f"New position is node {self.game_map.current_node.number}"
            )
            self.only_move = True
        else:
            self.speaker.output("We did not escape")
            damage_took = random.randint(damage_range[0], damage_range[1])
            self.health -= damage_took
            self.speaker.output(f"Took {damage_took} damage.")
            time.sleep(0.1)
            self.speaker.output(f"New health is {self.health}.")

    def build(self):
        return MyScreenManager()


class MyScreenManager(ScreenManager):
    ...


if __name__ == "__main__":
    TangoGameApp().run()
