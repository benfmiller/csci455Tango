from kivy.app import App
from kivy.uix.gridlayout import GridLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.image import Image
from kivy.uix.textinput import TextInput


class FirstHello(App):
    def build(self):
        self.window = GridLayout(spacing=20)
        self.window.cols = 2
        ##        self.window.size_hint = (0.6, 0.7)
        ##        self.window.pos_hint = {"center_x" : .5, "center_y" : 0.5}
        ##
        self.window.add_widget(Image(source="hello.jpeg"))
        self.question = Label(
            text="What is your robot's name?"
            ##                              font_size = 36,
            ##                              color = '#00abFF'
        )
        self.window.add_widget(self.question)
        ##        self.user = TextInput(
        ##                               multiline=False,
        ##                               padding_y = (20,20),
        ##                               size_hint = (1, 0.6)
        ##                              )
        ##        self.window.add_widget(self.user)
        ##        self.button = Button(text="Greet",
        ##                              size_hint = (1, 0.05),
        ##                              bold = True,
        ##                              background_color = '#00abFF',
        ##                              background_normal = ""
        ##                              )
        ##        self.button.bind(on_press = self.callback)
        ##        self.window.add_widget(self.button)

        return self.window

    def callback(self, instance):
        self.question.text = "Hello " + self.user.text + "!"


def main():
    FirstHello().run()


main()
