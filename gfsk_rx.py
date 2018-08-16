#!/usr/bin/env python2
# -*- coding: utf-8 -*-
##################################################
# GNU Radio Python Flow Graph
# Title: GFSK Receiver
# Author: Gabriel Mariano Marcelino
# Generated: Thu Aug 16 09:16:19 2018
##################################################


from gnuradio import analog
from gnuradio import blocks
from gnuradio import digital
from gnuradio import eng_notation
from gnuradio import filter
from gnuradio import gr
from gnuradio.eng_option import eng_option
from gnuradio.filter import firdes
from grc_gnuradio import blks2 as grc_blks2
from optparse import OptionParser
import math
import osmosdr
import time


class gfsk_rx(gr.top_block):

    def __init__(self, default_bandwidth=20e3, default_baud=9600, default_bin_file_sink="/tmp/rx_data.bin", default_freq=437.5e6, default_gain=1, default_ip_0='127.0.0.1', default_port_0=5000, default_samp=1000000, sdr_dev="rtl=0"):
        gr.top_block.__init__(self, "GFSK Receiver")

        ##################################################
        # Parameters
        ##################################################
        self.default_bandwidth = default_bandwidth
        self.default_baud = default_baud
        self.default_bin_file_sink = default_bin_file_sink
        self.default_freq = default_freq
        self.default_gain = default_gain
        self.default_ip_0 = default_ip_0
        self.default_port_0 = default_port_0
        self.default_samp = default_samp
        self.sdr_dev = sdr_dev

        ##################################################
        # Blocks
        ##################################################
        self.osmosdr_source_0 = osmosdr.source( args="numchan=" + str(1) + " " + sdr_dev )
        self.osmosdr_source_0.set_sample_rate(default_samp)
        self.osmosdr_source_0.set_center_freq(default_freq, 0)
        self.osmosdr_source_0.set_freq_corr(0, 0)
        self.osmosdr_source_0.set_dc_offset_mode(0, 0)
        self.osmosdr_source_0.set_iq_balance_mode(0, 0)
        self.osmosdr_source_0.set_gain_mode(False, 0)
        self.osmosdr_source_0.set_gain(10, 0)
        self.osmosdr_source_0.set_if_gain(20, 0)
        self.osmosdr_source_0.set_bb_gain(20, 0)
        self.osmosdr_source_0.set_antenna('', 0)
        self.osmosdr_source_0.set_bandwidth(0, 0)

        self.low_pass_filter_1 = filter.fir_filter_fff(100, firdes.low_pass(
        	1, default_samp, default_baud, default_baud/6, firdes.WIN_HAMMING, 6.76))
        self.low_pass_filter_0 = filter.fir_filter_ccf(1, firdes.low_pass(
        	1, default_samp, default_bandwidth/2, default_bandwidth/2/6, firdes.WIN_HAMMING, 6.76))
        self.digital_clock_recovery_mm_xx_0 = digital.clock_recovery_mm_ff(default_samp/(default_baud*100), 0.001, 0, 0.25, 0.001)
        self.digital_binary_slicer_fb_0 = digital.binary_slicer_fb()
        self.blocks_unpacked_to_packed_xx_0 = blocks.unpacked_to_packed_bb(1, gr.GR_MSB_FIRST)
        self.blocks_file_sink_1 = blocks.file_sink(gr.sizeof_char*1, default_bin_file_sink, False)
        self.blocks_file_sink_1.set_unbuffered(False)
        self.blks2_tcp_sink_0 = grc_blks2.tcp_sink(
        	itemsize=gr.sizeof_char*1,
        	addr=default_ip_0,
        	port=default_port_0,
        	server=True,
        )
        self.analog_quadrature_demod_cf_0 = analog.quadrature_demod_cf(default_gain)

        ##################################################
        # Connections
        ##################################################
        self.connect((self.analog_quadrature_demod_cf_0, 0), (self.low_pass_filter_1, 0))
        self.connect((self.blocks_unpacked_to_packed_xx_0, 0), (self.blks2_tcp_sink_0, 0))
        self.connect((self.blocks_unpacked_to_packed_xx_0, 0), (self.blocks_file_sink_1, 0))
        self.connect((self.digital_binary_slicer_fb_0, 0), (self.blocks_unpacked_to_packed_xx_0, 0))
        self.connect((self.digital_clock_recovery_mm_xx_0, 0), (self.digital_binary_slicer_fb_0, 0))
        self.connect((self.low_pass_filter_0, 0), (self.analog_quadrature_demod_cf_0, 0))
        self.connect((self.low_pass_filter_1, 0), (self.digital_clock_recovery_mm_xx_0, 0))
        self.connect((self.osmosdr_source_0, 0), (self.low_pass_filter_0, 0))

    def get_default_bandwidth(self):
        return self.default_bandwidth

    def set_default_bandwidth(self, default_bandwidth):
        self.default_bandwidth = default_bandwidth
        self.low_pass_filter_0.set_taps(firdes.low_pass(1, self.default_samp, self.default_bandwidth/2, self.default_bandwidth/2/6, firdes.WIN_HAMMING, 6.76))

    def get_default_baud(self):
        return self.default_baud

    def set_default_baud(self, default_baud):
        self.default_baud = default_baud
        self.low_pass_filter_1.set_taps(firdes.low_pass(1, self.default_samp, self.default_baud, self.default_baud/6, firdes.WIN_HAMMING, 6.76))
        self.digital_clock_recovery_mm_xx_0.set_omega(self.default_samp/(self.default_baud*100))

    def get_default_bin_file_sink(self):
        return self.default_bin_file_sink

    def set_default_bin_file_sink(self, default_bin_file_sink):
        self.default_bin_file_sink = default_bin_file_sink
        self.blocks_file_sink_1.open(self.default_bin_file_sink)

    def get_default_freq(self):
        return self.default_freq

    def set_default_freq(self, default_freq):
        self.default_freq = default_freq
        self.osmosdr_source_0.set_center_freq(self.default_freq, 0)

    def get_default_gain(self):
        return self.default_gain

    def set_default_gain(self, default_gain):
        self.default_gain = default_gain
        self.analog_quadrature_demod_cf_0.set_gain(self.default_gain)

    def get_default_ip_0(self):
        return self.default_ip_0

    def set_default_ip_0(self, default_ip_0):
        self.default_ip_0 = default_ip_0

    def get_default_port_0(self):
        return self.default_port_0

    def set_default_port_0(self, default_port_0):
        self.default_port_0 = default_port_0

    def get_default_samp(self):
        return self.default_samp

    def set_default_samp(self, default_samp):
        self.default_samp = default_samp
        self.osmosdr_source_0.set_sample_rate(self.default_samp)
        self.low_pass_filter_1.set_taps(firdes.low_pass(1, self.default_samp, self.default_baud, self.default_baud/6, firdes.WIN_HAMMING, 6.76))
        self.low_pass_filter_0.set_taps(firdes.low_pass(1, self.default_samp, self.default_bandwidth/2, self.default_bandwidth/2/6, firdes.WIN_HAMMING, 6.76))
        self.digital_clock_recovery_mm_xx_0.set_omega(self.default_samp/(self.default_baud*100))

    def get_sdr_dev(self):
        return self.sdr_dev

    def set_sdr_dev(self, sdr_dev):
        self.sdr_dev = sdr_dev


def argument_parser():
    parser = OptionParser(usage="%prog: [options]", option_class=eng_option)
    parser.add_option(
        "-w", "--default-bandwidth", dest="default_bandwidth", type="eng_float", default=eng_notation.num_to_str(20e3),
        help="Set default_bandwidth [default=%default]")
    parser.add_option(
        "-b", "--default-baud", dest="default_baud", type="intx", default=9600,
        help="Set default_baud [default=%default]")
    parser.add_option(
        "-o", "--default-bin-file-sink", dest="default_bin_file_sink", type="string", default="/tmp/rx_data.bin",
        help="Set default_bin_file_sink [default=%default]")
    parser.add_option(
        "-f", "--default-freq", dest="default_freq", type="eng_float", default=eng_notation.num_to_str(437.5e6),
        help="Set default_freq [default=%default]")
    parser.add_option(
        "-g", "--default-gain", dest="default_gain", type="intx", default=1,
        help="Set default_gain [default=%default]")
    parser.add_option(
        "-i", "--default-ip-0", dest="default_ip_0", type="string", default='127.0.0.1',
        help="Set default_ip_0 [default=%default]")
    parser.add_option(
        "-p", "--default-port-0", dest="default_port_0", type="intx", default=5000,
        help="Set default_port_0 [default=%default]")
    parser.add_option(
        "-s", "--default-samp", dest="default_samp", type="eng_float", default=eng_notation.num_to_str(1000000),
        help="Set default_samp [default=%default]")
    parser.add_option(
        "-d", "--sdr-dev", dest="sdr_dev", type="string", default="rtl=0",
        help="Set sdr_dev [default=%default]")
    return parser


def main(top_block_cls=gfsk_rx, options=None):
    if options is None:
        options, _ = argument_parser().parse_args()
    if gr.enable_realtime_scheduling() != gr.RT_OK:
        print "Error: failed to enable real-time scheduling."

    tb = top_block_cls(default_bandwidth=options.default_bandwidth, default_baud=options.default_baud, default_bin_file_sink=options.default_bin_file_sink, default_freq=options.default_freq, default_gain=options.default_gain, default_ip_0=options.default_ip_0, default_port_0=options.default_port_0, default_samp=options.default_samp, sdr_dev=options.sdr_dev)
    tb.start()
    try:
        raw_input('Press Enter to quit: ')
    except EOFError:
        pass
    tb.stop()
    tb.wait()


if __name__ == '__main__':
    main()
