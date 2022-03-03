"""
Core robot functions for Robotics Group 26
- Ben, Isaac, Cameron
"""

import serial, time, sys
import tkinter as tk


class Tango:
    main_motor = None
    # motor_x = None

    MotorDict = {
        "waist": 0,
        "straight": 1,
        "turn": 2,
        "head": 3,
        "upDownHead": 4,
    }

    straightStopValue = 6000
    staightMediumForward = 5000
    straightSlowForward = 5400
    straightMaxForward = 4500

    straightMaxBackward = 7500
    straightMediumBackward = 7000
    straightSlowBackward = 5400
    motorSpeeds = [
        straightMaxBackward,
        straightMediumBackward,
        straightSlowBackward,
        straightStopValue,
        straightSlowForward,
        staightMediumForward,
        straightMaxForward,
    ]

    turnStopValue = 6000
    turnMaxLeft = 0
    turnMaxRight = 0

    headCenter = 6300
    headMidLeft = 7200
    headMaxLeft = 8000
    headMaxRight = 4000
    headMidRight = 5000
    headTurns = [
        headMaxLeft,
        headMidLeft,
        headCenter,
        headMidRight,
        headMaxRight,
    ]

    headTiltMid = 5300
    headTiltUp = 7000
    headTiltMidUp = 6500
    headTiltMidDown = 4500
    headTiltDown = 4000
    headTilts = [
        headTiltDown,
        headTiltMidDown,
        headTiltMid,
        headTiltMidUp,
        headTiltUp,
    ]

    waistCenter = 6000
    waistLeft = 7500
    waistRight = 4500
    waistTurn = [
        waistLeft,
        waistCenter,
        waistRight,
    ]

    current_motor_speed = straightStopValue
    current_waist = waistCenter
    current_head_turn = headCenter
    current_head_tilt = headCenter

    def __init__(self):
        print("class started")

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

    def tiltHeadUp(self):
        motor = self.MotorDict["upDownHead"]
        current_index = self.headTilts.index(self.current_head_tilt)
        if current_index == len(self.headTilts) - 1:
            print("Head too far up")
        else:
            current_index += 1
            self.current_head_tilt = self.headTilts[current_index]
            value = self.current_head_tilt
        self.run(value, motor)

    def tiltHeadDown(self):
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

    def turnWaistRight(self):
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
        try:
            self.main_motor = serial.Serial("/dev/ttyACM0")
        except:
            try:
                self.main_motor = serial.Serial("/dev/ttyACM1")
            except:
                print("No servo serial ports found")
                sys.exit(0)

        self.run(self.straightStopValue, self.MotorDict["straight"])
        return self

    def __exit__(self, exc_type, exc_value, exc_tb):
        self.neutral()
        self.main_motor.close()
