#!/usr/bin python
# Parameters: <read/write> <is_random> <block_size> <n_threads>
import sys
import threading
from random import sample
from datetime import datetime
# This limit is to set to get a maximum of 1MB of memory access.
MAX_SIZE = 1024*1024 
TIMING = []
BANDWIDTH = []

class memory(threading.Thread):

    def __init__(self,cmd,is_ran,blks):
        super(memory,self).__init__()
        self.cmd = cmd
        self.ran = int(is_ran)
        self.blks = int(blks)
        if self.blks > MAX_SIZE:
            print 'The maximum block size is 1MB'
            sys.exit(1)
        self.in_memory = ['M']*MAX_SIZE
            
    # This function reads random data (random access) from the array in memory.        
    def r_read(self):
        for var in sample(xrange(MAX_SIZE),self.blks):
            tmp = self.in_memory[var]
    
    # This function writes into random position of the array in memory (random writes).
    def r_write(self):
        tmp = 'Z'
        for var in sample(xrange(MAX_SIZE),self.blks):
            self.in_memory[var] = tmp
    
    # This function reads sequentially from the memory array (sequential access).
    def read(self):
        for var in xrange(self.blks):
            tmp = self.in_memory[var]
    
    # This function writes sequentially from the memory (sequential writes).
    def write(self):
        tmp = 'X'
        for var in xrange(self.blks):
            self.in_memory[var] = tmp

    # This function controls the thread execution flow.        
    def run(self):
        if self.ran == 1:
            if self.cmd == 'read':
                r_read_start = datetime.now()
                self.r_read()
                r_read_stop = datetime.now() 
                diff = r_read_stop - r_read_start
                TIMING.append(diff.total_seconds()) 
                BANDWIDTH.append(self.blks/diff.total_seconds())
                print 'Thread execution time:', TIMING[-1]
                print 'Memory Bandwidth for current thread: %f Bytes/Sec' % BANDWIDTH[-1] 
            else:
                r_write_start = datetime.now()
                self.r_write()
                r_write_stop = datetime.now()  
                diff = r_write_stop - r_write_start
                TIMING.append(diff.total_seconds())  
                BANDWIDTH.append(self.blks/diff.total_seconds()) 
                print 'Thread execution time:', TIMING[-1]
                print 'Memory Bandwidth for current thread: %f Bytes/Sec' % BANDWIDTH[-1] 
        else:
            if self.cmd == 'read':
                read_start = datetime.now()
                self.read()
                read_stop = datetime.now()  
                diff = read_stop - read_start
                TIMING.append(diff.total_seconds())
                BANDWIDTH.append(self.blks/diff.total_seconds()) 
                print 'Thread execution time:', TIMING[-1]
                print 'Memory Bandwidth for current thread: %f Bytes/Sec' % BANDWIDTH[-1] 
            else:       
                write_start = datetime.now()
                self.write()
                write_stop = datetime.now()  
                diff = write_stop - write_start
                TIMING.append(diff.total_seconds())  
                BANDWIDTH.append(self.blks/diff.total_seconds()) 
                print 'Thread execution time:', TIMING[-1]
                print 'Memory Bandwidth for current thread: %f Bytes/Sec' % BANDWIDTH[-1] 
    
if __name__ == '__main__':
    Threads = []
    if len(sys.argv) != 5:
        print 'Usage: memory.py <read/write> <random/not_random> <blocks in bytes> <thread count>'
        sys.exit(1)
    else:
        mem = memory(sys.argv[1].lower(),sys.argv[2],sys.argv[3])
        for i in range(int(sys.argv[4])):
            print '\nThread %d Started' % (i+1)
            mem.start()
            Threads.append(mem)
            mem.join()

        sum_ = 0
        avg_bw = 0  
        for val in range(1,len(int(sys.argv[4])+1)):
            sum_ += TIMING[-(val)]
            avg_bw += BANDWIDTH[-(val)]

        print 'TOTAL NUMBER OF THREADS:',sys.argv[4]
        print 'TOTAL TIME TAKEN       :',sum_
        print 'Averange Bandwidth is  :' %  (avg_bw /sys.argv[4])
