import microbit
import machine
import struct
import time
I2caddr = 0x10

class MaqueenPlus:
    def __init__(self):
        self._spd = 0
        microbit.i2c.init(freq=100000, sda=microbit.pin20, scl=microbit.pin19)
        # Motors
        self.MT_L = 0
        self.MT_R = 1

        # ServoMotors
        self.S1 = 1
        self.S2 = 2
        self.S3 = 3

        # RGB LED
        self.RGB_L = 1
        self.RGB_R = 2
        self.RGB_ALL = 3
        self.RED = 1
        self.GREEN = 2
        self.BLUE = 4
        self.YELLOW = 3
        self.PINK = 5
        self.CYAN = 6
        self.WHITE = 7
        self.OFF = 8

        # Line tracking sensors
        self.L1 = 1
        self.L2 = 2
        self.L3 = 5
        self.R1 = 3
        self.R2 = 4
        self.R3 = 6

    def motorControl(self, mot, dir, spd):

        buf = bytearray(3)
        if mot == self.MT_L:
            buf[0] = 0x00
        else:
            buf[0] = 0x02
        buf[1] = dir
        buf[2] = spd
        microbit.i2c.write(I2caddr, buf)

    def servo(self, number, angle):
        buf = bytearray(3)
        if number == self.S1:
            buf[0] = 0x14
            buf[1] = angle
            microbit.i2c.write(I2caddr, buf)
        elif number == self.S2:
            buf[0] = 0x15
            buf[1] = angle
            microbit.i2c.write(I2caddr, buf)
        else:
            buf[0] = 0x16
            buf[1] = angle
            microbit.i2c.write(I2caddr, buf)

    def RGBLight(self, rgbshow, color):
        buf = bytearray(3)
        if rgbshow == self.RGB_L:
            buf[0] = 0x0B
            buf[1] = color
            microbit.i2c.write(I2caddr, buf)
        elif rgbshow == self.RGB_R:
            buf[0] = 0x0C
            buf[1] = color
            microbit.i2c.write(I2caddr, buf)
        elif rgbshow == self.RGB_ALL:
            buf[0] = 0x0B
            buf[1] = color
            buf[2] = color
            microbit.i2c.write(I2caddr, buf)

    def stop(self):
        self.motorControl(self.MT_L, 1, 0)
        self.motorControl(self.MT_R, 1, 0)
        microbit.display.show('S')

    def move(self, dir, spd):
        if(dir == "F"):
            self.motorControl(self.MT_L, 1, spd)
            self.motorControl(self.MT_R, 1, spd)

        elif(dir == "L"):
            self.motorControl(self.MT_L, 1, spd)
            self.motorControl(self.MT_R, 1, 0)

        elif(dir == "R"):
            self.motorControl(self.MT_L, 1, 0)
            self.motorControl(self.MT_R, 1, spd)

        elif(dir == "B"):
            self.motorControl(self.MT_L, 2, spd)
            self.motorControl(self.MT_R, 2, spd)

    def ultrasonic(self):
        #trig_pin = pin2, echo_pin = pin8
        microbit.pin2.write_digital(1)
        time.sleep_ms(10)
        microbit.pin2.write_digital(0)

        microbit.pin8.read_digital()
        t2 = machine.time_pulse_us(microbit.pin8, 1, 15000)
        if (t2 > 0):
            distance = 340.29 * (t2 / (2*1000000))
        else:
            distance = 0.75

        return distance

    def readLineSensor(self, sensor_name):
        microbit.i2c.write(I2caddr, b'\x1D')
        # 0x10 -> adresse / 1 -> lecture de 1 byte
        patrol_y = microbit.i2c.read(I2caddr, 1)
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

    def motorSpeed(self, mot):
        microbit.i2c.write(I2caddr, b'\x00')
        speed_x = microbit.i2c.read(I2caddr, 4)
        return_speed = -1

        if(mot == self.MT_L):
            if(round(speed_x[1]) < 20 and round(speed_x[1]) != 0):
                return_speed = round(speed_x[1]) + 255
            else:
                return_speed = round(speed_x[1])

        elif(mot == self.MT_R):
            if(round(speed_x[3]) < 20 and round(speed_x[3]) != 0):
                return_speed = round(speed_x[3]) + 255
            else:
                return_speed = round(speed_x[3])

        return return_speed

    def getEncoders(self):
        buf = bytearray(1)
        buf[0] = 0x04
        microbit.i2c.write(I2caddr, buf)
        return struct.unpack('>HH', i2c.read(I2caddr, 4))
