from __future__ import print_function

import time
from sr.robot import *

a_th = 2.0
""" float: Threshold for the control of the orientation"""

d_th = 0.4
""" float: Threshold for the control of the linear distance"""

R = Robot()
""" instance of the class Robot"""

def drive(speed, seconds):
	"""
	Function for setting a linear velocity

	Args: speed (int): the speed of the wheels
	  seconds (int): the time interval
	"""
	R.motors[0].m0.power = speed
	R.motors[0].m1.power = speed
	time.sleep(seconds)
	R.motors[0].m0.power = 0
	R.motors[0].m1.power = 0

def turn(speed, seconds):
    """
    Function for setting an angular velocity

    Args: speed (int): the speed of the wheels
	  seconds (int): the time interval
    """
    R.motors[0].m0.power = speed
    R.motors[0].m1.power = -speed
    time.sleep(seconds)
    R.motors[0].m0.power = 0
    R.motors[0].m1.power = 0

def turnMove(speed, direction):
	print("DIRECTION", direction)
	if (direction == 'RIGHT'):

		R.motors[0].m0.power = speed
		R.motors[0].m1.power = speed/4
	elif (direction == 'LEFT'):

		R.motors[0].m0.power = speed/4
		R.motors[0].m1.power = speed
	time.sleep(0.01)

def find_token():
	"""
	Function to find the closest token

	Returns:
	dist (float): distance of the closest token (-1 if no token is detected)
	rot_y (float): angle between the robot and the token (-1 if no token is detected)
	"""
	dist=100
	for token in R.see():
		if token.dist < dist:
			dist=token.dist
		rot_y=token.rot_y
	if dist==100:
		return -1, -1
	else:
		return dist, rot_y

def driveToMarker(d_th,a_th):
	while True:
		silverList,_ = vision()
		silverList = filter(lambda x: abs(x.rot_y)<120, silverList)
		closestSilver = min(silverList, key=lambda x: x.dist)
		dist, rot_y = closestSilver.dist, closestSilver.rot_y
		if dist	==	(-1):
			print("I can't see *anything*...I am gonna turn")
			turn(1,1)

			# if no markers are detected, the program ends
		elif dist <= d_th:
			print("Found it!")
			R.grab() # if we are close to the token, we grab it.
			print("Grabbing.")
			print("Truning..")
			turn(60,1)
			if R.release() == True:

				print("Releasing...")
				turn(-60,1)
				# drive(60,0.5)
				break
		elif -a_th<= rot_y <= a_th: # if the robot is well aligned with the token, we go forward
			print("The robot is well aligned with the token, we go forward.")
			drive(50, 0.1)

		elif rot_y < -a_th: # if the robot is not well aligned with the token, we move it on the left or on the right
			print("Left a bit...")
			turn(-10, 0.1)

		elif rot_y > a_th:
			print("Right a bit...")
			turn(+10, 0.1)

# def markersNotDone(silverList,doneTokens):
# 	silverNotDone = []
# 	for silverToken in silverList:
# 		add = True
# 		for doneToken in doneTokens:
# 			if doneToken.info.offset == silverToken.info.offset:
# 				add = False
# 				break
# 		if add:
# 			silverNotDone.append(silverToken)
# 	return silverNotDone

def vision():
	silverList = []
	goldList = []
	for token in R.see():
		if token.info.marker_type == MARKER_TOKEN_SILVER:
			silverList.append(token)
		elif token.info.marker_type == MARKER_TOKEN_GOLD:
			goldList.append(token)
		while token.dist == -1:
			turn(1,1)
			R.see()
	return silverList, goldList

def scanSurroundings(coneAngle1,coneAngle2):
	markers = R.see()
	scanGoldRight = []
	scanGoldLeft = []
	for x in markers: #scanning for markers on right side
		if x.dist <= 2 and x.rot_y >= coneAngle1 and x.rot_y <= coneAngle2 :
			scanGoldRight.append(x.dist)
	for x in markers: #scanning for markers on left side
		if x.dist <= 2 and x.rot_y <= -coneAngle1 and x.rot_y >= -coneAngle2 :
			scanGoldLeft.append(x.dist)
	return scanGoldLeft, scanGoldRight

def main():
	while(1):
		print("--- going for SILVER token ---")
		while 1:
			silverList,goldList = vision()
			closestSilver = min(silverList, key=lambda x: x.dist)
			closestGold = min(goldList, key=lambda x: x.dist)

			meanRight = 100
			meanLeft = 100
			scanGoldLeft, scanGoldRight = scanSurroundings(0,100)

			if len(scanGoldRight) != 0:
				meanRight = sum(scanGoldRight)/len(scanGoldRight)
			if len(scanGoldLeft) != 0:
				meanLeft = sum(scanGoldLeft)/len(scanGoldLeft)
				
			silverList = filter(lambda x: abs(x.rot_y)<120, silverList)
			closestSilver = min(silverList, key=lambda x: x.dist)

			if closestSilver.dist < 2*d_th: #CATCHED THE MARKER
				print("Driving to silver marker...")
				driveToMarker(d_th, a_th)

			elif meanLeft > meanRight:
				if min(scanGoldRight)>1.5:
					turnMove(25, "LEFT")
				else:
					turnMove(100, "LEFT")
			else:
				if min(scanGoldLeft)>1.5:

					turnMove(25,"RIGHT")
				else:
					turnMove(100,"RIGHT")
			print("FORWARD")
			drive(100,0.009)
main()
