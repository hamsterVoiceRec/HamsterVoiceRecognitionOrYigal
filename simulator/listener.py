#!/usr/bin/env python
################################
#Commands thread listener
################################

import rospy
import os
from pocketsphinx import LiveSpeech, get_model_path
from std_msgs.msg import String
import thread
import time

msg = ""


#thread to publish audio commands
def func():
	global msg
	while(1):
		pub.publish(msg)
		time.sleep(0.1)

#listen to speaker voice commands 
def listener():	
	global msg
	while not rospy.is_shutdown():
		for p in speech:
			msg=speech.__str__()

		
		
if __name__ =='__main__':
	pub = rospy.Publisher('chatter',String,queue_size=10)
	rospy.init_node('proj', anonymous=True)
	model_path = get_model_path()
	#voice object of pocketsphinx livespeech
	speech = LiveSpeech(
		verbose=False,
		sampling_rate=16000,
		buffer_size=2048,
		no_search=False,
		full_utt=False,
		hmm=os.path.join(model_path,'en-us'),
		kws = '/home/or/catkin_ws/src/proj/9079.kws',
		dic = '/home/or/catkin_ws/src/proj/9079.dic',
		lm = '/home/or/catkin_ws/src/proj/9079.lm')
	try:
		thread.start_new_thread(func,())
		listener()
		
		
	except rospy.ROSInterruptException:
		pass



while not rospy.is_shutdown():
	rospy.spin()

