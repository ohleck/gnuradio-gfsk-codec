#!/usr/bin/env python2
# -*- coding: utf-8 -*-
##################################################
# GNU Radio Python Flow Graph
# Title: CSU_FSK_TX_Mod_PlutoSDR
# Author: Guilherme Theis
# Description: A FSK transmitter using ADALM-PLUTO
# Generated: Mon Aug  6 22:58:51 2018
##################################################


if __name__ == '__main__':
    import ctypes
    import sys
    if sys.platform.startswith('linux'):
        try:
            x11 = ctypes.cdll.LoadLibrary('libX11.so')
            x11.XInitThreads()
        except:
            print "Warning: failed to XInitThreads()"

from gnuradio import blocks
from gnuradio import digital
from gnuradio import eng_notation
from gnuradio import gr
from gnuradio import iio
from gnuradio import wxgui
from gnuradio.eng_option import eng_option
from gnuradio.fft import window
from gnuradio.filter import firdes
from gnuradio.wxgui import fftsink2
from grc_gnuradio import blks2 as grc_blks2
from grc_gnuradio import wxgui as grc_wxgui
from optparse import OptionParser
import epy_block_0
import pmt
import wx


class CSU_FSK_TX_Mod_PlutoSDR(grc_wxgui.top_block_gui):

    def __init__(self):
        grc_wxgui.top_block_gui.__init__(self, title="CSU_FSK_TX_Mod_PlutoSDR")
        _icon_path = "/usr/share/icons/hicolor/32x32/apps/gnuradio-grc.png"
        self.SetIcon(wx.Icon(_icon_path, wx.BITMAP_TYPE_ANY))

        ##################################################
        # Variables
        ##################################################
        self.sps = sps = 10
        self.samp_rate_tx = samp_rate_tx = 2000000
        self.samp_rate = samp_rate = 384000
        self.freq = freq = 436500000
        self.baud_rate = baud_rate = 9600

        ##################################################
        # Blocks
        ##################################################
        self.wxgui_fftsink2_0 = fftsink2.fft_sink_c(
        	self.GetWin(),
        	baseband_freq=freq,
        	y_per_div=10,
        	y_divs=10,
        	ref_level=0,
        	ref_scale=2.0,
        	sample_rate=samp_rate,
        	fft_size=1024,
        	fft_rate=15,
        	average=False,
        	avg_alpha=None,
        	title='FFT Plot',
        	peak_hold=False,
        )
        self.Add(self.wxgui_fftsink2_0.win)
        self.pluto_sink_0 = iio.pluto_sink('ip:pluto.local', freq, samp_rate_tx, 1 - 1, 10000000, 0x8000, False, 10.0, '', True)
        self.epy_block_0 = epy_block_0.msg_block()
        self.digital_gfsk_mod_0 = digital.gfsk_mod(
        	samples_per_symbol=2,
        	sensitivity=1.0,
        	bt=0.35,
        	verbose=False,
        	log=False,
        )
        self.blocks_pdu_to_tagged_stream_0 = blocks.pdu_to_tagged_stream(blocks.byte_t, 'packet_len')
        self.blocks_message_strobe_0 = blocks.message_strobe(pmt.intern("Hello World"), 10000)
        self.blks2_packet_encoder_0 = grc_blks2.packet_mod_b(grc_blks2.packet_encoder(
        		samples_per_symbol=sps,
        		bits_per_symbol=1,
        		preamble='',
        		access_code='1100',
        		pad_for_usrp=True,
        	),
        	payload_length=0,
        )

        ##################################################
        # Connections
        ##################################################
        self.msg_connect((self.blocks_message_strobe_0, 'strobe'), (self.epy_block_0, 'msg_in'))
        self.msg_connect((self.epy_block_0, 'msg_out'), (self.blocks_pdu_to_tagged_stream_0, 'pdus'))
        self.connect((self.blks2_packet_encoder_0, 0), (self.digital_gfsk_mod_0, 0))
        self.connect((self.blocks_pdu_to_tagged_stream_0, 0), (self.blks2_packet_encoder_0, 0))
        self.connect((self.digital_gfsk_mod_0, 0), (self.pluto_sink_0, 0))
        self.connect((self.digital_gfsk_mod_0, 0), (self.wxgui_fftsink2_0, 0))

    def get_sps(self):
        return self.sps

    def set_sps(self, sps):
        self.sps = sps

    def get_samp_rate_tx(self):
        return self.samp_rate_tx

    def set_samp_rate_tx(self, samp_rate_tx):
        self.samp_rate_tx = samp_rate_tx
        self.pluto_sink_0.set_params(self.freq, self.samp_rate_tx, 10000000, 10.0, '', True)

    def get_samp_rate(self):
        return self.samp_rate

    def set_samp_rate(self, samp_rate):
        self.samp_rate = samp_rate
        self.wxgui_fftsink2_0.set_sample_rate(self.samp_rate)

    def get_freq(self):
        return self.freq

    def set_freq(self, freq):
        self.freq = freq
        self.wxgui_fftsink2_0.set_baseband_freq(self.freq)
        self.pluto_sink_0.set_params(self.freq, self.samp_rate_tx, 10000000, 10.0, '', True)

    def get_baud_rate(self):
        return self.baud_rate

    def set_baud_rate(self, baud_rate):
        self.baud_rate = baud_rate


def main(top_block_cls=CSU_FSK_TX_Mod_PlutoSDR, options=None):

    tb = top_block_cls()
    tb.Start(True)
    tb.Wait()


if __name__ == '__main__':
    main()
