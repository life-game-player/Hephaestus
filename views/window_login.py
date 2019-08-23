from views.window_main import WindowMain

from PyQt5 import QtWidgets
from PyQt5 import QtCore
import rpyc

from qss.qss_setter import QSSSetter

import logging
import logging.handlers


class WindowLogin(QtWidgets.QWidget):
    def __init__(self, session_id, screen_width, screen_height):
        super().__init__()

        self.session_id = session_id

        # 日志设置
        logging_handler = logging.handlers.RotatingFileHandler(
            'logs/login.log',
            'a',
            1024 * 1024,
            10,
            'utf-8'
        )
        logging_format = logging.Formatter(
            '%(asctime)s [%(name)s - %(levelname)s] %(message)s'
        )
        logging_handler.setFormatter(logging_format)
        logger = logging.getLogger()
        logger.addHandler(logging_handler)
        logger.setLevel(logging.DEBUG)

        # 设置窗口大小
        self.setFixedSize(400, 300)

        # 设置窗口无边框
        self.setWindowFlags(
            QtCore.Qt.FramelessWindowHint
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
        self.kos = None
        try:
            self.kos = rpyc.connect("localhost", 18861)
        except Exception as e:
            self.label_info.setText('服务器连接失败!')
            logging.error(
                "{} occured".format(type(e).__name__),
                exc_info=True
            )

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
        self.widget_head.setFixedSize(400, 100)

        # 用户头像
        label_photo = QtWidgets.QLabel()
        label_photo.setFixedSize(100, 100)
        label_photo.setObjectName('user_photo')

        # 布局
        layout = QtWidgets.QVBoxLayout()
        layout.setSpacing(0)
        layout.setContentsMargins(160, 0, 0, 0)
        layout.addStretch(1)
        layout.addWidget(label_photo)

        self.widget_head.setLayout(layout)

    def set_body_widget(self):
        self.widget_body = QtWidgets.QWidget()
        self.widget_body.setObjectName('body')
        self.widget_body.setFixedSize(400, 300 - 100 - 30)

        # 用户名、密码及登录按钮
        line_edit_account = QtWidgets.QLineEdit(self)
        line_edit_account.setObjectName('login')
        line_edit_account.setPlaceholderText('账号')
        line_edit_account.setFixedSize(280, 40)
        line_edit_passwd = QtWidgets.QLineEdit()
        line_edit_passwd.setEchoMode(QtWidgets.QLineEdit.Password)
        line_edit_passwd.setObjectName('login')
        line_edit_passwd.setFixedSize(280, 40)
        line_edit_passwd.setPlaceholderText('密码')
        button_login = QtWidgets.QPushButton('登录')
        button_login.setObjectName('login')
        button_login.setFixedSize(280, 30)
        button_login.clicked.connect(
            lambda: self.login(
                line_edit_account.text(), line_edit_passwd.text()
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
        layout.addWidget(line_edit_passwd)
        layout.addStretch(0.9)
        layout.addWidget(self.label_info)
        layout.addStretch(1)
        layout.addWidget(button_login)
        layout.addStretch(1)

        self.widget_body.setLayout(layout)

    def login(self, account, pwd):
        if self.kos:
            if not (account and pwd):
                self.label_info.setText('用户名和密码不能为空!')
            else:
                token = self.kos.root.login(self.session_id, account, pwd)
                if token:
                    # 登录成功
                    self.close()
                    window_main = WindowMain(self.session_id, token)
                    window_main.show()
                else:
                    # 登录失败
                    self.label_info.setText('用户名密码不正确!')
