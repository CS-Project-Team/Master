#!/usr/bin/python

import thread
import time
import threading
import sys, getopt

def add_integer( thread, n ):
	count = 0
	print "%s: %s" % (thread, time.clock())
	while count < n:
		count += 1
	print "%s: %s" % (thread, time.clock())

class myThread(threading.Thread):
	def __init__(self, threadID, name):
		threading.Thread.__init__(self)
		self.threadID = threadID
		self.name = name
	def run(self):
		print "Starting " + self.name
		add_integer(self.name, 1000000)
		print "Exiting " + self.name

def main(argv):
	numThreads = ''
	outputFile = ''
	try:
		#thread.start_new_thread( add_integer, ("T2", 1000000000) )
		opts, args = getopt.getopt(argv,"t:o:",[])
	except getopt.GetoptError:
		print "cpu.py -t <#threads> -o <outputfile>"
		sys.exit(2)
	for opt, arg in opts:
		if opt == '-t':
			numThreads = arg
		elif opt == '-o':
			outputFile = arg
	print 'Number of threads: ', numThreads
	print 'Output file: ', outputFile
	threads = [] 	
	thread1 = myThread(1, "T1")
	thread2 = myThread(2, "T2")
	thread1.start()
	threads.append(thread1)
	threads.append(thread2)
	thread2.start()
	for t in threads:
		t.join()
	print "Exiting Main thread"
if __name__ == "__main__":
	main(sys.argv[1:])

