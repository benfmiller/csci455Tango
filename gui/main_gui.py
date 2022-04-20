#!/usr/bin/env python3

from kivy.app import App
from kivy.uix.label import Label

# importing builder from kivy
from kivy.lang import Builder
from kivy.uix.behaviors import DragBehavior

# using this class we will combine
# the drag behaviour to our label widget
class DraggableLabel(DragBehavior, Label):
    pass


# this is the main class which
# will render the whole application
class uiApp(App):

    # method which will render our application
    def build(self):
        return Builder.load_string(
            """
<DraggableLabel>:
    drag_rectangle: self.x, self.y, self.width, self.height
    drag_timeout: 10000
    drag_distance: 0
DraggableLabel:
    text:"[size=40]GeeksForGeeks[/size]"
    markup:True
                                   """
        )


if __name__ == "__main__":
    # running the application
    uiApp().run()
