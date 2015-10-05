#! python
from dyn.tm.session import DynectSession
from dyn.tm.zones import Zone
from dyn.tm.records import ARecord
from dyn.tm.records import CNAMERecord
from dyn.tm.zones import Node
import json, re, sys, math, time

## get the target zone
targetzone = Zone('targetzone.com')
## get the sourcedomain zone
sourcezone = Zone('sourcedomain.com')


## get all nodes from sourcedomain and copy all the AReords pointing to 127.0.0.1
sourcenodes = sourcezone.get_all_nodes()

nodescollection = []
print('#####################')
print('Loading sourcedomain nodes')
print('#####################')
for node in sourcenodes:
    name = str(node).split(': ')[1]
    pre = name.replace('.sourcedomain.com','')
    # now add this subnode to the listof all the nodes to reproduce
    # can add these to the targetzone
    # before i add check if it is pointing to the .1 address first
    noderec = dict
    try:
        print('#####################')
        print('Trying to find records in ' + pre)
        noderec = sourcezone.get_node(pre).get_any_records()
        if '127.0.0.1' in str(noderec['a_records'][0]).split(': ')[1]: 
            nodescollection.append(pre) 
            print('-->>> appending ' + pre)
    except Exception as inst:
        print(inst)
        pass


print('#####################')
print('sourcedomain node import successful')
print('#####################')

f = open('nodescollection','w')

for item in nodescollection:
    f.write("%s\n" % item)

print('#####################')
print('sourcedomain node list written to file successful')
print('#####################')
