#!/usr/bin/env python

import rospy
import os
from sensor_msgs.msg import LaserScan
from ackermann_msgs.msg import AckermannDriveStamped
from pocketsphinx import LiveSpeech, get_model_path
from std_msgs.msg import String

#class con connects between the two subscribers functions listenerCallback and wanderCallback
# audioCommand holds the last audio command
# wanderFlag indicated whether the car is in wander state
class con:
	audioCommand = ''
	wanderFlag = False

#handle the audio commands 
#"translate" the audio commands to car instructions
def listenerCallback(msg):
	con.audioCommand=msg.data
	print(msg.data)
	if(msg.data=="STOP"):
		ackMsg.drive.speed = 0
		ackMsg.drive.steering_angle = 0
		#stop the car / wander state
		con.wanderFlag = False
	elif(con.wanderFlag==False):
		if(msg.data=="FORWARD"):
			ackMsg.drive.speed=3
			ackMsg.drive.steering_angle=0
		elif(msg.data=="LEFT"):
			ackMsg.drive.speed=1
			ackMsg.drive.steering_angle=-90
		elif(msg.data=="RIGHT"):
			ackMsg.drive.speed=1
			ackMsg.drive.steering_angle=90
		elif(msg.data=="REVERSE"):
			ackMsg.drive.speed=-3
			ackMsg.drive.steering_angle=0
		elif(msg.data == "WANDER"):
			#start wander state
			con.wanderFlag = True
		
		
	print("speed ",ackMsg.drive.speed)
	pub.publish(ackMsg)

#wander state enables the car to wander autonomically
def wanderCallback(msg):
	if(con.audioCommand == "WANDER"):
		if(msg.ranges[180] > 2.2):
			ackMsg.drive.speed = 5 
			ackMsg.drive.steering_angle = 0
		else: 
			if(msg.ranges[215] > msg.ranges[135]):
				ackMsg.drive.steering_angle = -90
			else:
				ackMsg.drive.steering_angle = 90

		ackMsg.drive.speed = 2
		
		if(msg.ranges[170]<0.5 or msg.ranges[180]<0.5 or msg.ranges[190]<0.5):
			ackMsg.drive.speed = -4
			ackMsg.drive.steering_angle = 90


		pub.publish(ackMsg)

if __name__ =='__main__':

	ackMsg = AckermannDriveStamped()
	rospy.init_node('proj', anonymous=True)
	#subscribe to listener commands
	sub = rospy.Subscriber('chatter',String,listenerCallback)
	#subscribe to lidar
	sub2 = rospy.Subscriber('/agent1/scan',LaserScan,wanderCallback)
	#publish to hamster wheels(hamster movement control)
	pub = rospy.Publisher('/agent1/ackermann_cmd',AckermannDriveStamped,queue_size=1)



while not rospy.is_shutdown():
	rospy.spin()

