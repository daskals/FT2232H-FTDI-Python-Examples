########################################################
#     Spiros Daskalakis                                #
#     Last Revision: 20/10/2021                        #
#     Python Version:  3.9                             #
#     Email:Daskalakispiros@gmail.com                  #
#     Website: www.daskalakispiros.com                 #
########################################################
# use the Numpy library for faster array implementations

# import numpy as np
from pyftdi.spi import SpiController, SpiIOError
import usb
import usb.util
from pyftdi.ftdi import Ftdi
#from dac8552_ftdi import DAC8552, DAC_A, DAC_B, MODE_POWER_DOWN_100K
import numpy as np
import matplotlib.pyplot as plot
import DAC8552_default_config as DAC8552_default_config


def detect_FTDI():
    print("Print FTDI Connected Devices:")
    print(Ftdi.show_devices())

    # dev = usb.core.find(idVendor=0x0403, idProduct=0x6014)
    # dev=usb.core.show_devices()
    # print(dev)


def sine_generator(Fs=200000, t=0.1, freq=30000):
    print('Sine Generator')
    # sampling information
    # Fs = 200000  # sample rate
    T = 1 / Fs  # sampling period
    # t = 0.1  # seconds of sampling
    N = Fs * t  # total points in signal

    # signal information
    # freq = 100  # in hertz, the desired natural frequency
    omega = 2 * np.pi * freq  # angular frequency for sine waves
    t_vec = np.arange(N) * T  # time vector for plotting
    print('Number of Samples:', len(t_vec))
    signal = np.sin(omega * t_vec)

    # normalise the packet to 0 - 1.5 V
    # signal2 = daqV * (signal - np.amin(signal)) / (np.amax(signal) - np.amin(signal)) + minV

    # fig = plot.figure()
    # # Plot a sine wave using time and amplitude obtained for the sine wave
    # plot.plot(t_vec, signal)
    # # Give a title for the sine wave plot
    # plot.title('Sine wave')
    # # Give x axis label for the sine wave plot
    # plot.xlabel('Time')
    # # Give y axis label for the sine wave plot
    # plot.ylabel('Amplitude = sin(time)')
    # plot.grid(True, which='both')
    # plot.axhline(y=0, color='k')
    # plot.show()

    return signal


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    detect_FTDI()

    # STEP 1: Initialise DAC object:
    #dac = DAC8552()
    # STEP two produce the signal
    sine_signal = sine_generator(Fs=200000, t=0.1, freq=100)

    # V_out = V_ref * data / 65536
    Dac_Codes = (sine_signal * 65536) / DAC8552_default_config.v_ref

    ######Mode this part of code to the DAC file

    # Instantiate a SPI controller
    spi = SpiController()

    # Configure the first interface (IF/1) of the FTDI device as a SPI master
    spi.configure('ftdi://ftdi:2232:FT4W2JRU/1')

    # Get a port to a SPI slave w/ /CS on A*BUS3 and SPI mode 0 @ 12MHz
    slave = spi.get_port(cs=0, freq=0.1E6, mode=0)

    # Request the JEDEC ID from the SPI slave
    t_vec = np.arange(2000)
    jedec_id = slave.exchange([1])
    jedec_id = slave.exchange([2])

    ################## 
