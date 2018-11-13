import sys
import os
import traceback
import time
import datetime
import pcapy
import dpkt
from subtypes import *
import json
import csv


interface = 'wlo1'
monitor_enable  = 'sudo service network-manager stop;sudo ifconfig wlo1 down;sudo iwconfig wlo1 mode monitor;sudo ifconfig wlo1 up'
monitor_disable = 'sudo ifconfig wlo1 down;sudo iwconfig wlo1 mode Managed;sudo ifconfig wlo1 up;sudo service network-manager start'
change_channel  = 'iw dev wlo1 set channel %s'

channels = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13]


def start():
    os.system(monitor_enable)
    try: 
        sniff(interface)
    except KeyboardInterrupt: 
        with open("data_file.json", "w") as write_file:
            json.dump(recordToExport, write_file)

        with open("export.csv", "w") as output:
            writer = csv.writer(output, lineterminator='\n')
            writer.writerows(recordToExport)
        print foudedMac    
        print(str(len(foudedMac)) + " Found")
        os.system(monitor_disable)
        os.system("R < test.r --no-save")
        sys.exit()


def to_address(address):
    return ':'.join('%02x' % ord(b) for b in address)

def sniff(interface):
    channels_switch(5)
    max_packet_size = 256
    promiscuous = 0
    timeout = 100
    packets = pcapy.open_live(interface, max_packet_size, promiscuous, timeout)
    packets.setfilter('') 
    
    def loop(header, data):
        
        try:
            packet = dpkt.radiotap.Radiotap(data)
            packet_signal = -(256 - packet.ant_sig.db)
            frame = packet.data
            
            if frame.type == dpkt.ieee80211.MGMT_TYPE:
                record = {
                    'timestamp': '0',
                    'type': 'management',
                    'subtype': subtypes_management[frame.subtype],
                    'strength': packet_signal,
                    'source_address': to_address(frame.mgmt.src),
                    'destination_address': to_address(frame.mgmt.dst),
                    'access_point_name': frame.ssid.data if hasattr(frame, 'ssid') else '(n/a)',
                    'access_point_address': to_address(frame.mgmt.bssid)
                }
                addToArray(record["source_address"],record["strength"])
                print record
                
            elif frame.type == dpkt.ieee80211.CTL_TYPE:
                record = {
                    'timestamp': '0',
                    'type': 'control',
                    'subtype': subtypes_control[frame.subtype],
                    'strength': packet_signal,
                    'source_address': '(n/a)', 
                    'destination_address': '(n/a)', 
                    'access_point_name': '(n/a)', 
                    'access_point_address': '(n/a)' 
                }
                #addToArray(record["source_address"],record["strength"])
                print record
                
            elif frame.type == dpkt.ieee80211.DATA_TYPE:
                record = {
                    'timestamp': '0',
                    'type': 'data',
                    'subtype': subtypes_data[frame.subtype],
                    'strength': packet_signal,
                    'source_address': to_address(frame.data_frame.src),
                    'destination_address': to_address(frame.data_frame.dst),
                    'access_point_name': '(n/a)', 
                    'access_point_address': to_address(frame.data_frame.bssid) if hasattr(frame.data_frame, 'bssid') else '(n/a)'
                }
                addToArray(record["source_address"],record["strength"])
                print record
            
                 
        except Exception as e:
            print e            
    packets.loop(-1, loop)

def channels_switch(newchange):
    channel = str(channels[0])
    os.system(change_channel % channel)

foudedMac=[]
recordToExport=[]
recordToExport.append(["Date","mac","signal"])

def addToArray(mac,rssi):
    if rssi<-200:
        return
    foudedMac.append(mac)
    recordToExport.append([str(time.time()),mac,rssi])
       
    
start()
