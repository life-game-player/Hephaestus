import time

from PyQt5 import QtWidgets
from PyQt5 import QtCore

from qss.qss_setter import QSSSetter
from clio import logger
from views.window_main import WindowMain


class WindowLogin(QtWidgets.QWidget):
    def __init__(
        self, session_id, service,
        screen_width=None, screen_height=None
    ):
        super().__init__()

        self.session_id = session_id
        self.window_main = None

        # 设置窗口大小
        self.setFixedSize(400, 350)

        # 设置窗口无边框
        self.setWindowFlags(
            QtCore.Qt.FramelessWindowHint |
            QtCore.Qt.WindowStaysOnTopHint
        )

        # 设置窗口背景透明
        self.setAttribute(QtCore.Qt.WA_TranslucentBackground)

        # 设置窗口子部件
        self.set_window_buttons_widget()
        self.set_head_widget()
        self.set_body_widget()

        # 窗口组装
        self.layout_main = QtWidgets.QVBoxLayout()
        self.layout_main.addWidget(self.widget_window_buttons)
        self.layout_main.addWidget(self.widget_head)
        self.layout_main.addWidget(self.widget_body)
        self.layout_main.setSpacing(0)
        self.layout_main.setContentsMargins(0, 0, 0, 0)
        self.setLayout(self.layout_main)

        # 连接服务
        self.kos = service

        # 设置样式
        QSSSetter.set_qss(self, __file__)

    def set_window_buttons_widget(self):
        self.widget_window_buttons = QtWidgets.QWidget()
        self.widget_window_buttons.setMouseTracking(True)
        self.widget_window_buttons.setObjectName('window_buttons')
        self.widget_window_buttons.setFixedSize(400, 30)

        # 窗口按钮(最小化和关闭按钮)
        layout = QtWidgets.QHBoxLayout()
        layout.setSpacing(0)
        layout.setContentsMargins(0, 0, 0, 0)

        button_min_window = QtWidgets.QPushButton()
        button_min_window.clicked.connect(self.showMinimized)
        button_min_window.setObjectName('button_min_window')
        button_min_window.setFixedSize(20, 20)
        button_close_window = QtWidgets.QPushButton()
        button_close_window.clicked.connect(QtWidgets.qApp.quit)
        button_close_window.setFixedSize(20, 20)
        button_close_window.setObjectName('button_close_window')

        layout.addStretch(30)
        layout.addWidget(button_min_window)
        layout.addStretch(1.5)
        layout.addWidget(button_close_window)
        layout.addStretch(1)
        self.widget_window_buttons.setLayout(layout)

    def set_head_widget(self):
        self.widget_head = QtWidgets.QWidget()
        self.widget_head.setObjectName('head')
        self.widget_head.setFixedSize(400, 150)

        # 用户头像
        label_photo = QtWidgets.QLabel(self.widget_head)
        label_photo.setFixedSize(100, 100)
        label_photo.setObjectName('user_photo')

        # 布局
        widget_head_up = QtWidgets.QLabel(self.widget_head)
        widget_head_up.setObjectName('head_up')
        widget_head_up.lower()
        widget_head_down = QtWidgets.QLabel(self.widget_head)
        widget_head_down.setObjectName('head_down')
        widget_head_down.lower()
        widget_head_up.setGeometry(0, 0, 400, 100)
        widget_head_down.setGeometry(0, 100, 400, 50)
        label_photo.setGeometry(150, 50, 100, 100)

        #widget_head_up.lower()
        #widget_head_down.lower()

    def set_body_widget(self):
        self.widget_body = QtWidgets.QWidget()
        self.widget_body.setObjectName('body')
        self.widget_body.setFixedSize(400, 300 - 100 - 30)

        # 用户名、密码及登录按钮
        line_edit_account = QtWidgets.QLineEdit(self)
        line_edit_account.setObjectName('login')
        line_edit_account.setPlaceholderText('账号')
        line_edit_account.setFixedSize(280, 40)
        self.line_edit_passwd = QtWidgets.QLineEdit()
        self.line_edit_passwd.setEchoMode(QtWidgets.QLineEdit.Password)
        self.line_edit_passwd.setObjectName('login')
        self.line_edit_passwd.setFixedSize(280, 40)
        self.line_edit_passwd.setPlaceholderText('密码')
        button_login = QtWidgets.QPushButton('登录')
        button_login.setObjectName('login')
        button_login.setFixedSize(280, 30)
        button_login.clicked.connect(
            lambda: self.login(
                line_edit_account.text(), self.line_edit_passwd.text()
            )
        )
        self.label_info = QtWidgets.QLabel()
        self.label_info.setObjectName('info')

        # 布局
        layout = QtWidgets.QVBoxLayout()
        layout.setSpacing(0)
        layout.setContentsMargins(60, 0, 0, 0)
        layout.addStretch(0.5)
        layout.addWidget(line_edit_account)
        layout.addWidget(self.line_edit_passwd)
        layout.addStretch(0.9)
        layout.addWidget(self.label_info)
        layout.addStretch(1)
        layout.addWidget(button_login)
        layout.addStretch(1)

        # 测试
        line_edit_account.setText('Bill Guo')
        self.line_edit_passwd.setText('!QAZ2wsx')

        self.widget_body.setLayout(layout)

    def login(self, account, pwd):
        if self.kos:
            if not (account and pwd):
                self.label_info.setText('用户名和密码不能为空!')
            else:
                token = None
                try:
                    token, username, role = self.kos.root.login(
                        self.session_id, account, pwd
                    )
                except Exception as e:
                    self.label_info.setText('服务器连接失败!')
                    logger.error(
                        "{} occured".format(type(e).__name__),
                        exc_info=True
                    )
                    return
                if token:
                    if token == 'DISABLED':
                        self.label_info.setText('此账户已被禁用!请联系管理员!')
                    else:
                        # 登录成功
                        self.line_edit_passwd.clear()
                        self.hide()
                        if self.window_main:
                            self.window_main.renew_token(token)
                            self.window_main.refresh_env()
                            self.window_main.setEnabled(True)
                            self.window_main.set_enabled_cascade(True)
                        else:
                            self.window_main = WindowMain(
                                self.session_id, token, self.kos, self,
                                username, role
                            )
                            self.window_main.show()
                else:
                    # 登录失败
                    self.label_info.setText('用户名密码不正确!')
