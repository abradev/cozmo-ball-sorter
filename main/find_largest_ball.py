from collections import deque
from imutils.video import VideoStream
from numpy import sqrt, array
import argparse
import cv2
import imutils
from time import sleep, perf_counter
from math import inf

import cozmo
from cozmo.util import degrees

def cozmo_program(robot: cozmo.robot.Robot):
	colors = {'Green': ([26, 109, 206], [38, 129, 246])}   # with red after effect
	# greenLower = (47, 54, 10)
	# greenUpper = (80, 155, 150) 
	#opencv uses 0 360 as the range for hue
	# 0-255 as the range for sat and value
	robot.camera.color_image_enabled = True #turn on color
	robot.camera.image_stream_enabled = True #turn on camera feed
	robot.set_head_angle(degrees(0)).wait_for_completed()
	sleep(2.0)

	start = perf_counter()
	final_degree, largest_contour = 0, 0.1
	rotate = 360 // 8
	for degree in range(0, 360, rotate):
		print("-At", degree, "degrees")
		image = robot.world.latest_image.raw_image 
		frame = cv2.cvtColor(array(image), cv2.COLOR_RGB2BGR)
		fname = "camera image: " + str(degree)
		cv2.imshow(fname,frame)
		cv2.waitKey(1000)
		for color, bounds in colors.items():
			contour_size = get_cont(image, bounds)
			print("---Search for %s Complete" % color)
			#need to check that its a ball, etc  //kathline's shape recognition code
			if contour_size > largest_contour:
				final_degree, largest_contour = degree, contour_size
		robot.turn_in_place(degrees(rotate)).wait_for_completed() # rotate n degrees counterclockwise
	print("Largest Contour Size:", largest_contour)
	print("Found at %d degrees" % final_degree)

	robot.turn_in_place(degrees(final_degree)).wait_for_completed()
	print("total time for cycle", perf_counter()-start)
	# image = robot.world.latest_image.raw_image 
	# frame = cv2.cvtColor(array(image), cv2.COLOR_RGB2BGR)
	# frame = cv2.resize(frame, (640, 480))
	# cv2.imshow("final image",frame)
	# cv2.waitKey(4000)




def get_cont(img, bounds):
	#  initialize the list of tracked points	
	# cntr_ind = 0
	# to_return = -1
	frame = cv2.cvtColor(array(img), cv2.COLOR_RGB2BGR)
	# frame = imutils.resize(frame, width=600) # resize the frame

	# try:
	cs = generate_contours(frame, bounds[0], bounds[1])
		# cs = cv2.contourArea(max(pre_sort, key=cv2.contourArea))
		# hsv_frame = cv2.cvtColor(array(img), cv2.COLOR_RGB2HSV)
		# mask = cv2.inRange(hsv_frame, bounds[0], bounds[1])
	print("--Size:", cs)
	return cs
	# except ValueError:
		# return 0
		
	# for c in sorted(pre_sort, key=cv2.contourArea, reverse=True):  # generates list of green contours 
	# 	contour_area = cv2.contourArea(c)
	# 	if to_return < 0:
	# 		to_return = contour_area
	# 	print("--Size", contour_area)
	# 	if contour_area < 2000:  # not large enough to be considered
	# 		break

	# 	# update the points queue

	# 	x1,y1,w1,h1 = cv2.boundingRect(c)
	# 	cv2.rectangle(frame, (x1,y1) , (x1+w1,y1+h1) , box_color[cntr_ind], 2)
	# 	# loop over the set of tracked points

	# 	# cv2.imshow("Frame", frame)
	# 	# sleep(5)
	# 	cntr_ind +=1
	# return to_return

# construct the argument parse and parse the arguments

def generate_contours(frame, low, high):
	# frame = cv2.GaussianBlur(frame, (11, 11), 0)
	hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
	cv2.imshow('hsv img', hsv)
	cv2.waitKey(2000)
	# construct a mask for the color "green", then perform
	# a series of dilations and erosions to remove any small
	# blobs left in the mask
	mask = cv2.inRange(hsv, array(low), array(high))
	cv2.imshow('post masks', mask)
	cv2.waitKey(1000)
	mask = cv2.erode(mask, None, iterations=2)
	mask = cv2.dilate(mask, None, iterations=2)
	return cv2.countNonZero(mask)
	# find contours in the mask and initialize the current
	# (x, y) center of the ball
	# contours = cv2.findContours(mask.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
	# return imutils.grab_contours(contours)	





cozmo.run_program(cozmo_program)