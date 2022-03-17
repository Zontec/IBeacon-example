#This is a working prototype. DO NOT USE IT IN LIVE PROJECTS


import sys
import struct
import bluetooth._bluetooth as bluez

OGF_LE_CTL=0x08
OCF_LE_SET_SCAN_ENABLE=0x000C

def hci_enable_le_scan(sock):
    hci_toggle_le_scan(sock, 0x01)

def hci_disable_le_scan(sock):
    hci_toggle_le_scan(sock, 0x00)

def hci_toggle_le_scan(sock, enable):
    cmd_pkt = struct.pack("<BB", enable, 0x00)
    bluez.hci_send_cmd(sock, OGF_LE_CTL, OCF_LE_SET_SCAN_ENABLE, cmd_pkt)

def packetToString(packet):
    """
    Returns the string representation of a raw HCI packet.
    """
    if sys.version_info > (3, 0):
        return ''.join('%02x' % struct.unpack("B", bytes([x]))[0] for x in packet)
    else:
        return ''.join('%02x' % struct.unpack("B", x)[0] for x in packet)

def parse_events(sock, loop_count=100):
    old_filter = sock.getsockopt( bluez.SOL_HCI, bluez.HCI_FILTER, 14)
    flt = bluez.hci_filter_new()
    bluez.hci_filter_all_events(flt)
    bluez.hci_filter_set_ptype(flt, bluez.HCI_EVENT_PKT)
    sock.setsockopt( bluez.SOL_HCI, bluez.HCI_FILTER, flt )
    results = []
    for i in range(0, loop_count):
        packet = sock.recv(255)
        dataString = packetToString(packet)
        """
        If the bluetooth device is an beacon then show the beacon.
        """
        
############# @ Main logic
        data_array = bytearray.fromhex(dataString)
        custom_device_uuid = b'\x11\x22\x33\x44\x55\x66\x77\x88'
        signature_position = data_array.find(custom_device_uuid)
        #print(dataString)
        if b'\x02\x01\x06' in data_array and signature_position != -1:
            # rssi is always byte number 18 in that package
            rssi = data_array[18]
        # As from the IBeacon spec:
        # 02 01 1A 1A FF 4C 00 02 15 - IBeacon 9 byte prefix for Apple, inc. Please, 
        # refer to a IBeacon frame spec to get more details. 
        # UUID 16-18 bytes. We fix as 16
        # Major
        # Minor
        # 1E - length of the message for driver
        # 02 01 06 - BLE discoverable mode
        # 1A - length of the content
        # FF - custom manufacturer data
        # 4C 00 - Apple's Bluetooth code
        # 02 - Apple's iBeacon type of custom data
        # 15 - length of rest IBeacon data

            device_id_position = signature_position + len(custom_device_uuid)
            x_position = device_id_position + 8 # 8 bytes device id
            y_position = x_position + 2 # 2 bytes major
            tx_position = y_position + 2 # 2 bytes minor

            device_id = data_array[device_id_position : device_id_position + 8]
            x = data_array[x_position : x_position + 2]
            y = data_array[y_position : y_position + 2]
            tx = data_array[tx_position]
            return {
                "dev_id" : device_id,
                "x" : x,
                "y" : y,
                "tx" : -((int(tx) ^ 0xFF) + 1), #convert to 2s complement
                "rssi" : -((int(rssi) ^ 0xFF) + 1), #convert to 2s complement
            }
        return {}
