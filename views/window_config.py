from PyQt5 import QtWidgets
from PyQt5 import QtCore
from PyQt5 import QtGui

from views.window_dragable import WindowDragable
from qss.qss_setter import QSSSetter


class WindowConfig(WindowDragable):
    def __init__(self, main_window):
        super().__init__()

        self.main_window = main_window

        # 设置窗口无边框
        self.setWindowFlags(
            QtCore.Qt.FramelessWindowHint
        )
        # 设置窗口背景透明
        self.setAttribute(QtCore.Qt.WA_TranslucentBackground)

        # 设置窗口大小
        self.window_min_width = 500
        self.window_max_width = 500
        self.window_min_height = 300
        self.window_max_height = 300
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

        # 窗口按钮(最小化和关闭按钮)
        layout = QtWidgets.QHBoxLayout()
        layout.setSpacing(0)
        layout.setContentsMargins(0, 0, 0, 0)

        button_min_window = QtWidgets.QPushButton()
        button_min_window.clicked.connect(self.showMinimized)
        button_min_window.setObjectName('button_min_window')
        button_min_window.setFixedSize(20, 20)
        button_close_window = QtWidgets.QPushButton()
        button_close_window.clicked.connect(self.close_window)
        button_close_window.setFixedSize(20, 20)
        button_close_window.setObjectName('button_close_window')

        layout.addStretch(30)
        layout.addWidget(button_min_window)
        layout.addStretch(1.5)
        layout.addWidget(button_close_window)
        layout.addStretch(1)
        self.widget_head.setLayout(layout)

    def set_body_widget(self):
        self.widget_body = QtWidgets.QWidget()
        self.widget_body.setMouseTracking(True)
        self.widget_body.setObjectName('body')
        self.widget_body.setFixedSize(
            self.window_min_width,
            self.window_min_height - 30
        )

        # 表单组件
        label_env = QtWidgets.QLabel('环境')
        lineedit_env = QtWidgets.QLineEdit()
        self.label_env_hint = QtWidgets.QLabel('必填字段')
        self.label_env_hint.setObjectName('hint')
        label_read_host = QtWidgets.QLabel('读库地址')
        lineedit_read_host = QtWidgets.QLineEdit()
        label_write_host = QtWidgets.QLabel('写库地址')
        lineedit_write_host = QtWidgets.QLineEdit()
        self.label_write_host_hint = QtWidgets.QLabel('必填字段')
        self.label_write_host_hint.setObjectName('hint')
        label_username = QtWidgets.QLabel('用户名')
        lineedit_username = QtWidgets.QLineEdit()
        self.label_username_hint = QtWidgets.QLabel('必填字段')
        self.label_username_hint.setObjectName('hint')
        label_passwd = QtWidgets.QLabel('密码')
        lineedit_passwd = QtWidgets.QLineEdit()
        lineedit_passwd.setEchoMode(QtWidgets.QLineEdit.Password)
        self.label_passwd_hint = QtWidgets.QLabel('密码不能为空')
        self.label_passwd_hint.setObjectName('hint')
        button_save = QtWidgets.QPushButton('测试连接并保存')
        button_save.setObjectName('save')
        button_save.setFixedSize(140, 30)
        button_save.clicked.connect(
            lambda: self.save_connection(
                lineedit_env.text(),
                lineedit_read_host.text(),
                lineedit_write_host.text(),
                lineedit_username.text(),
                lineedit_passwd.text()
            )
        )

        # 初始时提示不可见
        self.label_env_hint.setVisible(False)
        self.label_write_host_hint.setVisible(False)
        self.label_username_hint.setVisible(False)
        self.label_passwd_hint.setVisible(False)

        # 布局管理
        layout = QtWidgets.QVBoxLayout()
        groupbox_form = QtWidgets.QGroupBox()
        layout_form = QtWidgets.QGridLayout()
        #layout_form.setHorizontalSpacing(10)
        #layout_form.setVerticalSpacing(10)
        layout_form.addWidget(label_env, 1, 1)
        layout_form.addWidget(lineedit_env, 1, 2)
        layout_form.addWidget(self.label_env_hint, 1, 3)
        layout_form.addWidget(label_read_host, 2, 1)
        layout_form.addWidget(lineedit_read_host, 2, 2)
        layout_form.addWidget(label_write_host, 3, 1)
        layout_form.addWidget(lineedit_write_host, 3, 2)
        layout_form.addWidget(self.label_write_host_hint, 3, 3)
        layout_form.addWidget(label_username, 4, 1)
        layout_form.addWidget(lineedit_username, 4, 2)
        layout_form.addWidget(self.label_username_hint, 4, 3)
        layout_form.addWidget(label_passwd, 5, 1)
        layout_form.addWidget(lineedit_passwd, 5, 2)
        layout_form.addWidget(self.label_passwd_hint, 5, 3)
        groupbox_form.setLayout(layout_form)
        layout_button = QtWidgets.QHBoxLayout()
        layout_button.addStretch(1)
        layout_button.addWidget(button_save)
        layout_button.addStretch(1)
        layout_info = QtWidgets.QHBoxLayout()
        self.label_info = QtWidgets.QLabel()
        self.label_info.setObjectName('info')
        layout_info.addStretch(1)
        layout_info.addWidget(self.label_info)
        layout_info.addStretch(1)
        layout.addWidget(groupbox_form)
        layout.addLayout(layout_info)
        layout.addLayout(layout_button)

        self.widget_body.setLayout(layout)

    def close_window(self):
        self.close()
        self.main_window.children_windows['config'] = None

    def save_connection(
        self, env, read_host, write_host, user, passwd
    ):
        if not env:
            self.label_env_hint.setVisible(True)
        if not write_host:
            self.label_write_host_hint.setVisible(True)
        if not user:
            self.label_username_hint.setVisible(True)
        if not passwd:
            self.label_passwd_hint.setVisible(True)

        if env and write_host and user and passwd:
            result = 999
            try:
                result = self.main_window.kos.root.create_env(
                    self.main_window.session_id,
                    self.main_window.token,
                    env, read_host, write_host, user, passwd
                )
            except EOFError:
                # 正在尝试重新连接服务器
                pass
            if result == 0:
                self.close_window()
            elif result == 1:
                self.label_info.setText('读库连接失败!')
            elif result == 2:
                self.label_info.setText('写库连接失败!')
            elif result == 3:
                self.label_info.setText('数据库发生错误!')
            elif result == 4:
                self.label_info.setText('权限不足!')
            elif result == -1:
                # token过期
                self.setEnabled(False)
                self.main_window.login_window.show()
            elif isinstance(result, str):
                self.label_info.setText('已存在重复的环境: {}'.format(result))
            else:
                self.label_info.setText('未知错误!')
