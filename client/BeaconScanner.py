#This is a working prototype. DO NOT USE IT IN LIVE PROJECTS

import ScanUtility
import bluetooth._bluetooth as bluez
import threading
import math
from datetime import datetime

devices = {}
RSSI_CORRELATION_VALUE = 2.5

def computeCoordinates(point1 : tuple, point2 : tuple) -> tuple:
	""" 
	Compute intersection points between circles.
	No/One point intersection not counted into
	"""
	x0, y0, r0 = point1
	x1, y1, r1 = point2
	d = math.sqrt((x1-x0)**2+(y1-y0)**2)
	a = (r0**2-r1**2+d**2)/(2*d)
	h = math.sqrt(abs(r0**2-a**2))
	x2 = x0+a*(x1-x0)/d   
	y2 = y0+a*(y1-y0)/d   
	x3 = x2+h*(y1-y0)/d
	y3 = y2-h*(x1-x0)/d
	return ((x2,y2), (x3, y3))

def getDist(rssi : int, tx : int) -> float:
	""" 
	Ekvilibristika function to count distance in meters from RSSI value and TX power.
	The values should be 2's complement 
	"""
	return 10.**(float(tx - rssi) /(10 * RSSI_CORRELATION_VALUE))

def printPointsAndDevicesInfo(points : tuple, devices : dict) -> None:
	print(f"############### {datetime.now()} ###############")
	print(f"Info: {devices}")
	print(f"Points: {points}\n")

# No race condition within the function since of python GIL
def updateDistances(device_info : dict) -> None:
	""" 
	Function add/update values for each device and prints distances.
	Important: implemented distance count only for two points.
	In the case of 3,4... points, the strategy may be taking the points with the smallest RSSI value.
	"""
	# get hashable string
	dev_id = device_info['dev_id'].hex()
	# the structure is kept as (x, y, dist)
	devices[dev_id] = (
		int.from_bytes(device_info['x'], byteorder='big', signed=True),
		int.from_bytes(device_info['y'], byteorder='big', signed=True),
		getDist(device_info['rssi'], device_info['tx'])
	)
	
	# when there's more 2 and more unique devices
	if len(devices) >= 2:
		# take only first two unique devices
		key0, key1 = list(devices)[:2]
		points = computeCoordinates(devices[key0], devices[key1])
		printPointsAndDevicesInfo(points, devices)


def main() -> None:
	# Set bluetooth device. Default 0.
	dev_id = 0
	try:
		sock = bluez.hci_open_dev(dev_id)
		print ("\n *** Looking for BLE Beacons ***\n")
		print ("\n *** CTRL-C to Cancel ***\n")
	except:
		print ("Error accessing bluetooth")

	ScanUtility.hci_enable_le_scan(sock)
	#Scans for iBeacons
	try:
		while True:
			device_info = ScanUtility.parse_events(sock, 100)
			if device_info != {}:
				print(device_info)
				threading.Thread(target=updateDistances, args=(device_info,)).start()

	except KeyboardInterrupt:
		pass

if __name__ == "__main__":
	main()
