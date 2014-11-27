#!/usr/bin/python

import sys
import argparse
from mininet.topolib import TreeNet
from mininet.topolib import TreeTopo
from mininet.topo import Topo
from mininet.net import Mininet
from mininet.node import OVSSwitch, Controller, RemoteController



def perfTest(d =2, f = 3):
    "Create network and run simple performance test"
    c = RemoteController( 'c', ip='127.0.0.1' )
    topo = TreeTopo( depth=d, fanout=f )
    net = Mininet( topo=topo,controller=lambda name: RemoteController(name, ip='127.0.0.1'))
    #net.addController(c)
    #net.build()
    net.start()
    hosts = net.hosts
    for h in hosts:
        if str(h) != 'h1' or str(h)!= 'h2':
            print(h)
    net.stop()

if __name__ == '__main__':
    if len(sys.argv) < 3:
        print('Usage tree.py depth fanout')
    parser = argparse.ArgumentParser()
    parser.add_argument('depth', help='The depth of the tree topology')
    parser.add_argument('fanout', help='The fanout of each node in the topology')
    args = parser.parse_args()
    depth = int(args.depth)
    fanout = int(args.fanout)
    perfTest(depth, fanout)
    print('Tada!!!')