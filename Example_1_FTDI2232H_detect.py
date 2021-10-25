########################################################
#     Spiros Daskalakis                                #
#     Last Revision: 20/10/2021                        #
#     Python Version:  3.9                             #
#     Email:Daskalakispiros@gmail.com                  #
#     Website: www.daskalakispiros.com                 #
########################################################
# use the Numpy library for faster array implementations

#import numpy as np
import usb
import usb.util
from pyftdi.ftdi import Ftdi

def detect_FTDI():
    """
    Prints the existing FTDI interfaces.

            Parameters:
                    none

            Returns:
                    nullpython
    """
    print("Print FTDI Connected Devices:")
    print(Ftdi.show_devices())
    #dev = usb.core.find(idVendor=0x0403, idProduct=0x6014)
    #dev=usb.core.show_devices()
    #print(dev)


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    detect_FTDI()

