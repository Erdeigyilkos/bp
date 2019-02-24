import sys
import os
import traceback
import time
import datetime
import pcapy
import dpkt
from subtypes import *
from oui import *
from settings import * 
import json
import csv





minutes = datetime.datetime.now().minute
minuteDeviceExport = datetime.datetime.now().minute+1



def start():

    SSIDMac.append("00:00:00:00:00:01")
    setupExportFolder()
    os.system(monitor_enable)

    try: 
        sniff(interface)
    except KeyboardInterrupt: 
        
        os.system(monitor_disable)
        writeVentorCount()
        os.system("R < graphexport.R --no-save")
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
        global minutes,minuteDeviceExport
        
        if minutes!= datetime.datetime.now().minute:
            minutes=datetime.datetime.now().minute
            addNumberOfDevices()
        

        if minuteDeviceExport== datetime.datetime.now().minute:
            
            minuteDeviceExport=(datetime.datetime.now().minute+1)%60
            print('Time' + str(datetime.datetime.now().minute))
            print('NextTime' + str(minuteDeviceExport))
            writeNumberOfDevice()
            writeFullTraffic()
            
        
        
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
recordToExport.append(["Date","mac","signal","vendor"])

NumberOfDevicesExport=[["Date","number",]]

foundedMac = []
SSIDMac = []


foundedMacVendor=[]
DeviceVendor = {}

def addNumberOfDevices():
    NumberOfDevicesExport.append([str(time.time()),len(foundedMac)])
    while len(foundedMac) > 0 : foundedMac.pop()

def checkMac(mac,manufacter):
    global DeviceVendor
    if mac not in foundedMacVendor: 
        foundedMacVendor.append(mac)
        if manufacter not in DeviceVendor:
            DeviceVendor[manufacter]=1
        else:
            count = DeviceVendor[manufacter]+1
            DeviceVendor[manufacter]=count
            #print(DeviceVendor)
            



def addToFullExport(mac,rssi,sub_type):
    if rssi<-80:
        return

    if sub_type in sub_type_filter and mac not in SSIDMac:
        SSIDMac.append(mac)
        return
    
    if mac in SSIDMac:
        return

    if mac not in foundedMac:
        foundedMac.append(mac)

    device_type = 'unknown'
    if mac[0:8] in oui:
        device_type = oui[mac[0:8]]
        checkMac(mac,device_type)
    
    
    print(sub_type)
    recordToExport.append([str(time.time()),mac,rssi,device_type])
       
def writeNumberOfDevice():
    name = 'export/Device/numberDevice' + str(datetime.datetime.now()) + '.csv'
    with open(name, "w") as output:
        writer = csv.writer(output, lineterminator='\n')
        writer.writerows(NumberOfDevicesExport)
    while len(NumberOfDevicesExport) > 1 : NumberOfDevicesExport.pop()

def writeFullTraffic():
    name = 'export/Full/fullexport' + str(datetime.datetime.now()) + '.csv'
    with open(name, "w") as output:
        writer = csv.writer(output, lineterminator='\n')
        writer.writerows(recordToExport)
    while len(recordToExport) > 1 : recordToExport.pop()

def writeVentorCount():
    name = 'export/Vendor/vendor' + str(datetime.datetime.now()) + '.csv'
    ExportList=[]
    ExportList.append(["Date","Vendor","Count"])
    for x, y in DeviceVendor.items():
        ExportList.append([str(time.time()),x,y])
   
    with open(name, "w") as output:
        writer = csv.writer(output,lineterminator='\n')
        writer.writerows(ExportList)
    DeviceVendor.clear()


    
def setupExportFolder():
    if not os.path.exists("export"):
        os.makedirs("export")
    if not os.path.exists("export/Full"):
        os.makedirs("export/Full")
    if not os.path.exists("export/Device"):
        os.makedirs("export/Device")
    if not os.path.exists("export/Vendor"):
        os.makedirs("export/Vendor")
    
start()
