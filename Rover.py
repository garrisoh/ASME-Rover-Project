"""
Main rover class
"""



import Motor.py
import utiliies.py


def class Rover:
	
	
	wheel_type = "leg"
	
	def __init__(self):
		self.front_left = Motor("P9_14")
		self.front_right = Motor("P9_16")
		self.back_left = Motor("P8_13")
		self.back_right = Motor("P8_19")
	
	def cleanup(self):
		self.front_left.cleanup()
		self.front_right.cleanup()
		self.back_left.cleanup()
		self.back_right.cleanup()
	
	def set_velocities(linear_velocity, angular_velocity):
		"""
		Sets the velocity of the robot
		linear_velocity: Vec2 representing the velocity in the x and y directions
		angular_velocity: float representing the desired angular velocity
		"""
		if(wheel_type != "mecanum" && linear_velocity.x != 0.0):
			print("non-mecanum wheels do not support movement in the x direction. Ignoring x component")
			linear_velocity.x = 0.0
		wheel_to_cog = 1.0	# distance from wheel to center of gravity in x direction plus distance from wheel to center of gravity in y direction.
		
		# clamp speeds if necessary
		max_combined_speed = Math.abs(linear_velocity.x) + Math.abs(linear_velocity.y) + Math.abs(wheel_to_cog * angular_velocity)
		if(max_combined_speed > 1.0):
			linear_velocity /= max_combined_speed
			angular_velocity /= max_combined_speed 
		
		self.front_left.set_speed(linear_velocity.x - linear_velocity.y - wheel_to_cog * angular_velocity)
		self.front_right.set_speed(linear_velocity.x + linear_velocity.y + wheel_to_cog * angular_velocity)
		self.back_left.set_speed(linear_velocity.x + linear_velocity.y - wheel_to_cog * angular_velocity)
		self.back_right.set_speed(linear_velocity.x - linear_velocity.y + wheel_to_cog * angular_velocity)
		


