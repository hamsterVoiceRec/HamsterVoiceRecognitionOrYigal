#!/usr/bin/env python

import rospy
import os
import time
from pocketsphinx import LiveSpeech, get_model_path
from std_msgs.msg import String
import thread
import time
import multiprocessing

msg = ""
start = 0
def time_func():
	global start
	time.sleep(0.2)	
	start = time.time()

def func():
	global msg
	global start
	global p
	p = multiprocessing.Process(target=time_func,args=())
	if(p.is_alive()):
		p.terminate()	
	
	start = time.time()
	p.start()
	while(1):
		splitmsg = msg.split(" ")
		print(splitmsg)
		if (start < time.time()-0.4):
			pub.publish(splitmsg[0])
			

def talker():		
	global msg

	while not rospy.is_shutdown():
		for p in speech:
			msg=speech.__str__()
		
		
if __name__ =='__main__':
	pub = rospy.Publisher('chatter',String,queue_size=10)
	rospy.init_node('guides', anonymous=True)
	model_path = get_model_path()
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
		talker()
		
		
	except rospy.ROSInterruptException:
		pass



while not rospy.is_shutdown():
	rospy.spin()

