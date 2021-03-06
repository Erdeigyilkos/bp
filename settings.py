interface = 'wlo1'
monitor_enable  = 'sudo service network-manager stop;sudo ifconfig wlo1 down;sudo iwconfig wlo1 mode monitor;sudo ifconfig wlo1 up'
monitor_disable = 'sudo ifconfig wlo1 down;sudo iwconfig wlo1 mode Managed;sudo ifconfig wlo1 up;sudo service network-manager start'
change_channel  = 'iw dev wlo1 set channel %s'
channels = [6]
sub_type_filter=["beacon","probe-response","qos-data"]
rssi_level_filter = -900
learning = False
learning_interval = 3
export_interval = 1
generate_graph=True