'''
Created on Oct 26, 2014

This module was created to interface with the L3GD20 Gyroscope
on the Adafruit 10-DOF sensor board.  It is modified from the
original Arduino version to work with the Beaglebone Black using
the Adafruit GPIO library.

@author: Haley Garrison
'''

from Adafruit_I2C import Adafruit_I2C

class Adafruit_L3GD20(Adafruit_I2C):
    '''
    A class representing the L3GD20 Gyroscope.
    Enables reading from the gyros over an I2C
    connection.
    '''
    
    # I2C address of the gyro
    L3GD20_ADDRESS = 0x6B
    
    # Registers addresses
    GYRO_REGISTER_CTRL_REG1 = 0x20
    GYRO_REGISTER_CTRL_REG4 = 0x23
    GYRO_REGISTER_OUT_X_L   = 0x28
    
    # Gyro sensitivity at 250dps
    GYRO_SENSITIVITY_250DPS = 0.00875
    
    # Gyro unit conversion factor
    DPS_TO_RAD = 0.017453293

    def __init__(self, busnum = -1, debug = False):
        '''
        Enables I2C communication with the gyroscope, sets
        the control registers to the appropriate values.
        '''
        # Initialize I2C with the correct address on the given bus no.
        self.gyro = Adafruit_I2C(self.L3GD20_ADDRESS, busnum, debug)
        
        # Set the control registers
        
        # Clear/reset the register
        self.gyro.write8(self.GYRO_REGISTER_CTRL_REG1, 0x00)
        
        # Enable all three axes and set to normal mode (not power down)
        self.gyro.write8(self.GYRO_REGISTER_CTRL_REG1, 0x0F)
        
        # Set the range to the default value (250dps)
        self.gyro.write8(self.GYRO_REGISTER_CTRL_REG4, 0x00)
        
    def gyro16(self, blist, idx):
        '''
        Properly formats the 16 bits of data as an integer.
        '''
        # Low byte is first, shift the high byte up by 8
        n = blist[idx] | (blist[idx + 1] << 8);
        
        # Arduino integer is signed 16 bits, so we need to convert from
        # 16-bit 2's complement to a standard signed 32-bit integer
        return n if n < 32768 else n - 65536
    
    def read(self):
        # Read 6 bytes of data from the gyros
        blist = self.gyro.readList(self.GYRO_REGISTER_OUT_X_L | 0x80, 6)
        
        # Return a tuple with the (x, y, z) gyro readings in rad/s
        res = (self.gyro16(blist, 0) * self.GYRO_SENSITIVITY_250DPS * self.DPS_TO_RAD, 
               self.gyro16(blist, 2) * self.GYRO_SENSITIVITY_250DPS * self.DPS_TO_RAD, 
               self.gyro16(blist, 4) * self.GYRO_SENSITIVITY_250DPS * self.DPS_TO_RAD)
        return res

# A test script to make sure everything works ok      
if __name__ == '__main__':
    from time import sleep
    
    # Create the gyro instance
    l3g = Adafruit_L3GD20()
    
    # Loop, printing the gyro values at 1Hz
    print '(Gyro X, Y, Z) (rad/s)'
    while True:
        print l3g.read()
        sleep(1)
        