#!/usr/bin/env python
# encoding: utf-8

"""
ifstats.py
TODO:  lots of clean up.  make configurable using ConfigParser.
"""

from time import sleep
from pysnmp.entity.rfc3413.oneliner import cmdgen

interval = 5
cg = cmdgen.CommandGenerator()
comm_data = cmdgen.CommunityData('', 'SNMP-RO-COMMUNITY')
transport = cmdgen.UdpTransportTarget(('IP_OR_HOSTNAME', 161))

# Interface 2.1
# these OIDs are valid for BIG-IP LTM 3900
inbound1 = (1, 3, 6, 1, 4, 1, 3375, 2, 1, 2, 4, 4, 3, 1, 3, 3, 50, 46, 49)
outbound1 = (1, 3, 6, 1, 4, 1, 3375, 2, 1, 2, 4, 4, 3, 1, 5, 3, 50, 46, 49)

# Interface 2.2
# these OIDs are valid for BIG-IP LTM 3900
inbound2 = (1, 3, 6, 1, 4, 1, 3375, 2, 1, 2, 4, 4, 3, 1, 3, 3, 50, 46, 50)
outbound2 = (1, 3, 6, 1, 4, 1, 3375, 2, 1, 2, 4, 4, 3, 1, 5, 3, 50, 46, 50)

# Poll both interfaces (clean up needed)
errIndication, errStatus, errIndex, int1in1 = cg.getCmd(comm_data, transport, inbound1)
errIndication, errStatus, errIndex, int1out1 = cg.getCmd(comm_data, transport, outbound1)
errIndication, errStatus, errIndex, int2in1 = cg.getCmd(comm_data, transport, inbound2)
errIndication, errStatus, errIndex, int2out1 = cg.getCmd(comm_data, transport, outbound2)

# sleep for 5s
sleep(interval)

# Poll both interfaces again (clean up needed)
errIndication, errStatus, errIndex, int1in2 = cg.getCmd(comm_data, transport, inbound1)
errIndication, errStatus, errIndex, int1out2 = cg.getCmd(comm_data, transport, outbound1)
errIndication, errStatus, errIndex, int2in2 = cg.getCmd(comm_data, transport, inbound2)
errIndication, errStatus, errIndex, int2out2 = cg.getCmd(comm_data, transport, outbound2)

# Interface 1:  convert to lists rather than individual variables, clean up
int1mbpsIn = (float(int1in2[0][1]) - float(int1in1[0][1])) * 8 / (interval*1000000)
int1mbpsOut = (float(int1out2[0][1]) - float(int1out1[0][1])) * 8 / (interval*1000000)
int1mbpsTotal = int1mbpsIn + int1mbpsOut
int1pctIn = "{:.2%}".format(int1mbpsIn / 1000)
int1pctOut = "{:.2%}".format(int1mbpsOut / 1000)
int1pctTotal = "{:.2%}".format(int1mbpsTotal / 2000) 

# Interface 2:  convert to lists rather than individual variables, clean up
int2mbpsIn = (float(int2in2[0][1]) - float(int2in1[0][1])) * 8 / (interval*1000000)
int2mbpsOut = (float(int2out2[0][1]) - float(int2out1[0][1])) * 8 / (interval*1000000)
int2mbpsTotal = int2mbpsIn + int2mbpsOut
int2pctIn = "{:.2%}".format(int2mbpsIn / 1000)
int2pctOut = "{:.2%}".format(int2mbpsOut / 1000)
int2pctTotal = "{:.2%}".format(int2mbpsTotal / 2000)

# Display
print "\nInterface 2.1:\n"
print("\tThroughput\t\tUtilization")
print("\t===================================")
print("\t" + str(int1mbpsIn) + "\t(IN)\t" + int1pctIn)
print("\t" + str(int1mbpsOut) + "\t(OUT)\t" + int1pctOut) 
print("\t" + str(int1mbpsTotal) + "\t(TOTAL)\t" + int1pctTotal + "\n")
print "\nInterface 2.2:\n"
print("\tThroughput\t\tUtilization")
print("\t===================================")
print("\t" + str(int2mbpsIn) + "\t(IN)\t" + int2pctIn)
print("\t" + str(int2mbpsOut) + "\t(OUT)\t" + int2pctOut) 
print("\t" + str(int2mbpsTotal) + "\t(TOTAL)\t" + int2pctTotal + "\n")
