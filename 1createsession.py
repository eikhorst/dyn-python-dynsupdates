#! python
########################
### Add my session: (login)
########################
from dyn.tm.session import DynectSession
from dyn.tm.zones import Zone
from dyn.tm.records import ARecord
from dyn.tm.records import CNAMERecord
from dyn.tm.zones import Node
import json, re, sys, math, time, logging

logging.basicConfig(filename='logging.log', filemode='w', level=logging.DEBUG, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', datefmt='%m/%d/%Y %I:%M:%S %p')

print('#####################')
print('Creating Dyn Session')
print('#####################')
dynect_session = DynectSession('customer', 'username', 'password')
if 'username' in dynect_session.username:
	logging.debug('Successfully created session')
else:
	logging.debug('Failed to create session')