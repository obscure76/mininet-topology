for((port=500;port<=505;port++))
do
    echo 'Starting UDP server on port' $port
    /home/anil/mininet/mininet-tests-master/buffersizing/iperf-2.0.5/src/iperf -s -u -p $port -t 250 &
done;
for((port=506;port<=515;port++))
do
    echo 'Starting TCP server on port' $port
    /home/anil/mininet/mininet-tests-master/buffersizing/iperf-2.0.5/src/iperf -s -p $port -t 270 &
done;
