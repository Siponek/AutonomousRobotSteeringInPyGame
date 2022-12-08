Python Robot Drunk Driver
================================

Research Track for Robot Rngineering<br>
Author Szymon Zinkowicz

**Introduction**
---
First assignment for Research Track 1 


**Requirements**
---
The simulator requires a Python 2.7 installation, the pygame library, PyPyBox2D, and PyYAML.

**How to run**
---
Type in console:
```
python2 run.py finalAssignment.py
```
**Description**
--
Tasks for the robot:
- constrantly drive the robot around the circuit in the counter clockwise direction
- avoid touching the golden boxes
- when the robot is close to a silver box, it should grab it, and move it behind itself

Due to a bug of the arena it was not possible to run the robot with creating a map for the its movement. Sort of "reactive" behaviour was invented as the robot either must almost bump into gold markers at 90 deg and then using pre-destined instructions turn left or right OR scan for distance of the markers on both sides and turn where the distance is longer.

In this implementation the second version was used. Robot constantly scans the area in certain radius in from of him and on the sides.
The most important aspect of this implementation is to turn and move at the same time since only by that it is possible to move out the robot out of "close zone" to the golden markers.


**Pseudocode**
---
```
while True
	filter out silvers and golds from markers
	check for the closest silvers and golds
	scan for surroundings and calculate the mean distance for left and right
	if silver token is near
		drive to silver token and perform the grab
	elif mean of the left distance is higher:
		if distance to front obstacle is long
			turn to left slower
		else
			turn to left
		
	elif mean of the right distance is higher:
		if distance to front obstacle is long
			turn to right slower
		else
			turn to right
	else
		drive forward
```

**Conceptual movement**
---
![Sketch](https://user-images.githubusercontent.com/91413093/141127749-691f032c-7a15-4409-afa2-11f423f4ec55.png)

:)
