NOW=$(date +"%m-%d-%Y.%H.%M.%S") 
REPORT_FILE="report."$NOW".txt"

BLOCKSIZE="1 1000 1000000"
THREAD_NB="1 2 4"
FILE="temp"
MODE0="write read"
MODE1="sequential random"
CPU_THREADS="1 2 4 8"

echo ""
echo "==== DISK BENCHMARKING ===="
echo "Starting Benchmark ..."
echo "Varying mode ..."
for k in $MODE0; do
	for l in $MODE1; do
	echo "Current mode : $k / $l"
	echo "  Varying blocksize ..."
		for j in $BLOCKSIZE; do
		echo "    Current Blocksize : $j Bytes"
		echo "      Varying number of threads ..."
			for i in $THREAD_NB; do
				echo "        Number of threads : $i" 
				python disk.py $k $l $j $FILE $i >> $REPORT_FILE
			done		
		done	
	echo ""	
	done
done
echo "Removing temporary files ..."‫
rm temp*
echo ""
echo "==== CPU BENCHMARKING ===="
echo "Starting Benchmark ..."
for i in $CPU_THREADS; do
	echo "        Testing for $i threads . . ."
	python cpu.py -t $i >> $REPORT_FILE
done
echo ""
echo "Benchmark terminated successfully."
echo ""
read -p "Do you want to open report file $REPORT_FILE in the console ? y/n  " response
if [ "$response" == "y" ]; then
	gedit $REPORT_FILE
else
	echo "End of program."
fi
echo ""
