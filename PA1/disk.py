import re
import sys
import threading
import math
from random import randint
from datetime import datetime

TIMING = []
BANDWITH = []
MODE = []
filesize = 10000000 


class disk(threading.Thread):

	def __init__(self, rw, sr,blocksize, file_name):
		super(disk,self).__init__()
		self.file_name = file_name
		self.blocksize = int(blocksize)
		self.rw = rw  #BOOL > read       : rw = 0  write  : rw = 1
		self.sr = sr  #BOOL > sequential : sr = 0; random : sr = 1
		
	def file_read_seq_access(self):
		f = open(self.file_name,"rb")
		f.read(self.blocksize)
		f.close()

	def file_write_seq_access(self):
		f = open(self.file_name,"wb")
		for i in range(self.blocksize):
			f.write(b'0')
		f.close()

	def file_read_random_access(self):
		f = open(self.file_name,"rb")
		dif = filesize - self.blocksize
		randint(0, dif)
		f.seek(dif)
		f.read(self.blocksize)
		f.close()

	def file_write_random_access(self):
		f = open(self.file_name,"wb")
		diff_size = filesize - self.blocksize
		random_size = randint(0, diff_size)
		f.seek(random_size)
		for i in range(self.blocksize):
			f.write(b'0')
		f.close()
	
	def run(self):

		"""Pattern search :
		 If there is a r in the first argument, mode will switch to write.
		 Else it will switch to read mode (default).
		
		 If there is ran in the second argument, node will switch to random.
		 Else it will switch to sequential."""
	
		if re.search(r'w',self.rw):
			mode0 = 1
		else:
			mode0 = 0
		if re.search(r'ran',self.sr):
			mode1 = 1
		else:
			mode1 = 0
		mode = str(mode0) + str(mode1)

		
		"""Choice of the right function among those defined :
			file_read_seq_access()
			file_read_random_access()
			file_write_seq_access()
			file_write_random_access()
		 Latency and bandwith are calculated here"""

		if(mode == "00"):  #Read / Sequential
			start_time = datetime.now()
			self.file_read_seq_access()
			stop_time = datetime.now()
			diff_time = stop_time - start_time	
			TIMING.append(diff_time.total_seconds())
			BANDWITH.append(self.blocksize/diff_time.total_seconds())
			MODE.append("Read / Sequential")
		elif(mode == "01"): #Read / Random
			start_time = datetime.now()
			self.file_read_random_access()
			stop_time = datetime.now()
			diff_time = stop_time - start_time
			TIMING.append(diff_time.total_seconds())
			BANDWITH.append(self.blocksize/diff_time.total_seconds())
			MODE.append("Read / Random")
		elif(mode == "10"): #Write / Sequential
			start_time = datetime.now()
			self.file_write_seq_access()
			stop_time = datetime.now()
			diff_time = stop_time - start_time
			TIMING.append(diff_time.total_seconds())
			BANDWITH.append(self.blocksize/diff_time.total_seconds())
			MODE.append("Write / Sequential")
		elif(mode == "11"): #Write / Random
			start_time = datetime.now()
			self.file_write_random_access()
			stop_time = datetime.now()
			diff_time = stop_time - start_time
			TIMING.append(diff_time.total_seconds())
			BANDWITH.append(self.blocksize/diff_time.total_seconds())
			MODE.append("Write / Random")
		else:
			print "rw argument must contain r(read) or w(write).\n seqrand argument must contain seq(sequential access) or ran(random access)"
			sys.exit(1)
		print "Latency    :",(TIMING[-1]*1000),"ms"
		print "Throughput :",(BANDWITH[-1]/1000000),"MB/s"
if __name__ == '__main__':

	Threads = []
	Disk = {}
	sum_ = 0
	avg_bw = 0

	if len(sys.argv) != 6:
		print "Usage: disk.py <0:read 1:write><0:sequential 1:random><blocks in bytes><thread count>"
		sys.exit(1)
	else:
		for i in range(int(sys.argv[5])):	
			print "\nThread %d / %d started" % ((i+1),int(sys.argv[5]))
			Disk[i] = disk(sys.argv[1],sys.argv[2],sys.argv[3],sys.argv[4]+str(i)+".txt")
			Threads.append(Disk[i])
			Disk[i].start()
			Disk[i].join()
			sum_ += TIMING[i]
			avg_bw += BANDWITH[i]
 
		print "\n=======SUMMARY OF PERFORMANCE======="
		print "Mode               :",MODE[-1]
		print "Number of threads  :",sys.argv[5]
		print "Blocksize          :",sys.argv[3], "B" 
		print "Total time taken   :",(sum_*1000), "ms"
		print "Average latency    :",((sum_/int(sys.argv[5]))*1000),"ms"
		print "Average Throughput :",((avg_bw/int(sys.argv[5]))/1000000),"MB/s" 
		print "=====================================\n\n"
