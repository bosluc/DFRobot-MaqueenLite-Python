import microbit
import machine
import time


class Robot:
    def __init__(self):
        self._vit = 0
        microbit.i2c.init(freq=100000, sda=microbit.pin20, scl=microbit.pin19)
        # Motors
        self.MG = 0
        self.MD = 1

        # ServoMotors
        self.S1 = 1
        self.S2 = 2
        self.S3 = 3

        # RGB LED
        self.RGB_G = 1
        self.RGB_D = 2
        self.RGB_G_D = 3
        self.RED = 1,
        self.GREEN = 2,
        self.BLUE = 4,
        self.YELLOW = 3,
        self.PINK = 5,
        self.CYAN = 6,
        self.WHITE = 7,
        self.OFF = 8

        # Line tracking sensors
        self.L1 = 1
        self.L2 = 2
        self.L3 = 5
        self.R1 = 3
        self.R2 = 4
        self.R3 = 6

    def run(self, mot, sens, vit):
        # mot left:0 ; mot right:1
        # sens forward : 1; sens backward :2
        # speed max :255; stop :0
        buf = bytearray(3)
        if mot == self.MG:
            buf[0] = 0x00
        else:
            buf[0] = 0x02
        buf[1] = sens
        buf[2] = vit
        microbit.i2c.write(0x10, buf)

    def servo(self, number, angle):
        """Move a servo for a given angle

        Args:
            number (int): number of the servo to move
            angle (int): rotating angle (min=0  max=180)
        """
        buf = bytearray(3)
        if number == self.S1:
            buf[0] = 0x14
            buf[1] = angle
            microbit.i2c.write(0x10, buf)
        elif number == self.S2:
            buf[0] = 0x15
            buf[1] = angle
            microbit.i2c.write(0x10, buf)
        else:
            buf[0] = 0x16
            buf[1] = angle
            microbit.i2c.write(0x10, buf)

    def RGBLight(self, rgbshow, color):
        """Turn on/off the rbg light of your choice with the color you want.


        Args:
            rgbshow (int): rgb light object attribute defined in the constructor :
                REB_G : left led,
                REB_D : right led,
                REB_G_D : center led

            color (int): color of the led:
                RED,GREEN,
                BLUE,YELLOW,
                PINK,CYAN,
                WHITE, OFF
        """
        buf = bytearray(3)
        if rgbshow == self.RGB_G:
            buf[0] = 0x0B
            buf[1] = color
            microbit.i2c.write(0x10, buf)
        elif rgbshow == self.RGB_D:
            buf[0] = 0x0C
            buf[1] = color
            microbit.i2c.write(0x10, buf)
        elif rgbshow == self.RGB_G_D:
            buf[0] = 0x0B
            buf[1] = color
            buf[2] = color
            microbit.i2c.write(0x10, buf)

    def stop(self):
        """Stop the robot 
        """
        self.run(self.MG, 1, 0)
        self.run(self.MD, 1, 0)
        microbit.display.show('S')

    def direction(self, vit, dir):
        """  
        Move the robot along 4 axis :
            * TD -> forward
            * AR -> backward 
            * G -> left
            * D -> right 

        Args:
            vit(pwm) : 0 -> 255
            dir(string) : "TD" or "AR" or "G" or "D"
        """

        if(dir == "TD"):
            self.run(0, 1, vit)
            self.run(1, 1, vit)

        elif(dir == "D"):
            self.run(0, 1, vit)
            self.run(1, 1, 0)

        elif(dir == "G"):
            self.run(0, 1, 0)
            self.run(1, 1, vit)

        elif(dir == "AR"):
            self.run(0, 2, vit)
            self.run(1, 2, vit)

    def ultrasonic(self):
        """Get the distance between the robot and an object.

        Returns:
            [float]: distance to the object it one is detected else max value.
        """
        #trig_pin = pin1, echo_pin = pin2
        microbit.pin1.write_digital(1)
        time.sleep_ms(10)
        microbit.pin1.write_digital(0)

        microbit.pin2.read_digital()
        t2 = machine.time_pulse_us(microbit.pin2, 1)
        distance = 340.29 * (t2 / (2*1000000))

        return distance

    def readLineSensor(self, sensor_name):
        """Read line tracking state for a given sensor

        Args:
            sensor_name (int): object attribut define in constructor 

        Returns:
            [int]: 0 : black / 1 : white 
        """
        microbit.i2c.write(0x10, b'\x1D')
        # 0x10 -> adresse / 1 -> lecture de 1 byte
        patrol_y = microbit.i2c.read(0x10, 1)
        mark = -1

        if (sensor_name == self.L1):
            if((patrol_y[0] & 0x04) == 0x04):
                mark = 1
            else:
                mark = 0
        if (sensor_name == self.L2):
            if((patrol_y[0] & 0x02) == 0x02):
                mark = 1
            else:
                mark = 0
        if (sensor_name == self.R1):
            if((patrol_y[0] & 0x08) == 0x08):
                mark = 1
            else:
                mark = 0
        if (sensor_name == self.R2):
            if((patrol_y[0] & 0x10) == 0x10):
                mark = 1
            else:
                mark = 0
        if (sensor_name == self.L3):
            if((patrol_y[0] & 0x01) == 0x01):
                mark = 1
            else:
                mark = 0
        if (sensor_name == self.R3):
            if((patrol_y[0] & 0x20) == 0x20):
                mark = 1
            else:
                mark = 0

        return mark

    def motor_speed(self, mot):
        """Get the linear speed of a given motor 

        Args:
            mot (int): object attribut define in constructor (MG, MD)

        Returns:
            [type]: [description]
        """
        microbit.i2c.write(0x10, b'\x00')
        # 0x10 -> adresse / 4 -> lecture de 4 bytes
        speed_x = microbit.i2c.read(0x10, 4)
        return_speed = -1

        # 0 -> G / 1 -> D
        if(mot == self.MG):
            if(round(speed_x[1]) < 20 and round(speed_x[1]) != 0):
                return_speed = round(speed_x[1]) + 255
            else:
                return_speed = round(speed_x[1])

        elif(mot == self.MD):
            if(round(speed_x[3]) < 20 and round(speed_x[3]) != 0):
                return_speed = round(speed_x[3]) + 255
            else:
                return_speed = round(speed_x[3])

        return return_speed
