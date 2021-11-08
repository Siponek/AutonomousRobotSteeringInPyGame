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

def closestMarker(listOf):

	res = min(listOf, key=lambda x: x.dist)
	return res

def driveToMarker(marker,d_th,a_th):
	dist, rot_y = marker.dist, marker.rot_y
	if dist	==	(-1):
		print("I can't see shit...I am gonna turn")
		turn(1,1)
		return False

		# if no markers are detected, the program ends
	elif dist <	d_th:
		print("Found it!")
		R.grab() # if we are close to the token, we grab it.
		print("Grabbing.")
		print("Truning..")
		turn(60,1)
		R.release()
		print("Releasing...")
		turn(-60,1)
		return True
	elif -a_th<= rot_y <= a_th: # if the robot is well aligned with the token, we go forward
		print("The robot is well aligned with the token, we go forward.")
		drive(15, 0.5)
		return False

	elif rot_y < -a_th: # if the robot is not well aligned with the token, we move it on the left or on the right
		print("Left a bit...")
		turn(-2, 0.3)
		return False

	elif rot_y > a_th:
		print("Right a bit...")
		turn(+2, 0.3)
		return False

def markersNotDone(silverList,doneTokens):
	silverNotDone = []
	for silverToken in silverList:
		add = True
		for doneToken in doneTokens:
			if doneToken.info.offset == silverToken.info.offset:
				add = False
				break
		if add:
			silverNotDone.append(silverToken)
	return silverNotDone


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



# markers = R.see()
# print ("I can see", len(markers), "markers:")
#
# for m in markers:
#     if m.info.marker_type in (MARKER_TOKEN_GOLD, MARKER_TOKEN_SILVER):
#         print (" - Token {0} is {1} metres away, type : {2}".format( m.info.offset, m.dist, m.info.marker_type ))
#     elif m.info.marker_type == MARKER_ARENA:
#         print (" - Arena marker {0} is {1} metres away".format( m.info.offset, m.dist ))
doneTokens = []

while(1):
	print("going for SILVER token")
	while 1:
		silverList,goldList = vision()

		silverNotDone = markersNotDone(silverList,doneTokens)

		if len(silverNotDone) == 0:
			closestSilver = min(silverList, key=lambda x: x.dist)
		else:
			closestSilver = min(silverNotDone, key=lambda x: x.dist)
		closestGold = min(goldList, key=lambda x: x.dist)

		print("rot_y :	",			closestGold.rot_y)
		print("dist :	",			closestGold.dist)
		print("rot_y SILVER:	",	closestSilver.rot_y)
		print("dist SILVER:	",		closestSilver.dist)

		if closestGold.dist < 0.48 and abs(closestGold.rot_y) < 90:
			print("--GOING BACK--")
			drive(-20,0.5)
		if closestGold.dist < 0.6:
			if abs(closestSilver.rot_y) > 90:
				if closestSilver.rot_y > 0:
					bias = "left"
				elif closestSilver.rot_y <= 0:
					bias = "right"
			print("Bias is:	", bias)
			# if abs(closestGold.rot_y) <= 90 :
			# 	print("Driving 168 line")
			#
			# 	if closestGold.rot_y > 0:
			# 		turn(20,0.1)
			# 		print("Truning right")
			# 	elif closestGold.rot_y <= 0:
			# 		turn(-20,0.1)
			# 		print("Truning left")
			if abs(closestGold.rot_y) <= 90 :
				print("$$$ Gold rot_y smaller than 90 $$$")
				if closestSilver.dist <= 3 and abs(closestGold.rot_y) >=30:
					if driveToMarker(closestSilver, d_th, a_th) == True: #CATCHED THE MARKER
						doneTokens.append(closestSilver)
						print("appeding doneTokens...")
						break
				elif closestGold.rot_y <= 0:
					turn(20,0.1)
				else:
					turn(-20,0.1)
				# if bias == "left":
				# 	turn(10,0.1)
				# 	print("Truning right")
				# else:
				# 	turn(-10,0.1)
				# 	print("Truning left")
			else:
				print("----Driving 50----")
				drive(50,0.1)

		elif closestSilver.dist <= 3*d_th:
			print("about to go to markerSilver")
			if driveToMarker(closestSilver, d_th, a_th) == True: #CATCHED THE MARKER
				doneTokens.append(closestSilver)
				print("appeding doneTokens...")
				break
		else:
			print("### Driving forward 80 ###")
			drive(80,0.1)
