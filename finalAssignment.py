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
		drive(50, 0.1)
		return False

	elif rot_y < -a_th: # if the robot is not well aligned with the token, we move it on the left or on the right
		print("Left a bit...")
		turn(-10, 0.1)
		return False

	elif rot_y > a_th:
		print("Right a bit...")
		turn(+10, 0.1)
		return False

def turnToMarker(marker,d_th,a_th):
	dist, rot_y = marker.dist, marker.rot_y
	if dist	==	(-1):
		print("I can't see shit...I am gonna turn")
		turn(1,1)
		return False
	elif -a_th<= rot_y <= a_th: # if the robot is well aligned with the token, we go forward
		print("The robot is well aligned with the token, we go forward.")
		return True

	elif rot_y < -a_th: # if the robot is not well aligned with the token, we move it on the left or on the right
		print("Left a bit...")
		turn(-15, 0.1)
		return False

	elif rot_y > a_th:
		print("Right a bit...")
		turn(+15, 0.1)
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
	
doneTokens = []

while(1):
	print("---going for SILVER token---")
	while 1:
		silverList,goldList = vision()
		silverNotDone = markersNotDone(silverList,doneTokens)
		if len(silverNotDone) == 0:
			closestSilver = min(silverList, key=lambda x: x.dist)
		else:
			closestSilver = min(silverNotDone, key=lambda x: x.dist)
		closestGold = min(goldList, key=lambda x: x.dist)

		# print("rot_y GOLD:	",			closestGold.rot_y)
		# print("dist GOLD:	",			closestGold.dist)
		# print("rot_y SILVER:	",	closestSilver.rot_y)
		# print("dist SILVER:	",		closestSilver.dist)
		scanGoldLeft = []
		scanGoldRight = []
		coneAngle1 = 0
		coneAngle2 = 60
		markers = R.see()
		scanFRONT = []
		for x in markers:
			if x.dist <= 3 and x.rot_y >= coneAngle1 and x.rot_y <= coneAngle2 :
				scanGoldRight.append(x.dist)
		for x in markers:
			if x.dist <= 3 and x.rot_y <= -coneAngle1 and x.rot_y >= -coneAngle2 :
				scanGoldLeft.append(x.dist)
		for x in markers:
			if abs(x.rot_y)>= 0 and abs(x.rot_y)<= 45:
				scanFRONT.append(x.dist)
				print(x.info.marker_type)
		print("Mean of distance to gold markers, front:	", sum(scanFRONT)/len(scanFRONT) )
		print("Distance to gold marker:	", closestGold.dist )
		print("abount of markers in front:", len(scanFRONT))

		# try:
		# # 	if sum(scanFRONT)/len(scanFRONT) < closestGold.dist+0.5 :
		# # 		print("Mean of left side : 		", sum(scanGoldLeft)/len(scanGoldLeft))
		# # 		print("Mean of right side : 	", sum(scanGoldRight)/len(scanGoldRight))
		# # 		try:
		# # 			if (sum(scanGoldLeft)/len(scanGoldLeft))-(sum(scanGoldRight)/len(scanGoldRight)) < 0:
		# # 				turn(15,0.1)
		# # 				print("turning left")
		# # 			elif (sum(scanGoldLeft)/len(scanGoldLeft)) - (sum(scanGoldRight)/len(scanGoldRight)) > 0:
		# # 				turn(-15,0.1)
		# # 				print("turning right")
		# # 			else:
		# # 				pass
		# # 		except:
		# # 			pass
		# # 	if closestSilver.dist <= 2*d_th:
		# # 		print("about to go to markerSilver")
		# # 		if closestSilver.dist < 2*d_th and driveToMarker(closestSilver, d_th, a_th) == True: #CATCHED THE MARKER
		# # 			doneTokens.append(closestSilver)
		# # 			print("Appeding doneTokens...")
		# # 			break
		# # 	else:
		# # 		print("== Driving straight 50 ==")
		# # 		drive(50,0.1)
		# # except:
		# # 	print("fuck this")

		try:
			if closestSilver.dist <= 2*d_th:
				print("about to go to markerSilver")
				if closestSilver.dist <= 2*d_th and driveToMarker(closestSilver, d_th, a_th) == True: #CATCHED THE MARKER
					doneTokens.append(closestSilver)
					print("Appeding doneTokens...")
					break
			elif min(scanFRONT, key=lambda x: x) < 1:
				print("Mean of left side : 	", sum(scanGoldLeft)/len(scanGoldLeft))
				print("Mean of right side : ", sum(scanGoldRight)/len(scanGoldRight))
				try:
					if (sum(scanGoldLeft)/len(scanGoldLeft)) < (sum(scanGoldRight)/len(scanGoldRight)):
						turn(20,0.1)
						print("---turning right---")
					elif (sum(scanGoldLeft)/len(scanGoldLeft)) > (sum(scanGoldRight)/len(scanGoldRight)):
						turn(-20,0.1)
						print("---turning left---")
					else:
						print("passing")
						pass
				except:
					print("except...")
					pass
			else:
				print("== Driving straight 50 ==")
				drive(30,0.1)
		except:
			print("fuck this")
			drive(30,0.1)
