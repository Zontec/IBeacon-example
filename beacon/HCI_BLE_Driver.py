from lib2to3.pytree import Base
import os
# implementation over Host Controller Interface(HCI) component to prevent extra instalation 
# and keep simplicity as much as possible 
class HCI_BLE_Driver():

    HCI_BLE_CONTROLLER = (
        "hci0",
        "hci1",
        "hci2",
        "hci3",
        "hci4",
    )

    CONFIG_PREAMBLE = "sudo hciconfig"

    def __init__(self) -> None:
        """ Initially by default hci0 controller is used. Not checked for availability. """
        self.hci_controller = HCI_BLE_Driver.HCI_BLE_CONTROLLER[0]

    def checkIsHCIControllerAvailable(self):
        """ Checks for controller availability. 0 if everything is fine """
        return os.system(f"{HCI_BLE_Driver.CONFIG_PREAMBLE} {self.hci_controller} > /dev/null")

    def init(self) -> None:
        """ Looks for free HCI controller. Base exception will be raised if not found """

        is_found = False
        for hci_controller in HCI_BLE_Driver.HCI_BLE_CONTROLLER:
            status = os.system(f"{HCI_BLE_Driver.CONFIG_PREAMBLE} {hci_controller} > /dev/null")
            if status == 0:
                self.hci_controller = hci_controller
                is_found = True
                break
        
        if is_found == False:
            raise BaseException("No controller was found!")


    def setSanningState(self, state:bool) -> None:
        """ 
        Set up scanning state. If there's a need to scan for BLE devices True should be passed. 
        False in opposite. In case of failure the exception will be raised
        """

        if state == False:
            res = os.system(f"{HCI_BLE_Driver.CONFIG_PREAMBLE} {self.hci_controller} noscan")
        else:
            res = os.system(f"{HCI_BLE_Driver.CONFIG_PREAMBLE} {self.hci_controller} scan")

        if res != 0:
            raise BaseException(f"set scanning state with {state} fails with error {res}")

    def __setTransmitMode(self, mode):
        return os.system(f"{HCI_BLE_Driver.CONFIG_PREAMBLE} {self.hci_controller} leadv {mode}")

    def setAdvertisingMode(self) -> None:
        """ Set broadcast advertising mode """

        res = self.__setTransmitMode(3) # see HCI configuration instruction
        if res != 0:
            raise BaseException(f"setAdvertisingMode fails with error {res}. Check status on HCI spec")

    def setGeneralMode(self) -> None:
        """ Set general transmission mode """

        res = self.__setTransmitMode(0) # see HCI configuration instruction
        if res != 0:
            raise BaseException(f"setGeneralMode fails with error {res}. Check status on HCI spec")
    
    def up(self) -> None:
        """ switch on HCI controller """
        os.system(f"{HCI_BLE_Driver.CONFIG_PREAMBLE} {self.hci_controller} up")

    def down(self) -> None:
        """ switch off HCI controller """
        os.system(f"{HCI_BLE_Driver.CONFIG_PREAMBLE} {self.hci_controller} down")

    def sendRawData(self, payload : str) -> None:
        """ 
        Sends raw string to the controller to be transmitted over BLE. 
        In case of failure raise exception.
        """

        # 0x08 0x0008 should be observed over documentation. For the version from 2020 
        # the following parameters are used for transmission
        res = os.system(f"sudo hcitool -i {self.hci_controller} cmd 0x08 0x0008 " + payload + " 00")

        if res != 0:
            raise BaseException(f"Transmission fail with error {res}")
