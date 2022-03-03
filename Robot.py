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
            "waist": 0,
            "straight": 1,
            "turn": 2,
            "head": 3,
            "upDownHead": 4,
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

        self.run(self.straightStopValue, self.MotorDict["straight"])

    def forward(self, duration=0):
        motor = self.MotorDict["straight"]
        current_index = self.motorSpeeds.index(self.current_motor_speed)
        # value = self.straightStopValue + 200
        if current_index == len(self.motorSpeeds) - 1:
            print("Speed already maxed out")
        else:
            current_index += 1
            self.current_motor_speed = self.motorSpeeds[current_index]
            value = self.current_motor_speed
        self.run(value, motor, duration=duration)

    def backward(self, duration=0):
        motor = self.MotorDict["straight"]
        current_index = self.motorSpeeds.index(self.current_motor_speed)
        # value = self.straightStopValue + 200
        if current_index == 0:
            print("Speed already Minimummed out")
        else:
            current_index -= 1
            self.current_motor_speed = self.motorSpeeds[current_index]
            value = self.current_motor_speed
        self.run(value, motor, duration=duration)

    def turnRight(self):
        pass
        # motor = self.MotorDict["turn"]
        # value = self.turnStopValue + 200

    def turnLeft(self):
        pass
        motor = self.MotorDict["turn"]
        value = self.turnStopValue - 200
        # duration = 0.1
        self.run(value, motor, duration)

    def turnHeadLeft(self):
        motor = self.MotorDict["head"]
        current_index = self.headTurns.index(self.current_head_turn)
        if current_index == len(self.headTurns) - 1:
            print("Head too far left")
        else:
            current_index += 1
            self.current_head_turn = self.headTurns[current_index]
            value = self.current_head_turn
        self.run(value, motor)

    def turnHeadRight(self):
        motor = self.MotorDict["head"]
        current_index = self.headTurns.index(self.current_head_turn)
        if current_index == 0:
            print("Head too far right")
        else:
            current_index -= 1
            self.current_head_turn = self.headTurns[current_index]
            value = self.current_head_turn
        self.run(value, motor)

    def tiltHeadDown(self):
        motor = self.MotorDict["upDownHead"]
        current_index = self.headTilts.index(self.current_head_tilt)
        if current_index == len(self.headTilts) - 1:
            print("Head too far up")
        else:
            current_index += 1
            self.current_head_tilt = self.headTilts[current_index]
            value = self.current_head_tilt
        self.run(value, motor)

    def turnHeadRight(self):
        motor = self.MotorDict["upDownHead"]
        current_index = self.headTilts.index(self.current_head_tilt)
        if current_index == 0:
            print("Head too far down")
        else:
            current_index -= 1
            self.current_head_tilt = self.headTilts[current_index]
            value = self.current_head_tilt
        self.run(value, motor)

    def turnWaistLeft(self):
        motor = self.MotorDict["waist"]
        current_index = self.waistTurn.index(self.current_waist)
        if current_index == len(self.waistTurn) - 1:
            print("Waist is too far left")
        else:
            current_index += 1
            self.current_waist = self.waistTurn[current_index]
            value = self.current_waist
        self.run(value, motor)

    def turnHeadRight(self):
        motor = self.MotorDict["waist"]
        current_index = self.waistTurn.index(self.current_waist)
        if current_index == 0:
            print("Head too far right")
        else:
            current_index -= 1
            self.current_waist = self.waistTurn[current_index]
            value = self.current_waist
        self.run(value, motor)

    def stop(self):
        while self.current_motor_speed > self.straightStopValue:
            self.forward(duration=0.2)
        while self.current_motor_speed < self.straightStopValue:
            self.backward(duration=0.2)

    def neutral(self):
        self.current_motor_speed = self.straightStopValue
        self.stop()
        self.current_waist = self.waistCenter
        self.run(self.current_waist, self.MotorDict["waist"])
        self.current_head_turn = self.headCenter
        self.run(self.current_head_turn, self.MotorDict["head"])
        self.current_head_tilt = self.headCenter
        self.run(self.current_head_tilt, self.MotorDict["upDownHead"])

    def run(self, value: int, motor: int, duration: float = 0):
        lsb = value & 0x7F
        msb = (value >> 7) & 0x7F

        # base string
        cmd = chr(0xAA) + chr(0xC) + chr(0x04)
        cmd += chr(motor)
        # value
        cmd += chr(lsb) + chr(msb)

        print("writing")
        self.main_motor.write(cmd.encode("utf-8"))
        time.sleep(duration)

        print("Done Writing")

    def __enter__(self):
        # self.main_motor = serial.Serial("/dev/ttyACM0")
        # self.main_motor = serial.Serial("/dev/ttyACM1")
        # return self
        try:
            self.main_motor = serial.Serial("/dev/ttyACM0")
        except:
            try:
                self.main_motor = serial.Serial("/dev/ttyACM1")
            except:
                print("No servo serial ports found")
                sys.exit(0)
        return self

    def __exit__(self, exc_type, exc_value, exc_tb):
        self.neutral()
        self.main_motor.close()


with Tango() as tango:
    Dict = {
        "waist": 0,
        "straight": 1,
        "turn": 2,
        "head": 3,
        "upDownHead": 4,
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


win = tk.Tk()
# keys = keyControl(win)
win.bind("<Up>", keys.arrow)  # head tilt up
win.bind("<Left>", keys.arrow)  # head turn left
win.bind("<Down>", keys.arrow)  # head tilt down
win.bind("<Right>", keys.arrow)  # head turn right
win.bind("<z>", keys.waist)  # turn waist left
win.bind("<c>", keys.waist)  # turn waist right
win.bind("<w>", keys.head)  # drive forward
win.bind("<s>", keys.head)  # drive backward
win.bind("<a>", keys.head)  # turn left
win.bind("<d>", keys.head)  # turn right
