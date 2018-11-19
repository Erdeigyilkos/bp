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

minutes = 0
sub_type_filter=["beacon","probe-response","qos-data"]

def start():
    os.system(monitor_enable)
    try: 
        sniff(interface)
    except KeyboardInterrupt: 
        with open("export.csv", "w") as output:
            writer = csv.writer(output, lineterminator='\n')
            writer.writerows(recordToExport)
        with open("exportNumberOfDevice.csv", "w") as output:
            writer = csv.writer(output, lineterminator='\n')
            writer.writerows(NumberOfDevicesExport)
        
        os.system(monitor_disable)
        os.system("R < test.r --no-save")
        os.system("R < graphDevices.r --no-save")
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
        global minutes
        
        if minutes!= datetime.datetime.now().minute:
            minutes=datetime.datetime.now().minute
            addNumberOfDevices()
        exit
        
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
                addToFullExport(record["source_address"],record["strength"],record["subtype"])
                #print record
                
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
                #print record
                
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
                addToFullExport(record["source_address"],record["strength"],record["subtype"])
                #print record
            
                 
        except Exception as e:
            print e            
    packets.loop(-1, loop)

def channels_switch(newchange):
    channel = str(channels[0])
    os.system(change_channel % channel)


recordToExport=[]
recordToExport.append(["Date","mac","signal"])

NumberOfDevicesExport=[["Date","number",]]

foundedMac = []


def addNumberOfDevices():
    NumberOfDevicesExport.append([str(time.time()),len(foundedMac)])
    while len(foundedMac) > 0 : foundedMac.pop()

def checkMac(mac):
    
    if mac not in foundedMac:
        foundedMac.append(mac)


def addToFullExport(mac,rssi,sub_type):
    
    if sub_type not in sub_type_filter:
        checkMac(mac)
        print(sub_type)
    if rssi<-200:
        return
    recordToExport.append([str(time.time()),mac,rssi])
       
    
start()
