from PyQt5 import QtWidgets
from PyQt5 import QtCore

from qss.qss_setter import QSSSetter


class WindowWarning(QtWidgets.QDialog):
    def __init__(self, parent):
        super().__init__(parent, QtCore.Qt.FramelessWindowHint)
        self.parent = parent

        # 设置窗口大小
        self.window_min_width = 250
        self.window_max_width = 500
        self.window_min_height = 120
        self.window_max_height = 120
        self.setMinimumSize(self.window_min_width, self.window_min_height)
        self.setMaximumSize(self.window_max_width, self.window_max_height)

        # 设置窗口背景透明
        self.setAttribute(QtCore.Qt.WA_TranslucentBackground)

        widget_warning = QtWidgets.QWidget()
        widget_warning.setObjectName('warning')
        widget_warning.setMinimumSize(
            self.window_min_width, self.window_min_height
        )
        widget_warning.setMaximumSize(
            self.window_max_width, self.window_max_height
        )
        button_box = QtWidgets.QDialogButtonBox(
            QtWidgets.QDialogButtonBox.Ok |
            QtWidgets.QDialogButtonBox.Cancel
        )
        button_box.accepted.connect(self.accept)
        button_box.rejected.connect(self.reject)
        button_ok = button_box.button(QtWidgets.QDialogButtonBox.Ok)
        button_ok.setText('确定')
        button_cancel = button_box.button(QtWidgets.QDialogButtonBox.Cancel)
        button_cancel.setText('取消')
        button_ok.setFixedSize(50, 25)
        button_cancel.setFixedSize(50, 25)
        button_ok.setStyleSheet(
            'QPushButton{'
            'border-radius:2px;'
            'font-size:12px;'
            'font-family:"微软雅黑";'
            'color:white;'
            'background-color:rgba(255,102,51,90%);'
            '}'
        )
        button_cancel.setStyleSheet(
            'QPushButton{'
            'border-radius:2px;'
            'font-size:12px;'
            'font-family:"微软雅黑";'
            'color:white;'
            'background-color:rgba(255,102,51,90%);'
            '}'
        )
        self.label_info = QtWidgets.QLabel()
        self.label_info.setObjectName('info')
        label_icon = QtWidgets.QLabel()
        label_icon.setFixedSize(32, 32)
        label_icon.setObjectName('icon')

        layout = QtWidgets.QVBoxLayout()
        layout.setSpacing(0)
        layout.setContentsMargins(20, 0, 20, 0)
        layout_info = QtWidgets.QHBoxLayout()
        layout_info.setSpacing(10)
        layout_info.addWidget(label_icon)
        layout_info.addWidget(self.label_info)
        layout.addStretch(1)
        layout.addLayout(layout_info)
        layout.addStretch(1)
        layout.addWidget(button_box)
        layout.addStretch(1)
        widget_warning.setLayout(layout)
        layout_main = QtWidgets.QVBoxLayout()
        layout_main.addWidget(widget_warning)
        layout_main.setSpacing(0)
        layout_main.setContentsMargins(0, 0, 0, 0)
        self.setLayout(layout_main)

        # 设置样式
        QSSSetter.set_qss(self, __file__)

    def accept(self):
        self.done(1)

    def reject(self):
        self.done(0)

    def set_info(self, info):
        self.label_info.setText(info)
