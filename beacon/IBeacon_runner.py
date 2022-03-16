import sys
from HCI_BLE_Driver import HCI_BLE_Driver
from IBeacon import IBeacon
from IBeaconConfig import IBeaconConfig

def main(args : list) -> None:

    ibeacon = IBeacon(HCI_BLE_Driver())
    ibeacon.setUUID(IBeaconConfig.UUID)
    ibeacon.setMinor(IBeaconConfig.MINOR)
    ibeacon.setMajor(IBeaconConfig.MAJOR)
    ibeacon.setTXPower(IBeaconConfig.TXPOWER)
    ibeacon.up()

    print("Transmission has been started successfully!")
    print("Type <exit> to stop the transmission.")

    while True:
        command = input()
        if command == "exit":
            break

    ibeacon.down()

if __name__ == "__main__":
    main(sys.argv[1:])
