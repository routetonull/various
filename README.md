# various scripts


##o3652asa.py

Why? Permit Office 365 public url/addresses on Cisco ASA firewall.

How? Download XML file from Microsoft and use it as source to create objects on ASA CLI.

Usage: download xml file from Microsoft webiste

wget https://support.content.office.net/en-us/static/O365IPAddresses.xml

and run the script:

python o2652asa.py

Copy&paste the output on ASA CLI, create an object group, allow http and https from inside network to internet. Office 365 should work.

Remember to check if the XML from Microsoft is updated from time to time (or even better, automate it).


##DISCLAMER
I take no responsibility for any damage you may do running the scripts I provide here. Use it at your own risk, alway test before running in production.
