#!/usr/bin/env python2
# -*- coding: utf-8 -*-
##################################################
# GNU Radio Python Flow Graph
# Title: GFSK TX
# Author: Gabriel Mariano Marcelino
# Generated: Wed Aug  8 17:39:37 2018
##################################################


from gnuradio import blocks
from gnuradio import digital
from gnuradio import eng_notation
from gnuradio import filter
from gnuradio import gr
from gnuradio.eng_option import eng_option
from gnuradio.filter import firdes
from optparse import OptionParser
import osmosdr
import time


class gfsk_tx(gr.top_block):

    def __init__(self, baudrate=1200, bin_file_input='/tmp/tx_data.bin', freq=437.5e6, samp_rate_tx=1000000, sdr_dev='uhd=0'):
        gr.top_block.__init__(self, "GFSK TX")

        ##################################################
        # Parameters
        ##################################################
        self.baudrate = baudrate
        self.bin_file_input = bin_file_input
        self.freq = freq
        self.samp_rate_tx = samp_rate_tx
        self.sdr_dev = sdr_dev

        ##################################################
        # Variables
        ##################################################
        self.sps = sps = 20
        self.deviation = deviation = 3200
        self.samp_rate = samp_rate = sps*baudrate
        self.mod_index = mod_index = (1.0*deviation)/(1.0*baudrate)/0.5
        self.bps = bps = 1

        ##################################################
        # Blocks
        ##################################################
        self.rational_resampler_xxx_0 = filter.rational_resampler_ccc(
                interpolation=samp_rate_tx,
                decimation=samp_rate,
                taps=None,
                fractional_bw=None,
        )
        self.osmosdr_sink_0 = osmosdr.sink( args="numchan=" + str(1) + " " + sdr_dev )
        self.osmosdr_sink_0.set_sample_rate(samp_rate_tx)
        self.osmosdr_sink_0.set_center_freq(freq, 0)
        self.osmosdr_sink_0.set_freq_corr(0, 0)
        self.osmosdr_sink_0.set_gain(30, 0)
        self.osmosdr_sink_0.set_if_gain(20, 0)
        self.osmosdr_sink_0.set_bb_gain(20, 0)
        self.osmosdr_sink_0.set_antenna('', 0)
        self.osmosdr_sink_0.set_bandwidth(0, 0)

        self.digital_gfsk_mod_0 = digital.gfsk_mod(
        	samples_per_symbol=sps,
        	sensitivity=(3.141593*mod_index)/sps,
        	bt=0.5,
        	verbose=False,
        	log=False,
        )
        self.blocks_file_source_0 = blocks.file_source(gr.sizeof_char*1, '/tmp/tx_data.bin', False)

        ##################################################
        # Connections
        ##################################################
        self.connect((self.blocks_file_source_0, 0), (self.digital_gfsk_mod_0, 0))
        self.connect((self.digital_gfsk_mod_0, 0), (self.rational_resampler_xxx_0, 0))
        self.connect((self.rational_resampler_xxx_0, 0), (self.osmosdr_sink_0, 0))

    def get_baudrate(self):
        return self.baudrate

    def set_baudrate(self, baudrate):
        self.baudrate = baudrate
        self.set_samp_rate(self.sps*self.baudrate)
        self.set_mod_index((1.0*self.deviation)/(1.0*self.baudrate)/0.5)

    def get_bin_file_input(self):
        return self.bin_file_input

    def set_bin_file_input(self, bin_file_input):
        self.bin_file_input = bin_file_input

    def get_freq(self):
        return self.freq

    def set_freq(self, freq):
        self.freq = freq
        self.osmosdr_sink_0.set_center_freq(self.freq, 0)

    def get_samp_rate_tx(self):
        return self.samp_rate_tx

    def set_samp_rate_tx(self, samp_rate_tx):
        self.samp_rate_tx = samp_rate_tx
        self.osmosdr_sink_0.set_sample_rate(self.samp_rate_tx)

    def get_sdr_dev(self):
        return self.sdr_dev

    def set_sdr_dev(self, sdr_dev):
        self.sdr_dev = sdr_dev

    def get_sps(self):
        return self.sps

    def set_sps(self, sps):
        self.sps = sps
        self.set_samp_rate(self.sps*self.baudrate)

    def get_deviation(self):
        return self.deviation

    def set_deviation(self, deviation):
        self.deviation = deviation
        self.set_mod_index((1.0*self.deviation)/(1.0*self.baudrate)/0.5)

    def get_samp_rate(self):
        return self.samp_rate

    def set_samp_rate(self, samp_rate):
        self.samp_rate = samp_rate

    def get_mod_index(self):
        return self.mod_index

    def set_mod_index(self, mod_index):
        self.mod_index = mod_index

    def get_bps(self):
        return self.bps

    def set_bps(self, bps):
        self.bps = bps


def argument_parser():
    parser = OptionParser(usage="%prog: [options]", option_class=eng_option)
    parser.add_option(
        "-b", "--baudrate", dest="baudrate", type="intx", default=1200,
        help="Set baudrate [default=%default]")
    parser.add_option(
        "-o", "--bin-file-input", dest="bin_file_input", type="string", default='/tmp/tx_data.bin',
        help="Set input_file [default=%default]")
    parser.add_option(
        "-f", "--freq", dest="freq", type="eng_float", default=eng_notation.num_to_str(437.5e6),
        help="Set frequency [default=%default]")
    parser.add_option(
        "-s", "--samp-rate-tx", dest="samp_rate_tx", type="intx", default=1000000,
        help="Set samp_rate [default=%default]")
    parser.add_option(
        "-d", "--sdr-dev", dest="sdr_dev", type="string", default='uhd=0',
        help="Set SDR Device [default=%default]")
    return parser


def main(top_block_cls=gfsk_tx, options=None):
    if options is None:
        options, _ = argument_parser().parse_args()
    if gr.enable_realtime_scheduling() != gr.RT_OK:
        print "Error: failed to enable real-time scheduling."

    tb = top_block_cls(baudrate=options.baudrate, bin_file_input=options.bin_file_input, freq=options.freq, samp_rate_tx=options.samp_rate_tx, sdr_dev=options.sdr_dev)
    tb.start()
    tb.wait()


if __name__ == '__main__':
    main()
