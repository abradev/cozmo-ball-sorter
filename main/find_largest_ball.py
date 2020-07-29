from numpy import array
import cv2
import imutils
from time import sleep, perf_counter

import cozmo
from cozmo.util import degrees

def cozmo_program(robot: cozmo.robot.Robot):
	colors = {'Green': ([26-10, 109-27, 206-50], [38, 129, 255])}   # with red after effect
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
		# cv2.namedWindow(fname)
		# cv2.moveWindow(fname, 10, 10)
		# cv2.imshow(fname,frame)
		# cv2.waitKey(1000)
		for color, bounds in colors.items():
			contour_size = get_cont(frame, bounds)
			print("---Search for %s Complete" % color)
			# need to check that its a ball, etc  //kathline's shape recognition code
			if contour_size > largest_contour:
				final_degree, largest_contour = degree, contour_size
		# cv2.destroyWindow(fname)
		robot.turn_in_place(degrees(rotate)).wait_for_completed() # rotate n degrees counterclockwise
	print("Largest Contour Size:", largest_contour)
	print("Found at %d degrees" % final_degree)

	if final_degree>180:
		robot.turn_in_place(degrees(final_degree-360)).wait_for_completed()
	else:
		robot.turn_in_place(degrees(final_degree)).wait_for_completed()
	print("total time for cycle", perf_counter()-start)




def get_cont(frame, bounds):
	# frame = imutils.resize(frame, width=600) # resize the frame
	pre_sort = generate_contours(frame, bounds[0], bounds[1])
	post_sort = sorted(pre_sort, reverse=True, key=cv2.contourArea)
	if len(post_sort)>0:	
		print("--Length:", len(pre_sort))
		cs = cv2.contourArea(post_sort[0])
		print("--Size:", cs)
		return cs
	else:
		return 0

def generate_contours(frame, low, high):
	frame = cv2.GaussianBlur(frame, (9, 9), 0)
	hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
	""" construct a mask for the color "green", then perform
	a series of dilations and erosions to remove any small
	blobs left in the mask"""
	mask = cv2.inRange(hsv, array(low), array(high))
	mask = cv2.erode(mask, None, iterations=2)
	mask = cv2.dilate(mask, None, iterations=2)
	# cv2.namedWindow('post masks')
	# cv2.moveWindow('post masks', 400, 10)
	# cv2.imshow('post masks', mask)
	# cv2.waitKey(1000)
	
	contours = cv2.findContours(mask.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
	return imutils.grab_contours(contours)	


cozmo.run_program(cozmo_program)
