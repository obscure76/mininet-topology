#!/usr/bin/python

"""
multiping.py: monitor multiple sets of hosts using ping

This demonstrates how one may send a simple shell script to
multiple hosts and monitor their output interactively for a period=
of time.
"""

from mininet.net import Mininet
from mininet.node import Node
import os
#from mininet.topo import SingleSwitchTopo
from mininet.log import setLogLevel
from mininet.topolib import TreeTopo
from mininet.node import RemoteController

from select import poll, POLLIN
#from time import time
import time

CUSTOM_IPERF_PATH = '/home/anil/mininet/mininet-tests-master/buffersizing/iperf-2.0.5/src/iperf'
mytopo = TreeTopo( depth=2, fanout=2 )
net = Mininet( topo=mytopo, controller=lambda name: RemoteController(name, ip='10.23.4.62'))

def killhosts():
    hosts = net.hosts
    for host in hosts:
        host.sendInt()
        host.cmd('pkill -f "home/anil/mininet/mininet-tests-master/buffersizing/iperf-2.0.5/src/iperf"')
        host.cmd( 'kill %while' )
    net.stop()



def chunks( l, n ):
    "Divide list l into chunks of size n - thanks Stackoverflow"
    return [ l[ i: i + n ] for i in range( 0, len( l ), n ) ]

def startpings(host, targetips ):

    targetips = ' '.join( targetips )
    cmd = ( 'while true; do '
            ' for ip in %s; do ' % targetips +
            '  echo -n %s "->" $ip ' % host.IP() +
            '  `echo $home` '+
            '   `ping -c1 -w 1 $ip | grep packets` ;'
            '  sleep 1;'
            ' done; '
            'done &' )
    print ( '*** Host %s (%s) will be pinging ips: %s' % \
                ( host.name, host.IP(), targetips ) )

    host.cmd( cmd )

def starttraffic( host, total_ips, seconds, count):
    "Tell host to repeatedly ping targets"
    total_ips = ' '.join( total_ips )
    cmd = ( 'while true; do '
            ' for ip in %s; do ' % total_ips +
            '  echo -n %s "->" $ip ' % host.IP() +
            '   `bash traffic.sh $ip `; '
            '  sleep 1;'
            ' done; '
            'done &' )
    #time.sleep(0.001)
    host.cmd(cmd)



def startserver( host):
    "Tell host to repeatedly ping targets"
    cmd = ( 'bash tcpservers.sh' )
    print cmd
    try:
        print host.cmd(cmd)
    except:
        print 'SERVER start failed'
        killhosts()


def startclient( host, seconds, subnetcount, count):
    "Tell host to repeatedly ping targets"
    portlist = range(500, 502, 1)
    totalHosts = len(net.hosts)
    print 'For client ', str(host)
    SERV1 = '10.0.0.1'
    SERV2 = '10.0.0.2'
    if subnetcount %2 == 0:
        for port in portlist:
            if count < totalHosts/2 :
                cmdudp = ('%s -c %s -u -p %s -t %s  -i 1 '
                     '-yc -b 100000 &' % (CUSTOM_IPERF_PATH, SERV1, port, seconds-5))
            else:
                cmdudp = ('%s -c %s -u -p %s -t %s  -i 1 '
                     '-yc -b 100000 &' % (CUSTOM_IPERF_PATH, SERV2, port, seconds-5))
            try:
                print host.cmd(cmdudp)
            except:
                print cmdudp
    else:
        for port in range(506, 507, 1):
            if count < totalHosts/2:
                cmdtcp = ('%s -c %s -p %s -t %s -i 1 '
                     '-yc -Z %s &' % (CUSTOM_IPERF_PATH, SERV1, port, seconds-5, 'reno'))
            else:
                cmdtcp = ('%s -c %s -p %s -t %s -i 1 '
                     '-yc -Z %s &' % (CUSTOM_IPERF_PATH, SERV2, port, seconds-5, 'reno'))
            try:
                print host.cmd(cmdtcp)
            except:
                print cmdtcp

def multiping( chunksize, seconds):
    "Ping subsets of size chunksize in net of size netsize"
    #topo = SingleSwitchTopo( netsize )
    net.start()
    hosts = net.hosts
    subnets = chunks( hosts, chunksize )
    # Create polling object
    fds = [ host.stdout.fileno() for host in hosts ]
    poller = poll()
    for fd in fds:
        poller.register( fd, POLLIN )

    # Start pings
    total_ips = []
    count = 0
    subnetcount = 0
    for subnet in subnets:
        subnetcount += 1
        ips = [ host.IP() for host in subnet ]
        for host in subnet:
            fp = open(host.name + 'out', "w")
            if count < 2:
                count += 1
                startserver(host)
                continue
            count += 1
            startclient(host, seconds-2, subnetcount, count)
            #starttraffic( host, total_ips, seconds, count)
            #startpings( host, ips)
    print 'All clients started\n'
    # Monitor output
    endTime = time.time() + seconds
    startTime = time.time()
    print 'Starting polling for each host'
    while time.time() < endTime:
        readable = poller.poll(5000)
        print time.time()-startTime, 'Seconds passed'
        for fd, _mask in readable:
            try:
                node = Node.outToNode[ fd ]
                #print '%s:' % node.name, node.monitor().strip()
                s = str(node.monitor()) + ':'
                fp = open(node.name + 'out', "a")
                fp.write(s)
            except:
                print time.time()-startTime, 'Seconds passed'
                print '%s:' % node.name, node.monitor().strip()
                print 'Exception'
                pass
    # Stop pings
    killhosts()

if __name__ == '__main__':
    setLogLevel( 'info' )
    multiping(chunksize=4, seconds=300 )
