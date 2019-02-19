#!/usr/bin/env python

import rospy
import os
from sensor_msgs.msg import LaserScan
from ackermann_msgs.msg import AckermannDriveStamped
from pocketsphinx import LiveSpeech, get_model_path
from std_msgs.msg import String

class con:
	x = ''
	flag = False
		
def callback(msg):

	con.x=msg.data
	
	if(msg.data=="STOP"):
		ackMsg.drive.speed = 0
		ackMsg.drive.steering_angle = 0
		con.flag = False
	elif(con.flag==False):
		if(msg.data=="FORWARD"):
			ackMsg.drive.speed=0.5
			ackMsg.drive.steering_angle=0
		elif(msg.data=="LEFT"):
			ackMsg.drive.speed=0.2
			ackMsg.drive.steering_angle=90
		elif(msg.data=="RIGHT"):
			ackMsg.drive.speed=0.2
			ackMsg.drive.steering_angle=-90
		elif(msg.data=="REVERSE"):
			ackMsg.drive.speed=-0.5
			ackMsg.drive.steering_angle=0
		elif(msg.data == "WANDER"):
			con.flag = True
		
		
	print("speed ",ackMsg.drive.speed)
	pub.publish(ackMsg)

def callback2(msg):
	if(con.x == "WANDER"):
		if(msg.ranges[180] > 2.2):
			ackMsg.drive.speed = 0.5
			ackMsg.drive.steering_angle = 0
		else: 
			if(msg.ranges[215] > msg.ranges[135]):
				ackMsg.drive.steering_angle = 90
			else:
				ackMsg.drive.steering_angle = -90

		ackMsg.drive.speed = 0.5
		
		if(msg.ranges[170]<0.5 or msg.ranges[180]<0.5 or msg.ranges[190]<0.5):
			ackMsg.drive.speed = -0.5
			ackMsg.drive.steering_angle = 90


		pub.publish(ackMsg)

if __name__ =='__main__':

	ackMsg = AckermannDriveStamped()
	rospy.init_node('proj', anonymous=True)
	sub = rospy.Subscriber('chatter',String,callback)
	sub2 = rospy.Subscriber('/agent1/scan',LaserScan,callback2)
	pub = rospy.Publisher('/agent1/ackermann_cmd',AckermannDriveStamped,queue_size=1)



while not rospy.is_shutdown():
	rospy.spin()

