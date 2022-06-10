import microbit as mb
import machine
import struct
import time
adr = 0x10

class MaqueenPlus:
    def __init__(self):
        self._spd = 0
        mb.i2c.init(freq=100000, sda=mb.pin20, scl=mb.pin19)
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

        # Linetrack sensors
        self.patrol = {
            "L1": 0x04,
            "L2": 0x02,
            "L3": 0x01,
            "R1": 0x08,
            "R2": 0x10,
            "R3": 0x20
        }

    def motorControl(self, mot, dir, spd):
        buf = bytearray(3)
        if mot == self.MT_L:
            buf[0] = 0x00
        else:
            buf[0] = 0x02
        buf[1] = dir
        buf[2] = spd
        mb.i2c.write(adr, buf)

    def servo(self, number, angle):
        buf = bytearray(3)
        if number == self.S1:
            buf[0] = 0x14
            buf[1] = angle
            mb.i2c.write(adr, buf)
        elif number == self.S2:
            buf[0] = 0x15
            buf[1] = angle
            mb.i2c.write(adr, buf)
        else:
            buf[0] = 0x16
            buf[1] = angle
            mb.i2c.write(adr, buf)

    def RGBLight(self, rgbshow, color):
        buf = bytearray(3)
        if rgbshow == self.RGB_L:
            buf[0] = 0x0B
            buf[1] = color
            mb.i2c.write(adr, buf)
        elif rgbshow == self.RGB_R:
            buf[0] = 0x0C
            buf[1] = color
            mb.i2c.write(adr, buf)
        elif rgbshow == self.RGB_ALL:
            buf[0] = 0x0B
            buf[1] = color
            buf[2] = color
            mb.i2c.write(adr, buf)

    def stop(self):
        self.motorControl(self.MT_L, 1, 0)
        self.motorControl(self.MT_R, 1, 0)

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
        # trig_pin = pin2, echo_pin = pin8
        mb.pin2.write_digital(1)
        time.sleep_ms(10)
        mb.pin2.write_digital(0)
        mb.pin8.read_digital()
        t2 = machine.time_pulse_us(mb.pin8, 1, 15000)
        if (t2 > 0):
            distance = 340.29 * (t2 / (2*1000000))
        else:
            distance = 0.75
        return distance

    def getLine(self):
        mb.i2c.write(adr, b'\x1D')
        patrol_y = mb.i2c.read(adr, 1)
        sens = {
            "L1": -1,
            "L2": -1,
            "L3": -1,
            "R1": -1,
            "R2": -1,
            "R3": -1
        }
        for x in self.patrol:
            if((patrol_y[0] & self.patrol[x]) == self.patrol[x]):
                sens[x] = 1
            else:
                sens[x] = 0
        return sens

    def motorSpeed(self, mot):
        mb.i2c.write(adr, b'\x00')
        spd_x = mb.i2c.read(adr, 4)
        return_spd = -1
        if(mot == self.MT_L):
            if(round(spd_x[1]) < 20 and round(spd_x[1]) != 0):
                return_spd = round(spd_x[1]) + 255
            else:
                return_spd = round(spd_x[1])
        elif(mot == self.MT_R):
            if(round(spd_x[3]) < 20 and round(spd_x[3]) != 0):
                return_spd = round(spd_x[3]) + 255
            else:
                return_spd = round(spd_x[3])
        return return_spd

    def getEncoders(self):
        buf = bytearray(1)
        buf[0] = 0x04
        mb.i2c.write(adr, buf)
        return struct.unpack('>HH', mb.i2c.read(adr, 4))

    def clearEncoders(self):
        buf = bytearray(5)
        buf[0] = 0x04
        buf[1] = buf[2] = buf[3] = buf[4] = 0x00
        mb.i2c.write(adr, buf)
