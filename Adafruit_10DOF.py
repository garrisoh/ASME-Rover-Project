'''
Created on Oct 26, 2014

A modified version of the Adafruit 10-DOF Arduino library
for compatibility with the beaglebone black.

@author: Haley Garrison
'''
from Adafruit_L3GD20 import Adafruit_L3GD20
from Adafruit_LSM303 import Adafruit_LSM303
from Adafruit_BMP085 import BMP085
from math import atan, atan2, sqrt, pi, sin, cos, pow

class Adafruit_10DOF(object):
    '''
    This class provides methods for getting raw data and orientation
    data from each of the sensors on the Adafruit 10-DOF board.
    It also provides a fusion orientation method that fuses accelerometer
    and magnetometer data for determining pitch, roll, and heading
    '''
    
    # Average sea level pressure in hPa
    PRESSURE_SEALEVELHPA = 1013.25
    
    def __init__(self):
        '''
        Initializes the sensors on the 10-DOF board
        '''
        # Create instances of each of the sensors
        self.accelMag = Adafruit_LSM303()
        self.gyro = Adafruit_L3GD20()
        self.barom = BMP085()
        
    def accel_get_orientation(self):
        '''
        Get pitch and roll values in degrees as a tuple:
        (pitch, roll)
        '''
        (x, y, z) = self.accel_get_raw()
        sign_of_z = z if z > 0 else -1
        
        # Calculate pitch and roll, convert to degrees
        pitch = -atan2(y, sqrt(x * x + z * z)) * 180 / pi
        roll = atan2(x, sign_of_z * sqrt(y * y + z * z)) * 180 / pi
        
        return (pitch, roll)
    
    def accel_get_raw(self):
        '''
        Gets the raw (x, y, z) accelerometer data in units of m/s^2
        '''
        return self.accelMag.read()[0]
        
    def mag_get_orientation(self):
        '''
        Gets the heading of the board in degrees from magnetic north on z-axis
        '''
        (x, y, ) = self.mag_get_raw()
        return atan2(y, x) * 180 / pi
    
    def mag_get_raw(self):
        '''
        Gets the raw (x, y, z) heading in degrees along each axis from magnetic north
        '''
        return  self.accelMag.read()[1]
    
    def gyro_get_raw(self):
        '''
        Gets the raw (x, y, z) gyro data in rad/s on each axis
        '''
        return self.gyro.read()
    
    def fusion_get_orientation(self):
        '''
        Fuses data from accelerometer and magnetometer.  Same algorithm as the
        original Adafruit 10-DOF function except pitch = -roll and roll = pitch
        since this makes much more sense for the board layout.
        Returns a tuple of (pitch, roll, heading)
        '''
        # Calculate pitch based only on accel
        (accelX, accelY, accelZ) = self.accel_get_raw()
        pitch = -atan2(accelY, accelZ)
        
        # Calculate roll based on pitch and accel
        if accelY * sin(-pitch) + accelZ * cos(-pitch) == 0:
            roll = pi / 2 if accelX > 0 else -pi / 2
        else:
            roll = atan(-accelX / (accelY * sin(-pitch) + accelZ * cos(-pitch)))
            
        # Calculate heading based on pitch, roll, and mag
        (magX, magY, magZ) = self.mag_get_raw()
        heading = atan2(magZ * sin(-pitch) - magY * cos(-pitch), 
                        magX * cos(roll) +
                        magY * sin(roll) * sin(-pitch) +
                        magZ * sin(roll) * cos(-pitch))
        
        return (pitch * 180 / pi, roll * 180 / pi, heading * 180 / pi)
    
    def get_pressure(self):
        '''
        Gets the pressure in Pa
        '''
        return self.barom.read_pressure()
    
    def get_temperature(self):
        '''
        Gets the temperature in degrees C
        '''
        return self.barom.read_temperature()
    
    def get_altitude(self):
        '''
        Gets the approximate altitude above sea level in m
        '''
        press = self.get_pressure()
        temp = self.get_temperature()
        return ((pow((self.PRESSURE_SEALEVELHPA / press), 0.190223) - 1) * (temp + 273.15)) / 0.0065
        
    