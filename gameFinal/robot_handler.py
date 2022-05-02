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

    def turn(self):
        print(Direction)
        print(Direction["Up"])

        # if robot.turnRight():
        #     Direction["Front"] = "East"
        #     Direction["Left"] = "North"
        #     Direction["Right"] = "South"
        #     Direction["Behind"] = "West"

        # if robot.turnLeft():
        #     Direction["Front"] = "West"
        #     Direction["Left"] = "South"
        #     Direction["Right"] = "North"
        #     Direction["Behind"] = "East"

        # if robot.moveForward():
        #     Direction["Front"] = "North"
        #     Direction["Left"] = "West"
        #     Direction["Right"] = "East"
        #     Direction["Behind"] = "South"

        # if robot.moveBackward():
        #     Direction["Front"] = "South"
        #     Direction["Left"] = "East"
        #     Direction["Right"] = "West"
        #     Direction["Behind"] = "North"
