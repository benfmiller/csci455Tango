#!/usr/bin/env python3

import random
from in_out import Listener, Speaker
from map_memory import Map, EasyEnemy, StrongEnemy, Enemy, RechargingNode, EndNode
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
max_moves = 30
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
            app.root.current = "gameScreen"  # type: ignore
            Thread(target=app.start_game).start()  # type: ignore
        return super().on_touch_down(touch)


class ReturnToMainButton(Button):
    def on_touch_down(self, touch):
        if self.collide_point(*touch.pos):
            print("Moving to start screen")
            app = App.get_running_app()
            app.root.current = "mainScreen"  # type: ignore
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

    def start_game(self):
        print("Running")
        while True:
            self.game_loop()

    def game_loop(self):
        # TODO: finish game loop
        # update gui
        # speak state and options to user
        # get input from user
        # perform action given input
        # Then return
        if self.only_move:
            input_options = self.game_map.get_input_options(only_move=True)
        else:
            input_options = self.game_map.get_input_options(only_move=False)

        if isinstance(self.game_map.current_node, EndNode):
            if self.has_key:
                self.speaker.output("Win! We have the key, so we win")
                app.root.ids.mainButton.text = "Win!"  # type: ignore
                self.robot_handler.win()
            else:
                self.speaker.output("At the End, but we need the key!")

        if "fight" in input_options:
            self.fight_mode()
        else:
            self.move_mode(input_options)

        # TODO: movement isn't working quite right

        if self.health <= 0:
            self.speaker.output("We died. Game Over")
            app = App.get_running_app()
            app.root.ids.mainButton.text = "Dead"  # type: ignore
            self.robot_handler.death()
        if self.move_number > max_moves:
            self.speaker.output("You ran out of moves!")
            self.speaker.output(f"Max moves is {max_moves}")
            self.speaker.output("Game Over")
            app = App.get_running_app()
            app.root.ids.mainButton.text = "Dead"  # type: ignore
            self.robot_handler.death()
        else:
            self.speaker.output(f"Move {self.move_number} out of {max_moves}")
            time.sleep(0.1)
        self.move_number += 1

    def move_mode(self, input_options: list[str]):
        current_node = self.game_map.current_node
        app = App.get_running_app()
        if isinstance(current_node, RechargingNode):
            app.root.ids.mainButton.text = "Recharging"  # type: ignore
            self.speaker.output(f"Health recharged to {starting_health}")
            time.sleep(0.1)
            self.health = starting_health
        else:
            app.root.ids.mainButton.text = "Moving"  # type: ignore

        self.speaker.output(
            f"You are at node {current_node.number} facing {self.game_map.direction}"
        )
        input_string = ""
        while True:
            self.speaker.output(f"Please input a direction {' '.join(input_options)}")
            input_string = self.listener.get_input()
            print(f"input is '{input_string}'")
            selected_option = ""
            for option in input_options:
                if option in input_string:
                    selected_option = option
                    break
            if selected_option != "":
                break
        self.move_direction(selected_option)

    def move_direction(self, direction):
        print("Turning")
        position = self.game_map.get_change_direction(direction)
        while position > 0:
            print("Turning right")
            self.game_map.update_right()
            self.robot_handler.turn_right()
            time.sleep(0.1)
            position -= 1
        while position < 0:
            print("Turning left")
            self.game_map.update_left()
            self.robot_handler.turn_left()
            time.sleep(0.1)
            position += 1
        print("Moving forward")
        self.game_map.update_move_forward()
        self.only_move = False
        self.robot_handler.stop()
        self.robot_handler.forward()

    def fight_mode(self):
        self.speaker.output("Fight!")
        time.sleep(0.1)
        if isinstance(self.game_map.current_node, EasyEnemy):
            app = App.get_running_app()
            app.root.ids.mainButton.text = "Easy Enemy"  # type: ignore
            enemy_string = f"The enemy is weak. {int(self.game_map.current_node.health)} health points left"
        else:
            app = App.get_running_app()
            app.root.ids.mainButton.text = "Strong Enemy"  # type: ignore
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
        app.root.ids.mainButton.text = "Smack!"  # type: ignore
        self.robot_handler.fight()
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
            app.root.ids.mainButton.text = "Run!"  # type: ignore
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
