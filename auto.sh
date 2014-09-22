NOW=$(date +"%m-%d-%Y.%H.%M.%S")
REPORT_FILE="report."$NOW".txt"
NB_THREADS="1 2 4"
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
	echo "Mode: $mode";
	for threads in $NB_THREADS; do
		echo "   Number of threads: $threads"
		sleep 2 
		./disk $mode $threads >> $REPORT_FILE
	done
	echo "done."
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

