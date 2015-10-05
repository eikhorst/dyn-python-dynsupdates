#! python
from dyn.tm.zones import Zone
from dyn.tm.records import ARecord
from dyn.tm.records import CNAMERecord
from dyn.tm.zones import Node
import time

########################
#Load zone function not working just leave in here for now
########################
#exec(open('loadzone.py').read())
def loadzone(zone):
    thezone = Zone('zone')
    print('Loaded: ')
    print(thezone)


########################
### Function to add new zones to targetzone ###
########################
def createArecord(thenewnode): 
    thenewnode2 = ARecord
    thenewnode2 = thezone.add_record(thenewnode, record_type='A', address='127.0.0.1', ttl='14400')
    print('Created: '+ thenewnode2.fqdn)

########################
### Function to Check if zone exists ###
########################
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



def deleterecord(thenode): 
    removenode = thenode+'.targetzone.com'
    node2delete = Node('targetzone.com', removenode)
    print('Deleting: '+ node2delete.fqdn)
    node2delete.delete()
    print('Deleted: ' + node2delete.fqdn)


def createcname(thenewnode): 
    thenewnode2 = CNAMERecord
    thenewnode3 = thenewnode + '.targetzone.com'
    thenewnode2 = CNAMERecord('targetzone.com', thenewnode3, cname='prod.sourcedomain.com', ttl='14400')
    print('Created: ' + thenewnode2.fqdn)    


def setttl4Arec(thenode, thettl):
    myNoderecs = thezone.get_node(thenode).get_all_records()
    thefqdn = thenode + '.' + zonename
    print(thenode)
    print(myNoderecs)
    for rec in myNoderecs['a_records']:
        print(rec._record_id)
        rec.api_args = {'rdata': {'zone':zonename, 'fqdn': thefqdn, 'record_id':rec._record_id} }
        rec.address = '127.0.0.1'
        rec.ttl = thettl
        rec._update_record


def convertrecord(therec):
    try:
        print('--DELETING ' + therec)
        deleterecord(therec)
        print('--PUBLISHING ' + therec)
        thezone.publish()
        thezone = Zone(thezonename)
        print('--CREATING CNAME ' + therec)
        createcname(therec)
        print('--PUBLISHING CNAME ' + therec)
        thezone.publish()
        thezone = Zone(thezonename)
    except Exception as inst:
        print(inst)
        pass


thezonename = 'targetzone.com'
thezone = Zone(thezonename)


## for testing
f = open('nodescollection','r')
nodescollection = []
nodescollection = f.read().lower().split()


icount = 0
for counter, i in enumerate(nodescollection):
    try:
        print('--DELETING ' + i)
        deleterecord(i)
        print('--PUBLISHING ' + i)
        thezone.publish()
        thezone = Zone(thezonename)
        print('--CREATING CNAME ' + i)
        createcname(i)
        print('--PUBLISHING CNAME ' + i)
        thezone.publish()
        thezone = Zone(thezonename)
        time.sleep(5)   
    except Exception:
        pass
    finally:
        thezone.publish()
