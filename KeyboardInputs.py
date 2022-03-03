from Robot import Tango
import tkinter as tk


class KeyControl:
    def __init__(self, robot: Tango) -> None:
        self.win = tk.Tk()
        # self.win.geometry("200x100")
        self.robot = robot
        self.bindings()

    def bindingworks(self, event):
        print(event)

    def bindings(self):
        self.win.bind("<Up>", self.robot.tiltHeadUp)
        self.win.bind("<Left>", self.robot.turnHeadLeft)
        self.win.bind("<Down>", self.robot.tiltHeadDown)
        self.win.bind("<Right>", self.robot.turnHeadRight)
        self.win.bind("<z>", self.robot.turnWaistLeft)
        self.win.bind("<c>", self.robot.turnWaistRight)
        self.win.bind("<q>", self.robot.stop)
        self.win.bind("<w>", self.robot.forward)
        self.win.bind("<s>", self.robot.backward)
        self.win.bind("<a>", self.robot.turnLeft)
        self.win.bind("<d>", self.robot.turnRight)
        # self.win.bind("<d>", self.bindingworks)

    def run(self):
        self.win.mainloop()


with Tango() as tango:
    keys = KeyControl(tango)
    keys.run()
