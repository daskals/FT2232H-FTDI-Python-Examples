# -*- coding: utf-8 -*-
"""DAC8552 - Python module for interfacing Texas Instruments DAC8552
digital to analog converter with the Raspberry Pi via SPI bus.

Download: https://github.com/adn05/dac8552

Depends on PiGPIO library, see:
http://abyz.me.uk/rpi/pigpio/python.html

Code inspired from PiPyADC: https://github.com/ul-gh/PiPyADC

License: GNU LGPLv2.1, see:
https://www.gnu.org/licenses/old-licenses/lgpl-2.1-standalone.html

Narcisse Assogba, 2018-07-17
"""
from time import sleep

import pigpio as io

import DAC8552_default_config as DAC8552_default_config

# --- Definition of control byte bits constants --- #
# Control byte : logic OR together to form the control command value.
# Example: control = BUFFER_A | MODE_POWER_DOWN_1K | UPDATE_CHANNEL_A
# Write to Buffer A Power-Down Command and LOAD DAC A (DAC A Powered Down with 1kΩ tired to ground)

# Buffer select bit that control the destination of the data between DAC A and DAC B
BUFFER_A = 0x00
BUFFER_B = 0x04

# DAC output updating control, you can use the two options simultaneously
UPDATE_DAC_A = 0x10
UPDATE_DAC_B = 0x20

# Operating modes, Table 3, p.15
MODE_NORMAL = 0x00
MODE_POWER_DOWN_1K = 0x01
MODE_POWER_DOWN_100K = 0x02
MODE_POWER_DOWN_HI = 0x03  # High Impedance Mode

# --- Channel selection constants --- #
DAC_A = BUFFER_A | UPDATE_DAC_A
DAC_B = BUFFER_B | UPDATE_DAC_B

# --- Timing constants --- #
# When using hardware/hard-wired chip select, still a command to command
# timeout of t_9 is needed as a minimum for the next commands.
T_9_TIMEOUT = 100 / (10 ** 9)


class DAC8552(object):
    """Python class for interfacing the DAC8552 digital to analog converters with the Raspberry Pi.

    Download: https://github.com/adn05/dac8552

    Default pin and settings configuration is for the Open Hardware
    "Waveshare High-Precision AD/DA Board"
    See file DAC8552_default_config.py for configuration settings and description.

    Documentation source: Texas Instruments DAC8552
    datasheet SBAS288: http://www.ti.com/lit/ds/symlink/dac8552.pdf
    """

    @property
    def v_ref(self):
        """Get/Set DAC analog reference input voltage differential.

        This is only for calculation of output value scale factor.
        """
        return self._v_ref

    @v_ref.setter
    def v_ref(self, value):
        self._v_ref = value

    @property
    def digit_per_v(self):
        """Get DAC numeric output digit per volts.

        Readonly: This is a convenience value calculated from v_ref.
        """
        return int(65535 / self.v_ref)

    @digit_per_v.setter
    def digit_per_v(self, value):
        raise AttributeError("This is a read-only attribute")

    def __init__(self, conf=DAC8552_default_config, pi=None):
        """Constructor for the DAC object

        Hardware pin configuration must be set up at initialization phase and can not be changed later.
        Default config is read from external file (module) import
        :param conf: config file imported
        :param pi: PiGPIO object
        """
        # Set up the pigpio object if not provided as an argument
        if pi is None:
            pi = io.pi()
        self.pi = pi
        if not pi.connected:
            raise IOError("Could not connect to hardware via pigpio library")
        # Config and initialize the SPI and GPIO pins used by the ADC.
        self.SPI_CHANNEL = conf.SPI_CHANNEL
        self.CS_PIN = conf.CS_PIN

        # GPIO Outputs the CS_PIN.
        if conf.CS_PIN is not None:
            pi.set_mode(conf.CS_PIN, io.OUTPUT)
            pi.write(conf.CS_PIN, 1)

        # Initialize the pigpio SPI setup. Return value is a handle for the
        # SPI device.
        self.spi_id = pi.spi_open(conf.SPI_CHANNEL, conf.SPI_FREQUENCY, conf.SPI_FLAGS)

        # Initialise class properties
        self.v_ref = conf.v_ref

    def _chip_select(self):
        """If chip select hardware pin is connected to SPI bus hardware pin or hardwired to GND, do nothing.

        In a normal write sequence, kept the SYNC line LOW for at least 24 falling edges of SCLK and the
        addressed DAC register is updated on the 24th falling edge.
        """
        if self.CS_PIN is not None:
            self.pi.write(self.CS_PIN, 0)

    def _chip_release(self):
        """ Release chip select """
        if self.CS_PIN is not None:
            self.pi.write(self.CS_PIN, 1)
        sleep(T_9_TIMEOUT)  # Minimal time before the next command. I think this can be void

    def power_down(self, channel, mode):
        """Toggle the selected channel to Power Down Mode

        There are the three power-down modes. The supply current falls to 700nA at 5V (400nA at 3V).
        And the output stage is also internally switched from the output of the amplifier to a
        resistor network of known values. The output is connected internally to GND through a 1kΩ
        resistor, a 100kΩ resistor, or it is left open-circuited (High-Impedance).
        :param channel: DAC_A or DAC_B , to select DAC A or DAC B
        :param mode: MODE_POWER_DOWN_1K , MODE_POWER_DOWN_100K or MODE_POWER_DOWN_HI
        """
        control = (channel | mode) & 0xFF
        self._chip_select()
        # we send the control byte 0 like data to fill the 24 bits.
        self.pi.spi_write(self.spi_id, [control, 0, 0])
        self._chip_release()

    def write_dac(self, channel, data):
        """Write a 16 bit data to th selected channel

        The input coding for each device is unipolar straight binary, so the ideal output voltage
        is given by: V_out = V_ref * data / 65536
        :param channel: DAC_A or DAC_B , to select DAC A or DAC B
        :param data: 0 - 65535 , decimal equivalent of the binary code that is loaded to the DAC register
        """
        control = channel | MODE_NORMAL
        self._chip_select()
        # we send the control byte, the first 8 data bits (MSB) and the final 8 data bits.
        self.pi.spi_write(self.spi_id, [control, data >> 8, data & 0xFF])
        self._chip_release()
