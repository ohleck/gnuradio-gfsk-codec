#!/usr/bin/expect
set timeout -1
set code [lindex $argv 0]
set device [lindex $argv 1]
set sample [lindex $argv 2]
set frequency [lindex $argv 3]
set baud [lindex $argv 4]
set bandwidth [lindex $argv 5]
set output [lindex $argv 6]
set ip [lindex $argv 7]
set port [lindex $argv 8]



spawn python2.7 -u $code -d $device -s $sample -f $frequency -b $baud -w $bandwidth -g 1 -o $output -i $ip -p $port 

expect "Press Enter to quit: file_descriptor_sink"
send -- 'r'
