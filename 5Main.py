#! python
from dyn.tm.zones import Zone
from dyn.tm.records import ARecord
from dyn.tm.records import CNAMERecord
from dyn.tm.zones import Node
import time
import logging
import datetime


logging.basicConfig(filename='logging.log', filemode='w', level=logging.DEBUG, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', datefmt='%m/%d/%Y %I:%M:%S %p')
# START FUNCTIONS


def createArecord(thenewnode):
    thenewnode2 = ARecord
    thenewnode2 = thezone.add_record(thenewnode, record_type='A', address='127.0.0.1', ttl='900')
    print('Created ARecord for : ' + thenewnode2.fqdn)
    logging.debug('Creating ARec: ' + thenewnode2.fqdn)


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
    try:
        removenode = thenode + '.' + zonename
        node2delete = Node(zonename, removenode)
        print('----Deleting: ' + node2delete.fqdn)
        node2delete.delete()
        print('----Deleted: ' + node2delete.fqdn)
        logging.debug('Deleting Node: ' + node2delete.fqdn)
    except Exception:
        pass

def createcname(thenewnode):
    thenewnode2 = CNAMERecord  # create a new instance of the dyn cname record
    thenewnode3 = thenewnode + '.' + zonename  # form the full nodename
    thenewnode2 = CNAMERecord(zonename, thenewnode3, cname='prod.sourcedomain.com', ttl='900')
    print('----Created CNameRecord for : ' + thenewnode2.fqdn)


def setttl4Arec(thenode, thettl):
    myNoderecs = thezone.get_node(thenode).get_all_records()
    thefqdn = thenode + '.' + zonename
    print(thenode)
    print(myNoderecs)
    for rec in myNoderecs['a_records']:
        print(rec._record_id)
        rec.api_args = {'rdata': {'zone':zonename, 'fqdn': thefqdn, 'record_id':rec._record_id}}
        rec.address = '127.0.0.1'
        rec.ttl = thettl
        rec._update_record
        logging.debug('Setting ARecord TTL for:' + thefqdn)


def setttl4CName(thenode, thettl):
    myNoderecs = thezone.get_node(thenode).get_all_records()
    thefqdn = thenode + '.' + zonename
    print(thenode)
    print(myNoderecs)
    for rec in myNoderecs['cname_records']:
        print(rec._record_id)
        rec.api_args = {'rdata': {'zone': zonename, 'fqdn': thefqdn, 'record_id': rec._record_id}}
        rec.cname = 'prod.sourcedomain.com'
        rec.ttl = thettl
        rec._update_record
        logging.debug('Setting CName TTL for:' + thefqdn)
#  Start Methods


def DeleteAll(thezone):
    icount = 1
    print('*** DeleteAll beginning ***')
    try:
        for counter, i in enumerate(nodescollection):
            print(icount)
            print('--deleting ' + i)
            deleterecord(i)
            icount += 1
            print(icount)
    except Exception:
        pass
    finally:
        logging.debug('Final block - DeleteAll')
        print('--publishing all deletes in ' + str(thezone))
        thezone.publish()


def ReimportFreshList(thezone):
    icount = 1
    print('*** ReimportFreshList beginning ***')
    try:
        for counter, i in enumerate(nodescollection):
            print(icount)
            print('--creating ' + i)
            createArecord(i)
            print('--publishing ' + i)
            if counter % 25:
                print('not publishing yet')
                icount += 1
            else:
                if counter == 0:
                    pass  # skip the first publish
                else:
                    print('publish records + import new zone')
                    thezone.publish()
                    time.sleep(1)  # sleep for some time before you continue
                    thezone = Zone(zonename)
                    icount += 1
                    print(icount)
    except Exception:
        pass
    finally:
        logging.debug('Final block - ReimportFreshList')
        thezone.publish()


def UpdateTTLofArecords(thezone, ttl):
    icount = 1
    print('*** UpdateTTLofArecords beginning ***')
    try:
        for counter, i in enumerate(nodescollection):
            print(icount)
            print('--updating TTL of ' + i + ' to ' + str(ttl))
            setttl4Arec(i, ttl)
            if counter % 25:
                print('---NOT PUBLISHING---')
            else:
                if counter == 0:
                    pass  # skip the first publish
                else:
                    print('--------------- PUBLISHING ARecords with new ttl')
                    thezone.publish()
                    time.sleep(1)  # sleep for some time before you continue
                    thezone = Zone(zonename)
                    print(icount)
            icount += 1
    except Exception:
        pass
    finally:
        logging.debug('Final block - UpdateTTLofArecords')
        thezone.publish()
        print('--------------- FINAL PUBLISH ')


def ConvertArecToCname(thezone):
    icount = 1
    batch = []
    print('*** ConvertArecToCname beginning ***')
    try:
        for counter, i in enumerate(nodescollection):
            print(icount)
            print('-- batching zone ARecord deletes ' + i)
            deleterecord(i)
            print('-- before batch.append()' + i)
            batch.append(i)
            print('-- after batch.append()' + i)
            if counter % 25:
                print('---NOT PUBLISHING---')
            else:
                if counter == 0:
                    print('--counter==0 # skip the first publish')
                else:
                    print('--------------- PUBLISHING deletes to ARecords ')
                    thezone.publish()
                    time.sleep(1)  # sleep for some time  before you continue
                    thezone = Zone(zonename)
                    print('***** BEGIN GENERATING CNAMES FOR THIS BATCH *****')
                    for cname in batch:
                        print('### callng cname creation method:  ' + cname)
                        createcname(cname)
                    print('--------------- PUBLISHING CNAMES FOR THIS BATCH ')
                    thezone.publish()
                    time.sleep(1)  # sleep for some time  before you continue
                    thezone = Zone(zonename)
                    print('#### RESETTING THE BATCH ####')
                    batch = []
            icount += 1
    except Exception as inst:
        print(inst)
        pass
    finally:
        logging.debug('Final block - ConvertArecToCname')
        print('----Finally Block - publishing Deletes')
        thezone.publish()
        time.sleep(1)  # sleep for some time  before you continue
        thezone = Zone(zonename)
        print('***** CNAMES - LAST BATCH*****')
        for cname in batch:
            print('### callng cname creation method: ' + cname)
            createcname(cname)
        print('--------------- PUBLISHING LAST BATCH ')
        thezone.publish()
        print('--------------- FINAL PUBLISH ')


def main(thezone):
    stime = datetime.datetime.now()
    logging.debug('START TIME - ' + str(stime.hour)+':'+str(stime.minute))
    print('START TIME - ' + str(stime.hour)+':'+str(stime.minute))
    #DeleteAll(thezone)  # for fast delete of all records
    #ReimportFreshList(thezone)  # for resetting the list for testing
    #UpdateTTLofArecords(thezone, ttl)  # updating ttl of a records
    #ConvertArecToCname(thezone)  # updating ttl of a records
    # tomk UpdateTTLofCNames(thezone, 900) # updating ttl of a records
    etime = datetime.datetime.now()
    logging.debug('END TIME - ' + str(etime.hour)+':'+str(etime.minute))
    print('END TIME - ' + str(etime.hour)+':'+str(etime.minute))


##################
#
#  START HERE SET YOUR ZONE AND TTL:
#
##################
zonename = 'sourcedomain.com'
thezone = Zone(zonename)
ttl = 14400


######
#
#   Nodes to act on from a line delimited file
#
######
f = open('threenodes', 'r')
nodescollection = []
nodescollection = f.read().lower().split()
print("*************")
print(str(len(nodescollection)) + " records")
print("*************")
main(thezone)
