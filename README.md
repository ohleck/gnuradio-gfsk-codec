# GFSK TX/RX with GNURadio


## 1. Description 

This software is a generic receiver and transmitter, using SDRs and GNURadio scripts, to receive and transmit GFSK signals.

While the GNURadio receiver is running, the program automatically detects new packets.

Given the appropriate parameters, it is also a GMSK or FSK decoder/encoder.


## 2. Installation

- Dependencies installation. In a Debian-like distribution, these dependencies can be installed with the command: (tested on Ubuntu 18.04 x64)
`sudo apt install gnuradio gr-osmosdr`



### 2.1 Supported SDRs

Currently, the program works with the following SDR devices:

* [RTL-SDR](https://www.rtl-sdr.com/about-rtl-sdr/)
* [FunCube Dongle](http://www.funcubedongle.com/)
* [Ettus USRP Bus Series](https://www.ettus.com/product/category/USRP-Bus-Series)

After the installation of the dependencies, the first two does not require any additional procedure. But, to use a USRP SDR, there is one more step described below:
`TODO: confirm if the source runs with mentioned SDR families without any chance, or some minor tweak is needed. List SDR models fully tested.`

### 2.2 Configuring permissions

Before the first use of the any of the SDRs, it is necessary to download the FPGA images to the computer. This can be done with the following command:

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



## 3. Usage

**Disclaimer**: All the usage codes are for the application of the Ettus USRP, for other SDRs you may need to change the parameters to the acceptable/ideal for it.

### 3.1 To run the TX and RX flow directly from terminal:

Parameters:

-d determines the device used ("rtl_sdr = 0" for RTL-SDR and FunCUBE dongle and "uhd=0" for Ettus USRP)

-s determines the sampling rate (minimal and maximal values to be verified for each SDR)

-f determines the central frequency

-b determines the baudrate

-w determines the bandwith of the input filter (**RX only**)

-g determines the gain of the demodulator block (1 is the recommended value) (**RX only**)

-o determines the name of the output file -- "/dev/null" allows to discard the file directly (**RX only**)

-i determines the ip adress of the TCP server

-p determines the port of the TCP server

-q determines if the input file should be a raw bitstream or an lower case hexadecimal stream (0 for binary stream or 1 for hexadecimal stream) (**TX only**)

**Note**: for the Ettus USRP at a sampling rate of more than 1 MHz implicates in an overflow and in the terminal it will be printed "O"s to flag the overflow. As the Ettus USRP accepts only fixed values of sampling rate (250 KHz, 500 KHz, 1 MHz, 2 MHz and 4 MHz), the maximal recommended sampling rate for this application is 1 MHz.

#### 3.1.1 For RX only

`python2.7 -u gfsk_rx.py -d "rtl_sdr=0" -s 1000000 -f 437500000 -b 9600 -w 25000 -g 1 -o "/dev/null" -i "127.0.0.1" -p 7000`

##### 3.1.1.1 To verify if the flow works


To be able to verify if the server works this commenad should be used in the terminal:

`nc 127.0.0.1 7000 | hexdump`

This command connects a client to the TCP server created and receives the data from it, while grouping the bits into a hexadecimal code. 

##### 3.1.1.2 To automate RX flow from the terminal

To be able to run the bash terminal it is necessary to install (in a Debian like distribuition):

`$ sudo apt install expect `

To fully automate the RX flow from the terminal a bash script is used. To run it you should run the command:

`while true; do expect gfsk_RX_starting_loop.sh gfsk_rx.py "rtl_sdr=0" 1000000 437500000 9600 25000 "/dev/null" "127.0.0.1" 7000 ; done`

This codes input already the parameters in the same order as the python execution code.

**Note**: in this case the RX options are hardcoded in the script, if needed to change/know just look the `spawn` line.

#### 3.1.2 For TX only 

`python2.7 -u gfsk_tx.py -d "rtl_sdr=0" -s 1000000 -f 437500000 -b 9600 -i "127.0.0.1" -p 7000 -q 0`

### 4.  Examples

This is section describes how to run the examples

#### 4.1 Netcat server to test

This code allows the creation of a NetCat TCP server to fully test the python parser code, in a infinite loop. To do this it is needed to modify the *gfsk_sample.bin* file in the repository by adding your sync word anywhere and then run this command + python script (it only sends data once the server is connected to the client):

`while true; do nc -l 127.0.0.1 7000 < samples/gfsk_sample.bin; done`

Filter stream and display only the desired packet (sync word + N bytes):
`./streamFilter.py -ip localhost -port 7000 -syncWord 0x53 -packet_length 4 -display_time -verbose`