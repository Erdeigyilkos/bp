import os
import threading
import json
import datetime
import subprocess


os.system("sudo tshark -I -i wlo1 -a duration:60 -w /tmp/tshark-output")

command = [
        'tshark', '-r',
        '/tmp/tshark-output', '-T',
        'fields', '-e',
        'wlan.sa', '-e',
        'wlan.bssid', '-e',
        'radiotap.dbm_antsignal'
    ]

tshark = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
output,n = tshark.communicate()

foundMacs = []
foundMacs2 = []

for line in output.decode('utf-8').split('\n'):
        print("Line:" + line)
        if line.strip() == '':
            continue
        if len(line.split()) is not 3:
            continue
        
        mac = line.split()[0]
        rssi = line.split()[2]
        if(len(mac)>6):
            if mac not in foundMacs:
                foundMacs.append(mac)
                foundMacs2.append([mac,str(datetime.datetime.now()),rssi])

         
print("Nalezeno: " + str(len(foundMacs2)))
print(foundMacs2)


with open("data_file.json", "w") as write_file:
    json.dump(foundMacs2, write_file)
