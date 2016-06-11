
'''
sourcefile from Microsoft:
 https://support.content.office.net/en-us/static/O365IPAddresses.xml

hot to extract network-object list to create a group on ASA:
  python o3652asa.py | grep object | gawk "{print \"network-object object \"$3}"

'''

import xml.etree.ElementTree as etree
import re


def asaIpNetworkObject(ip,net):
	print "object network O365_"+ip
	print "subnet "+net
	return 1

def asaFqdnNetworkObject(fqdn):
	#fqdn = fqdn.replace ("*","")
	fqdn = re.sub("^\*\.","",fqdn)
	fqdn = re.sub("^.*\*","",fqdn)
	fqdn = re.sub("^\.","",fqdn)
	print "object network O365_"+fqdn
	print "fqdn "+fqdn
	return 1

def slash2sub(ip):	
	sub = ip
	if "/4" in ip:
		sub = ip.replace("/4"," 240.0.0.0")
	elif "/5" in ip:
		sub = ip.replace("/5"," 248.0.0.0")
	elif "/6" in ip:
		sub = ip.replace("/6"," 252.0.0.0")
	elif "/7" in ip:
		sub = ip.replace("/7"," 254.0.0.0")
	elif "/8" in ip:
		sub = ip.replace("/8"," 255.0.0.0")
	elif "/9" in ip:
		sub = ip.replace("/9"," 255.128.0.0")
	elif "/10" in ip:
		sub = ip.replace("/10"," 255.192.0.0")
	elif "/11" in ip:
		sub = ip.replace("/11"," 255.224.0.0")
	elif "/12" in ip:
		sub = ip.replace("/12"," 255.240.0.0")
	elif "/13" in ip:
		sub = ip.replace("/13"," 255.248.0.0")
	elif "/14" in ip:
		sub = ip.replace("/14"," 255.252.0.0")
	elif "/15" in ip:
		sub = ip.replace("/15"," 255.254.0.0")
	elif "/16" in ip:
		sub = ip.replace("/16"," 255.255.0.0")
	elif "/17" in ip:
		sub = ip.replace("/17"," 255.255.128.0")
	elif "/18" in ip:
		sub = ip.replace("/18"," 255.255.192.0")
	elif "/19" in ip:
		sub = ip.replace("/19"," 255.255.224.0")
	elif "/20" in ip:
		sub = ip.replace("/20"," 255.255.240.0")
	elif "/21" in ip:
		sub = ip.replace("/21"," 255.255.248.0")
	elif "/22" in ip:
		sub = ip.replace("/22"," 255.255.252.0")
	elif "/23" in ip:
		sub = ip.replace("/23"," 255.255.254.0")
	elif "/24" in ip:
		sub = ip.replace("/24"," 255.255.255.0")
	elif "/25" in ip:
		sub = ip.replace("/25"," 255.255.255.128")
	elif "/26" in ip:
		sub = ip.replace("/26"," 255.255.255.192")
	elif "/27" in ip:
		sub = ip.replace("/27"," 255.255.255.224")
	elif "/28" in ip:
		sub = ip.replace("/28"," 255.255.255.240")
	elif "/29" in ip:
		sub = ip.replace("/29"," 255.255.255.248")
	elif "/30" in ip:
		sub = ip.replace("/30"," 255.255.255.252")
	elif "/31" in ip:
		sub = ip.replace("/31"," 255.255.255.254",1)
	elif "/32" in ip:
		sub = ip.replace("/32"," 255.255.255.255")
	elif "/1" in ip:
		sub = ip.replace("/1"," 128.0.0.0")
	elif "/2" in ip:
		sub = ip.replace("/2"," 192.0.0.0")
	elif "/3" in ip:
		sub = ip.replace("/3"," 224.0.0.0")
	else:
		sub = ip+" 255.255.255.255"
	return sub


tree = etree.parse('O365IPAddresses.xml') 

root = tree.getroot()

e = tree.findall('product')

for i in e:
	#print i.attrib
	if i.attrib['name'] == "o365":
		#print "o365"
		for type in i:
			#print type.attrib
			if type.attrib['type'] == "IPv4":
				#print type
				for ip in type:
					#print slash2sub(ip.text)
					asaIpNetworkObject(ip.text.replace("/","_"),slash2sub(ip.text))
					#print ip.text
			#if type.attrib['type'] == "IPv6":
			#	print type
			#	for ipv6 in type:
			#		print ipv6.text
			if type.attrib['type'] == "URL":
				#print type
				for url in type:
					#fqdn = str(url.text)					
					asaFqdnNetworkObject(url.text)
