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
        print("Making fight motions")
        if self.root_robot is not None:
            shoulder = 5
            self.root_robot.run(5500, shoulder, 0)
            time.sleep(0.4)
            self.root_robot.run(8000, shoulder, 0)
            time.sleep(0.4)
            self.root_robot.turnWaistLeft()
            time.sleep(0.3)
            self.root_robot.turnHeadLeft()
            time.sleep(0.3)
            self.root_robot.turnHeadLeft()
            time.sleep(0.3)
            self.root_robot.turnWaistRight()
            time.sleep(0.3)
            self.root_robot.turnHeadRight()
            time.sleep(0.3)
            self.root_robot.turnHeadRight()
            time.sleep(0.3)
            self.root_robot.turnHeadRight()
            shoulder = 5
            self.root_robot.run(5500, shoulder, 0)
            time.sleep(0.4)
            self.root_robot.run(8000, shoulder, 0)
            time.sleep(0.8)
            self.root_robot.run(7000, shoulder, 0)
            time.sleep(0.4)
            self.root_robot.run(6000, shoulder, 0)
            self.neutral()

    def death(self):
        print("making death motions")
        if self.root_robot is not None:
            for i in range(3):
                self.root_robot.turnHeadLeft()
                time.sleep(0.2)
                self.root_robot.turnHeadRight()
                time.sleep(0.2)
                self.root_robot.turnHeadRight()
                time.sleep(0.2)
                self.root_robot.turnHeadLeft()
                time.sleep(0.2)
            self.neutral()

    def recharging(self):
        print("Making recharging movements")
        if self.root_robot is not None:
            self.root_robot.tiltHeadUp()
            time.sleep(0.2)
            self.root_robot.tiltHeadUp()
            time.sleep(2)
            self.root_robot.tiltHeadDown()
            time.sleep(0.2)
            self.root_robot.tiltHeadDown()
            self.neutral()

    def win(self):
        if self.root_robot is not None:
            for i in range(2):
                self.root_robot.tiltHeadUp()
                time.sleep(0.2)
                self.root_robot.tiltHeadDown()
                time.sleep(0.2)
                self.root_robot.tiltHeadDown()
                time.sleep(0.2)
                self.root_robot.tiltHeadUp()
                time.sleep(0.2)
            elbow = 7
            self.root_robot.run(5500, elbow, 0)
            time.sleep(0.4)
            self.root_robot.run(3000, elbow, 0)
            time.sleep(0.8)
            self.root_robot.run(4000, elbow, 0)
            time.sleep(0.4)
            self.root_robot.run(5500, elbow, 0)
            for i in range(2):
                self.root_robot.tiltHeadUp()
                time.sleep(0.2)
                self.root_robot.tiltHeadDown()
                time.sleep(0.2)
                self.root_robot.tiltHeadDown()
                time.sleep(0.2)
                self.root_robot.tiltHeadUp()
                time.sleep(0.2)
            self.neutral()

    def turn_right(self):
        self.stop()
        print("Turned right 90 degrees")
        if self.root_robot is not None:
            position = 3
            while position > 0:
                self.root_robot.turnRight()
                time.sleep(0.05)
                position -= 1
        time.sleep(0.6)
        if self.root_robot is not None:
            self.root_robot.stop()
        time.sleep(0.1)

    def turn_left(self):
        self.stop()
        print("Turned left 90 degrees")
        if self.root_robot is not None:
            position = 3
            while position > 0:
                self.root_robot.turnLeft()
                time.sleep(0.05)
                position -= 1
        time.sleep(0.6)
        if self.root_robot is not None:
            self.root_robot.stop()
        time.sleep(0.1)

    def stop(self):
        if self.root_robot is not None:
            self.root_robot.forward()
            time.sleep(0.05)
            self.root_robot.stop()
        print("regular stop")

    def big_stop(self):
        if self.root_robot is not None:
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
        time.sleep(0.1)

    def neutral(self):
        if self.root_robot is not None:
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
    my_robot = RobotHandler(True)
    print("robot started")
    my_robot.win()
