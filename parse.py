__author__ = 'anil'
import os
#import sys

#20140702052857,10.0.0.2,59506,10.0.0.1,500,7,26.0-27.0,45490620,363924960
rootdir = os.getcwd()
totalBW = {}
linecount = 0
filecount = 0

for root, subFolders, files in os.walk(rootdir):
    for filename in files:
        if(filename.endswith('out')):
            portBW = {}
            filecount += 1
            filePath = os.path.join(root, filename)
            fp = open(filePath, 'r')
            content = fp.read().split(':')
            #print content
            for line in content:
                if(len(line.split(',')) == 9):
                    stat = line.split(',')
                    currCount = long(stat[7]) + long(stat[8])
                    if(portBW.has_key(stat[4])):
                        if(portBW.get(stat[4]) < currCount):
                            portBW[stat[4]] = currCount
                    else:
                        portBW[stat[4]] = currCount
                else:
                    print line
            print 'processed', filename
            currBW = 0
            for each in portBW:
                currBW += portBW[each]
            totalBW[filename] = currBW/1000

print totalBW
throughPut = 0
for each in totalBW:
    throughPut += totalBW[each]
print throughPut/300000 *8 , 'kbps'
