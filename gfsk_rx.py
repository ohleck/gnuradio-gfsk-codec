#!/usr/bin/env python2
# -*- coding: utf-8 -*-
##################################################
# GNU Radio Python Flow Graph
# Title: GFSK Receiver
# Author: Gabriel Mariano Marcelino
# Generated: Wed Aug  8 10:46:06 2018
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

from gnuradio import analog
from gnuradio import blocks
from gnuradio import digital
from gnuradio import eng_notation
from gnuradio import filter
from gnuradio import gr
from gnuradio import wxgui
from gnuradio.eng_option import eng_option
from gnuradio.fft import window
from gnuradio.filter import firdes
from gnuradio.wxgui import fftsink2
from gnuradio.wxgui import forms
from gnuradio.wxgui import waterfallsink2
from grc_gnuradio import wxgui as grc_wxgui
from optparse import OptionParser
import math
import osmosdr
import time
import wx


class gfsk_rx(grc_wxgui.top_block_gui):

    def __init__(self, default_bandwidth=20e3, default_baud=9600, default_bin_file_sink="/tmp/rx_data.bin", default_freq=437.5e6, default_gain=1, default_samp=1800000, sdr_dev="rtl=0"):
        grc_wxgui.top_block_gui.__init__(self, title="GFSK Receiver")
        _icon_path = "/usr/share/icons/hicolor/32x32/apps/gnuradio-grc.png"
        self.SetIcon(wx.Icon(_icon_path, wx.BITMAP_TYPE_ANY))

        ##################################################
        # Parameters
        ##################################################
        self.default_bandwidth = default_bandwidth
        self.default_baud = default_baud
        self.default_bin_file_sink = default_bin_file_sink
        self.default_freq = default_freq
        self.default_gain = default_gain
        self.default_samp = default_samp
        self.sdr_dev = sdr_dev

        ##################################################
        # Variables
        ##################################################
        self.sdr_rf_gain = sdr_rf_gain = 10
        self.sdr_if_gain = sdr_if_gain = 20
        self.sdr_bb_gain = sdr_bb_gain = 20
        self.samp_rate = samp_rate = default_samp
        self.freq = freq = default_freq
        self.baudrate = baudrate = default_baud
        self.bandwidth = bandwidth = default_bandwidth

        ##################################################
        # Blocks
        ##################################################
        _sdr_rf_gain_sizer = wx.BoxSizer(wx.VERTICAL)
        self._sdr_rf_gain_text_box = forms.text_box(
        	parent=self.GetWin(),
        	sizer=_sdr_rf_gain_sizer,
        	value=self.sdr_rf_gain,
        	callback=self.set_sdr_rf_gain,
        	label='RF gain [dB]',
        	converter=forms.int_converter(),
        	proportion=0,
        )
        self._sdr_rf_gain_slider = forms.slider(
        	parent=self.GetWin(),
        	sizer=_sdr_rf_gain_sizer,
        	value=self.sdr_rf_gain,
        	callback=self.set_sdr_rf_gain,
        	minimum=0,
        	maximum=20,
        	num_steps=20,
        	style=wx.SL_HORIZONTAL,
        	cast=int,
        	proportion=1,
        )
        self.GridAdd(_sdr_rf_gain_sizer, 2, 1, 1, 1)
        _sdr_if_gain_sizer = wx.BoxSizer(wx.VERTICAL)
        self._sdr_if_gain_text_box = forms.text_box(
        	parent=self.GetWin(),
        	sizer=_sdr_if_gain_sizer,
        	value=self.sdr_if_gain,
        	callback=self.set_sdr_if_gain,
        	label='IF gain [dB]',
        	converter=forms.int_converter(),
        	proportion=0,
        )
        self._sdr_if_gain_slider = forms.slider(
        	parent=self.GetWin(),
        	sizer=_sdr_if_gain_sizer,
        	value=self.sdr_if_gain,
        	callback=self.set_sdr_if_gain,
        	minimum=0,
        	maximum=30,
        	num_steps=30,
        	style=wx.SL_HORIZONTAL,
        	cast=int,
        	proportion=1,
        )
        self.GridAdd(_sdr_if_gain_sizer, 3, 1, 1, 1)
        _sdr_bb_gain_sizer = wx.BoxSizer(wx.VERTICAL)
        self._sdr_bb_gain_text_box = forms.text_box(
        	parent=self.GetWin(),
        	sizer=_sdr_bb_gain_sizer,
        	value=self.sdr_bb_gain,
        	callback=self.set_sdr_bb_gain,
        	label='BB gain [dB]',
        	converter=forms.int_converter(),
        	proportion=0,
        )
        self._sdr_bb_gain_slider = forms.slider(
        	parent=self.GetWin(),
        	sizer=_sdr_bb_gain_sizer,
        	value=self.sdr_bb_gain,
        	callback=self.set_sdr_bb_gain,
        	minimum=0,
        	maximum=30,
        	num_steps=30,
        	style=wx.SL_HORIZONTAL,
        	cast=int,
        	proportion=1,
        )
        self.GridAdd(_sdr_bb_gain_sizer, 4, 1, 1, 1)
        _samp_rate_sizer = wx.BoxSizer(wx.VERTICAL)
        self._samp_rate_text_box = forms.text_box(
        	parent=self.GetWin(),
        	sizer=_samp_rate_sizer,
        	value=self.samp_rate,
        	callback=self.set_samp_rate,
        	label='Sample rate [S/s]',
        	converter=forms.int_converter(),
        	proportion=0,
        )
        self._samp_rate_slider = forms.slider(
        	parent=self.GetWin(),
        	sizer=_samp_rate_sizer,
        	value=self.samp_rate,
        	callback=self.set_samp_rate,
        	minimum=100e3,
        	maximum=4e6,
        	num_steps=1000,
        	style=wx.SL_HORIZONTAL,
        	cast=int,
        	proportion=1,
        )
        self.GridAdd(_samp_rate_sizer, 1, 1, 1, 1)
        _freq_sizer = wx.BoxSizer(wx.VERTICAL)
        self._freq_text_box = forms.text_box(
        	parent=self.GetWin(),
        	sizer=_freq_sizer,
        	value=self.freq,
        	callback=self.set_freq,
        	label='Frequency [Hz]',
        	converter=forms.float_converter(),
        	proportion=0,
        )
        self._freq_slider = forms.slider(
        	parent=self.GetWin(),
        	sizer=_freq_sizer,
        	value=self.freq,
        	callback=self.set_freq,
        	minimum=437e6,
        	maximum=438e6,
        	num_steps=1000,
        	style=wx.SL_HORIZONTAL,
        	cast=float,
        	proportion=1,
        )
        self.GridAdd(_freq_sizer, 0, 1, 1, 1)
        self._baudrate_text_box = forms.text_box(
        	parent=self.GetWin(),
        	value=self.baudrate,
        	callback=self.set_baudrate,
        	label='Baudrate [bps]',
        	converter=forms.int_converter(),
        )
        self.GridAdd(self._baudrate_text_box, 6, 1, 1, 1)
        _bandwidth_sizer = wx.BoxSizer(wx.VERTICAL)
        self._bandwidth_text_box = forms.text_box(
        	parent=self.GetWin(),
        	sizer=_bandwidth_sizer,
        	value=self.bandwidth,
        	callback=self.set_bandwidth,
        	label='Bandwidth [Hz]',
        	converter=forms.float_converter(),
        	proportion=0,
        )
        self._bandwidth_slider = forms.slider(
        	parent=self.GetWin(),
        	sizer=_bandwidth_sizer,
        	value=self.bandwidth,
        	callback=self.set_bandwidth,
        	minimum=0,
        	maximum=60e3,
        	num_steps=60,
        	style=wx.SL_HORIZONTAL,
        	cast=float,
        	proportion=1,
        )
        self.GridAdd(_bandwidth_sizer, 5, 1, 1, 1)
        self.wxgui_waterfallsink2_0 = waterfallsink2.waterfall_sink_c(
        	self.GetWin(),
        	baseband_freq=0,
        	dynamic_range=100,
        	ref_level=0,
        	ref_scale=2.0,
        	sample_rate=samp_rate,
        	fft_size=1024,
        	fft_rate=15,
        	average=False,
        	avg_alpha=0.1,
        	title='',
        	win=window.hanning,
        	size=([800,400]),
        )
        self.GridAdd(self.wxgui_waterfallsink2_0.win, 7, 0, 7, 1)
        self.wxgui_fftsink2_0 = fftsink2.fft_sink_c(
        	self.GetWin(),
        	baseband_freq=freq,
        	y_per_div=10,
        	y_divs=9,
        	ref_level=0,
        	ref_scale=2.0,
        	sample_rate=samp_rate,
        	fft_size=1024,
        	fft_rate=15,
        	average=True,
        	avg_alpha=0.5,
        	title='',
        	peak_hold=False,
        	win=window.hanning,
        	size=([800,100]),
        )
        self.GridAdd(self.wxgui_fftsink2_0.win, 0, 0, 7, 1)
        self.osmosdr_source_0 = osmosdr.source( args="numchan=" + str(1) + " " + sdr_dev )
        self.osmosdr_source_0.set_sample_rate(samp_rate)
        self.osmosdr_source_0.set_center_freq(freq, 0)
        self.osmosdr_source_0.set_freq_corr(0, 0)
        self.osmosdr_source_0.set_dc_offset_mode(0, 0)
        self.osmosdr_source_0.set_iq_balance_mode(0, 0)
        self.osmosdr_source_0.set_gain_mode(False, 0)
        self.osmosdr_source_0.set_gain(sdr_rf_gain, 0)
        self.osmosdr_source_0.set_if_gain(sdr_if_gain, 0)
        self.osmosdr_source_0.set_bb_gain(sdr_bb_gain, 0)
        self.osmosdr_source_0.set_antenna('', 0)
        self.osmosdr_source_0.set_bandwidth(0, 0)

        self.low_pass_filter_1 = filter.fir_filter_fff(100, firdes.low_pass(
        	1, samp_rate, baudrate, baudrate/6, firdes.WIN_HAMMING, 6.76))
        self.low_pass_filter_0 = filter.fir_filter_ccf(1, firdes.low_pass(
        	1, samp_rate, bandwidth/2, bandwidth/2/6, firdes.WIN_HAMMING, 6.76))
        self.digital_clock_recovery_mm_xx_0 = digital.clock_recovery_mm_ff(samp_rate/(baudrate*100), 0.001, 0, 0.25, 0.001)
        self.digital_binary_slicer_fb_0 = digital.binary_slicer_fb()
        self.blocks_file_sink_1 = blocks.file_sink(gr.sizeof_char*1, default_bin_file_sink, False)
        self.blocks_file_sink_1.set_unbuffered(False)
        self.analog_quadrature_demod_cf_0 = analog.quadrature_demod_cf(default_gain)

        ##################################################
        # Connections
        ##################################################
        self.connect((self.analog_quadrature_demod_cf_0, 0), (self.low_pass_filter_1, 0))
        self.connect((self.digital_binary_slicer_fb_0, 0), (self.blocks_file_sink_1, 0))
        self.connect((self.digital_clock_recovery_mm_xx_0, 0), (self.digital_binary_slicer_fb_0, 0))
        self.connect((self.low_pass_filter_0, 0), (self.analog_quadrature_demod_cf_0, 0))
        self.connect((self.low_pass_filter_1, 0), (self.digital_clock_recovery_mm_xx_0, 0))
        self.connect((self.osmosdr_source_0, 0), (self.low_pass_filter_0, 0))
        self.connect((self.osmosdr_source_0, 0), (self.wxgui_fftsink2_0, 0))
        self.connect((self.osmosdr_source_0, 0), (self.wxgui_waterfallsink2_0, 0))

    def get_default_bandwidth(self):
        return self.default_bandwidth

    def set_default_bandwidth(self, default_bandwidth):
        self.default_bandwidth = default_bandwidth
        self.set_bandwidth(self.default_bandwidth)

    def get_default_baud(self):
        return self.default_baud

    def set_default_baud(self, default_baud):
        self.default_baud = default_baud
        self.set_baudrate(self.default_baud)

    def get_default_bin_file_sink(self):
        return self.default_bin_file_sink

    def set_default_bin_file_sink(self, default_bin_file_sink):
        self.default_bin_file_sink = default_bin_file_sink
        self.blocks_file_sink_1.open(self.default_bin_file_sink)

    def get_default_freq(self):
        return self.default_freq

    def set_default_freq(self, default_freq):
        self.default_freq = default_freq
        self.set_freq(self.default_freq)

    def get_default_gain(self):
        return self.default_gain

    def set_default_gain(self, default_gain):
        self.default_gain = default_gain
        self.analog_quadrature_demod_cf_0.set_gain(self.default_gain)

    def get_default_samp(self):
        return self.default_samp

    def set_default_samp(self, default_samp):
        self.default_samp = default_samp
        self.set_samp_rate(self.default_samp)

    def get_sdr_dev(self):
        return self.sdr_dev

    def set_sdr_dev(self, sdr_dev):
        self.sdr_dev = sdr_dev

    def get_sdr_rf_gain(self):
        return self.sdr_rf_gain

    def set_sdr_rf_gain(self, sdr_rf_gain):
        self.sdr_rf_gain = sdr_rf_gain
        self._sdr_rf_gain_slider.set_value(self.sdr_rf_gain)
        self._sdr_rf_gain_text_box.set_value(self.sdr_rf_gain)
        self.osmosdr_source_0.set_gain(self.sdr_rf_gain, 0)

    def get_sdr_if_gain(self):
        return self.sdr_if_gain

    def set_sdr_if_gain(self, sdr_if_gain):
        self.sdr_if_gain = sdr_if_gain
        self._sdr_if_gain_slider.set_value(self.sdr_if_gain)
        self._sdr_if_gain_text_box.set_value(self.sdr_if_gain)
        self.osmosdr_source_0.set_if_gain(self.sdr_if_gain, 0)

    def get_sdr_bb_gain(self):
        return self.sdr_bb_gain

    def set_sdr_bb_gain(self, sdr_bb_gain):
        self.sdr_bb_gain = sdr_bb_gain
        self._sdr_bb_gain_slider.set_value(self.sdr_bb_gain)
        self._sdr_bb_gain_text_box.set_value(self.sdr_bb_gain)
        self.osmosdr_source_0.set_bb_gain(self.sdr_bb_gain, 0)

    def get_samp_rate(self):
        return self.samp_rate

    def set_samp_rate(self, samp_rate):
        self.samp_rate = samp_rate
        self._samp_rate_slider.set_value(self.samp_rate)
        self._samp_rate_text_box.set_value(self.samp_rate)
        self.wxgui_waterfallsink2_0.set_sample_rate(self.samp_rate)
        self.wxgui_fftsink2_0.set_sample_rate(self.samp_rate)
        self.osmosdr_source_0.set_sample_rate(self.samp_rate)
        self.low_pass_filter_1.set_taps(firdes.low_pass(1, self.samp_rate, self.baudrate, self.baudrate/6, firdes.WIN_HAMMING, 6.76))
        self.low_pass_filter_0.set_taps(firdes.low_pass(1, self.samp_rate, self.bandwidth/2, self.bandwidth/2/6, firdes.WIN_HAMMING, 6.76))
        self.digital_clock_recovery_mm_xx_0.set_omega(self.samp_rate/(self.baudrate*100))

    def get_freq(self):
        return self.freq

    def set_freq(self, freq):
        self.freq = freq
        self._freq_slider.set_value(self.freq)
        self._freq_text_box.set_value(self.freq)
        self.wxgui_fftsink2_0.set_baseband_freq(self.freq)
        self.osmosdr_source_0.set_center_freq(self.freq, 0)

    def get_baudrate(self):
        return self.baudrate

    def set_baudrate(self, baudrate):
        self.baudrate = baudrate
        self._baudrate_text_box.set_value(self.baudrate)
        self.low_pass_filter_1.set_taps(firdes.low_pass(1, self.samp_rate, self.baudrate, self.baudrate/6, firdes.WIN_HAMMING, 6.76))
        self.digital_clock_recovery_mm_xx_0.set_omega(self.samp_rate/(self.baudrate*100))

    def get_bandwidth(self):
        return self.bandwidth

    def set_bandwidth(self, bandwidth):
        self.bandwidth = bandwidth
        self._bandwidth_slider.set_value(self.bandwidth)
        self._bandwidth_text_box.set_value(self.bandwidth)
        self.low_pass_filter_0.set_taps(firdes.low_pass(1, self.samp_rate, self.bandwidth/2, self.bandwidth/2/6, firdes.WIN_HAMMING, 6.76))


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
        "-s", "--default-samp", dest="default_samp", type="eng_float", default=eng_notation.num_to_str(1800000),
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

    tb = top_block_cls(default_bandwidth=options.default_bandwidth, default_baud=options.default_baud, default_bin_file_sink=options.default_bin_file_sink, default_freq=options.default_freq, default_gain=options.default_gain, default_samp=options.default_samp, sdr_dev=options.sdr_dev)
    tb.Start(True)
    tb.Wait()


if __name__ == '__main__':
    main()
