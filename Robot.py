"""
Core robot functions for Robotics Group 26
- Ben, Isaac, Cameron
"""

import serial, time, sys
import tkinter as tk


class Tango:
    main_motor = None

    MotorDict = {
        "waist": 0,
        "leftDrive": 1,
        "rightDrive": 2,
        "head": 3,
        "upDownHead": 4,
    }

    straightMaxForward = 4500
    staightMediumForward = 5000
    straightSlowForward = 5400
    straightStopValue = 6000
    straightSlowBackward = 6600
    straightMediumBackward = 7000
    straightMaxBackward = 7500
    motorSpeeds = [
        straightMaxBackward,
        straightMediumBackward,
        straightSlowBackward,
        straightStopValue,
        straightSlowForward,
        staightMediumForward,
        straightMaxForward,
    ]

    turnDiffsLeft3 = 1300
    turnDiffsLeft2 = 900
    turnDiffsLeft1 = 600
    turnDiffStraight = 0
    turnDiffsRight1 = -600
    turnDiffsRight2 = -900
    turnDiffsRight3 = -1300
    turnDiffs = [
        turnDiffsLeft3,
        turnDiffsLeft2,
        turnDiffsLeft1,
        turnDiffStraight,
        turnDiffsRight1,
        turnDiffsRight2,
        turnDiffsRight3,
    ]

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
    current_head_tilt = headTiltMid
    current_turn_speed = turnDiffStraight

    def __init__(self):
        print("class started")

    def forward(self, _=None, duration=0.1):
        current_index = self.motorSpeeds.index(self.current_motor_speed)
        if current_index == len(self.motorSpeeds) - 1:
            print("Speed already maxed out")
        else:
            current_index += 1
        self.current_motor_speed = self.motorSpeeds[current_index]
        value = self.current_motor_speed
        motor_speeds_reversed = self.motorSpeeds[::-1]
        second_value = motor_speeds_reversed[current_index]
        self.run_drive(
            value + self.current_turn_speed,
            second_value + self.current_turn_speed,
            duration=duration,
        )

    def backward(self, _=None, duration=0.1):
        current_index = self.motorSpeeds.index(self.current_motor_speed)
        if current_index == 0:
            print("Speed already Minimummed out")
        else:
            current_index -= 1
        self.current_motor_speed = self.motorSpeeds[current_index]
        value = self.current_motor_speed
        motor_speeds_reversed = self.motorSpeeds[::-1]
        second_value = motor_speeds_reversed[current_index]
        self.run_drive(
            value + self.current_turn_speed,
            second_value + self.current_turn_speed,
            duration=duration,
        )

    def turnLeft(self, _=None, duration=0):
        current_index = self.motorSpeeds.index(self.current_motor_speed)
        self.current_motor_speed = self.motorSpeeds[current_index]
        value = self.current_motor_speed
        motor_speeds_reversed = self.motorSpeeds[::-1]
        second_value = motor_speeds_reversed[current_index]

        current_index = self.turnDiffs.index(self.current_turn_speed)
        if current_index == 0:
            print("Turning right too fast!")
        else:
            current_index -= 1
        self.current_turn_speed = self.turnDiffs[current_index]
        turn_diff = self.turnDiffs[current_index]

        self.run_drive(value + turn_diff, second_value + turn_diff, duration=duration)

    def turnRight(self, _=None, duration=0):
        current_index = self.motorSpeeds.index(self.current_motor_speed)
        self.current_motor_speed = self.motorSpeeds[current_index]
        value = self.current_motor_speed
        motor_speeds_reversed = self.motorSpeeds[::-1]
        second_value = motor_speeds_reversed[current_index]

        current_index = self.turnDiffs.index(self.current_turn_speed)
        if current_index == len(self.turnDiffs) - 1:
            print("Turning left too fast!")
        else:
            current_index += 1
        self.current_turn_speed = self.turnDiffs[current_index]
        turn_diff = self.turnDiffs[current_index]

        self.run_drive(value + turn_diff, second_value + turn_diff, duration=duration)

    def turnHeadLeft(self, _=None):
        motor = self.MotorDict["head"]
        current_index = self.headTurns.index(self.current_head_turn)
        if current_index == len(self.headTurns) - 1:
            print("Head too far left")
        else:
            current_index += 1
        self.current_head_turn = self.headTurns[current_index]
        value = self.current_head_turn
        self.run(value, motor)

    def turnHeadRight(self, _):
        motor = self.MotorDict["head"]
        current_index = self.headTurns.index(self.current_head_turn)
        if current_index == 0:
            print("Head too far right")
        else:
            current_index -= 1
        self.current_head_turn = self.headTurns[current_index]
        value = self.current_head_turn
        self.run(value, motor)

    def tiltHeadUp(self, _=None):
        motor = self.MotorDict["upDownHead"]
        current_index = self.headTilts.index(self.current_head_tilt)
        if current_index == len(self.headTilts) - 1:
            print("Head too far up")
        else:
            current_index += 1
        self.current_head_tilt = self.headTilts[current_index]
        value = self.current_head_tilt
        self.run(value, motor)

    def tiltHeadDown(self, _):
        motor = self.MotorDict["upDownHead"]
        current_index = self.headTilts.index(self.current_head_tilt)
        if current_index == 0:
            print("Head too far down")
        else:
            current_index -= 1
        self.current_head_tilt = self.headTilts[current_index]
        value = self.current_head_tilt
        self.run(value, motor)

    def turnWaistLeft(self, _=None):
        motor = self.MotorDict["waist"]
        current_index = self.waistTurn.index(self.current_waist)
        if current_index == len(self.waistTurn) - 1:
            print("Waist is too far left")
        else:
            current_index += 1
        self.current_waist = self.waistTurn[current_index]
        value = self.current_waist
        self.run(value, motor)

    def turnWaistRight(self, _=None):
        motor = self.MotorDict["waist"]
        current_index = self.waistTurn.index(self.current_waist)
        if current_index == 0:
            print("Head too far right")
        else:
            current_index -= 1
        self.current_waist = self.waistTurn[current_index]
        value = self.current_waist
        self.run(value, motor)

    def stop(self, _=None):
        while self.current_turn_speed > self.turnDiffStraight:
            self.turnRight(duration=0.2)
        while self.current_turn_speed < self.turnDiffStraight:
            self.turnLeft(duration=0.2)
        while self.current_motor_speed > self.straightStopValue:
            self.forward(duration=0.2)
        while self.current_motor_speed < self.straightStopValue:
            self.backward(duration=0.2)

    def neutral(self, _=None):
        self.current_motor_speed = self.straightStopValue
        self.stop()
        self.current_waist = self.waistCenter
        self.run(self.current_waist, self.MotorDict["waist"], duration=0.1)
        self.current_head_turn = self.headCenter
        self.run(self.current_head_turn, self.MotorDict["head"], duration=0.1)
        self.current_head_tilt = self.headTiltMid
        self.run(self.current_head_tilt, self.MotorDict["upDownHead"], duration=0.1)
        self.current_turn_speed = self.turnDiffStraight
        time.sleep(0.1)

    def run(self, value: int, motor: int, duration: float = 0):
        lsb = value & 0x7F
        msb = (value >> 7) & 0x7F

        # base string
        cmd = chr(0xAA) + chr(0xC) + chr(0x04)
        cmd += chr(motor)
        # value
        cmd += chr(lsb) + chr(msb)

        print(f"writing: motor {motor}, value {value}")
        self.main_motor.write(cmd.encode("utf-8"))
        time.sleep(duration)

        print("Done Writing")

    def run_drive(self, first_value: int, second_value: int, duration: float = 0):
        cmd = chr(0xAA) + chr(0xC) + chr(0x1F) + chr(0x02) + chr(0x01)
        # 0xAA, device number, 0x1F, number of targets, first channel number, first target low bits, first target high bits, second target low bits, second target high bits
        lsb1 = first_value & 0x7F
        msb1 = (first_value >> 7) & 0x7F
        lsb2 = second_value & 0x7F
        msb2 = (second_value >> 7) & 0x7F
        cmd += chr(lsb1) + chr(msb1) + chr(lsb2) + chr(msb2)

        print(
            f"writing: motor 1 and 2, first value {first_value}, second_value {second_value}"
        )
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

        return self

    def __exit__(self, exc_type, exc_value, exc_tb):
        self.neutral()
        self.main_motor.close()
