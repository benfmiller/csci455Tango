"""
Core robot functions for Robotics Group 26
- Ben, Isaac, Cameron
"""

import serial, time, sys
import tkinter as tk


class Tango:
    main_motor = None
    # motor_x = None

    def __init__(self):
        print("class started")
        self.MotorDict = {
            "motor": 0,
            "straight": 1,
            "turn": 2,
            "head": 3,
            "upDownHead": 4,
            "rightArm": 5,
            "rightArmOut": 6,
        }

        self.straightStopValue = 6000
        self.staightMediumForward = 5000
        self.straightSlowForward = 5400
        self.straightMaxForward = 4500

        self.straightMaxBackward = 7500
        self.straightMediumBackward = 7000
        self.straightSlowBackward = 5400
        self.motorSpeeds = [
            self.straightMaxBackward,
            self.straightMediumBackward,
            self.straightSlowBackward,
            self.straightStopValue,
            self.straightSlowForward,
            self.staightMediumForward,
            self.straightMaxForward,
        ]

        self.turnStopValue = 6000
        self.turnMaxLeft = 0
        self.turnMaxRight = 0

        self.headCenter = 6300
        self.headMidLeft = 7200
        self.headMaxLeft = 8000
        self.headMaxRight = 4000
        self.headMidRight = 5000
        self.headTurns = [
            self.headMaxLeft,
            self.headMidLeft,
            self.headCenter,
            self.headMidRight,
            self.headMaxRight,
        ]

        self.headTiltMid = 5300
        self.headTiltUp = 7000
        self.headTiltMidUp = 6500
        self.headTiltMidDown = 4500
        self.headTiltDown = 4000
        self.headTilts = [
            self.headTiltDown,
            self.headTiltMidDown,
            self.headTiltMid,
            self.headTiltMidUp,
            self.headTiltUp,
        ]

        self.waistCenter = 6000
        self.waistLeft = 7500
        self.waistRight = 4500
        self.waistTurn = [
            self.waistLeft,
            self.waistCenter,
            self.waistRight,
        ]

        self.current_motor_speed = self.straightStopValue
        self.current_waist = self.waistCenter
        self.current_head_turn = self.headCenter
        self.current_head_tilt = self.headCenter

    def forward(self):
        motor = self.MotorDict["straight"]
        value = self.straightStopValue + 200
        # duration = 0.1
        self.run(value, motor, duration)

    def backward(self):
        motor = self.MotorDict["straight"]
        value = self.straightStopValue - 200
        # duration = 0.1
        self.run(value, motor, duration)

    def turnRight(self):
        motor = self.MotorDict["turn"]
        value = self.turnStopValue + 200
        # duration = 0.1
        self.run(value, motor, duration)

    def turnLeft(self):
        motor = self.MotorDict["turn"]
        value = self.turnStopValue - 200
        # duration = 0.1
        self.run(value, motor, duration)

    def run(self, value: int, motor: int, duration: float = 0):
        lsb = value & 0x7F
        msb = (value >> 7) & 0x7F

        # base string
        cmd = chr(0xAA) + chr(0xC) + chr(0x04)
        cmd += chr(motor)
        # value
        cmd += chr(lsb) + chr(msb)

        print("writing")
        # current_time = time.time()
        self.main_motor.write(cmd.encode("utf-8"))
        time.sleep(duration)

        print("Done Writing")

    def __enter__(self):
        self.main_motor = serial.Serial("/dev/ttyACM0")
        # self.main_motor = serial.Serial("/dev/ttyACM1")
        return self

    def __exit__(self, exc_type, exc_value, exc_tb):
        if isinstance(exc_value, IndexError):
            # Handle IndexError here...
            print(f"An exception occurred in your with block: {exc_type}")
            print(f"Exception message: {exc_value}")
        self.main_motor.close()
        # self.motor_x.close()
        # self.motor_y.close()


with Tango() as tango:
    Dict = {
        "waist": 0,
        "straight": 1,
        "turn": 2,
        "head": 3,
        "upDownHead": 4,
        "rightArm": 5,
        "rightArmOut": 6,
    }
    # turn direction
    motor = 0x01
    value = 6000
    duration = 0.01
    tango.run(value, motor, duration)
    motor = 0x01
    value = 7000
    duration = 0.1
    tango.run(value, motor, duration)

    motor = 0x02
    value = 6000
    duration = 0.01
    tango.run(value, motor, duration)
    # value = 7000
    # tango.run(value, motor, duration)

    # motor speed
    # motor = 0x01
    # value = 6000
    # duration = 0.01
    tango.run(value, motor, duration)
    # value = 7000
    # duration = 1.5
    # tango.run(value, motor, duration)
    # value = 6000
    # duration = 0.5
    # tango.run(value, motor, duration)
    # value = 6800
    # motor = 0x01
    # tango.run(value, motor)


def keyControl(win):
    ...


win = tk.Tk()
keys = keyControl(win)
win.bind("<Up>", keys.arrow)  # head tilt up
win.bind("<Left>", keys.arrow)  # head turn left
win.bind("<Down>", keys.arrow)  # head tilt down
win.bind("<Right>", keys.arrow)  # head turn right
win.bind("<space>", keys.arrow)
win.bind("<z>", keys.waist)
win.bind("<c>", keys.waist)
win.bind("<w>", keys.head)
win.bind("<s>", keys.head)
win.bind("<a>", keys.head)
win.bind("<d>", keys.head)

# try:
#     usb = serial.Serial('/dev/ttyACM0')
#     print(usb.name)
#     print(usb.baudrate)
# except:
#     try:
#         usb = serial.Serial('/dev/ttyACM1')
#         print(usb.name)
#         print(usb.baudrate)
#     except:
#         print("No servo serial ports found")
#         sys.exit(0)
