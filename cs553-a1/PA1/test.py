#!/usr/bin/python

import thread
import time

def print_time( thread, t):
	count = 0
	while count < 5:
		time.sleep(t)
		count += 1
		print "%s: %s" % (thread, time.clock() )

try:
	thread.start_new_thread( print_time, ("T1", 2,) )
	thread.start_new_thread( print_time, ("T2", 4,) )
except:
	print "Error =("

while 1:
	pass
