#!/usr/bin/python

import thread
import time
import threading
import sys, getopt

def add_integer( thread, n ):
	count = 0
	startTime = time.clock()
	for i in xrange(n):	
		count += 1
	totalTime = time.clock() - startTime
	print "%s: %s" % (thread, totalTime)

def add_float( thread, n ):
        count = 0.00
	float_increment = 1.07
        startTime = time.clock()
        for i in xrange(n):
                count += float_increment
        totalTime = time.clock() - startTime
        print "%s: %s" % (thread, totalTime)

class myThread(threading.Thread):
	def __init__(self, threadID, name, opType, n):
		threading.Thread.__init__(self)
		self.threadID = threadID
		self.name = name
		self.opType = opType
		self.n = n
	def run(self):
		print "Started %s %s operations on %s" % (self.n,self.opType,self.name)
		if self.opType == "integer":
			add_integer(self.name, self.n)
		else:
			add_float(self.name, self.n)


def main(argv):
	numThreads = ''
	outputFile = ''
	try:
		opts, args = getopt.getopt(argv,"t:",[])
	except getopt.GetoptError:
		print "cpu.py -t <#threads>"
		sys.exit(2)
	for opt, arg in opts:
		if opt == '-t':
			if arg is None:
				print "cpu.py -t <#threads>"
				sys.exit(2)
			numThreads = arg
	
	n = int((10**8)/int(numThreads))
	threads = []
	startTime = time.clock()
	for i in range(0, int(numThreads)):
		thread = myThread(i, "T"+str(i),"integer", n)
		thread.start()
		threads.append(thread)

	for t in threads:
		t.join()
	totalTime = time.clock() - startTime
	giops = n / (totalTime*(10**9))
	print "Total time : %s  ### GIOPS : %s" % (totalTime, giops)

	threads = []
        startTime = time.clock()
        for i in range(0, int(numThreads)):
                thread = myThread(i, "T"+str(i), "float", n)
                thread.start()
                threads.append(thread)

        for t in threads:
                t.join()
        totalTime = time.clock() - startTime
        giops = n / (totalTime*(10**9))
        print "Total time : %s  ### FLOPS : %s" % (totalTime, giops)


if __name__ == "__main__":
	main(sys.argv[1:])
