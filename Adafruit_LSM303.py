#!/usr/bin/python

# Python library for Adafruit Flora Accelerometer/Compass Sensor (LSM303).
# This is pretty much a direct port of the current Arduino library and is
# similarly incomplete (e.g. no orientation value returned from read()
# method).  This does add optional high resolution mode to accelerometer
# though.

# Copyright 2013 Adafruit Industries

# Permission is hereby granted, free of charge, to any person obtaining a
# copy of this software and associated documentation files (the "Software"),
# to deal in the Software without restriction, including without limitation
# the rights to use, copy, modify, merge, publish, distribute, sublicense,
# and/or sell copies of the Software, and to permit persons to whom the
# Software is furnished to do so, subject to the following conditions:

# The above copyright notice and this permission notice shall be included
# in all copies or substantial portions of the Software.

# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL
# THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING
# FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER
# DEALINGS IN THE SOFTWARE.
#
# Modified 10/26/14 by Haley Garrison:
#     Included unit conversion
#     Fixed self parameter issue with setMagGain
#     Initialized the mag gain in the constructor
#     Removed unimplemented mag orientation

from Adafruit_I2C import Adafruit_I2C


class Adafruit_LSM303(Adafruit_I2C):

    # Minimal constants carried over from Arduino library
                                                # Default    Type
    LSM303_ADDRESS_ACCEL = (0x32 >> 1)          # 0011001x
    LSM303_ADDRESS_MAG   = (0x3C >> 1)          # 0011110x
    LSM303_REGISTER_ACCEL_CTRL_REG1_A = 0x20    # 00000111   rw
    LSM303_REGISTER_ACCEL_CTRL_REG4_A = 0x23    # 00000000   rw
    LSM303_REGISTER_ACCEL_OUT_X_L_A   = 0x28
    LSM303_REGISTER_MAG_CRB_REG_M     = 0x01
    LSM303_REGISTER_MAG_MR_REG_M      = 0x02
    LSM303_REGISTER_MAG_OUT_X_H_M     = 0x03

    # Gain settings for setMagGain()
    LSM303_MAGGAIN_1_3 = 0x20 # +/- 1.3
    # LSM303_MAGGAIN_1_9 = 0x40 # +/- 1.9
    # LSM303_MAGGAIN_2_5 = 0x60 # +/- 2.5
    # LSM303_MAGGAIN_4_0 = 0x80 # +/- 4.0
    # LSM303_MAGGAIN_4_7 = 0xA0 # +/- 4.7
    # LSM303_MAGGAIN_5_6 = 0xC0 # +/- 5.6
    # LSM303_MAGGAIN_8_1 = 0xE0 # +/- 8.1
    
    # Conversion values
    LSM303_ACCEL_MG_LSB = 0.001         # 1 millig per lsb
    GRAVITY_EARTH = 9.80665             # in m/s^2
    LSM303_MAG_GAUSS_LSB_XY = 1100.0    # lsb per gauss? at gain +/- 1.3
    LSM303_MAG_GAUSS_LSB_Z  = 980.0     # lsb per gauss? at gain +/- 1.3
    GAUSS_TO_MICROTESLA = 100           # 100 uT/gauss


    def __init__(self, busnum=-1, debug=False, hires=False):

        # Accelerometer and magnetometer are at different I2C
        # addresses, so invoke a separate I2C instance for each
        self.accel = Adafruit_I2C(self.LSM303_ADDRESS_ACCEL, busnum, debug)
        self.mag   = Adafruit_I2C(self.LSM303_ADDRESS_MAG  , busnum, debug)

        # Enable the accelerometer - Changed from 0x27 to 0x57 to keep consistent
        # with the Arduino code, not sure what the difference is, but the Arduino
        # code mentions some setting at 100Hz.
        self.accel.write8(self.LSM303_REGISTER_ACCEL_CTRL_REG1_A, 0x57)
        # Select hi-res (12-bit) or low-res (10-bit) output mode.
        # Low-res mode uses less power and sustains a higher update rate,
        # output is padded to compatible 12-bit units.
        if hires:
            self.accel.write8(self.LSM303_REGISTER_ACCEL_CTRL_REG4_A,
              0b00001000)
        else:
            self.accel.write8(self.LSM303_REGISTER_ACCEL_CTRL_REG4_A, 0)
  
        # Enable the magnetometer
        self.mag.write8(self.LSM303_REGISTER_MAG_MR_REG_M, 0x00)
        
        # Set the gain on the magnetometer to default value
        self.setMagGain()
        

    # Interpret signed 12-bit acceleration component from list
    def accel12(self, blist, idx):
        n = blist[idx] | (blist[idx+1] << 8) # Low, high bytes
        if n > 32767: n -= 65536           # 2's complement signed
        return n >> 4                      # 12-bit resolution


    # Interpret signed 16-bit magnetometer component from list
    def mag16(self, blist, idx):
        n = (blist[idx] << 8) | blist[idx+1]   # High, low bytes
        return n if n < 32768 else n - 65536 # 2's complement signed


    def read(self):
        # Read the accelerometer
        blist = self.accel.readList(
          self.LSM303_REGISTER_ACCEL_OUT_X_L_A | 0x80, 6)
        res = [( self.accel12(blist, 0) * self.LSM303_ACCEL_MG_LSB * self.GRAVITY_EARTH,
                 self.accel12(blist, 2) * self.LSM303_ACCEL_MG_LSB * self.GRAVITY_EARTH,
                 self.accel12(blist, 4) * self.LSM303_ACCEL_MG_LSB * self.GRAVITY_EARTH )]

        # Read the magnetometer
        blist = self.mag.readList(self.LSM303_REGISTER_MAG_OUT_X_H_M, 6)
        res.append((self.mag16(blist, 0) / self.LSM303_MAG_GAUSS_LSB_XY * self.GAUSS_TO_MICROTESLA,
                    self.mag16(blist, 2) / self.LSM303_MAG_GAUSS_LSB_XY * self.GAUSS_TO_MICROTESLA,
                    self.mag16(blist, 4) / self.LSM303_MAG_GAUSS_LSB_Z * self.GAUSS_TO_MICROTESLA))

        return res


    def setMagGain(self, gain=LSM303_MAGGAIN_1_3):
        self.mag.write8(self.LSM303_REGISTER_MAG_CRB_REG_M, gain)


# Simple example prints accel/mag data once per second:
if __name__ == '__main__':

    from time import sleep

    lsm = Adafruit_LSM303()

    print '[(Accelerometer X, Y, Z), (Magnetometer X, Y, Z)]'
    while True:
        print lsm.read()
        sleep(1) # Output is fun to watch if this is commented out