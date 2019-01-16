#!/usr/bin/env python2
# -*- coding: utf-8 -*-
##################################################
# GNU Radio Python Flow Graph
# Title: GFSK Receiver
# Generated: Wed Jan 16 18:56:43 2019
##################################################

from distutils.version import StrictVersion

if __name__ == '__main__':
    import ctypes
    import sys
    if sys.platform.startswith('linux'):
        try:
            x11 = ctypes.cdll.LoadLibrary('libX11.so')
            x11.XInitThreads()
        except:
            print "Warning: failed to XInitThreads()"

from PyQt5 import Qt
from PyQt5 import Qt, QtCore
from gnuradio import analog
from gnuradio import blocks
from gnuradio import digital
from gnuradio import eng_notation
from gnuradio import filter
from gnuradio import gr
from gnuradio import iio
from gnuradio import qtgui
from gnuradio.eng_option import eng_option
from gnuradio.filter import firdes
from gnuradio.qtgui import Range, RangeWidget
from optparse import OptionParser
import math
import sip
import sys
from gnuradio import qtgui


class gfsk_rx(gr.top_block, Qt.QWidget):

    def __init__(self, default_bandwidth=20e3, default_baud=9600, default_bin_file_sink="/tmp/rx_data.bin", default_freq=437500000, default_gain=16, default_ip='127.0.0.1', default_port=5000, default_samp=1920000, sdr_dev="rtl=0"):
        gr.top_block.__init__(self, "GFSK Receiver")
        Qt.QWidget.__init__(self)
        self.setWindowTitle("GFSK Receiver")
        qtgui.util.check_set_qss()
        try:
            self.setWindowIcon(Qt.QIcon.fromTheme('gnuradio-grc'))
        except:
            pass
        self.top_scroll_layout = Qt.QVBoxLayout()
        self.setLayout(self.top_scroll_layout)
        self.top_scroll = Qt.QScrollArea()
        self.top_scroll.setFrameStyle(Qt.QFrame.NoFrame)
        self.top_scroll_layout.addWidget(self.top_scroll)
        self.top_scroll.setWidgetResizable(True)
        self.top_widget = Qt.QWidget()
        self.top_scroll.setWidget(self.top_widget)
        self.top_layout = Qt.QVBoxLayout(self.top_widget)
        self.top_grid_layout = Qt.QGridLayout()
        self.top_layout.addLayout(self.top_grid_layout)

        self.settings = Qt.QSettings("GNU Radio", "gfsk_rx")

        if StrictVersion(Qt.qVersion()) < StrictVersion("5.0.0"):
            self.restoreGeometry(self.settings.value("geometry").toByteArray())
        else:
            self.restoreGeometry(self.settings.value("geometry", type=QtCore.QByteArray))

        ##################################################
        # Parameters
        ##################################################
        self.default_bandwidth = default_bandwidth
        self.default_baud = default_baud
        self.default_bin_file_sink = default_bin_file_sink
        self.default_freq = default_freq
        self.default_gain = default_gain
        self.default_ip = default_ip
        self.default_port = default_port
        self.default_samp = default_samp
        self.sdr_dev = sdr_dev

        ##################################################
        # Variables
        ##################################################
        self.interp_tx = interp_tx = default_samp/default_baud
        self.dec_rx = dec_rx = interp_tx/10
        self.t_points = t_points = 2000
        self.sps_rx = sps_rx = interp_tx/dec_rx
        self.rx_gain = rx_gain = 16

        self.low_pass_taps_2 = low_pass_taps_2 = firdes.low_pass(1.0, default_samp, 4800, 1200, firdes.WIN_HAMMING, 6.76)


        self.low_pass_taps = low_pass_taps = firdes.low_pass(1.0, default_samp, 10000, 5000, firdes.WIN_HAMMING, 6.76)

        self.f_dev = f_dev = default_baud/4

        ##################################################
        # Blocks
        ##################################################
        self.signals = Qt.QTabWidget()
        self.signals_widget_0 = Qt.QWidget()
        self.signals_layout_0 = Qt.QBoxLayout(Qt.QBoxLayout.TopToBottom, self.signals_widget_0)
        self.signals_grid_layout_0 = Qt.QGridLayout()
        self.signals_layout_0.addLayout(self.signals_grid_layout_0)
        self.signals.addTab(self.signals_widget_0, 'Receiver')
        self.signals_widget_1 = Qt.QWidget()
        self.signals_layout_1 = Qt.QBoxLayout(Qt.QBoxLayout.TopToBottom, self.signals_widget_1)
        self.signals_grid_layout_1 = Qt.QGridLayout()
        self.signals_layout_1.addLayout(self.signals_grid_layout_1)
        self.signals.addTab(self.signals_widget_1, 'Filter RX')
        self.signals_widget_2 = Qt.QWidget()
        self.signals_layout_2 = Qt.QBoxLayout(Qt.QBoxLayout.TopToBottom, self.signals_widget_2)
        self.signals_grid_layout_2 = Qt.QGridLayout()
        self.signals_layout_2.addLayout(self.signals_grid_layout_2)
        self.signals.addTab(self.signals_widget_2, 'Modulator')
        self.signals_widget_3 = Qt.QWidget()
        self.signals_layout_3 = Qt.QBoxLayout(Qt.QBoxLayout.TopToBottom, self.signals_widget_3)
        self.signals_grid_layout_3 = Qt.QGridLayout()
        self.signals_layout_3.addLayout(self.signals_grid_layout_3)
        self.signals.addTab(self.signals_widget_3, 'Dec Filter')
        self.signals_widget_4 = Qt.QWidget()
        self.signals_layout_4 = Qt.QBoxLayout(Qt.QBoxLayout.TopToBottom, self.signals_widget_4)
        self.signals_grid_layout_4 = Qt.QGridLayout()
        self.signals_layout_4.addLayout(self.signals_grid_layout_4)
        self.signals.addTab(self.signals_widget_4, 'Clock Recovery')
        self.top_grid_layout.addWidget(self.signals, 1, 0, 2, 4)
        [self.top_grid_layout.setRowStretch(r,1) for r in range(1,3)]
        [self.top_grid_layout.setColumnStretch(c,1) for c in range(0,4)]
        self.controls = Qt.QTabWidget()
        self.controls_widget_0 = Qt.QWidget()
        self.controls_layout_0 = Qt.QBoxLayout(Qt.QBoxLayout.TopToBottom, self.controls_widget_0)
        self.controls_grid_layout_0 = Qt.QGridLayout()
        self.controls_layout_0.addLayout(self.controls_grid_layout_0)
        self.controls.addTab(self.controls_widget_0, 'RF')
        self.controls_widget_1 = Qt.QWidget()
        self.controls_layout_1 = Qt.QBoxLayout(Qt.QBoxLayout.TopToBottom, self.controls_widget_1)
        self.controls_grid_layout_1 = Qt.QGridLayout()
        self.controls_layout_1.addLayout(self.controls_grid_layout_1)
        self.controls.addTab(self.controls_widget_1, 'Receiver DSP')
        self.top_grid_layout.addWidget(self.controls, 0, 0, 1, 4)
        [self.top_grid_layout.setRowStretch(r,1) for r in range(0,1)]
        [self.top_grid_layout.setColumnStretch(c,1) for c in range(0,4)]
        self._rx_gain_range = Range(0, 100, 1, 16, 200)
        self._rx_gain_win = RangeWidget(self._rx_gain_range, self.set_rx_gain, 'RX Power Gain', "counter_slider", float)
        self.controls_grid_layout_0.addWidget(self._rx_gain_win, 0, 0, 1, 1)
        [self.controls_grid_layout_0.setRowStretch(r,1) for r in range(0,1)]
        [self.controls_grid_layout_0.setColumnStretch(c,1) for c in range(0,1)]
        self.qtgui_waterfall_sink_x_0_0_0_0_0 = qtgui.waterfall_sink_f(
        	1024, #size
        	firdes.WIN_BLACKMAN_hARRIS, #wintype
        	0, #fc
        	default_samp/dec_rx, #bw
        	"", #name
                1 #number of inputs
        )
        self.qtgui_waterfall_sink_x_0_0_0_0_0.set_update_time(0.10)
        self.qtgui_waterfall_sink_x_0_0_0_0_0.enable_grid(False)
        self.qtgui_waterfall_sink_x_0_0_0_0_0.enable_axis_labels(True)

        if not True:
          self.qtgui_waterfall_sink_x_0_0_0_0_0.disable_legend()

        if "float" == "float" or "float" == "msg_float":
          self.qtgui_waterfall_sink_x_0_0_0_0_0.set_plot_pos_half(not True)

        labels = ['', '', '', '', '',
                  '', '', '', '', '']
        colors = [0, 0, 0, 0, 0,
                  0, 0, 0, 0, 0]
        alphas = [1.0, 1.0, 1.0, 1.0, 1.0,
                  1.0, 1.0, 1.0, 1.0, 1.0]
        for i in xrange(1):
            if len(labels[i]) == 0:
                self.qtgui_waterfall_sink_x_0_0_0_0_0.set_line_label(i, "Data {0}".format(i))
            else:
                self.qtgui_waterfall_sink_x_0_0_0_0_0.set_line_label(i, labels[i])
            self.qtgui_waterfall_sink_x_0_0_0_0_0.set_color_map(i, colors[i])
            self.qtgui_waterfall_sink_x_0_0_0_0_0.set_line_alpha(i, alphas[i])

        self.qtgui_waterfall_sink_x_0_0_0_0_0.set_intensity_range(-140, 10)

        self._qtgui_waterfall_sink_x_0_0_0_0_0_win = sip.wrapinstance(self.qtgui_waterfall_sink_x_0_0_0_0_0.pyqwidget(), Qt.QWidget)
        self.signals_grid_layout_3.addWidget(self._qtgui_waterfall_sink_x_0_0_0_0_0_win, 2, 0, 1, 6)
        [self.signals_grid_layout_3.setRowStretch(r,1) for r in range(2,3)]
        [self.signals_grid_layout_3.setColumnStretch(c,1) for c in range(0,6)]
        self.qtgui_waterfall_sink_x_0_0_0_0 = qtgui.waterfall_sink_f(
        	1024, #size
        	firdes.WIN_BLACKMAN_hARRIS, #wintype
        	0, #fc
        	default_samp, #bw
        	"", #name
                1 #number of inputs
        )
        self.qtgui_waterfall_sink_x_0_0_0_0.set_update_time(0.10)
        self.qtgui_waterfall_sink_x_0_0_0_0.enable_grid(False)
        self.qtgui_waterfall_sink_x_0_0_0_0.enable_axis_labels(True)

        if not True:
          self.qtgui_waterfall_sink_x_0_0_0_0.disable_legend()

        if "float" == "float" or "float" == "msg_float":
          self.qtgui_waterfall_sink_x_0_0_0_0.set_plot_pos_half(not True)

        labels = ['', '', '', '', '',
                  '', '', '', '', '']
        colors = [0, 0, 0, 0, 0,
                  0, 0, 0, 0, 0]
        alphas = [1.0, 1.0, 1.0, 1.0, 1.0,
                  1.0, 1.0, 1.0, 1.0, 1.0]
        for i in xrange(1):
            if len(labels[i]) == 0:
                self.qtgui_waterfall_sink_x_0_0_0_0.set_line_label(i, "Data {0}".format(i))
            else:
                self.qtgui_waterfall_sink_x_0_0_0_0.set_line_label(i, labels[i])
            self.qtgui_waterfall_sink_x_0_0_0_0.set_color_map(i, colors[i])
            self.qtgui_waterfall_sink_x_0_0_0_0.set_line_alpha(i, alphas[i])

        self.qtgui_waterfall_sink_x_0_0_0_0.set_intensity_range(-140, 10)

        self._qtgui_waterfall_sink_x_0_0_0_0_win = sip.wrapinstance(self.qtgui_waterfall_sink_x_0_0_0_0.pyqwidget(), Qt.QWidget)
        self.signals_grid_layout_2.addWidget(self._qtgui_waterfall_sink_x_0_0_0_0_win, 2, 0, 1, 6)
        [self.signals_grid_layout_2.setRowStretch(r,1) for r in range(2,3)]
        [self.signals_grid_layout_2.setColumnStretch(c,1) for c in range(0,6)]
        self.qtgui_waterfall_sink_x_0_0_0 = qtgui.waterfall_sink_c(
        	1024, #size
        	firdes.WIN_BLACKMAN_hARRIS, #wintype
        	0, #fc
        	default_samp, #bw
        	"", #name
                1 #number of inputs
        )
        self.qtgui_waterfall_sink_x_0_0_0.set_update_time(0.10)
        self.qtgui_waterfall_sink_x_0_0_0.enable_grid(False)
        self.qtgui_waterfall_sink_x_0_0_0.enable_axis_labels(True)

        if not True:
          self.qtgui_waterfall_sink_x_0_0_0.disable_legend()

        if "complex" == "float" or "complex" == "msg_float":
          self.qtgui_waterfall_sink_x_0_0_0.set_plot_pos_half(not True)

        labels = ['', '', '', '', '',
                  '', '', '', '', '']
        colors = [0, 0, 0, 0, 0,
                  0, 0, 0, 0, 0]
        alphas = [1.0, 1.0, 1.0, 1.0, 1.0,
                  1.0, 1.0, 1.0, 1.0, 1.0]
        for i in xrange(1):
            if len(labels[i]) == 0:
                self.qtgui_waterfall_sink_x_0_0_0.set_line_label(i, "Data {0}".format(i))
            else:
                self.qtgui_waterfall_sink_x_0_0_0.set_line_label(i, labels[i])
            self.qtgui_waterfall_sink_x_0_0_0.set_color_map(i, colors[i])
            self.qtgui_waterfall_sink_x_0_0_0.set_line_alpha(i, alphas[i])

        self.qtgui_waterfall_sink_x_0_0_0.set_intensity_range(-140, 10)

        self._qtgui_waterfall_sink_x_0_0_0_win = sip.wrapinstance(self.qtgui_waterfall_sink_x_0_0_0.pyqwidget(), Qt.QWidget)
        self.signals_grid_layout_1.addWidget(self._qtgui_waterfall_sink_x_0_0_0_win, 2, 0, 1, 6)
        [self.signals_grid_layout_1.setRowStretch(r,1) for r in range(2,3)]
        [self.signals_grid_layout_1.setColumnStretch(c,1) for c in range(0,6)]
        self.qtgui_waterfall_sink_x_0_0 = qtgui.waterfall_sink_c(
        	1024, #size
        	firdes.WIN_BLACKMAN_hARRIS, #wintype
        	0, #fc
        	default_samp, #bw
        	"", #name
                1 #number of inputs
        )
        self.qtgui_waterfall_sink_x_0_0.set_update_time(0.10)
        self.qtgui_waterfall_sink_x_0_0.enable_grid(False)
        self.qtgui_waterfall_sink_x_0_0.enable_axis_labels(True)

        if not True:
          self.qtgui_waterfall_sink_x_0_0.disable_legend()

        if "complex" == "float" or "complex" == "msg_float":
          self.qtgui_waterfall_sink_x_0_0.set_plot_pos_half(not True)

        labels = ['', '', '', '', '',
                  '', '', '', '', '']
        colors = [0, 0, 0, 0, 0,
                  0, 0, 0, 0, 0]
        alphas = [1.0, 1.0, 1.0, 1.0, 1.0,
                  1.0, 1.0, 1.0, 1.0, 1.0]
        for i in xrange(1):
            if len(labels[i]) == 0:
                self.qtgui_waterfall_sink_x_0_0.set_line_label(i, "Data {0}".format(i))
            else:
                self.qtgui_waterfall_sink_x_0_0.set_line_label(i, labels[i])
            self.qtgui_waterfall_sink_x_0_0.set_color_map(i, colors[i])
            self.qtgui_waterfall_sink_x_0_0.set_line_alpha(i, alphas[i])

        self.qtgui_waterfall_sink_x_0_0.set_intensity_range(-140, 10)

        self._qtgui_waterfall_sink_x_0_0_win = sip.wrapinstance(self.qtgui_waterfall_sink_x_0_0.pyqwidget(), Qt.QWidget)
        self.signals_grid_layout_0.addWidget(self._qtgui_waterfall_sink_x_0_0_win, 2, 0, 1, 6)
        [self.signals_grid_layout_0.setRowStretch(r,1) for r in range(2,3)]
        [self.signals_grid_layout_0.setColumnStretch(c,1) for c in range(0,6)]
        self.qtgui_time_sink_x_0_0_0_0_0_1 = qtgui.time_sink_f(
        	t_points, #size
        	default_samp/dec_rx, #samp_rate
        	'', #name
        	1 #number of inputs
        )
        self.qtgui_time_sink_x_0_0_0_0_0_1.set_update_time(0.10)
        self.qtgui_time_sink_x_0_0_0_0_0_1.set_y_axis(-2, 2)

        self.qtgui_time_sink_x_0_0_0_0_0_1.set_y_label('Amplitude', "")

        self.qtgui_time_sink_x_0_0_0_0_0_1.enable_tags(-1, True)
        self.qtgui_time_sink_x_0_0_0_0_0_1.set_trigger_mode(qtgui.TRIG_MODE_FREE, qtgui.TRIG_SLOPE_POS, 0.0, 0, 0, "")
        self.qtgui_time_sink_x_0_0_0_0_0_1.enable_autoscale(False)
        self.qtgui_time_sink_x_0_0_0_0_0_1.enable_grid(False)
        self.qtgui_time_sink_x_0_0_0_0_0_1.enable_axis_labels(True)
        self.qtgui_time_sink_x_0_0_0_0_0_1.enable_control_panel(False)
        self.qtgui_time_sink_x_0_0_0_0_0_1.enable_stem_plot(False)

        if not True:
          self.qtgui_time_sink_x_0_0_0_0_0_1.disable_legend()

        labels = ['', '', '', '', '',
                  '', '', '', '', '']
        widths = [1, 1, 1, 1, 1,
                  1, 1, 1, 1, 1]
        colors = ["blue", "red", "green", "black", "cyan",
                  "magenta", "yellow", "dark red", "dark green", "blue"]
        styles = [1, 1, 1, 1, 1,
                  1, 1, 1, 1, 1]
        markers = [-1, -1, -1, -1, -1,
                   -1, -1, -1, -1, -1]
        alphas = [1.0, 1.0, 1.0, 1.0, 1.0,
                  1.0, 1.0, 1.0, 1.0, 1.0]

        for i in xrange(1):
            if len(labels[i]) == 0:
                self.qtgui_time_sink_x_0_0_0_0_0_1.set_line_label(i, "Data {0}".format(i))
            else:
                self.qtgui_time_sink_x_0_0_0_0_0_1.set_line_label(i, labels[i])
            self.qtgui_time_sink_x_0_0_0_0_0_1.set_line_width(i, widths[i])
            self.qtgui_time_sink_x_0_0_0_0_0_1.set_line_color(i, colors[i])
            self.qtgui_time_sink_x_0_0_0_0_0_1.set_line_style(i, styles[i])
            self.qtgui_time_sink_x_0_0_0_0_0_1.set_line_marker(i, markers[i])
            self.qtgui_time_sink_x_0_0_0_0_0_1.set_line_alpha(i, alphas[i])

        self._qtgui_time_sink_x_0_0_0_0_0_1_win = sip.wrapinstance(self.qtgui_time_sink_x_0_0_0_0_0_1.pyqwidget(), Qt.QWidget)
        self.signals_grid_layout_3.addWidget(self._qtgui_time_sink_x_0_0_0_0_0_1_win, 0, 0, 1, 3)
        [self.signals_grid_layout_3.setRowStretch(r,1) for r in range(0,1)]
        [self.signals_grid_layout_3.setColumnStretch(c,1) for c in range(0,3)]
        self.qtgui_time_sink_x_0_0_0_0_0_0 = qtgui.time_sink_f(
        	t_points/10, #size
        	default_samp/dec_rx, #samp_rate
        	'Time RX In', #name
        	1 #number of inputs
        )
        self.qtgui_time_sink_x_0_0_0_0_0_0.set_update_time(0.10)
        self.qtgui_time_sink_x_0_0_0_0_0_0.set_y_axis(-2, 2)

        self.qtgui_time_sink_x_0_0_0_0_0_0.set_y_label('Amplitude', "")

        self.qtgui_time_sink_x_0_0_0_0_0_0.enable_tags(-1, True)
        self.qtgui_time_sink_x_0_0_0_0_0_0.set_trigger_mode(qtgui.TRIG_MODE_FREE, qtgui.TRIG_SLOPE_POS, 0.0, 0, 0, "")
        self.qtgui_time_sink_x_0_0_0_0_0_0.enable_autoscale(False)
        self.qtgui_time_sink_x_0_0_0_0_0_0.enable_grid(False)
        self.qtgui_time_sink_x_0_0_0_0_0_0.enable_axis_labels(True)
        self.qtgui_time_sink_x_0_0_0_0_0_0.enable_control_panel(False)
        self.qtgui_time_sink_x_0_0_0_0_0_0.enable_stem_plot(False)

        if not True:
          self.qtgui_time_sink_x_0_0_0_0_0_0.disable_legend()

        labels = ['', '', '', '', '',
                  '', '', '', '', '']
        widths = [1, 1, 1, 1, 1,
                  1, 1, 1, 1, 1]
        colors = ["blue", "red", "green", "black", "cyan",
                  "magenta", "yellow", "dark red", "dark green", "blue"]
        styles = [1, 1, 1, 1, 1,
                  1, 1, 1, 1, 1]
        markers = [-1, -1, -1, -1, -1,
                   -1, -1, -1, -1, -1]
        alphas = [1.0, 1.0, 1.0, 1.0, 1.0,
                  1.0, 1.0, 1.0, 1.0, 1.0]

        for i in xrange(1):
            if len(labels[i]) == 0:
                self.qtgui_time_sink_x_0_0_0_0_0_0.set_line_label(i, "Data {0}".format(i))
            else:
                self.qtgui_time_sink_x_0_0_0_0_0_0.set_line_label(i, labels[i])
            self.qtgui_time_sink_x_0_0_0_0_0_0.set_line_width(i, widths[i])
            self.qtgui_time_sink_x_0_0_0_0_0_0.set_line_color(i, colors[i])
            self.qtgui_time_sink_x_0_0_0_0_0_0.set_line_style(i, styles[i])
            self.qtgui_time_sink_x_0_0_0_0_0_0.set_line_marker(i, markers[i])
            self.qtgui_time_sink_x_0_0_0_0_0_0.set_line_alpha(i, alphas[i])

        self._qtgui_time_sink_x_0_0_0_0_0_0_win = sip.wrapinstance(self.qtgui_time_sink_x_0_0_0_0_0_0.pyqwidget(), Qt.QWidget)
        self.signals_grid_layout_4.addWidget(self._qtgui_time_sink_x_0_0_0_0_0_0_win, 0, 0, 2, 6)
        [self.signals_grid_layout_4.setRowStretch(r,1) for r in range(0,2)]
        [self.signals_grid_layout_4.setColumnStretch(c,1) for c in range(0,6)]
        self.qtgui_time_sink_x_0_0_0_0_0 = qtgui.time_sink_f(
        	t_points, #size
        	default_samp, #samp_rate
        	'', #name
        	1 #number of inputs
        )
        self.qtgui_time_sink_x_0_0_0_0_0.set_update_time(0.10)
        self.qtgui_time_sink_x_0_0_0_0_0.set_y_axis(-2, 2)

        self.qtgui_time_sink_x_0_0_0_0_0.set_y_label('Amplitude', "")

        self.qtgui_time_sink_x_0_0_0_0_0.enable_tags(-1, True)
        self.qtgui_time_sink_x_0_0_0_0_0.set_trigger_mode(qtgui.TRIG_MODE_FREE, qtgui.TRIG_SLOPE_POS, 0.0, 0, 0, "")
        self.qtgui_time_sink_x_0_0_0_0_0.enable_autoscale(True)
        self.qtgui_time_sink_x_0_0_0_0_0.enable_grid(False)
        self.qtgui_time_sink_x_0_0_0_0_0.enable_axis_labels(True)
        self.qtgui_time_sink_x_0_0_0_0_0.enable_control_panel(False)
        self.qtgui_time_sink_x_0_0_0_0_0.enable_stem_plot(False)

        if not True:
          self.qtgui_time_sink_x_0_0_0_0_0.disable_legend()

        labels = ['', '', '', '', '',
                  '', '', '', '', '']
        widths = [1, 1, 1, 1, 1,
                  1, 1, 1, 1, 1]
        colors = ["blue", "red", "green", "black", "cyan",
                  "magenta", "yellow", "dark red", "dark green", "blue"]
        styles = [1, 1, 1, 1, 1,
                  1, 1, 1, 1, 1]
        markers = [-1, -1, -1, -1, -1,
                   -1, -1, -1, -1, -1]
        alphas = [1.0, 1.0, 1.0, 1.0, 1.0,
                  1.0, 1.0, 1.0, 1.0, 1.0]

        for i in xrange(1):
            if len(labels[i]) == 0:
                self.qtgui_time_sink_x_0_0_0_0_0.set_line_label(i, "Data {0}".format(i))
            else:
                self.qtgui_time_sink_x_0_0_0_0_0.set_line_label(i, labels[i])
            self.qtgui_time_sink_x_0_0_0_0_0.set_line_width(i, widths[i])
            self.qtgui_time_sink_x_0_0_0_0_0.set_line_color(i, colors[i])
            self.qtgui_time_sink_x_0_0_0_0_0.set_line_style(i, styles[i])
            self.qtgui_time_sink_x_0_0_0_0_0.set_line_marker(i, markers[i])
            self.qtgui_time_sink_x_0_0_0_0_0.set_line_alpha(i, alphas[i])

        self._qtgui_time_sink_x_0_0_0_0_0_win = sip.wrapinstance(self.qtgui_time_sink_x_0_0_0_0_0.pyqwidget(), Qt.QWidget)
        self.signals_grid_layout_2.addWidget(self._qtgui_time_sink_x_0_0_0_0_0_win, 0, 0, 1, 3)
        [self.signals_grid_layout_2.setRowStretch(r,1) for r in range(0,1)]
        [self.signals_grid_layout_2.setColumnStretch(c,1) for c in range(0,3)]
        self.qtgui_time_sink_x_0_0_0_0 = qtgui.time_sink_c(
        	200, #size
        	default_samp, #samp_rate
        	'Time RX In', #name
        	1 #number of inputs
        )
        self.qtgui_time_sink_x_0_0_0_0.set_update_time(0.10)
        self.qtgui_time_sink_x_0_0_0_0.set_y_axis(-2, 2)

        self.qtgui_time_sink_x_0_0_0_0.set_y_label('Amplitude', "")

        self.qtgui_time_sink_x_0_0_0_0.enable_tags(-1, True)
        self.qtgui_time_sink_x_0_0_0_0.set_trigger_mode(qtgui.TRIG_MODE_FREE, qtgui.TRIG_SLOPE_POS, 0.0, 0, 0, "")
        self.qtgui_time_sink_x_0_0_0_0.enable_autoscale(False)
        self.qtgui_time_sink_x_0_0_0_0.enable_grid(False)
        self.qtgui_time_sink_x_0_0_0_0.enable_axis_labels(True)
        self.qtgui_time_sink_x_0_0_0_0.enable_control_panel(False)
        self.qtgui_time_sink_x_0_0_0_0.enable_stem_plot(False)

        if not True:
          self.qtgui_time_sink_x_0_0_0_0.disable_legend()

        labels = ['', '', '', '', '',
                  '', '', '', '', '']
        widths = [1, 1, 1, 1, 1,
                  1, 1, 1, 1, 1]
        colors = ["blue", "red", "green", "black", "cyan",
                  "magenta", "yellow", "dark red", "dark green", "blue"]
        styles = [1, 1, 1, 1, 1,
                  1, 1, 1, 1, 1]
        markers = [-1, -1, -1, -1, -1,
                   -1, -1, -1, -1, -1]
        alphas = [1.0, 1.0, 1.0, 1.0, 1.0,
                  1.0, 1.0, 1.0, 1.0, 1.0]

        for i in xrange(2):
            if len(labels[i]) == 0:
                if(i % 2 == 0):
                    self.qtgui_time_sink_x_0_0_0_0.set_line_label(i, "Re{{Data {0}}}".format(i/2))
                else:
                    self.qtgui_time_sink_x_0_0_0_0.set_line_label(i, "Im{{Data {0}}}".format(i/2))
            else:
                self.qtgui_time_sink_x_0_0_0_0.set_line_label(i, labels[i])
            self.qtgui_time_sink_x_0_0_0_0.set_line_width(i, widths[i])
            self.qtgui_time_sink_x_0_0_0_0.set_line_color(i, colors[i])
            self.qtgui_time_sink_x_0_0_0_0.set_line_style(i, styles[i])
            self.qtgui_time_sink_x_0_0_0_0.set_line_marker(i, markers[i])
            self.qtgui_time_sink_x_0_0_0_0.set_line_alpha(i, alphas[i])

        self._qtgui_time_sink_x_0_0_0_0_win = sip.wrapinstance(self.qtgui_time_sink_x_0_0_0_0.pyqwidget(), Qt.QWidget)
        self.signals_grid_layout_1.addWidget(self._qtgui_time_sink_x_0_0_0_0_win, 0, 0, 1, 3)
        [self.signals_grid_layout_1.setRowStretch(r,1) for r in range(0,1)]
        [self.signals_grid_layout_1.setColumnStretch(c,1) for c in range(0,3)]
        self.qtgui_time_sink_x_0_0_0 = qtgui.time_sink_c(
        	t_points, #size
        	default_samp, #samp_rate
        	'Time RX In', #name
        	1 #number of inputs
        )
        self.qtgui_time_sink_x_0_0_0.set_update_time(0.10)
        self.qtgui_time_sink_x_0_0_0.set_y_axis(-2, 2)

        self.qtgui_time_sink_x_0_0_0.set_y_label('Amplitude', "")

        self.qtgui_time_sink_x_0_0_0.enable_tags(-1, True)
        self.qtgui_time_sink_x_0_0_0.set_trigger_mode(qtgui.TRIG_MODE_FREE, qtgui.TRIG_SLOPE_POS, 0.0, 0, 0, "")
        self.qtgui_time_sink_x_0_0_0.enable_autoscale(False)
        self.qtgui_time_sink_x_0_0_0.enable_grid(False)
        self.qtgui_time_sink_x_0_0_0.enable_axis_labels(True)
        self.qtgui_time_sink_x_0_0_0.enable_control_panel(False)
        self.qtgui_time_sink_x_0_0_0.enable_stem_plot(False)

        if not True:
          self.qtgui_time_sink_x_0_0_0.disable_legend()

        labels = ['', '', '', '', '',
                  '', '', '', '', '']
        widths = [1, 1, 1, 1, 1,
                  1, 1, 1, 1, 1]
        colors = ["blue", "red", "green", "black", "cyan",
                  "magenta", "yellow", "dark red", "dark green", "blue"]
        styles = [1, 1, 1, 1, 1,
                  1, 1, 1, 1, 1]
        markers = [-1, -1, -1, -1, -1,
                   -1, -1, -1, -1, -1]
        alphas = [1.0, 1.0, 1.0, 1.0, 1.0,
                  1.0, 1.0, 1.0, 1.0, 1.0]

        for i in xrange(2):
            if len(labels[i]) == 0:
                if(i % 2 == 0):
                    self.qtgui_time_sink_x_0_0_0.set_line_label(i, "Re{{Data {0}}}".format(i/2))
                else:
                    self.qtgui_time_sink_x_0_0_0.set_line_label(i, "Im{{Data {0}}}".format(i/2))
            else:
                self.qtgui_time_sink_x_0_0_0.set_line_label(i, labels[i])
            self.qtgui_time_sink_x_0_0_0.set_line_width(i, widths[i])
            self.qtgui_time_sink_x_0_0_0.set_line_color(i, colors[i])
            self.qtgui_time_sink_x_0_0_0.set_line_style(i, styles[i])
            self.qtgui_time_sink_x_0_0_0.set_line_marker(i, markers[i])
            self.qtgui_time_sink_x_0_0_0.set_line_alpha(i, alphas[i])

        self._qtgui_time_sink_x_0_0_0_win = sip.wrapinstance(self.qtgui_time_sink_x_0_0_0.pyqwidget(), Qt.QWidget)
        self.signals_grid_layout_0.addWidget(self._qtgui_time_sink_x_0_0_0_win, 0, 0, 1, 3)
        [self.signals_grid_layout_0.setRowStretch(r,1) for r in range(0,1)]
        [self.signals_grid_layout_0.setColumnStretch(c,1) for c in range(0,3)]
        self.qtgui_freq_sink_x_0_0_1_0_0_0 = qtgui.freq_sink_f(
        	1024, #size
        	firdes.WIN_BLACKMAN_hARRIS, #wintype
        	0, #fc
        	default_samp/dec_rx, #bw
        	'FFT RX in', #name
        	1 #number of inputs
        )
        self.qtgui_freq_sink_x_0_0_1_0_0_0.set_update_time(0.10)
        self.qtgui_freq_sink_x_0_0_1_0_0_0.set_y_axis(-140, 10)
        self.qtgui_freq_sink_x_0_0_1_0_0_0.set_y_label('Relative Gain', 'dB')
        self.qtgui_freq_sink_x_0_0_1_0_0_0.set_trigger_mode(qtgui.TRIG_MODE_FREE, 0.0, 0, "")
        self.qtgui_freq_sink_x_0_0_1_0_0_0.enable_autoscale(False)
        self.qtgui_freq_sink_x_0_0_1_0_0_0.enable_grid(False)
        self.qtgui_freq_sink_x_0_0_1_0_0_0.set_fft_average(0.05)
        self.qtgui_freq_sink_x_0_0_1_0_0_0.enable_axis_labels(True)
        self.qtgui_freq_sink_x_0_0_1_0_0_0.enable_control_panel(False)

        if not True:
          self.qtgui_freq_sink_x_0_0_1_0_0_0.disable_legend()

        if "float" == "float" or "float" == "msg_float":
          self.qtgui_freq_sink_x_0_0_1_0_0_0.set_plot_pos_half(not True)

        labels = ['', '', '', '', '',
                  '', '', '', '', '']
        widths = [2, 1, 1, 1, 1,
                  1, 1, 1, 1, 1]
        colors = ["blue", "red", "green", "black", "cyan",
                  "magenta", "yellow", "dark red", "dark green", "dark blue"]
        alphas = [1.0, 1.0, 1.0, 1.0, 1.0,
                  1.0, 1.0, 1.0, 1.0, 1.0]
        for i in xrange(1):
            if len(labels[i]) == 0:
                self.qtgui_freq_sink_x_0_0_1_0_0_0.set_line_label(i, "Data {0}".format(i))
            else:
                self.qtgui_freq_sink_x_0_0_1_0_0_0.set_line_label(i, labels[i])
            self.qtgui_freq_sink_x_0_0_1_0_0_0.set_line_width(i, widths[i])
            self.qtgui_freq_sink_x_0_0_1_0_0_0.set_line_color(i, colors[i])
            self.qtgui_freq_sink_x_0_0_1_0_0_0.set_line_alpha(i, alphas[i])

        self._qtgui_freq_sink_x_0_0_1_0_0_0_win = sip.wrapinstance(self.qtgui_freq_sink_x_0_0_1_0_0_0.pyqwidget(), Qt.QWidget)
        self.signals_grid_layout_3.addWidget(self._qtgui_freq_sink_x_0_0_1_0_0_0_win, 0, 3, 1, 3)
        [self.signals_grid_layout_3.setRowStretch(r,1) for r in range(0,1)]
        [self.signals_grid_layout_3.setColumnStretch(c,1) for c in range(3,6)]
        self.qtgui_freq_sink_x_0_0_1_0_0 = qtgui.freq_sink_f(
        	1024, #size
        	firdes.WIN_BLACKMAN_hARRIS, #wintype
        	0, #fc
        	default_samp, #bw
        	'FFT RX in', #name
        	1 #number of inputs
        )
        self.qtgui_freq_sink_x_0_0_1_0_0.set_update_time(0.10)
        self.qtgui_freq_sink_x_0_0_1_0_0.set_y_axis(-140, 10)
        self.qtgui_freq_sink_x_0_0_1_0_0.set_y_label('Relative Gain', 'dB')
        self.qtgui_freq_sink_x_0_0_1_0_0.set_trigger_mode(qtgui.TRIG_MODE_FREE, 0.0, 0, "")
        self.qtgui_freq_sink_x_0_0_1_0_0.enable_autoscale(False)
        self.qtgui_freq_sink_x_0_0_1_0_0.enable_grid(False)
        self.qtgui_freq_sink_x_0_0_1_0_0.set_fft_average(0.05)
        self.qtgui_freq_sink_x_0_0_1_0_0.enable_axis_labels(True)
        self.qtgui_freq_sink_x_0_0_1_0_0.enable_control_panel(False)

        if not True:
          self.qtgui_freq_sink_x_0_0_1_0_0.disable_legend()

        if "float" == "float" or "float" == "msg_float":
          self.qtgui_freq_sink_x_0_0_1_0_0.set_plot_pos_half(not True)

        labels = ['', '', '', '', '',
                  '', '', '', '', '']
        widths = [2, 1, 1, 1, 1,
                  1, 1, 1, 1, 1]
        colors = ["blue", "red", "green", "black", "cyan",
                  "magenta", "yellow", "dark red", "dark green", "dark blue"]
        alphas = [1.0, 1.0, 1.0, 1.0, 1.0,
                  1.0, 1.0, 1.0, 1.0, 1.0]
        for i in xrange(1):
            if len(labels[i]) == 0:
                self.qtgui_freq_sink_x_0_0_1_0_0.set_line_label(i, "Data {0}".format(i))
            else:
                self.qtgui_freq_sink_x_0_0_1_0_0.set_line_label(i, labels[i])
            self.qtgui_freq_sink_x_0_0_1_0_0.set_line_width(i, widths[i])
            self.qtgui_freq_sink_x_0_0_1_0_0.set_line_color(i, colors[i])
            self.qtgui_freq_sink_x_0_0_1_0_0.set_line_alpha(i, alphas[i])

        self._qtgui_freq_sink_x_0_0_1_0_0_win = sip.wrapinstance(self.qtgui_freq_sink_x_0_0_1_0_0.pyqwidget(), Qt.QWidget)
        self.signals_grid_layout_2.addWidget(self._qtgui_freq_sink_x_0_0_1_0_0_win, 0, 3, 1, 3)
        [self.signals_grid_layout_2.setRowStretch(r,1) for r in range(0,1)]
        [self.signals_grid_layout_2.setColumnStretch(c,1) for c in range(3,6)]
        self.qtgui_freq_sink_x_0_0_1_0 = qtgui.freq_sink_c(
        	1024, #size
        	firdes.WIN_BLACKMAN_hARRIS, #wintype
        	0, #fc
        	default_samp, #bw
        	'FFT RX in', #name
        	1 #number of inputs
        )
        self.qtgui_freq_sink_x_0_0_1_0.set_update_time(0.10)
        self.qtgui_freq_sink_x_0_0_1_0.set_y_axis(-140, 10)
        self.qtgui_freq_sink_x_0_0_1_0.set_y_label('Relative Gain', 'dB')
        self.qtgui_freq_sink_x_0_0_1_0.set_trigger_mode(qtgui.TRIG_MODE_FREE, 0.0, 0, "")
        self.qtgui_freq_sink_x_0_0_1_0.enable_autoscale(False)
        self.qtgui_freq_sink_x_0_0_1_0.enable_grid(False)
        self.qtgui_freq_sink_x_0_0_1_0.set_fft_average(1.0)
        self.qtgui_freq_sink_x_0_0_1_0.enable_axis_labels(True)
        self.qtgui_freq_sink_x_0_0_1_0.enable_control_panel(False)

        if not True:
          self.qtgui_freq_sink_x_0_0_1_0.disable_legend()

        if "complex" == "float" or "complex" == "msg_float":
          self.qtgui_freq_sink_x_0_0_1_0.set_plot_pos_half(not True)

        labels = ['', '', '', '', '',
                  '', '', '', '', '']
        widths = [2, 1, 1, 1, 1,
                  1, 1, 1, 1, 1]
        colors = ["blue", "red", "green", "black", "cyan",
                  "magenta", "yellow", "dark red", "dark green", "dark blue"]
        alphas = [1.0, 1.0, 1.0, 1.0, 1.0,
                  1.0, 1.0, 1.0, 1.0, 1.0]
        for i in xrange(1):
            if len(labels[i]) == 0:
                self.qtgui_freq_sink_x_0_0_1_0.set_line_label(i, "Data {0}".format(i))
            else:
                self.qtgui_freq_sink_x_0_0_1_0.set_line_label(i, labels[i])
            self.qtgui_freq_sink_x_0_0_1_0.set_line_width(i, widths[i])
            self.qtgui_freq_sink_x_0_0_1_0.set_line_color(i, colors[i])
            self.qtgui_freq_sink_x_0_0_1_0.set_line_alpha(i, alphas[i])

        self._qtgui_freq_sink_x_0_0_1_0_win = sip.wrapinstance(self.qtgui_freq_sink_x_0_0_1_0.pyqwidget(), Qt.QWidget)
        self.signals_grid_layout_1.addWidget(self._qtgui_freq_sink_x_0_0_1_0_win, 0, 3, 1, 3)
        [self.signals_grid_layout_1.setRowStretch(r,1) for r in range(0,1)]
        [self.signals_grid_layout_1.setColumnStretch(c,1) for c in range(3,6)]
        self.qtgui_freq_sink_x_0_0_1 = qtgui.freq_sink_c(
        	1024, #size
        	firdes.WIN_BLACKMAN_hARRIS, #wintype
        	0, #fc
        	default_samp, #bw
        	'FFT RX in', #name
        	1 #number of inputs
        )
        self.qtgui_freq_sink_x_0_0_1.set_update_time(0.10)
        self.qtgui_freq_sink_x_0_0_1.set_y_axis(-140, 10)
        self.qtgui_freq_sink_x_0_0_1.set_y_label('Relative Gain', 'dB')
        self.qtgui_freq_sink_x_0_0_1.set_trigger_mode(qtgui.TRIG_MODE_FREE, 0.0, 0, "")
        self.qtgui_freq_sink_x_0_0_1.enable_autoscale(False)
        self.qtgui_freq_sink_x_0_0_1.enable_grid(False)
        self.qtgui_freq_sink_x_0_0_1.set_fft_average(1.0)
        self.qtgui_freq_sink_x_0_0_1.enable_axis_labels(True)
        self.qtgui_freq_sink_x_0_0_1.enable_control_panel(False)

        if not True:
          self.qtgui_freq_sink_x_0_0_1.disable_legend()

        if "complex" == "float" or "complex" == "msg_float":
          self.qtgui_freq_sink_x_0_0_1.set_plot_pos_half(not True)

        labels = ['', '', '', '', '',
                  '', '', '', '', '']
        widths = [2, 1, 1, 1, 1,
                  1, 1, 1, 1, 1]
        colors = ["blue", "red", "green", "black", "cyan",
                  "magenta", "yellow", "dark red", "dark green", "dark blue"]
        alphas = [1.0, 1.0, 1.0, 1.0, 1.0,
                  1.0, 1.0, 1.0, 1.0, 1.0]
        for i in xrange(1):
            if len(labels[i]) == 0:
                self.qtgui_freq_sink_x_0_0_1.set_line_label(i, "Data {0}".format(i))
            else:
                self.qtgui_freq_sink_x_0_0_1.set_line_label(i, labels[i])
            self.qtgui_freq_sink_x_0_0_1.set_line_width(i, widths[i])
            self.qtgui_freq_sink_x_0_0_1.set_line_color(i, colors[i])
            self.qtgui_freq_sink_x_0_0_1.set_line_alpha(i, alphas[i])

        self._qtgui_freq_sink_x_0_0_1_win = sip.wrapinstance(self.qtgui_freq_sink_x_0_0_1.pyqwidget(), Qt.QWidget)
        self.signals_grid_layout_0.addWidget(self._qtgui_freq_sink_x_0_0_1_win, 0, 3, 1, 3)
        [self.signals_grid_layout_0.setRowStretch(r,1) for r in range(0,1)]
        [self.signals_grid_layout_0.setColumnStretch(c,1) for c in range(3,6)]
        self.iio_fmcomms2_source_0 = iio.fmcomms2_source_f32c('ip:pluto.local', default_freq, default_samp, 1 - 1, 20000000, True, False, 0x8000, True, True, True, "fast_attack", default_gain, "manual", 64.0, "A_BALANCED", '', True)
        self.fir_filter_xxx_0_0 = filter.fir_filter_fff(dec_rx, (low_pass_taps_2))
        self.fir_filter_xxx_0_0.declare_sample_delay(0)
        self.fir_filter_xxx_0 = filter.fir_filter_ccc(1, (low_pass_taps))
        self.fir_filter_xxx_0.declare_sample_delay(0)
        self.digital_diff_decoder_bb_0 = digital.diff_decoder_bb(2)
        self.digital_clock_recovery_mm_xx_0 = digital.clock_recovery_mm_ff(sps_rx, 0.25*0.175*0.175, 0.5, 0.175, 0.005)
        self.digital_binary_slicer_fb_0 = digital.binary_slicer_fb()
        self.blocks_file_sink_1 = blocks.file_sink(gr.sizeof_char*1, default_bin_file_sink, False)
        self.blocks_file_sink_1.set_unbuffered(False)
        self.analog_quadrature_demod_cf_0 = analog.quadrature_demod_cf((default_samp)/(2*math.pi*f_dev/8.0)/10)

        ##################################################
        # Connections
        ##################################################
        self.connect((self.analog_quadrature_demod_cf_0, 0), (self.fir_filter_xxx_0_0, 0))
        self.connect((self.analog_quadrature_demod_cf_0, 0), (self.qtgui_freq_sink_x_0_0_1_0_0, 0))
        self.connect((self.analog_quadrature_demod_cf_0, 0), (self.qtgui_time_sink_x_0_0_0_0_0, 0))
        self.connect((self.analog_quadrature_demod_cf_0, 0), (self.qtgui_waterfall_sink_x_0_0_0_0, 0))
        self.connect((self.digital_binary_slicer_fb_0, 0), (self.digital_diff_decoder_bb_0, 0))
        self.connect((self.digital_clock_recovery_mm_xx_0, 0), (self.digital_binary_slicer_fb_0, 0))
        self.connect((self.digital_clock_recovery_mm_xx_0, 0), (self.qtgui_time_sink_x_0_0_0_0_0_0, 0))
        self.connect((self.digital_diff_decoder_bb_0, 0), (self.blocks_file_sink_1, 0))
        self.connect((self.fir_filter_xxx_0, 0), (self.analog_quadrature_demod_cf_0, 0))
        self.connect((self.fir_filter_xxx_0, 0), (self.qtgui_freq_sink_x_0_0_1_0, 0))
        self.connect((self.fir_filter_xxx_0, 0), (self.qtgui_time_sink_x_0_0_0_0, 0))
        self.connect((self.fir_filter_xxx_0, 0), (self.qtgui_waterfall_sink_x_0_0_0, 0))
        self.connect((self.fir_filter_xxx_0_0, 0), (self.digital_clock_recovery_mm_xx_0, 0))
        self.connect((self.fir_filter_xxx_0_0, 0), (self.qtgui_freq_sink_x_0_0_1_0_0_0, 0))
        self.connect((self.fir_filter_xxx_0_0, 0), (self.qtgui_time_sink_x_0_0_0_0_0_1, 0))
        self.connect((self.fir_filter_xxx_0_0, 0), (self.qtgui_waterfall_sink_x_0_0_0_0_0, 0))
        self.connect((self.iio_fmcomms2_source_0, 0), (self.fir_filter_xxx_0, 0))
        self.connect((self.iio_fmcomms2_source_0, 0), (self.qtgui_freq_sink_x_0_0_1, 0))
        self.connect((self.iio_fmcomms2_source_0, 0), (self.qtgui_time_sink_x_0_0_0, 0))
        self.connect((self.iio_fmcomms2_source_0, 0), (self.qtgui_waterfall_sink_x_0_0, 0))

    def closeEvent(self, event):
        self.settings = Qt.QSettings("GNU Radio", "gfsk_rx")
        self.settings.setValue("geometry", self.saveGeometry())
        event.accept()

    def get_default_bandwidth(self):
        return self.default_bandwidth

    def set_default_bandwidth(self, default_bandwidth):
        self.default_bandwidth = default_bandwidth

    def get_default_baud(self):
        return self.default_baud

    def set_default_baud(self, default_baud):
        self.default_baud = default_baud
        self.set_f_dev(self.default_baud/4)
        self.set_interp_tx(self.default_samp/self.default_baud)

    def get_default_bin_file_sink(self):
        return self.default_bin_file_sink

    def set_default_bin_file_sink(self, default_bin_file_sink):
        self.default_bin_file_sink = default_bin_file_sink
        self.blocks_file_sink_1.open(self.default_bin_file_sink)

    def get_default_freq(self):
        return self.default_freq

    def set_default_freq(self, default_freq):
        self.default_freq = default_freq
        self.iio_fmcomms2_source_0.set_params(self.default_freq, self.default_samp, 20000000, True, True, True, "fast_attack", self.default_gain, "manual", 64.0, "A_BALANCED", '', True)

    def get_default_gain(self):
        return self.default_gain

    def set_default_gain(self, default_gain):
        self.default_gain = default_gain
        self.iio_fmcomms2_source_0.set_params(self.default_freq, self.default_samp, 20000000, True, True, True, "fast_attack", self.default_gain, "manual", 64.0, "A_BALANCED", '', True)

    def get_default_ip(self):
        return self.default_ip

    def set_default_ip(self, default_ip):
        self.default_ip = default_ip

    def get_default_port(self):
        return self.default_port

    def set_default_port(self, default_port):
        self.default_port = default_port

    def get_default_samp(self):
        return self.default_samp

    def set_default_samp(self, default_samp):
        self.default_samp = default_samp
        self.qtgui_waterfall_sink_x_0_0_0_0_0.set_frequency_range(0, self.default_samp/self.dec_rx)
        self.qtgui_waterfall_sink_x_0_0_0_0.set_frequency_range(0, self.default_samp)
        self.qtgui_waterfall_sink_x_0_0_0.set_frequency_range(0, self.default_samp)
        self.qtgui_waterfall_sink_x_0_0.set_frequency_range(0, self.default_samp)
        self.qtgui_time_sink_x_0_0_0_0_0_1.set_samp_rate(self.default_samp/self.dec_rx)
        self.qtgui_time_sink_x_0_0_0_0_0_0.set_samp_rate(self.default_samp/self.dec_rx)
        self.qtgui_time_sink_x_0_0_0_0_0.set_samp_rate(self.default_samp)
        self.qtgui_time_sink_x_0_0_0_0.set_samp_rate(self.default_samp)
        self.qtgui_time_sink_x_0_0_0.set_samp_rate(self.default_samp)
        self.qtgui_freq_sink_x_0_0_1_0_0_0.set_frequency_range(0, self.default_samp/self.dec_rx)
        self.qtgui_freq_sink_x_0_0_1_0_0.set_frequency_range(0, self.default_samp)
        self.qtgui_freq_sink_x_0_0_1_0.set_frequency_range(0, self.default_samp)
        self.qtgui_freq_sink_x_0_0_1.set_frequency_range(0, self.default_samp)
        self.set_interp_tx(self.default_samp/self.default_baud)
        self.iio_fmcomms2_source_0.set_params(self.default_freq, self.default_samp, 20000000, True, True, True, "fast_attack", self.default_gain, "manual", 64.0, "A_BALANCED", '', True)
        self.analog_quadrature_demod_cf_0.set_gain((self.default_samp)/(2*math.pi*self.f_dev/8.0)/10)

    def get_sdr_dev(self):
        return self.sdr_dev

    def set_sdr_dev(self, sdr_dev):
        self.sdr_dev = sdr_dev

    def get_interp_tx(self):
        return self.interp_tx

    def set_interp_tx(self, interp_tx):
        self.interp_tx = interp_tx
        self.set_sps_rx(self.interp_tx/self.dec_rx)
        self.set_dec_rx(self.interp_tx/10)

    def get_dec_rx(self):
        return self.dec_rx

    def set_dec_rx(self, dec_rx):
        self.dec_rx = dec_rx
        self.set_sps_rx(self.interp_tx/self.dec_rx)
        self.qtgui_waterfall_sink_x_0_0_0_0_0.set_frequency_range(0, self.default_samp/self.dec_rx)
        self.qtgui_time_sink_x_0_0_0_0_0_1.set_samp_rate(self.default_samp/self.dec_rx)
        self.qtgui_time_sink_x_0_0_0_0_0_0.set_samp_rate(self.default_samp/self.dec_rx)
        self.qtgui_freq_sink_x_0_0_1_0_0_0.set_frequency_range(0, self.default_samp/self.dec_rx)

    def get_t_points(self):
        return self.t_points

    def set_t_points(self, t_points):
        self.t_points = t_points

    def get_sps_rx(self):
        return self.sps_rx

    def set_sps_rx(self, sps_rx):
        self.sps_rx = sps_rx
        self.digital_clock_recovery_mm_xx_0.set_omega(self.sps_rx)

    def get_rx_gain(self):
        return self.rx_gain

    def set_rx_gain(self, rx_gain):
        self.rx_gain = rx_gain

    def get_low_pass_taps_2(self):
        return self.low_pass_taps_2

    def set_low_pass_taps_2(self, low_pass_taps_2):
        self.low_pass_taps_2 = low_pass_taps_2
        self.fir_filter_xxx_0_0.set_taps((self.low_pass_taps_2))

    def get_low_pass_taps(self):
        return self.low_pass_taps

    def set_low_pass_taps(self, low_pass_taps):
        self.low_pass_taps = low_pass_taps
        self.fir_filter_xxx_0.set_taps((self.low_pass_taps))

    def get_f_dev(self):
        return self.f_dev

    def set_f_dev(self, f_dev):
        self.f_dev = f_dev
        self.analog_quadrature_demod_cf_0.set_gain((self.default_samp)/(2*math.pi*self.f_dev/8.0)/10)


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
        "-f", "--default-freq", dest="default_freq", type="intx", default=437500000,
        help="Set default_freq [default=%default]")
    parser.add_option(
        "-g", "--default-gain", dest="default_gain", type="eng_float", default=eng_notation.num_to_str(16),
        help="Set default_gain [default=%default]")
    parser.add_option(
        "-i", "--default-ip", dest="default_ip", type="string", default='127.0.0.1',
        help="Set default_ip [default=%default]")
    parser.add_option(
        "-p", "--default-port", dest="default_port", type="intx", default=5000,
        help="Set default_port [default=%default]")
    parser.add_option(
        "-s", "--default-samp", dest="default_samp", type="intx", default=1920000,
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

    if StrictVersion("4.5.0") <= StrictVersion(Qt.qVersion()) < StrictVersion("5.0.0"):
        style = gr.prefs().get_string('qtgui', 'style', 'raster')
        Qt.QApplication.setGraphicsSystem(style)
    qapp = Qt.QApplication(sys.argv)

    tb = top_block_cls(default_bandwidth=options.default_bandwidth, default_baud=options.default_baud, default_bin_file_sink=options.default_bin_file_sink, default_freq=options.default_freq, default_gain=options.default_gain, default_ip=options.default_ip, default_port=options.default_port, default_samp=options.default_samp, sdr_dev=options.sdr_dev)
    tb.start()
    tb.show()

    def quitting():
        tb.stop()
        tb.wait()
    qapp.aboutToQuit.connect(quitting)
    qapp.exec_()


if __name__ == '__main__':
    main()
