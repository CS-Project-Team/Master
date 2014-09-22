NOW=$(date +"%m-%d-%Y.%H.%M.%S")
REPORT_FILE="report."$NOW".txt"
NB_THREADS="1 2 4"
BLOCKSIZE="1 1000 1000000"
MODE="ws wr rs rr"

echo ""
echo "======= DISK BENCHMARKING ======="
echo ""
echo "Compiling files ..."
gcc -pthread disk.c -o disk
echo "done."
echo ""
echo "Benchmarking ..."
echo ""
for mode in $MODE; do
	echo "Mode: $mode"
	for blocksize in $BLOCKSIZE; do
		echo "    Blocksize: $blocksize Bytes";
		for threads in $NB_THREADS; do
			echo "     Number of threads: $threads"
			sleep 2 
			./disk $mode $blocksize $threads >> $REPORT_FILE
		done
		echo "     done."
	done
	echo "    done."
done
echo ""
echo "Removing temporary files ..."
rm temp*
echo "done."
echo ""
echo "Disk Benchmarking ended successfully."
read -p "Do you want to open report file $REPORT_FILE ? y/n " response
if [ "$response" == "y" ]; then
	gedit $REPORT_FILE
else
	echo "End of program."
fi
echo ""

