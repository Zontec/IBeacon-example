# IBeacon-example

Client source code is from: https://github.com/bowdentheo/BLE-Beacon-Scanner used by GPL license.
The changes in the client also keep the GPL license.

# Results
Image Hardware.png shows how the system looks in hardware. Two raspberry pi with WiFi and BLE support with Debian-like OS. The Raspberry was located ~1 meter by X coordinate from one another.
Integration.png represents that the beacons are supported from the production tools and may be used with the platform supporting IBeacon BLE frame format
ScannerOut.png shows the result for the client. The actual distance between PIs and clients at the measurement time was ~5m. The approximate location X:2, Y:4.5.



# Beacon
To start with beacon, config the settings in IBeaconConfig.py and type ```sudo python3 IBeacon_runner.py```

# Client
The client is ready as it is. To start client ```sudo python3 BeaconScanner.py```
The client evaluates two points to calculate the rough position relative to the (0, 0) position. 

## License

MIT