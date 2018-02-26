#!/usr/bin/python
from easysnmp import Session
from datetime import datetime,timedelta
from datetime import date
import time
import sys
import argparse

# some usefuls OIDs
ifAlias = '1.3.6.1.2.1.31.1.1.1.18'
ifLastChange = '1.3.6.1.2.1.2.2.1.9'
ifName = '1.3.6.1.2.1.31.1.1.1.1'
ifIndex = '1.3.6.1.2.1.2.2.1.1'
ifOperStatus = '1.3.6.1.2.1.2.2.1.8'
sysUpTime = '1.3.6.1.2.1.1.3.0'
ifDescr = '1.3.6.1.2.1.2.2.1.2'
ifstatus={'1':'up','2':'down','3':'testing'}

description = """Lists device interfaces, current operstatus and lastchange days"""

def lastchange2date(uptime,lastchange):
    if uptime >= lastchange:
        diff = int(uptime)-int(lastchange)
    else:
        diff = int(uptime)

    d0 = datetime.fromtimestamp(time.time()-diff/100)
    d1 = datetime.now()
    delta = d1 - d0
    return str(delta.days)
        

def main():

    parser = argparse.ArgumentParser(description=description)
    parser.add_argument("-H", "--hostname", help="IP Address / Hostname to check [REQUIRED]",type=str, required=True)
    parser.add_argument("-c", "--community",help="SNMP Community (default 'public')",type=str,default='public')

    args = parser.parse_args()
    hostname = args.hostname
    comm = args.community
    
    session = Session(hostname=hostname, community=comm, version=2)
    try:
        item = session.walk(ifName)
    except:
        sys.exit('\nSNMP PROBLEM host '+hostname+" check IP and COMMUNITY\n")
    # get uptime to calculate last change
    uptime = session.get(sysUpTime).value
    print '\nHOST\t'+hostname
    print "\nUPTIME\t"+str(timedelta(seconds=(int(uptime)/100)))+"\n"
    # port names to include or ignore to filter useless values
    include= ('ethernet')
    ignore = ('StackSub-St-','StackPort','Vl','vlan','VLAN','VLAN-','Trk','lo','oobm','Po','Nu','Gi/--Uncontrolled','Gi/--Controlled','Te/--Uncontrolled','Te/--Controlled')
    for value in item:
        # remove all digits from port names before filtering
        result = ''.join(i for i in value.value if not i.isdigit())
        if (result in include) or (result not in ignore):
            ifname = value.value
            # id defines the interface, will be appended to following snmp get
            id = value.oid_index
            if not id:
                id = value.oid.split(".")[-1]
            opstatus = ifstatus[session.get(ifOperStatus+'.'+id).value]
            lastchangedate = lastchange2date(uptime,session.get(ifLastChange+'.'+id).value)
            print str(ifname)+"\tSTATUS "+opstatus+"\tLAST CHANGE SINCE DAYS\t"+lastchangedate

main()