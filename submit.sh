#!/bin/bash
#
#$ -cwd
#$ -j y
#$ -m n
#$ -pe mpich 1
#$ -S /bin/bash
#
./gpu
