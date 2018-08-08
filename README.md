# GFSK TX/RX with GNURadio


## Description 

This software is a generic receiver and transmitter, using SDRs and GNURadio scripts, to receive and transmit GFSK signals.

While the GNURadio receiver is running, the program automatically detects new packets.

Given the appropriate parameters, it is also a GMSK or FSK decoder/encoder.


## Installation

- Dependencies installation. In a Debian-like distribution, these dependencies can be installed with the command: (tested on Ubuntu 18.04 x64)
`sudo apt install gnuradio gr-osmosdr libgtkmm-3.0-1v5`



### Supported SDRs

Currently, the program works with the following SDR devices:

* [RTL-SDR](https://www.rtl-sdr.com/about-rtl-sdr/)
* [FunCube Dongle](http://www.funcubedongle.com/)
* [Ettus USRP Bus Series](https://www.ettus.com/product/category/USRP-Bus-Series)

After the installation of the dependencies, the first two does not require any additional procedure. But, to use a USRP SDR, there is one more step described below:
`TODO: confirm if the source runs with mentioned SDR families without any chance, or some minor tweak is needed. List SDR models fully tested.`

### Configuring the USRP

Before the first use of the USRP, it is necessary to download the FPGA images to the computer. This can be done with the following command:

`sudo uhd_images_downloader`

This procedure must be done only once. After that, when the USRP is connected to the computer, the correspondent FPGA image will be loaded to the USRP.

To allow non-root user to use USRP devices, use the following commands:

```  
cd /usr/lib/uhd/utils
sudo cp uhd-usrp.rules /etc/udev/rules.d/
sudo udevadm control --reload-rules
sudo udevadm trigger
```

After that, any user will be able to use USRP devices.



## Usage

To run the flow directly from terminal:

`python -u gfsk_rx.py -d "rtl_sdr=0" -s 2000000 -f 437500000 -b 1200 -w 25000 -g 1 -o "output.bin"`

Whereas:

-d determines the device used ("rtl_sdr = 0" for RTL-SDR and FunCUBE dongle and "uhd=0" for Ettus USRP)

-s determines the sample rate (minimal and maximal values to be verified for each SDR)

-f determines the central frequency

-b determines the baudrate

-w determines the bandwith of the input filter

-g determines the gain of the demodulator block (1 is the recommended value)

-o determines the name of the output file


### Examples




