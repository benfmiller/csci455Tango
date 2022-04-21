#!/usr/bin/env python3

from kivy.app import App
from kivy.uix.widget import Widget
from kivy.properties import NumericProperty, ReferenceListProperty
from kivy.vector import Vector
from kivy.uix.behaviors import DragBehavior

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

categories = {
    "drive": [],
    "turn": [],
    "head_tilt": [],
    "head_turn": [],
    "waist_turn": [],
    "input": [],
    "speak": [],
}


class ClearButton(Button):
    def on_touch_down(self, touch):
        if self.collide_point(*touch.pos):
            print("Clearing placeholders")
            app = App.get_running_app()
            num = 8
            for button in app.root.ids.placeHolderLayout.children:
                button.reset()
                button.text = str(num)
                num -= 1
        return super().on_touch_down(touch)


class ActivateButton(Button):
    def on_touch_down(self, touch):
        if self.collide_point(*touch.pos):
            print("Activating setup!")
            app = App.get_running_app()
            for button in app.root.ids.placeHolderLayout.children[::-1]:
                print("Running ")
                print(button.text)
        return super().on_touch_down(touch)


class PlaceHolderButton(Button):
    num = 0
    category = None

    def on_touch_down(self, touch):
        if self.collide_point(*touch.pos):
            print("I've been touched!")
        return super().on_touch_down(touch)

    def extra_func(self):
        print("Calling extra_func")
        self.text = "blah"
        self.background_normal = "./hello.jpeg"

    def reset(self):
        # TODO: reset text
        self.category = None
        # print(self.parent.ids)

        # print(self.find_id)

    # def find_id(self, parent, widget):
    #     for id, obj in parent.ids.items():
    #         if obj == widget:
    #             print(id)
    #             return id


class ActionWidge(DragBehavior, Button):
    dragging = BooleanProperty(False)
    original_pos = ListProperty()

    def on_touch_down(self, touch):
        # self.add_widget(
        #     PongBall(),
        # )
        # self.parent.add_widget(DragButton())
        if self.collide_point(*touch.pos):
            print("on touch down")
            self.original_pos = self.pos
        return super().on_touch_down(touch)

    def on_touch_move(self, touch):
        if touch.grab_current is self:
            self.opacity = 0.4
            self.dragging = True
        return super().on_touch_move(touch)

    def on_touch_up(self, touch):
        app = App.get_running_app()
        # print(app.root.ids)
        if self.dragging:
            self.opacity = 1
            self.dragging = False
            if self.collide_widget(app.root.ids["place1"]):
                app.root.ids["place1"].extra_func()
            anim = Animation(pos=self.original_pos, duration=0.0)
            anim.start(self)
        return super().on_touch_up(touch)


class TangoApp(App):
    def build(self):
        return super().build()


if __name__ == "__main__":
    TangoApp().run()
