from PyQt5 import QtWidgets
from PyQt5 import QtCore

from qss.qss_setter import QSSSetter


class WindowMain(QtWidgets.QWidget):
    def __init__(self, screen_width, screen_height):
        super().__init__()

        # 设置窗口大小
        self.window_width = screen_width * 0.2
        self.window_height = screen_height * 0.8
        self.resize(self.window_width, self.window_height)

        # 设置窗口透明度
        self.setWindowOpacity(0.5)
        # 设置窗口无边框
        self.setWindowFlags(
            QtCore.Qt.FramelessWindowHint
        )
        # 设置窗口背景透明
        self.setAttribute(QtCore.Qt.WA_TranslucentBackground)

        # 设置窗口子部件
        self.set_head_widget()
        self.set_body_widget()
        self.set_bottom_widget()

        # 窗口组装
        self.layout_main = QtWidgets.QVBoxLayout()
        self.layout_main.setSpacing(0)
        self.layout_main.addWidget(self.widget_head)
        self.layout_main.addWidget(self.widget_body)
        self.layout_main.addWidget(self.widget_bottom)
        self.setLayout(self.layout_main)

        # 设置样式
        QSSSetter.set_qss(self, __file__)

    def set_head_widget(self):
        self.widget_head = QtWidgets.QWidget()
        self.widget_head.setObjectName('head')
        self.widget_head.setFixedSize(
            self.window_width,
            self.window_height * 0.2
        )

    def set_body_widget(self):
        self.widget_body = QtWidgets.QWidget()
        self.widget_body.setObjectName('body')
        self.widget_body.setFixedSize(
            self.window_width,
            self.window_height * 0.74
        )

    def set_bottom_widget(self):
        self.widget_bottom = QtWidgets.QWidget()
        self.widget_bottom.setObjectName('bottom')
        self.widget_bottom.setFixedSize(
            self.window_width,
            self.window_height * 0.06
        )
