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
        self.window_min_width = 500
        self.window_max_width = 500
        self.window_min_height = 400
        self.window_max_height = 400
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

        # 组件
        label_username = QtWidgets.QLabel('用户名')
        label_username.setObjectName('title')
        lineedit_username = QtWidgets.QLineEdit()
        button_save_username = QtWidgets.QPushButton()
        button_save_username.setFixedSize(30, 30)
        button_unsave_username = QtWidgets.QPushButton()
        button_unsave_username.setFixedSize(30, 30)
        label_created = QtWidgets.QLabel('创建时间')
        label_created.setObjectName('title')
        label_created_value = QtWidgets.QLabel('2001-01-01 00:00:00')
        label_modified = QtWidgets.QLabel('修改时间')
        label_modified.setObjectName('title')
        label_modified_value = QtWidgets.QLabel('2001-01-01 00:00:00')

        # 布局管理
        layout = QtWidgets.QVBoxLayout()
        groupbox_form = QtWidgets.QGroupBox()
        layout_form = QtWidgets.QGridLayout()
        layout_form.setSpacing(10)
        layout_username = QtWidgets.QHBoxLayout()
        layout_form.addWidget(label_username, 1, 1)
        layout_username.addWidget(lineedit_username)
        layout_username.addWidget(button_save_username)
        layout_username.addWidget(button_unsave_username)
        layout_form.addLayout(layout_username, 1, 2)
        layout_form.addWidget(label_created, 2, 1)
        layout_form.addWidget(label_created_value, 2, 2)
        layout_form.addWidget(label_modified, 3, 1)
        layout_form.addWidget(label_modified_value, 3, 2)
        groupbox_form.setLayout(layout_form)
        layout.addWidget(groupbox_form)
        layout.addStretch(1)

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
