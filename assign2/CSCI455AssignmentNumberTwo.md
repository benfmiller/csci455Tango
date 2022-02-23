# CSCI 455 Assignment Number Two
# “Make it Move”
# Due in two weeks March 4th

For this assignment you need to make the robot controllable with a keyboard. Either plugged in
or remotely SSH into the robot and run a Python program that will allow you to control the
robot.
With keys on a keyboard, you will need to be able to:
    1. Drive forward and reverse. 3 speeds in both directions, if the robot tips you are going
    too fast and should step up and step down the values in a for loop.
    2. Turn left or right. Do not tip with the speed.
    3. STOP the robot…….get this done early.
    a. Be careful, if you stop too fast it will tip the robot.
    b. If your program crashes you lose control of the stop function, be prepared to hit
    the power switch.
    4. Twist the upper body left, right and center with thee keys, three steps of resolution.
    5. Twist head left, right and center, 5 steps of resolution.
    6. Raise and lower the head tilt, 5 degrees of resolution.
    7. Fool proof your code.
    8. Prepare in advance, Write your code so the controller can take input from a keyboard,
    network or possibly the touch screen or pre-created text file. Be prepared for any type
    of data input.

## Setting up SD Cards
    1. There are two computers in lab that have the image and capability to write to SD Cards
    if needed. You have to be logged on as Admin to get this work so I have to be there.
    2. Here is the link to the software to burn the OS image on to the SD card
    a. https://www.raspberrypi.com/software/
    3. I used the default Raspberry Pi OS, there are a lot of choices, I suggest you use the same
    one I use unless you are comfortable with Debian or another OS you really want to use.
    4. Before you take the SD card out of your computer you should find the config.txt file and
    edit the board to work with the touch screens.
    a. There are two types of screens on the robots.

    i. Most of the robots have 800x480
    1. Use this link to add lines to the config.txt so the touch screen will
    work.
    2. https://www.waveshare.com/wiki/7inch_HDMI_LCD_(B)
    3. There is a section called working with Raspberry Pi
    ii. If you have one of the 39, 40 robots that are marked with
    1. https://www.waveshare.com/wiki/7inch_HDMI_LCD_(C)

## PI Boards:

Card goes in bottom of board, near front of robot, metal leads are pointing up.

    1. There is a bin in the robot lab that has keyboards and mice, more to come soon.
    2. After you get the image on the SD card there are a few housekeeping elements you
    need to do to get the board to work with the robots.
    a. Open Rasberry-Configuration and turn on:
    i. SSH
    ii. Serial Port
    iii. Change the password to what your team wants.
    iv. Any other items you want set up in the configuration.
    b. Connect the board to MSU-GUEST or MSU-Secure wi-fi
    3. Open up a command prompt and do the following commands to update the board:
    a. sudo apt-get upgrade and sudo apt-get update
    4. Should be ready to go.

Keyboards and mice can be plugged in the USB, but you need to keep the USB to Servo
Controller plugged in and the touch screen plugged in. The USB to the Android plug can be
removed.
The boards will connect to the wifi in room, MSU Guest automatically.
The desktops computers in the room do not have WIFI unfortunately.

I am using Bitvise SSH Client to log in, it has a nice FTP client that comes along with it, free.
When using SSH, make sure you are connecting to correct robot. If you click on wifi icon on
touch screen then click again it will show you the IP address followed by /24 like this:
192.168.1.3/24
No keyboard needed to see IP address, just hold your finger on the wifi icon in top right corner
of the touch screen.

## SD Card Rules:

Every team will get an SD card and you must make a bootable copy of the Raspbian O.S.
configured for our robots. You have to turn the cards back in at the end of the semester.
These SD cards are a little fragile. Rules to live by:
    1. Always keep a copy of your code and any external files on another computer.
    2. I have been shutting down the PI with the touchscreen before I turn off the robot. It’s a
    safer way to turn off robot……..but I have had to hit emergency power off a few times
    and the cards have been fine.
    3. If you have three people that don’t see each other or work together in the same room
    much you can create a second SD card. You will be responsible for getting the second
    card.
        a. Then keep your code on a repository.
    4. If you damage the card I can try to put the image back on, if you damage the card and it
    can’t be repaired you need to purchase your own…..and then turn it in at the end of the
    semester. I bought these for about $8 a piece. (You can ruin about fifty for the price of a
    single textbook, which I didn’t make you buy).
    5. SSH, touch screen and WIFI should be configured and turned on.

Robots
The robots can take off and get out of control quickly. BE CAREFUL.
Make sure you have somebody ready to hit the power switch on back of robot as fast as
possible when working with robots.

When finished with robot plug it in to one of the chargers.
If you notice the green light is on charger, unplug and plug in another one.
Green light is charged, red is charging, and blinking is close to being charged.
You can drive the robots around the building, but make sure you bring them back when you’re
done. Take your robot for a walk, people will think you’re cool, “You have a pet robot?”
Maybe some of you can use the robot to get a date.

# The Assignment:

You will need to create a remote control for your robot as said
in section one of this document.
Remember to use good OO programming to do this.
We will build on to this software as the semester goes on.
Make sure you keep your keyboard input separate than your
control software. Design it with the following in mind, one of
the next assignments is going to program the robot to do
several tasks in a row. You should be able to replace the
keyboard input with a list of instructions for the robot to
complete so the robot controls should be in a class that doesn’t
use any keyboard input. The robot input should come from
other classes then call methods in the Robot Class to control all
aspects of the robot.
For this assignment you should be able to test the following
functions of the robot by pressing keys.

    1. Motors
        a. You should be able to drive the robot forward,
            backwards, and turn left to right with a enough
            precision that you can drive down a hallway easily.
            Turn a corner, do a 180 and drive back down the hall.
    2. Control the waist servo to turn fully in both directions
    3. Control the head tilt and pan to put the head in just about
        any position it can handle.
    4. All of these functions can be done with hitting the keys
        needed several times, each key press will increment the
        amounts small amounts at a time.
    5. Make sure the touch screen is working.
    6. Don’t need to worry about arms on this assignment.
