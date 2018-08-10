#!/usr/bin/env python2
# -*- coding: utf-8 -*-
##################################################
# GNU Radio Python Flow Graph
# Title: GFSK TX
# Author: Gabriel Mariano Marcelino
# Generated: Fri Aug 10 12:21:02 2018
##################################################


from gnuradio import blocks
from gnuradio import digital
from gnuradio import eng_notation
from gnuradio import filter
from gnuradio import gr
from gnuradio.eng_option import eng_option
from gnuradio.filter import firdes
from grc_gnuradio import blks2 as grc_blks2
from optparse import OptionParser
import osmosdr
import time


class gfsk_tx(gr.top_block):

    def __init__(self, baudrate=1200, default_input=0, default_ip_0='127.0.0.1', default_port_0=5000, freq=437.5e6, samp_rate_tx=1000000, sdr_dev='uhd=0'):
        gr.top_block.__init__(self, "GFSK TX")

        ##################################################
        # Parameters
        ##################################################
        self.baudrate = baudrate
        self.default_input = default_input
        self.default_ip_0 = default_ip_0
        self.default_port_0 = default_port_0
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
        self.blocks_repack_bits_bb_0 = blocks.repack_bits_bb(4, 1, "", False, gr.GR_MSB_FIRST)
        self.blocks_null_sink_0 = blocks.null_sink(gr.sizeof_char*1)
        self.blks2_tcp_source_0 = grc_blks2.tcp_source(
        	itemsize=gr.sizeof_char*1,
        	addr=default_ip_0,
        	port=default_port_0,
        	server=True,
        )
        self.blks2_selector_0 = grc_blks2.selector(
        	item_size=gr.sizeof_char*1,
        	num_inputs=2,
        	num_outputs=2,
        	input_index=default_input,
        	output_index=0,
        )

        ##################################################
        # Connections
        ##################################################
        self.connect((self.blks2_selector_0, 1), (self.blocks_null_sink_0, 0))
        self.connect((self.blks2_selector_0, 0), (self.digital_gfsk_mod_0, 0))
        self.connect((self.blks2_tcp_source_0, 0), (self.blks2_selector_0, 0))
        self.connect((self.blks2_tcp_source_0, 0), (self.blocks_repack_bits_bb_0, 0))
        self.connect((self.blocks_repack_bits_bb_0, 0), (self.blks2_selector_0, 1))
        self.connect((self.digital_gfsk_mod_0, 0), (self.rational_resampler_xxx_0, 0))
        self.connect((self.rational_resampler_xxx_0, 0), (self.osmosdr_sink_0, 0))

    def get_baudrate(self):
        return self.baudrate

    def set_baudrate(self, baudrate):
        self.baudrate = baudrate
        self.set_samp_rate(self.sps*self.baudrate)
        self.set_mod_index((1.0*self.deviation)/(1.0*self.baudrate)/0.5)

    def get_default_input(self):
        return self.default_input

    def set_default_input(self, default_input):
        self.default_input = default_input
        self.blks2_selector_0.set_input_index(int(self.default_input))

    def get_default_ip_0(self):
        return self.default_ip_0

    def set_default_ip_0(self, default_ip_0):
        self.default_ip_0 = default_ip_0

    def get_default_port_0(self):
        return self.default_port_0

    def set_default_port_0(self, default_port_0):
        self.default_port_0 = default_port_0

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
        "-q", "--default-input", dest="default_input", type="intx", default=0,
        help="Set Input [default=%default]")
    parser.add_option(
        "-i", "--default-ip-0", dest="default_ip_0", type="string", default='127.0.0.1',
        help="Set default_ip_0 [default=%default]")
    parser.add_option(
        "-p", "--default-port-0", dest="default_port_0", type="intx", default=5000,
        help="Set default_port_0 [default=%default]")
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

    tb = top_block_cls(baudrate=options.baudrate, default_input=options.default_input, default_ip_0=options.default_ip_0, default_port_0=options.default_port_0, freq=options.freq, samp_rate_tx=options.samp_rate_tx, sdr_dev=options.sdr_dev)
    tb.start()
    tb.wait()


if __name__ == '__main__':
    main()
