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
import csv

dirname, filename = os.path.split(os.path.abspath(__file__))
dirname+="/export"
Rcommand= "sudo Rscript graphexport.R " + dirname


minuteLearning = (datetime.datetime.now().minute+learning_interval)%60

if learning == True:
    minutes = datetime.datetime.now().minute+interval+learning_interval%60
    minuteDeviceExport = (datetime.datetime.now().minute+interval+learning_interval)%60
else:
    minutes = datetime.datetime.now().minute+interval%60
    minuteDeviceExport = (datetime.datetime.now().minute+interval)%60


def start():

    SSIDMac.append("00:00:00:00:00:01")
    setupExportFolder()
    os.system(monitor_enable)

    try: 
        sniff(interface)
    except KeyboardInterrupt: 
        
        os.system(monitor_disable)
        writeVentorCount()
        exportStackBar()
        os.system(Rcommand)
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
        global minutes,minuteDeviceExport,StackBarActualRecord,StackBarAllRecords,StackBarMAC,learning,minuteLearning,interval
        
        if learning == True and minuteLearning == datetime.datetime.now().minute:
            learning = False


        if minutes == datetime.datetime.now().minute:
            minutes=(datetime.datetime.now().minute+interval)%60
            addNumberOfDevices()
        

        if minuteDeviceExport== datetime.datetime.now().minute:
            
            minuteDeviceExport=(datetime.datetime.now().minute+interval)%60
            print('Time' + str(datetime.datetime.now().minute))
            print('NextTime' + str(minuteDeviceExport))
            writeNumberOfDevice()
            writeFullTraffic()
            
            StackBarAllRecords[str(time.time())] = StackBarActualRecord
            StackBarMAC=[]
            StackBarActualRecord={}
                  
        
        
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
                addToFullExport(record["source_address"],record["strength"],record["subtype"])
                print record
            
                 
        except Exception as e:
            print ''            
    packets.loop(-1, loop)

def channels_switch(newchange):
    channel = str(channels[0])
    os.system(change_channel % channel)


recordToExport=[]
recordToExport.append(["Date","mac","signal","vendor"])

NumberOfDevicesExport=[["Date","number",]]

foundedMac = []
SSIDMac = []

staticDevices = []


foundedMacVendor=[]
DeviceVendor = {}

def addNumberOfDevices():
    NumberOfDevicesExport.append([str(time.time()),len(foundedMac)])
    while len(foundedMac) > 0 : foundedMac.pop()


StackBarAllRecords = {}
StackBarActualRecord={}
StackBarMAC=[]
StackBarManufacter=[]

def checkMac(mac,manufacter):
    global DeviceVendor,StackBarMAC

    if mac not in StackBarMAC:
        StackBarMAC.append(mac)

        if manufacter not in StackBarManufacter:
            StackBarManufacter.append(manufacter)

        if manufacter not in StackBarActualRecord:
            StackBarActualRecord[manufacter] = 1
        else:
            StackBarActualRecord[manufacter] +=1 


    if mac not in foundedMacVendor: #pocty zarizeni
        foundedMacVendor.append(mac)
        if manufacter not in DeviceVendor:
            DeviceVendor[manufacter]=1
        else:
            count = DeviceVendor[manufacter]+1
            DeviceVendor[manufacter]=count
            #print(DeviceVendor)
            



def addToFullExport(mac,rssi,sub_type):
    if rssi<rssi_level_filter:
        return

    if mac in staticDevices:
        print("ignored")
        return

    if learning == True and mac not in staticDevices:
        staticDevices.append(mac)
        print("Mac:" + mac + "ignored")


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

def exportStackBar():
    global StackBarAllRecords,StackBarManufacter

    print('--------PRED dopnineni 0-----------')
    for x,y in StackBarAllRecords.items():
        print(x)
        print(StackBarAllRecords[x])
    print('--------------/PRED dopleni 0-----------')

    for time,manufacter_dict in StackBarAllRecords.items():
        for manufacter in StackBarManufacter:
            if manufacter not in manufacter_dict:
                manufacter_dict[manufacter]=0

    print('--------Po doplneni 0-----------')
    for x in sorted(StackBarAllRecords.iterkeys()):
        print(x)
        print(StackBarAllRecords[x])
    print('--------------/Po dolneni 0-----------')

    StackBarExport=[]
    StackBarLine=["Date"]
        
    for manufacter in sorted(StackBarAllRecords.values()[0].iterkeys()):
        StackBarLine.append(manufacter)
    
    StackBarExport.append(StackBarLine)
    
    StackBarLine=[]
    for time in sorted(StackBarAllRecords.iterkeys()):
        StackBarLine.append(time)
        for manufacter in sorted(StackBarAllRecords[time].iterkeys()):
            StackBarLine.append(StackBarAllRecords[time][manufacter])
        StackBarExport.append(StackBarLine)
        StackBarLine=[]

    print('-----------EXPORT---------')
    print(StackBarExport)
    print('-----------EXPORT---------')

    name = 'export/StackBar/stackBar' + str(datetime.datetime.now()) + '.csv'
    with open(name, "w") as output:
        writer = csv.writer(output, lineterminator='\n')
        writer.writerows(StackBarExport)
   


    
def setupExportFolder():
    if not os.path.exists("export"):
        os.makedirs("export")
    if not os.path.exists("export/Full"):
        os.makedirs("export/Full")
    if not os.path.exists("export/Device"):
        os.makedirs("export/Device")
    if not os.path.exists("export/Vendor"):
        os.makedirs("export/Vendor")
    if not os.path.exists("export/StackBar"):
        os.makedirs("export/StackBar")
    
start()
