"""
Core robot functions for Robotics Group 26
- Ben, Isaac, Cameron
"""

import serial, time, sys


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
        self.stopValue = 6000
    
    def forward(self):
        motor = self.MotorDict["straight"]
        value = self.stopValue + 200
        duration = 0.1
        self.run(value, motor, duration)

    def backward(self):
        motor = self.MotorDict["straight"]
        value = self.stopValue - 200
        duration = 0.1
        self.run(value, motor, duration)

    def turnRight(self):
        motor = self.MotorDict["turn"]
        value = self.stopValue + 200
        duration = 0.1
        self.run(value, motor, duration)

    def forward(self):
        motor = self.MotorDict["turn"]
        value = self.stopValue - 200
        duration = 0.1
        self.run(value, motor, duration)

    def run(self, value: int, motor: int, duration: float):
        lsb = value & 0x7F
        msb = (value >> 7) & 0x7F

        # base string
        cmd = chr(0xAA) + chr(0xC) + chr(0x04)
        # motor index
        # 0 is the turn
        # 1 is broken arm?
        # 2 is arm elbow
        # 3 is head
        # 4 is up down for head
        # 5 is right arm
        # 6 is moving right out (elbow)
        cmd += chr(motor)
        # value
        cmd += chr(lsb) + chr(msb)

        print("writing")
        # current_time = time.time()
        self.main_motor.write(cmd.encode("utf-8"))
        time.sleep(duration)
        # while time.time() - current_time < duration:
        # self.main_motor.write(cmd.encode("utf-8"))

        print("Done Writing")
        return None

    def __enter__(self):
        # self.main_motor = serial.Serial("/dev/ttyACM0")
        self.main_motor = serial.Serial("/dev/ttyACM1")
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
        "motor": 0,
        "straight": 1,
        "turn": 2,
        "head": 3,
        "upDownHead": 4,
        "rightArm": 5,
        "rightArmOut": 6,
    }
    # motor = Dict["motor"]
    motor = 0x03
    value = 6000
    duration = 1.0
    tango.run(value, motor, duration)
    value = 7800
    duration = 1.5
    tango.run(value, motor, duration)
    # value = 6800
    # motor = 0x01
    # tango.run(value, motor)


# def controls(self):
# win = tk.Tk()
# keys = keyControl(win)
# win.bind('<Up>', keys.arrow)
# win.bind('<Left>',keys.arrow)
# win.bind('<Down>',keys.arrow)
# win.bind('<Right>',keys.arrow)
# win.bind('<space>',keys.arrow)
# win.bind('<z>', keys.waist)
# win.bind('<c>',keys.waist)
# win.bind('<w>',keys.head)
# win.bind('<s>',keys.head)
# win.bind('<a>',keys.head)
# win.bind('<d>',keys.head)


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

# target = 6700

# lsb = target &0x7F
# msb = (target >> 7) & 0x7F

# cmd = chr(0xaa) + chr(0xC) + chr(0x04) + chr(0x03) + chr(lsb) + chr(msb)
# print("writing")
# usb.write(cmd.encode('utf-8'))
# print("reading")


# class Robot:
#     def __init__(self):
#         pass
