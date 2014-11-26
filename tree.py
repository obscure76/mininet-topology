#!/usr/bin/python

import sys
import argparse
from mininet.topo import Topo
from mininet.net import Mininet
from mininet.node import CPULimitedHost
from mininet.link import TCLink
from mininet.util import dumpNodeConnections



class SingleSwitchTopo(Topo):
    "Single switch connected to n hosts."
    def __init__(self, n=2, **opts):
        Topo.__init__(self, **opts)
        switch = self.addSwitch('s1')
        for h in range(n):
            # Each host gets 50%/n of system CPU
            host = self.addHost('h%s' % (h + 1),
               cpu=.5/n)
            # 10 Mbps, 5ms delay, 10% loss, 1000 packet queue
            self.addLink(host, switch,
               bw=10, delay='5ms', loss=10, max_queue_size=1000, use_htb=True)

def perfTest():
    "Create network and run simple performance test"
    topo = TreeTopo( depth=2, fanout=3 )
    net = Mininet( topo=topo, controller=lambda name: RemoteController(name, ip='127.0.0.1'))
    net.start()
    hosts = net.hosts
    for h in hosts:
        print(h)
    net.stop()

if __name__ == '__main__':
    if len(sys.argv) < 3:
        print('Usage tree.py depth fanout')
    parser = argparse.ArgumentParser()
    parser.add_argument('depth', help='The depth of the tree topology')
    parser.add_argument('fanout', help='The fanout of each node in the topology')
    args = parser.parse_args()
    depth = args.depth
    fanout = args.fanout
    perfTest(depth, fanout)