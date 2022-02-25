#!/usr/bin/env python3
# -*- coding: utf-8 -*-

#
# SPDX-License-Identifier: GPL-3.0
#
# GNU Radio Python Flow Graph
# Title: MODULACIONPM
# Author: josue
# GNU Radio version: 3.9.5.0

from distutils.version import StrictVersion

if __name__ == '__main__':
    import ctypes
    import sys
    if sys.platform.startswith('linux'):
        try:
            x11 = ctypes.cdll.LoadLibrary('libX11.so')
            x11.XInitThreads()
        except:
            print("Warning: failed to XInitThreads()")

from gnuradio import blocks
from gnuradio import gr
from gnuradio.filter import firdes
from gnuradio.fft import window
import sys
import signal
from PyQt5 import Qt
from argparse import ArgumentParser
from gnuradio.eng_arg import eng_float, intx
from gnuradio import eng_notation



from gnuradio import qtgui

class L4P1(gr.top_block, Qt.QWidget):

    def __init__(self, Ac=100e-3, kp=1):
        gr.top_block.__init__(self, "MODULACIONPM", catch_exceptions=True)
        Qt.QWidget.__init__(self)
        self.setWindowTitle("MODULACIONPM")
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

        self.settings = Qt.QSettings("GNU Radio", "L4P1")

        try:
            if StrictVersion(Qt.qVersion()) < StrictVersion("5.0.0"):
                self.restoreGeometry(self.settings.value("geometry").toByteArray())
            else:
                self.restoreGeometry(self.settings.value("geometry"))
        except:
            pass

        ##################################################
        # Parameters
        ##################################################
        self.Ac = Ac
        self.kp = kp

        ##################################################
        # Variables
        ##################################################
        self.samp_rate = samp_rate = 32000

        ##################################################
        # Blocks
        ##################################################
        self.blocks_transcendental_1 = blocks.transcendental('sin', "float")
        self.blocks_transcendental_0 = blocks.transcendental('cos', "float")
        self.blocks_multiply_const_vxx_0_0 = blocks.multiply_const_cc(Ac)
        self.blocks_multiply_const_vxx_0 = blocks.multiply_const_ff(kp)
        self.blocks_float_to_complex_0 = blocks.float_to_complex(1)


        ##################################################
        # Connections
        ##################################################
        self.connect((self.blocks_float_to_complex_0, 0), (self.blocks_multiply_const_vxx_0_0, 0))
        self.connect((self.blocks_multiply_const_vxx_0, 0), (self.blocks_transcendental_0, 0))
        self.connect((self.blocks_multiply_const_vxx_0, 0), (self.blocks_transcendental_1, 0))
        self.connect((self.blocks_multiply_const_vxx_0_0, 0), (self, 0))
        self.connect((self.blocks_transcendental_0, 0), (self.blocks_float_to_complex_0, 0))
        self.connect((self.blocks_transcendental_1, 0), (self.blocks_float_to_complex_0, 1))
        self.connect((self, 0), (self.blocks_multiply_const_vxx_0, 0))


    def closeEvent(self, event):
        self.settings = Qt.QSettings("GNU Radio", "L4P1")
        self.settings.setValue("geometry", self.saveGeometry())
        self.stop()
        self.wait()

        event.accept()

    def get_Ac(self):
        return self.Ac

    def set_Ac(self, Ac):
        self.Ac = Ac
        self.blocks_multiply_const_vxx_0_0.set_k(self.Ac)

    def get_kp(self):
        return self.kp

    def set_kp(self, kp):
        self.kp = kp
        self.blocks_multiply_const_vxx_0.set_k(self.kp)

    def get_samp_rate(self):
        return self.samp_rate

    def set_samp_rate(self, samp_rate):
        self.samp_rate = samp_rate



def argument_parser():
    parser = ArgumentParser()
    parser.add_argument(
        "--Ac", dest="Ac", type=eng_float, default=eng_notation.num_to_str(float(100e-3)),
        help="Set Amplitud de portadora [default=%(default)r]")
    parser.add_argument(
        "--kp", dest="kp", type=eng_float, default=eng_notation.num_to_str(float(1)),
        help="Set coeficiente de modulacion [default=%(default)r]")
    return parser


def main(top_block_cls=L4P1, options=None):
    if options is None:
        options = argument_parser().parse_args()

    if StrictVersion("4.5.0") <= StrictVersion(Qt.qVersion()) < StrictVersion("5.0.0"):
        style = gr.prefs().get_string('qtgui', 'style', 'raster')
        Qt.QApplication.setGraphicsSystem(style)
    qapp = Qt.QApplication(sys.argv)

    tb = top_block_cls(Ac=options.Ac, kp=options.kp)

    tb.start()

    tb.show()

    def sig_handler(sig=None, frame=None):
        tb.stop()
        tb.wait()

        Qt.QApplication.quit()

    signal.signal(signal.SIGINT, sig_handler)
    signal.signal(signal.SIGTERM, sig_handler)

    timer = Qt.QTimer()
    timer.start(500)
    timer.timeout.connect(lambda: None)

    qapp.exec_()

if __name__ == '__main__':
    main()
