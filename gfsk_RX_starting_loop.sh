#!/usr/bin/expect
set timeout -1

spawn python2.7 -u gfsk_rx.py -d "rtl_sdr=0" -s 1000000 -f 437500000 -b 9600 -w 25000 -g 1 -o "/dev/null" -i "127.0.0.1" -p 7000 

expect "Press Enter to quit: file_descriptor_sink"
send -- 'r'