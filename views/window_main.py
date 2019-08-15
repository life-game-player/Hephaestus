from PyQt5 import QtWidgets
from PyQt5 import QtCore

from qss.qss_setter import QSSSetter


class WindowMain(QtWidgets.QWidget):
    def __init__(self, screen_width, screen_height):
        super().__init__()

        # 设置窗口大小
        window_width = screen_width * 0.2
        window_height = screen_height * 0.8
        self.resize(window_width, window_height)

        self.setWindowOpacity(0.5)  # 设置窗口透明度
        self.setWindowFlags(
            QtCore.Qt.FramelessWindowHint
        )  # 设置窗口无边框
        self.setAttribute(QtCore.Qt.WA_TranslucentBackground)

        self.widget_head = QtWidgets.QWidget()
        self.widget_head.setObjectName('head')
        self.widget_head.setFixedSize(window_width, window_height * 0.2)

        self.widget_body = QtWidgets.QWidget()
        self.widget_body.setObjectName('body')
        self.widget_body.setFixedSize(window_width, window_height * 0.74)

        self.widget_bottom = QtWidgets.QWidget()
        self.widget_bottom.setObjectName('bottom')
        self.widget_bottom.setFixedSize(window_width, window_height * 0.06)

        self.layout_main = QtWidgets.QVBoxLayout()
        self.layout_main.setSpacing(0)
        self.layout_main.addWidget(self.widget_head)
        self.layout_main.addWidget(self.widget_body)
        self.layout_main.addWidget(self.widget_bottom)
        self.setLayout(self.layout_main)

        QSSSetter.set_qss(self, __file__)
