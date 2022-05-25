# DFRobot-Maqueenplus-Python

Python library for maqueenplus robot developed by DFRobot. 

This library is a python version of the one proposed by DFRobot used for block coding. 

This version has been developed for students to let them play and enjoy coding this nice little robot.

Link to DFRobot page : [https://www.dfrobot.com/product-2026.html]

# Usage 

- Create robot object

Instantiate the robot object 

```python
import microbit
import lib_robot_maqueen as mqn
import time #can be removed if not used
import struct

mq = mqn.MaqueenPlus()
```

# Methods 

- Move the robot

Move the robot along 4 axis :
    * F -> forward
    * B -> backward 
    * L -> left
    * R -> right 

Function definition :
```python
def move(speed, dir):
    """
    speed(pwm) : 0 -> 255
    dir(string) : "F" or "B" or "L" or "R"
    """
```

Example :
```python 
    mq.move(70, "F")
    time.sleep(1) #wait for 1s
    mq.move(70, "R")
```

To move the robot you can also use the motorControl method.

Function definition :
```python
def motorControl(self, mot, dir, spd):
    """
        mot left: MT_L ; mot right: MT_R
        dir (forward): 1; dir (backward): 2
        spd max: 255; stop: 0
    """
```

Example :
```python 
    mq.motorControl(mq.MT_L,2,50)
    mq.motorControl(mq.MT_R,2,70)
```

- Stop 

Stop the robot 

Function definition:
```python
    def stop(self):
        """Stop the robot 
        """
```

Example:
```python
    mq.stop()
```

- Control ServoMotor

You can move three servos with the version of the library, S1, S2, S3.

Function definition:
```python
    def servo(self, number, angle):
        """Move a servo for a given angle

        Args:
            number (int): number of the servo to move
            angle (int): rotating angle (min=0  max=180)
        """
```

Example:
```python
    mq.servo(mq.S3,90)
    time.sleep(1)
    mq.servo(mq.S3,0)
```

- Line tracking sensor

Read line tracking sensor state for a given sensor.
All the functions proposed by DFRobot have not been implemented.
It is up to you to do so.

Function declaration:
```python
    def readLineSensor(self, sensor_name):
        """Read line tracking state for a given sensor

        Args:
            sensor_name (int): object attribut define in constructor (R1,R2,R3,L1,L2,L3)

        Returns:
            [int]: 0 : black / 1 : white 
        """
```

Example:
```python
    #Read R1 (Right #1) line tracking sensor state
    state = mq.readLineSensor(mq.R1)
    
    #you can display the value by doing :
    #display.show(state)
```

- Ultrasonic sensor 

Get the distance between the robot and an object.

Function defition:
```python
    def ultrasonic(self):
        """Get the distance between the robot and an object.

        Returns:
            [float]: distance to the object if one is detected else max value.
        """
```

Example:

```python
    distance = mq.ultrasonic()
```

- Motor Speed 

Get the linear speed of a given motor. 
INFO : This method has no been tested yet but you can test it and set an issue for feedback. 


Function defition:
```python
    def motorSpeed(self, mot):
        """Get the linear speed of a given motor 

        Args:
            mot (int): object attribute define in the constructor (MG, MD)

        Returns:
            [type]: [description]
        """
```

Example:

```python
    mq.move(70, "F")
    time.sleep(1) #delay is necessary. Otherwise the robot read the speed before the motor started.
    spd = mq.motorSpeed(mq.MT_L)
    display.show(str(spd))
    time.sleep(5)
    mq.stop()
```

- RGB Lights
Turn on/off the rbg light of your choice with the color you want.

* RGB LED choice:
RGB_L : left led,
RGB_R : right led,
RGB_ALL : both leds

* Color choice:
RED,
GREEN,
BLUE,
YELLOW,
PINK,
CYAN,
WHITE,
OFF

Function declaration:
```python
    def RGBLight(self, rgbshow, color):
        """Turn on/off the rbg light of your choice with the color you want.


        Args:
            rgbshow (int): rgb light object attribute defined in the constructor :
                RGB_L : left led,
                RGB_R : right led,
                RGB_ALL : both leds

            color (int): color of the led:
                RED,GREEN,
                BLUE,YELLOW,
                PINK,CYAN,
                WHITE, OFF
        """
```

Example:
```python
    mq.RGBLight(mq.RGB_L,mq.RED)
```


# Updates 
One major update that should be added soon concerns the rotation movements of the robot. In fact, when we ask the robot to move right of left no information is given concerning the angle to rotate. Only time.sleep(_) is used actually which is not accurate.
