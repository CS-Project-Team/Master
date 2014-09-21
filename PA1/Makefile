.PHONY: all clean
CCC=g++
CCFLAGS=-pthread -std=c++11 -Wl,--no-as-needed 
OBJECTS=cpu 

all: $(OBJECTS)

run: all
	##./cpu

cpu: cpu.cpp
	$(CCC) cpu.cpp -o cpu $(CCFLAGS)

