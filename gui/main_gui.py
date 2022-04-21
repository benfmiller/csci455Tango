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


class PongBall(Widget):
    velocity_x = NumericProperty(0)
    velocity_y = NumericProperty(0)
    velocity = ReferenceListProperty(velocity_x, velocity_y)

    def move(self):
        self.pos = Vector(*self.velocity) + self.pos


class ActionButton(DragBehavior, Button):
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
        if self.dragging:
            self.opacity = 1
            self.dragging = False
            if self.collide_widget(app.root.ids.remove_zone):
                self.parent.remove_widget(self)
            else:
                anim = Animation(pos=self.original_pos, duration=0.0)
                anim.start(self)
        return super().on_touch_up(touch)

    #
    # # velocity of the ball on x and y axis
    # velocity_x = NumericProperty(0)
    # velocity_y = NumericProperty(0)
    #
    # # referencelist property so we can use ball.velocity as
    # # a shorthand, just like e.g. w.pos for w.x and w.y
    # velocity = ReferenceListProperty(velocity_x, velocity_y)
    #
    # # ``move`` function will move the ball one step. This
    # #  will be called in equal intervals to animate the ball
    # def move(self):
    #     self.pos = Vector(*self.velocity) + self.pos


class TangoApp(App):
    def build(self):
        # return MainLayout()
        return super().build()


if __name__ == "__main__":
    TangoApp().run()

# <PongBall>:
#     size: 50, 50
#     drag_rectangle: self.x, self.y, self.width, self.height
#     drag_timeout: 10000
#     drag_distance: 0
#     canvas:
#         Ellipse:
#             pos: self.pos
#             size: self.size

# 1. Motors with speed, time and direction.
# 2. Motors turn robot left, or right for x amount of seconds.
# 3. Head tilt both directions
# 4. Head pan both directions
# 5. Waist turn both directions
# 6. A wait for human speech input
# 7. Talking, be able to type in what sentence you want to say and the robot says it.
