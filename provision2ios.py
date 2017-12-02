'''
read this for details
https://www.ifconfig.it/hugo/post/2017-08-07-python-hp-to-cisco-switchport-migration/
'''
from netmiko import ConnectHandler
import getpass
swip = raw_input('IP ADDRESS: ')
swun = raw_input('SWITCH USERNAME: ')
swpass = getpass.getpass()
connection = ConnectHandler(ip=swip, device_type='hp_procurve', username=swun, password=swpass)
cisco_output = open("cisco_output.txt", 'w')
portlist = open("portlist.total.txt", 'r')
for port in portlist:
	porthp = port.strip().split()[0]
	portcisco = port.strip().split()[1]
	print ("MAPPING HP PORT "+porthp+" TO CISCO PORT "+portcisco)
	command="sh vlans ports "+porthp+" detail"
	result = connection.send_command(command)
	cisco_output.write("interface "+portcisco+"\n") 
	trunk = 0
	if "Tagged" in result:
		trunk = 1
		cisco_output.write("switchport mode trunk\n")
		cisco_output.write("switchport trunk allowed vlan 1\n")
		if "Untagged" not in result:
			cisco_output.write("switchport trunk native vlan 1\n")            
	else:
		cisco_output.write("switchport mode access\n")
	for line in result.splitlines():     
		if "Tagged" in line and trunk:
			fields = line.strip().split()
			cisco_output.write("switchport trunk allowed vlan add "+fields[0]+"\n")
		elif "Untagged" in line:
			fields = line.strip().split()
			if trunk: cisco_output.write("switchport trunk allowed vlan add "+fields[0]+"\n"+"switchport trunk native vlan "+fields[0]+"\n")
			else: cisco_output.write("switchport access vlan "+fields[0]+"\n")
		elif "Port name" in line:
			fields = line.strip().split(":")
			cisco_output.write("description "+fields[1]+"\n")
cisco_output.close()
connection.disconnect()
