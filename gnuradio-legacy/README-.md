This project uses a SDR to receive and transmit data in FSK modulation by first creating a GNU Radio flow and then tweaking 
the automatically generated python code. The SDR used is the Analog's PlutoSDR, which is hardcoded in the python code and 
GRC flow.

##Pre-requisites

It is recommended to follow the PlutoSDR drivers procedure from Analog's website:
https://wiki.analog.com/university/tools/pluto/drivers/linux

As for installation packages you need to:

sudo apt install python gnuradio gr-iio python-matplotlib python-numpy

##Usage

python2.7 CSU_FSK_Demod_PlutoSDR.py
python2.7 CSU_FSK_TX_Mod_PlutoSDR.py
