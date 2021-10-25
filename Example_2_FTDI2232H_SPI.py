########################################################
#     Spiros Daskalakis                                #
#     Last Revision: 20/10/2021                        #
#     Python Version:  3.9                             #
#     Email:Daskalakispiros@gmail.com                  #
#     Website: www.daskalakispiros.com                 #
########################################################
# use the Numpy library for faster array implementations

#import numpy as np
from pyftdi.spi import SpiController, SpiIOError
import usb
import usb.util
from pyftdi.ftdi import Ftdi

def detect_FTDI():
   
    print("Print FTDI Connected Devices:")
    print(Ftdi.show_devices())

    #dev = usb.core.find(idVendor=0x0403, idProduct=0x6014)
    #dev=usb.core.show_devices()
    #print(dev)


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    
    detect_FTDI()
    # Instantiate a SPI controller
    spi = SpiController()

    # Configure the first interface (IF/1) of the FTDI device as a SPI master
    spi.configure('ftdi://ftdi:2232:FT4W2JRU/1')

    # Get a port to a SPI slave w/ /CS on A*BUS3 and SPI mode 0 @ 12MHz
    slave = spi.get_port(cs=0, freq=12E6, mode=0)

    # Request the JEDEC ID from the SPI slave
    jedec_id = slave.exchange([0x9f], 3)

