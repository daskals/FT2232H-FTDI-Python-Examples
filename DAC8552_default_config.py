# -*- coding: utf-8 -*-

# ###############  Raspberry Pi Physical Interface Properties  #################
# SPI bus configuration and GPIO pins used for the ADS1255/ADS1256.
# These defaults are used by the constructor of the ADS1256 class.
#
# The following pins are compatible
# with the Waveshare High Precision AD/DA board on the Raspberry Pi 2B and 3B
#
# SPI_CHANNEL corresponds to the chip select hardware bin controlled by the
# SPI hardware. For the Waveshare board this pin is not even connected, so this
# code does not use hardware-controlled CS and this is a don't care value.
# FIXME: Implement hardware chip select as an option.


SPI_CHANNEL = 1
# SPI_FLAGS sets MODE=1 <=> CPOL=0, CPHA=1. See pigpio documentation.
# The waveshare ADC board does not use the SPI peripheral hardware for the chip
# select lines, but uses the CS_PIN GPIO defined further below. CS disabled:
#             bbbbbbRTnnnnWAuuupppmm
SPI_FLAGS = 0b0000000000000011100001
# When using the SPI hardware chip select lines, use the following flags:
# SPI_FLAGS      = 0b0000000000000000000001

# The DAC8552 serial clock frequency can be as high as 30MHz, making it compatible
# with high speed DSPs.
# But the second circuit on the the Waveshare board, the ADS1256, limit SPI frequency
# to 1920000 Hz. However, since the Raspberry pi works better with power-of-two
# fractions of the system clock, the closest value would be 250MHz/256 = 976563 Hz
# for RPi 2 and 400MHz/256 = 1562500 Hz for RPi 3.
# SPI_FREQUENCY = 30000000
SPI_FREQUENCY = 976563

# The RPI GPIOs used: All of these are optional and must be set to None if not
# used. See datasheet.
# CS_PIN = None
CS_PIN = 23

# Analog reference voltage at VREF pin
v_ref = 3.3
###############################################################################

"""####################  Extended Description: DAC8552 Input Shift Register  ####################
The input shift register of the DAC8552 is 24 bits wide and is made up of eight control 
bits (DB16–DB23) and 16 data bits (DB0–DB15). 

       DB23                                                                    DB16        DB15               DB0
    |    0    |    0    |   LDB   |   LDA   |    X    | Buf Sel |    PD1    |    PD0    |        D15 ... D0        | 
    
Logically OR all desired option values together to form a control byte.
Data bits are transferred to the specified Data Buffer or DAC Register, depending on the command 
issued by the control byte.

=>  The first two control bits (DB22 and DB23) are reserved and must be '0' for proper operation.

=>  LDA (DB20) and LDB (DB21) control the updating of each analog output with the specified
    16-bit data value or power-down command. 
    
    # LDA value definitions:
        UPDATE_DAC_A = 0x10
        UPDATE_DAC_B = 0x20
    
=>  Bit DB19 is a don't care bit that does not affect the operation of the DAC8552.
    
=>  Buffer Select (DB18), controls the destination of the data (or power-down command)
    between DAC A and DAC B. 
    
    # Buffer select definitions:
        BUFFER_A = 0x00
        BUFFER_B = 0x04
    
=>  PD0 (DB16) and PD1 (DB17), select the power-down mode of one or both of the DAC
    channels. The four modes are normal mode or any one of three power-down modes. 
     
    In power-down modes, the supply current falls to 700nA at 5V (400nA at 3V).
    And the output stage is also internally switched from the output of the amplifier to a
    resistor network of known values. The output is connected internally to GND through a 1kΩ
    resistor, a 100kΩ resistor, or it is left open-circuited (High-Impedance).
    
            PD1 (DB17)  PD0 (DB16)      OPERATING MODE
                0           0           Normal Operation
                0           1           Output typically 1kΩ to GND
                1           0           Output typically 100kΩ to GND
                1           1           High impedance
    
    # Modes value definitions:
        MODE_NORMAL           = 0x00
        MODE_POWER_DOWN_1K    = 0x01
        MODE_POWER_DOWN_100K  = 0x02
        MODE_POWER_DOWN_HI    = 0x03 
"""
