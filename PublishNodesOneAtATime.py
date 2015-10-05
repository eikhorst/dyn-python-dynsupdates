#! python
from dyn.tm.zones import Zone
from dyn.tm.records import ARecord
from dyn.tm.records import CNAMERecord
from dyn.tm.zones import Node
import time, logging

logging.basicConfig(filename='test.py.log', filemode='w', level=logging.DEBUG, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', datefmt='%m/%d/%Y %I:%M:%S %p')

#### START FUNCTIONS

def createArecord(thenewnode): 
    thenewnode2 = ARecord
    thenewnode2 = thezone.add_record(thenewnode, record_type='A', address='127.0.0.1', ttl='900')
    print('Created: ' + thenewnode2.fqdn)


def existsinzonealready(thenode):
    noderec = thezone.get_node(thenode).get_any_records()
    try:
        if '127.0.0.1' in str(noderec['a_records'][0]).split(': ')[1]:
            print(thenode + ' exists already')
            return True
        else:
            print(thenode + ' does not exist and should be added')
            return False
    except Exception:
        return False


def deleterecord(thenode): 
    removenode = thenode + '.' + zonename
    node2delete = Node(zonename, removenode)
    print('----Deleting: ' + node2delete.fqdn)
    node2delete.delete()
    print('----Deleted: ' + node2delete.fqdn)


def createcname(thenewnode): 
    thenewnode2 = CNAMERecord  ## create a new instance of the dyn cname record
    thenewnode3 = thenewnode + '.' + zonename # form the full nodename
    thenewnode2 = CNAMERecord(zonename, thenewnode3, cname='www.sourcedomain.com', ttl='14400')
    print('----Created: ' + thenewnode2.fqdn)    


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


def setttl4CName(thenode, thettl):
    myNoderecs = thezone.get_node(thenode).get_all_records()
    thefqdn = thenode + '.' + zonename
    print(thenode)
    print(myNoderecs)
    for rec in myNoderecs['cname_records']:
        print(rec._record_id)
        rec.api_args = {'rdata': {'zone':zonename, 'fqdn': thefqdn, 'record_id':rec._record_id} }
        rec.cname = 'prod.sourcedomain.com'
        rec.ttl = thettl
        rec._update_record


def ReimportFreshList(thezone):    
    icount = 1    
    for counter, i in enumerate(nodescollection):
        try:  
            print(icount)      
            print('--deleting ' + i)
            deleterecord(i)
            print('--publishing ' + i)
            thezone.publish()
            #time.sleep(1)   
            thezone = Zone(zonename)
            print('--creating Arecord ' + i)
            createArecord(i)
            print('--republishing ' + i)
            thezone.publish()        
            #time.sleep(1)   
            thezone = Zone(zonename)
            icount += 1
        except Exception:
            pass
        finally:
            thezone.publish()


def main(thezone):
    ReimportFreshList(thezone)

#### end FUNCTIONS


##################
#
#  START HERE SET YOUR ZONE:  
#
##################
zonename = 'targetzone.com'
thezone = Zone(zonename)

######  
#
#   Designate the list of nodes to act on
#
######
f = open('nodescollection','r')
nodescollection = []
nodescollection = f.read().lower().split()

main(thezone)