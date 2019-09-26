from PyQt5 import QtWidgets
from PyQt5 import QtCore
from PyQt5 import QtGui

from views.window_dragable import WindowDragable
from views.window_warning import WindowWarning
from views.window_error import WindowError
from views.window_update_passwd import WindowUpdatePass
from qss.qss_setter import QSSSetter


class WindowUserProfile(WindowDragable):
    def __init__(self, parent, user):
        super().__init__()
        self.parent = parent
        self.children_windows = dict()
        self.user = user

        self.installEventFilter(self)
        self.activated = False

        # 设置窗口无边框
        self.setWindowFlags(
            QtCore.Qt.FramelessWindowHint
        )
        # 设置窗口背景透明
        self.setAttribute(QtCore.Qt.WA_TranslucentBackground)

        # 设置窗口大小
        self.window_min_width = 392
        self.window_max_width = 392
        self.window_min_height = 165
        self.window_max_height = 165
        self.setMinimumSize(self.window_min_width, self.window_min_height)
        self.setMaximumSize(self.window_max_width, self.window_max_height)

        # 设置窗口子部件
        self.set_body_widget()

        # 窗口组装
        self.layout_main = QtWidgets.QVBoxLayout()
        self.layout_main.addWidget(self.widget_body)
        self.layout_main.setSpacing(0)
        self.layout_main.setContentsMargins(0, 0, 0, 0)
        self.setLayout(self.layout_main)

        parent_pos = parent.pos()
        self.setGeometry(
            parent_pos.x() - self.window_min_width,
            parent_pos.y(),
            self.window_min_width,
            self.window_min_height
        )

        # 设置样式
        QSSSetter.set_qss(self, __file__)

    def set_body_widget(self):
        self.widget_body = QtWidgets.QWidget()
        self.widget_body.setMouseTracking(True)
        self.widget_body.setObjectName('body')
        self.widget_body.setFixedSize(
            self.window_min_width,
            self.window_min_height
        )

        # 组件
        label_username = QtWidgets.QLabel('用户名')
        label_username.setObjectName('title')
        self.lineedit_username = QtWidgets.QLineEdit()
        self.lineedit_username.setFixedWidth(160)
        self.lineedit_username.installEventFilter(self)
        self.button_update_passwd = QtWidgets.QPushButton('修改密码')
        self.button_update_passwd.clicked.connect(self.update_passwd)
        self.button_update_passwd.setFixedSize(70, 30)
        self.button_update_passwd.setObjectName('update')
        label_last_login = QtWidgets.QLabel('上次登录时间')
        self.label_last_login_value = QtWidgets.QLabel()
        self.label_last_login_value.setObjectName('value')
        label_created = QtWidgets.QLabel('创建时间')
        label_created.setObjectName('title')
        self.label_created_value = QtWidgets.QLabel()
        self.label_created_value.setObjectName('value')
        label_modified = QtWidgets.QLabel('修改时间')
        label_modified.setObjectName('title')
        self.label_modified_value = QtWidgets.QLabel()
        self.label_modified_value.setObjectName('value')
        self.load_user_info()

        # 布局管理
        layout = QtWidgets.QVBoxLayout()
        groupbox_form = QtWidgets.QGroupBox()
        layout_form = QtWidgets.QGridLayout()
        layout_form.setSpacing(10)
        layout_username = QtWidgets.QHBoxLayout()
        layout_form.addWidget(label_username, 1, 1)
        layout_username.addWidget(self.lineedit_username)
        layout_username.addWidget(self.button_update_passwd)
        layout_username.addStretch(1)
        layout_form.addLayout(layout_username, 1, 2)
        layout_form.addWidget(label_last_login, 3, 1)
        layout_form.addWidget(self.label_last_login_value, 3, 2)
        layout_form.addWidget(label_created, 4, 1)
        layout_form.addWidget(self.label_created_value, 4, 2)
        layout_form.addWidget(label_modified, 5, 1)
        layout_form.addWidget(self.label_modified_value, 5, 2)
        groupbox_form.setLayout(layout_form)
        layout.addStretch(1)
        layout.addWidget(groupbox_form)
        layout.addStretch(1)

        self.widget_body.setLayout(layout)

    def eventFilter(self, source, event):
        if (
            event.type() == QtCore.QEvent.ActivationChange and
            source == self
        ):
            self.activated = not self.activated
            if (
                not self.activated and
                (
                    'warning' not in self.children_windows.keys() or
                    self.children_windows['warning'] is None
                )
            ):
                self.close()
                self.parent.children_windows['profile'] = None
        return super().eventFilter(source, event)

    def load_user_info(self):
        self.lineedit_username.setText(self.user['name'])
        self.lineedit_username.setStyleSheet('QLineEdit{border:None}')
        self.lineedit_username.setReadOnly(True)
        self.label_last_login_value.setText(
            str(self.user['last_login'])
        )
        self.label_created_value.setText(
            str(self.user['created'])
        )
        self.label_modified_value.setText(
            str(self.user['modified'])
        )

    def update_passwd(self):
        window_update_passwd = WindowUpdatePass(self)
        window_update_passwd.setWindowModality(2)
        self.children_windows['warning'] = window_update_passwd
        window_update_passwd.show()
