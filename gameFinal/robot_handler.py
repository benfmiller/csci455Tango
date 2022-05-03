import time


class RobotHandler:
    def __init__(self, actually_move=False) -> None:
        if actually_move:
            from robot import Tango

            self.root_robot = Tango()
            time.sleep(0.2)
            self.root_robot.forward()
            time.sleep(0.05)
            self.root_robot.stop()
            time.sleep(0.2)
            self.root_robot.neutral()
        else:
            self.root_robot = None

    def fight(self):
        # TODO: fight animation
        print("Making fight motions")
        ...

    def death(self):
        # TODO: death movements
        print("making death motions")

    def win(self):
        # TODO: win movements
        ...

    def turn_right(self):
        print("Turned right 90 degrees")
        if self.root_robot is not None:
            position = 2
            while position > 0:
                self.root_robot.turnLeft()
                time.sleep(0.05)
                position -= 1
        time.sleep(2)
        if self.root_robot is not None:
            self.root_robot.stop()
        time.sleep(0.1)

    def turn_left(self):
        print("Turned left 90 degrees")
        if self.root_robot is not None:
            position = 2
            while position > 0:
                self.root_robot.turnRight()
                time.sleep(0.05)
                position -= 1
        time.sleep(2)
        if self.root_robot is not None:
            self.root_robot.stop()
        time.sleep(0.1)

    def stop(self):
        # TODO: stop
        self.root_robot.forward()
        time.sleep(0.05)
        self.root_robot.stop()
        print("regular stop")

    def big_stop(self):
        self.root_robot.forward()
        time.sleep(0.05)
        self.root_robot.stop()
        time.sleep(0.05)
        self.root_robot.backward()
        time.sleep(0.05)
        self.root_robot.stop()
        time.sleep(0.05)
        self.root_robot.turnLeft()
        time.sleep(0.05)
        self.root_robot.stop()
        print("Big stopped")

    def forward(self):
        print("Driving")
        if self.root_robot is not None:
            position = 2
            while position > 0:
                self.root_robot.forward()
                time.sleep(0.05)
                position -= 1
        time.sleep(1)
        if self.root_robot is not None:
            self.root_robot.stop()
        time.sleep(float(self.delay_input.text))

    def neutral(self):
        self.root_robot.neutral()
        time.sleep(0.05)
        self.root_robot.neutral()
        time.sleep(0.05)
        self.root_robot.neutral()
        time.sleep(0.05)
        self.root_robot.forward()
        time.sleep(0.05)
        self.root_robot.stop()
        time.sleep(0.05)
        self.root_robot.backward()
        time.sleep(0.05)
        self.root_robot.stop()
        print("neutralized")


if __name__ == "__main__":
    my_robot = RobotHandler()
    print("robot started")
    my_robot.fight()
    my_robot
