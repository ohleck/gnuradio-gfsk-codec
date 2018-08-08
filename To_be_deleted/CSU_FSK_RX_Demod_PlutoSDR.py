#!/usr/bin/env python2
# -*- coding: utf-8 -*-
##################################################
# GNU Radio Python Flow Graph
# Title: FSK reception + demodulation with PlutoSDR
# Author: Guilherme Theis
# Description: Flow used to receive an FSK signal and demodulate it directly
# Generated: Mon Aug  6 23:24:28 2018
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
from gnuradio import iio
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
import wx


class CSU_FSK_RX_Demod_PlutoSDR(grc_wxgui.top_block_gui):

    def __init__(self, default_baud=9600, default_bin_file_sink="/tmp/rx_data.bin", default_freq=437500000, default_samp=4000000):
        grc_wxgui.top_block_gui.__init__(self, title="FSK reception + demodulation with PlutoSDR")
        _icon_path = "/usr/share/icons/hicolor/32x32/apps/gnuradio-grc.png"
        self.SetIcon(wx.Icon(_icon_path, wx.BITMAP_TYPE_ANY))

        ##################################################
        # Parameters
        ##################################################
        self.default_baud = default_baud
        self.default_bin_file_sink = default_bin_file_sink
        self.default_freq = default_freq
        self.default_samp = default_samp

        ##################################################
        # Variables
        ##################################################
        self.samp_rate = samp_rate = default_samp
        self.center_freq = center_freq = default_freq
        self.baudrate = baudrate = default_baud
        self.bandwidth = bandwidth = 50e3

        ##################################################
        # Blocks
        ##################################################
        _samp_rate_sizer = wx.BoxSizer(wx.VERTICAL)
        self._samp_rate_text_box = forms.text_box(
        	parent=self.GetWin(),
        	sizer=_samp_rate_sizer,
        	value=self.samp_rate,
        	callback=self.set_samp_rate,
        	label='Sample rate [S/s]',
        	converter=forms.float_converter(),
        	proportion=0,
        )
        self._samp_rate_slider = forms.slider(
        	parent=self.GetWin(),
        	sizer=_samp_rate_sizer,
        	value=self.samp_rate,
        	callback=self.set_samp_rate,
        	minimum=100000,
        	maximum=4000000,
        	num_steps=1000,
        	style=wx.SL_HORIZONTAL,
        	cast=float,
        	proportion=1,
        )
        self.GridAdd(_samp_rate_sizer, 1, 1, 1, 1)
        _center_freq_sizer = wx.BoxSizer(wx.VERTICAL)
        self._center_freq_text_box = forms.text_box(
        	parent=self.GetWin(),
        	sizer=_center_freq_sizer,
        	value=self.center_freq,
        	callback=self.set_center_freq,
        	label='Frequency [Hz]',
        	converter=forms.float_converter(),
        	proportion=0,
        )
        self._center_freq_slider = forms.slider(
        	parent=self.GetWin(),
        	sizer=_center_freq_sizer,
        	value=self.center_freq,
        	callback=self.set_center_freq,
        	minimum=437000000,
        	maximum=438000000,
        	num_steps=1000,
        	style=wx.SL_HORIZONTAL,
        	cast=float,
        	proportion=1,
        )
        self.GridAdd(_center_freq_sizer, 0, 1, 1, 1)
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
        	fft_size=512,
        	fft_rate=15,
        	average=False,
        	avg_alpha=None,
        	title='Waterfall Plot',
        )
        self.Add(self.wxgui_waterfallsink2_0.win)
        self.wxgui_fftsink2_0 = fftsink2.fft_sink_c(
        	self.GetWin(),
        	baseband_freq=0,
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
        	peak_hold=True,
        )
        self.Add(self.wxgui_fftsink2_0.win)
        self.pluto_source_0 = iio.pluto_source('ip:pluto.local', center_freq, samp_rate, 1 - 1, 25000, 0x8000, True, True, True, "manual", 20, '', True)
        self.low_pass_filter_1 = filter.fir_filter_fff(100, firdes.low_pass(
        	1, samp_rate, baudrate, baudrate/6, firdes.WIN_HAMMING, 6.76))
        self.low_pass_filter_0 = filter.fir_filter_ccf(1, firdes.low_pass(
        	1, samp_rate, bandwidth/2, bandwidth/2/6, firdes.WIN_HAMMING, 6.76))
        self.digital_clock_recovery_mm_xx_0 = digital.clock_recovery_mm_ff(samp_rate/(baudrate*100), 0.001, 0, 0.25, 0.001)
        self.digital_binary_slicer_fb_0 = digital.binary_slicer_fb()
        self.blocks_file_sink_1 = blocks.file_sink(gr.sizeof_char*1, default_bin_file_sink, False)
        self.blocks_file_sink_1.set_unbuffered(False)
        self.analog_quadrature_demod_cf_0 = analog.quadrature_demod_cf(1)

        ##################################################
        # Connections
        ##################################################
        self.connect((self.analog_quadrature_demod_cf_0, 0), (self.low_pass_filter_1, 0))
        self.connect((self.digital_binary_slicer_fb_0, 0), (self.blocks_file_sink_1, 0))
        self.connect((self.digital_clock_recovery_mm_xx_0, 0), (self.digital_binary_slicer_fb_0, 0))
        self.connect((self.low_pass_filter_0, 0), (self.analog_quadrature_demod_cf_0, 0))
        self.connect((self.low_pass_filter_1, 0), (self.digital_clock_recovery_mm_xx_0, 0))
        self.connect((self.pluto_source_0, 0), (self.low_pass_filter_0, 0))
        self.connect((self.pluto_source_0, 0), (self.wxgui_fftsink2_0, 0))
        self.connect((self.pluto_source_0, 0), (self.wxgui_waterfallsink2_0, 0))

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
        self.set_center_freq(self.default_freq)

    def get_default_samp(self):
        return self.default_samp

    def set_default_samp(self, default_samp):
        self.default_samp = default_samp
        self.set_samp_rate(self.default_samp)

    def get_samp_rate(self):
        return self.samp_rate

    def set_samp_rate(self, samp_rate):
        self.samp_rate = samp_rate
        self._samp_rate_slider.set_value(self.samp_rate)
        self._samp_rate_text_box.set_value(self.samp_rate)
        self.wxgui_waterfallsink2_0.set_sample_rate(self.samp_rate)
        self.wxgui_fftsink2_0.set_sample_rate(self.samp_rate)
        self.pluto_source_0.set_params(self.center_freq, self.samp_rate, 25000, True, True, True, "manual", 20, '', True)
        self.low_pass_filter_1.set_taps(firdes.low_pass(1, self.samp_rate, self.baudrate, self.baudrate/6, firdes.WIN_HAMMING, 6.76))
        self.low_pass_filter_0.set_taps(firdes.low_pass(1, self.samp_rate, self.bandwidth/2, self.bandwidth/2/6, firdes.WIN_HAMMING, 6.76))
        self.digital_clock_recovery_mm_xx_0.set_omega(self.samp_rate/(self.baudrate*100))

    def get_center_freq(self):
        return self.center_freq

    def set_center_freq(self, center_freq):
        self.center_freq = center_freq
        self._center_freq_slider.set_value(self.center_freq)
        self._center_freq_text_box.set_value(self.center_freq)
        self.pluto_source_0.set_params(self.center_freq, self.samp_rate, 25000, True, True, True, "manual", 20, '', True)

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
    description = 'Flow used to receive an FSK signal and demodulate it directly'
    parser = OptionParser(usage="%prog: [options]", option_class=eng_option, description=description)
    parser.add_option(
        "-b", "--default-baud", dest="default_baud", type="intx", default=9600,
        help="Set default_baud [default=%default]")
    parser.add_option(
        "-o", "--default-bin-file-sink", dest="default_bin_file_sink", type="string", default="/tmp/rx_data.bin",
        help="Set default_bin_file_sink [default=%default]")
    parser.add_option(
        "-f", "--default-freq", dest="default_freq", type="long", default=437500000,
        help="Set default_freq [default=%default]")
    parser.add_option(
        "-s", "--default-samp", dest="default_samp", type="long", default=4000000,
        help="Set default_samp [default=%default]")
    return parser


def main(top_block_cls=CSU_FSK_RX_Demod_PlutoSDR, options=None):
    if options is None:
        options, _ = argument_parser().parse_args()

    tb = top_block_cls(default_baud=options.default_baud, default_bin_file_sink=options.default_bin_file_sink, default_freq=options.default_freq, default_samp=options.default_samp)
    tb.Start(True)
    tb.Wait()


if __name__ == '__main__':
    main()
