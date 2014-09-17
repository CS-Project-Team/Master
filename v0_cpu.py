#!/usr/bin/python

import thread
import time

def add_integer( thread, n ):
	count = 0
	print "%s: %s" % (thread, time.clock())
	while count < n:
		count += 1
	print "%s: %s" % (thread, time.clock())

try:
	thread.start_new_thread( add_integer, ("T1", 10) )
	thread.start_new_thread( add_integer, ("T2", 1000000000) )
	print "Starting..."
except:
	print "Error =("
while 1:
	pass
