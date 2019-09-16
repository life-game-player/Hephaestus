from PyQt5 import QtWidgets
from PyQt5 import QtCore
from PyQt5 import QtGui

from views.window_dragable import WindowDragable
from qss.qss_setter import QSSSetter


class WindowUserDetail(WindowDragable):
    def __init__(self, parent):
        super().__init__()
        self.parent = parent

        self.installEventFilter(self)
        self.activated = False

        # 设置窗口无边框
        self.setWindowFlags(
            QtCore.Qt.FramelessWindowHint
        )
        # 设置窗口背景透明
        self.setAttribute(QtCore.Qt.WA_TranslucentBackground)

        # 设置窗口大小
        self.window_min_width = 302
        self.window_max_width = 302
        self.window_min_height = 550
        self.window_max_height = 550
        self.setMinimumSize(self.window_min_width, self.window_min_height)
        self.setMaximumSize(self.window_max_width, self.window_max_height)

        # 设置窗口子部件
        self.set_head_widget()
        self.set_body_widget()

        # 窗口组装
        self.layout_main = QtWidgets.QVBoxLayout()
        self.layout_main.addWidget(self.widget_head)
        self.layout_main.addWidget(self.widget_body)
        self.layout_main.setSpacing(0)
        self.layout_main.setContentsMargins(0, 0, 0, 0)
        self.setLayout(self.layout_main)

        # 设置样式
        QSSSetter.set_qss(self, __file__)

    def set_head_widget(self):
        self.widget_head = QtWidgets.QWidget()
        self.widget_head.setMouseTracking(True)
        self.widget_head.setObjectName('head')
        self.widget_head.setFixedSize(self.window_min_width, 30)

    def set_body_widget(self):
        self.widget_body = QtWidgets.QWidget()
        self.widget_body.setMouseTracking(True)
        self.widget_body.setObjectName('body')
        self.widget_body.setFixedSize(
            self.window_min_width,
            self.window_min_height - 30
        )

        label_username = QtWidgets.QLabel('用户名')

        layout = QtWidgets.QVBoxLayout()
        groupbox_form = QtWidgets.QGroupBox()
        layout_form = QtWidgets.QGridLayout()
        layout_form.addWidget(label_username, 1, 1)
        groupbox_form.setLayout(layout_form)
        layout.addWidget(groupbox_form)

        self.widget_body.setLayout(layout)

    def eventFilter(self, source, event):
        if (
            event.type() == QtCore.QEvent.ActivationChange and
            source == self
        ):
            self.activated = not self.activated
            if not self.activated:
                self.close()
        return super().eventFilter(source, event)
