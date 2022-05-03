import time


class RobotHandler:
    def __init__(self, actually_move=False) -> None:
        if actually_move:
            from robot import Tango

            root_robot = Tango()
            time.sleep(0.2)
            root_robot.forward()
            time.sleep(0.05)
            root_robot.stop()
            time.sleep(0.2)
            root_robot.neutral()
        else:
            root_robot = None

    def fight(self):
        # TODO: fight animation
        print("Making fight motions")
        ...

    def death(self):
        # TODO: death movements
        print("making death motions")

    def turn_right(self):
        # TODO: turn right 90 degrees
        print("Turned right 90 degrees")

    def turn_left(self):
        # TODO: turn left 90 degrees
        print("Turned left 90 degrees")

    def stop(self):
        # TODO: stop
        ...

    def big_stop(self):
        # TODO: Big stop, do all the writes to make sure it moves properly
        ...

    def forward(self):
        # TODO: robot move forward one tile
        ...

    def win(self):
        # TODO: win movements
        ...

    def neutral(self):
        # TODO: nice neutral state
        ...


if __name__ == "__main__":
    my_robot = RobotHandler()
    print("robot started")
    my_robot.fight()
    my_robot
