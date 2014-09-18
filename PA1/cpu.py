#!/usr/bin/python

import thread
import time
import threading
import sys, getopt
import math

#Number of operations that will run on each test
N_OPERATIONS = 10**8
#Number of tests for each operation type
N_TESTS = 3
#Execution time for each test
TIME_INT = []
TIME_FL = []

def add_integer( thread, n ):
	count = 0
	startTime = time.clock()
	for i in xrange(n):	
		count += 1
	totalTime = time.clock() - startTime
	#print "%s: %s" % (thread, totalTime)

def add_float( thread, n ):
        count = 0.00
	float_increment = 1.07
        startTime = time.clock()
        for i in xrange(n):
                count += float_increment
        totalTime = time.clock() - startTime
        #print "%s: %s" % (thread, totalTime)

def average( values ):
	sum_ = 0.00
	for val in range(1,N_TESTS+1):
                sum_ += values[-(val)]
        return sum_ /float(N_TESTS)

def stand_deviation( values, average ):
	variance = 0.00
	for val in range(1,N_TESTS+1):
                variance += ((average - values[-(val)])**2)
	variance = variance / N_TESTS
	return math.sqrt( variance )

#Calculates GIOPS or GFLOPS for a given performance time
def calc_gops( time):
	return N_OPERATIONS / (time*(10**9))

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
	
	print "\n\n========== CPU PERFORMANCE BECHMARKING ==========\n"
	n = int((N_OPERATIONS)/int(numThreads))

	#Testing time for an empty loop
        startTime = time.clock()
	for i in xrange(n):
                pass
        loopTime = time.clock() - startTime

	threads = []
	startTime = time.clock()
	for i in range(0, int(numThreads)):
		thread = myThread(i, "T"+str(i),"integer", n)
		thread.start()
		threads.append(thread)

	for t in threads:
		t.join()
	totalTime = time.clock() - startTime - loopTime
	TIME_INT.append(totalTime);
	giops = n / (totalTime*(10**9))
	print "   Total time : %s  ### GIOPS : %s" % (totalTime, giops)

	threads = []
        startTime = time.clock()
        for i in range(0, int(numThreads)):
                thread = myThread(i, "T"+str(i), "float", n)
                thread.start()
                threads.append(thread)

        for t in threads:
                t.join()
        totalTime = time.clock() - startTime - loopTime
	TIME_FL.append(totalTime)
        flops = n / (totalTime*(10**9))
        print "   Total time : %s  ### FLOPS : %s" % (totalTime, flops)


if __name__ == "__main__":
	if len(sys.argv) != 3:
		print 'Usage: cpu.py -t <number of thread>'
		sys.exit(1)
	for i in range(0,N_TESTS):
		print "----- Running test #%s" % (i)
		main(sys.argv[1:])
	
	sum_int = 0
	sum_float = 0
	avg_int = average(TIME_INT)
	avg_float = average(TIME_FL)
	sd_int = stand_deviation(TIME_INT, avg_int)
	sd_float = stand_deviation(TIME_FL, avg_float)
	
        print "\n======= SUMMARY OF CPU PERFORMANCE ======="
        print "Tests                                    : %s" % (N_TESTS)
	print "Number of threads                        : %s" % (sys.argv[2])
        print "Average time for integer operations      : %ss" % (avg_int)
        print "Standard deviation for integer operations: %ss" % (sd_int)
	print "Average integer operations per second    : %s GIOPS" %(calc_gops(avg_int)) 
        print "Average time for float operations        : %ss" % (avg_float)
        print "Standard deviation for float operations  : %ss" % (sd_float)
	print "Average float operations per second      : %s GFLOPS" %(calc_gops(avg_float)) 
        print "=====================================\n\n"

