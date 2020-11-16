# -*- coding: utf-8 -*-
import nmap
import sys

scan_row = []
input_data = input('Please input hosts and port: ')
scan_row = input_data.split(" ")
if len(scan_row) != 2:
    print('Input errors, example \"192.168.1.0/24 80,443,22\"')
    sys.exit()

hosts = scan_row[0]
port = scan_row[1]

try:
    nm = nmap.PortScanner()
except nmap.PortScannerError:
    print('Nmap not found', sys.exc_info()[0])
    sys.exit()
except:
    print('Unexpected error:', sys.exc_info()[0])
    sys.exit()

try:
    nm.scan(hosts=hosts, arguments=' -v -sS -p ' + port)
except Exception as e:
    print('Scan error:' + str(e))

for host in nm.all_hosts():
    print('----------------------------' + host + '-------------------------------')
    print('Hostname %s' % nm[host].hostname())
    print('State %s' % nm[host].state())
    for proto in nm[host].all_protocols():
        print('================')
        print('Protocol: %s' % proto)

        lport = nm[host][proto].keys()
        list(lport).sort()
        for port in lport:
            print('port: %s\tstate: %s' % (port, nm[host][proto][port]['state']))
