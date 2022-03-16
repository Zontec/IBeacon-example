
class IBeacon():

    def __init__(self, driver_instace) -> None:
        self.ble_driver_instace = driver_instace

    def setUUID(self, uuid : str) -> None:
        "uuid is 16 bytes should be represented as a string of hex-decimal format: XX XX XX XX ..."
        self.uuid = uuid

    def setMajor(self, major : str) -> None:
        "major is 2 bytes should be represented as string of hex-decimal format: XX XX"
        self.major = major
    
    def setMinor(self, minor : str) -> None:
        "minor is 2 bytes should be represented as string of hex-decimal format: XX XX"
        self.minor = minor

    def setTXPower(self, txpower : str) -> None:
        "txpower used to measure RSSI loss"
        self.txpower = txpower


    def __makeIBeaconMessage(self):

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
        return "1E 02 01 06 1A FF 4C 00 02 15 " + self.uuid + " " + self.major + " " + self.minor + " " + self.txpower

    def up(self) -> None:
        """ start transmission """

        self.ble_driver_instace.init()
        self.ble_driver_instace.up()
        self.ble_driver_instace.setAdvertisingMode()
        self.ble_driver_instace.setSanningState(False)
        self.ble_driver_instace.sendRawData(self.__makeIBeaconMessage())
    
    def down(self):
        """ Start transmission """
        self.ble_driver_instace.down()