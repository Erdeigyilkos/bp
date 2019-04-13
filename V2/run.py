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

exportname="/export-" + str(time.time())
dirname, filename = os.path.split(os.path.abspath(__file__))
dirname+=exportname
Rcommand= "sudo Rscript graphexport.R " + dirname


minuteLearning = (datetime.datetime.now().minute+learning_interval)%60

if learning == True:
    minuteDeviceExport = (datetime.datetime.now().minute+export_interval+learning_interval)%60
else:
    minuteDeviceExport = (datetime.datetime.now().minute+export_interval)%60


def start():
 
    setupExportFolder()
    os.system(monitor_enable)

    try: 
        sniff(interface)
    except KeyboardInterrupt: 
        
        os.system(monitor_disable)
        writeVentorCount()
        exportStackBar()
        if(generate_graph == True):
            os.system(Rcommand)
        sys.exit()


def to_address(address):
    return ':'.join('%02x' % ord(b) for b in address)

def sniff(interface):
    max_packet_size = 256
    promiscuous = 0
    timeout = 100
    packets = pcapy.open_live(interface, max_packet_size, promiscuous, timeout)
    packets.setfilter('') 

    
    print("Scanning")    
    
    def loop(header, data):
        global minuteDeviceExport,StackBarActualRecord,StackBarAllRecords,StackBarMAC,learning,minuteLearning,export_interval
        
        if learning == True and minuteLearning == datetime.datetime.now().minute:
            learning = False
         
        if minuteDeviceExport== datetime.datetime.now().minute:
            
            channels_switch()

            minuteDeviceExport=(datetime.datetime.now().minute+export_interval)%60
            
            writeNumberOfDevice()
            
            writeFullTraffic()
                    

            StackBarAllRecords[str(time.time())] = StackBarActualRecord
            StackBarMAC=[]
            StackBarActualRecord={}

            exportStackBar()
            writeVentorCount()
                  
        
        
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
                ProcessFrame(record)
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
                #ProcessFrame(record)
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
                ProcessFrame(record)
                #print record
            
                 
        except Exception as e:
            print ''            
    packets.loop(-1, loop)

def channels_switch():
    global minuteDeviceExport
    channel = str(channels[minuteDeviceExport%len(channels)])
    os.system(change_channel % channel)


FullRecordsToExport=[]
FullRecordsToExport.append(["Date","mac","signal","vendor"])

foundedMac = []
SSIDMac = []

staticDevices = []



foundedMacVendor=[]
DeviceVendor = {}


StackBarAllRecords = {}
StackBarActualRecord={}
StackBarMAC=[]
StackBarManufacter=[]

def ProcessMac(mac,manufacter):
    global DeviceVendor,StackBarMAC,foundedMacVendor

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
            



def ProcessFrame(record):
    if record["strength"]<rssi_level_filter:
        return
    if learning == True and record["source_address"] not in staticDevices:
        staticDevices.append(record["source_address"])
        print("Mac:" + record["source_address"] + "ignored")
    if record["source_address"] in staticDevices:        
        return
    if record["subtype"] in sub_type_filter and record["source_address"] not in SSIDMac:
        SSIDMac.append(record["source_address"])
        return
    if record["source_address"] in SSIDMac:
        return
    if record["source_address"] not in foundedMac:
        foundedMac.append(record["source_address"])
    record["device_type"]= 'unknown'
    if record["source_address"][0:8] in oui:
        record["device_type"] = oui[record["source_address"][0:8]]
        ProcessMac(record["source_address"],record["device_type"])
    printFrame(record)
    FullRecordsToExport.append([str(time.time()),record["source_address"],record["strength"],record["device_type"]])


def printFrame(frame):
    print('Sender:'+ frame["source_address"] + '  Type:' + frame["subtype"]  + '  Strength:' + str(frame["strength"]) + 'dBm')

def writeNumberOfDevice():
    global foundedMac
    NumberOfDevicesExport=[["Date","number",]]
    NumberOfDevicesExport.append([str(time.time()),len(foundedMac)])

    name = dirname+'/Device/numberDevice' + str(datetime.datetime.now()) + '.csv'
    with open(name, "w") as output:
        writer = csv.writer(output, lineterminator='\n')
        writer.writerows(NumberOfDevicesExport)
    foundedMac = []

def writeFullTraffic():
    global FullRecordsToExport
    name = dirname+'/Full/fullexport' + str(datetime.datetime.now()) + '.csv'
    with open(name, "w") as output:
        writer = csv.writer(output, lineterminator='\n')
        writer.writerows(FullRecordsToExport)
    FullRecordsToExport=[]
    FullRecordsToExport.append(["Date","mac","signal","vendor"])

def writeVentorCount():
    os.system("sudo rm " + dirname + "/Vendor/vendor*")
    name = dirname+'/Vendor/vendor' + str(datetime.datetime.now()) + '.csv'
    ExportList=[]
    ExportList.append(["Date","Vendor","Count"])
    for x, y in DeviceVendor.items():
        ExportList.append([str(time.time()),x,y])
   
    with open(name, "w") as output:
        writer = csv.writer(output,lineterminator='\n')
        writer.writerows(ExportList)
    

def exportStackBar():
    
    os.system("sudo rm " + dirname + "/StackBar/stack*")
    global StackBarAllRecords,StackBarManufacter
    
    StackBarAllRecordsExport = StackBarAllRecords
    StackBarManufacterExport = StackBarManufacter

   
    for time,manufacter_dict in StackBarAllRecordsExport.items():
        for manufacter in StackBarManufacterExport:
            if manufacter not in manufacter_dict:
                manufacter_dict[manufacter]=0

   
    StackBarExport=[]
    StackBarLine=["Date"]
        
    for manufacter in sorted(StackBarAllRecordsExport.values()[0].iterkeys()):
        StackBarLine.append(manufacter)
    
    StackBarExport.append(StackBarLine)
    
    StackBarLine=[]
    for time in sorted(StackBarAllRecordsExport.iterkeys()):
        StackBarLine.append(time)
        for manufacter in sorted(StackBarAllRecordsExport[time].iterkeys()):
            StackBarLine.append(StackBarAllRecordsExport[time][manufacter])
        StackBarExport.append(StackBarLine)
        StackBarLine=[]

    name = dirname+'/StackBar/stackBar' + str(datetime.datetime.now()) + '.csv'
    with open(name, "w") as output:
        writer = csv.writer(output, lineterminator='\n')
        writer.writerows(StackBarExport)
  
 
def setupExportFolder():
    os.makedirs(dirname)
    os.makedirs(dirname+"/Full")
    os.makedirs(dirname+"/Device")
    os.makedirs(dirname+"/Vendor")
    os.makedirs(dirname+"/StackBar")
    
start()
