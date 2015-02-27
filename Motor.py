'''
This class allows for 50Hz Pulse Width Modulation (PWM) control of a motor speed controller 
or servo motor using the Beaglebone Black and the Adafruit python library for accessing the
Beaglebone's General Purpose I/O pins (GPIO).  Documentation for these libraries
can be found here:

https://github.com/adafruit/adafruit-beaglebone-io-python
https://github.com/adafruit/Adafruit_Python_GPIO

Author: Haley Garrison
Date: 2/24/14
'''
# Import the Adafruit library.  This has already been installed on the Beaglebone.
import Adafruit_BBIO.PWM as PWM

def class Motor:
	
	FREQ = 50 # PWM frequency in Hz
	DUTY_MIN = 5 # Minimum pulse width as percent of frequency
	DUTY_MAX = 10 # Maximum pulse width as percent of frequency
	DUTY_ZERO = 7.5 # Motor will stop at this point

	def __init__(self, pin, invert=False):
		'''
		Creates a new motor object attached to the given pin on the Beaglebone.  Pin names
		are strings indicating either pin set 8 or 9 and the pin number on that set of pins.
		Each set of pins has pin 1 labeled on the Beaglebone. Available PWM pins are 'P9_14', 
		'P9_16', 'P8_13', 'P8_19', 'P8_34', 'P8_36', 'P8_45', and 'P8_46':
		
		http://2.bp.blogspot.com/-FYgz2ERQq-w/U3ANJLt3XxI/AAAAAAAAClQ/rOrAV70-nA8/s1600/cape-headers-pwm.png
		
		'''
		# Starts PWM on this instance's pin.  Sets the initial speed/duty cycle to the minimum
		self.pin = pin
		self.invert = invert
		PWM.start(pin, Motor.DUTY_ZERO, Motor.FREQ)

	def get_duty_cycle(self, speed):
		'''
		Returns the duty cycle for the speed value between -1 (full backwards) and 
		1 (full forwards)
		'''
		# Clamp speed to +/-1
		if speed > 1:
			speed = 1
		elif speed < -1:
			speed = -1
	
		# Calculate the duty cycle by determining the percent of the max pulse width for the
		# given speed
		return (speed + 1.0) / 2.0 * (Motor.DUTY_MAX - Motor.DUTY_MIN) + Motor.DUTY_MIN
	
	def set_speed(self, speed):
		'''
		This method accepts a floating point value of the speed from -1.0 to 1.0.  -1.0
		causes full backwards movement, 0 stops the motor, and 1.0 causes full forward
		movement.
		'''
		# Invert the speed value if necessary
		if self.invert:
			speed *= -1

		# Get the necessary duty cycle for the speed and set the PWM output to this duty cycle
		duty_cycle = get_duty_cycle(speed)
		PWM.set_duty_cycle(self.pin, duty_cycle)
		
	def cleanup(self):
		'''
		Stops PWM on this motor's pin and calls the Adafruit cleanup method.
		'''
		PWM.stop(self.pin)
		PWM.cleanup()

if __name__ == '__main__':
	'''
	This program is an example of how to use the Motor class and can be used for testing
	motors.
	'''
	# Prompt for the pin number
	pin = raw_input("Enter the motor pin number (Available PWM pins are 'P9_14', \
		'P9_16', 'P8_13', 'P8_19', 'P8_34', 'P8_36', 'P8_45', and 'P8_46'): ")
	motor = Motor(pin)
	
	while True:
		# Prompt for motor speed
		speed = raw_input('Enter the speed from -1.0 to 1.0 or q to quit: ')

		# Quit if q pressed
		if speed == 'q':
			break

		# Set the correct speed
		motor.set_speed(float(speed))
		
	# Cleanup when we are done
	motor.cleanup()
