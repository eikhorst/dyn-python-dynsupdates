#! python
from dyn.tm.zones import Zone
from dyn.tm.records import ARecord
from dyn.tm.records import CNAMERecord
from dyn.tm.zones import Node
import time
########################
### Function to add new zones to targetzone ###
########################
def createArecord(thenewnode): 
    thenewnode2 = ARecord
    thenewnode2 = thezone.add_record(thenewnode, record_type='A', address='127.0.0.1', ttl='900')
    print('Created: '+ thenewnode2.fqdn)

def existsinzonealready(thenode):
    noderec = thezone.get_node(thenode).get_any_records()
    try:
        if '127.0.0.1' in str(noderec['a_records'][0]).split(': ')[1]: 
            print(thenode+' exists already')
            return True
        else:
            print(thenode+ ' does not exist and should be added')
            return False
    except Exception:
        return False


#targetzone = Zone('targetzone.com') ## create input here to take in whatever zone

zonename = 'targetzone.com'
thezone = Zone(zonename)

################################
f = open('nodescollection','r')
nodescollection = []
nodescollection = f.read().lower().split()

#total = len(nodescollection)
#numsubmitted = 25

icount = 0
for counter, i in enumerate(nodescollection):
    try:
        createArecord(i)
        if counter % 25:
            print('not publishing yet')
        else:
            if counter == 0:
                pass #skip the first publish
            else:
                print('publish records + import new zone') 
                thezone.publish()               
                time.sleep(1) # sleep for some time before you continue
                thezone = Zone(zonename)
                icount += 1
                print(icount)
    except Exception:
        pass
    finally:
        thezone.publish()
