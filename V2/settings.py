interface = 'wlo1'
monitor_enable  = 'sudo service network-manager stop;sudo ifconfig wlo1 down;sudo iwconfig wlo1 mode monitor;sudo ifconfig wlo1 up'
monitor_disable = 'sudo ifconfig wlo1 down;sudo iwconfig wlo1 mode Managed;sudo ifconfig wlo1 up;sudo service network-manager start'
change_channel  = 'iw dev wlo1 set channel %s'

channels = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13]

sub_type_filter=["beacon","probe-response","qos-data"]

rssi_level_filter = 60