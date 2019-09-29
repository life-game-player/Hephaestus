from PyQt5 import QtWidgets
from PyQt5 import QtCore
from PyQt5 import QtGui

from views.window_dragable import WindowDragable
from views.window_warning import WindowWarning
from views.window_info import WindowInfo
from views.window_error import WindowError
from qss.qss_setter import QSSSetter


class WindowEnvDetail(WindowDragable):
    def __init__(self, parent, env, x, y, parent_row):
        super().__init__()
        self.parent = parent
        self.row = parent_row
        self.children_windows = dict()
        self.env = env

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
        self.window_min_height = 240
        self.window_max_height = 300
        self.setMinimumSize(self.window_min_width, self.window_min_height)
        self.setMaximumSize(self.window_max_width, self.window_max_height)

        # 设置窗口子部件
        self.set_body_widget()

        # 窗口组装
        self.layout_main = QtWidgets.QVBoxLayout()
        self.layout_main.addWidget(self.widget_body)
        self.layout_main.setSpacing(5)
        self.layout_main.setContentsMargins(0, 0, 0, 0)
        self.setLayout(self.layout_main)

        self.setGeometry(
            x - self.window_min_width,
            y,
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
        label_envname = QtWidgets.QLabel('环境')
        label_envname.setObjectName('title')
        self.lineedit_envname = QtWidgets.QLineEdit()
        self.lineedit_envname.setFixedWidth(160)
        self.lineedit_envname.installEventFilter(self)
        self.button_save_envname = QtWidgets.QPushButton()
        self.button_save_envname.setFixedSize(24, 24)
        self.button_save_envname.setObjectName('save_envname')
        self.button_save_envname.clicked.connect(self.save_envname)
        self.button_unsave_envname = QtWidgets.QPushButton()
        self.button_unsave_envname.setFixedSize(24, 24)
        self.button_unsave_envname.setObjectName('unsave_envname')
        self.button_unsave_envname.clicked.connect(self.unsave_envname)
        label_read_host = QtWidgets.QLabel('读库地址')
        label_read_host.setObjectName('title')
        self.lineedit_read_host = QtWidgets.QLineEdit()
        self.lineedit_read_host.setFixedSize(240, 24)
        self.lineedit_read_host.installEventFilter(self)
        label_write_host = QtWidgets.QLabel('写库地址')
        label_write_host.setObjectName('title')
        self.lineedit_write_host = QtWidgets.QLineEdit()
        self.lineedit_write_host.setFixedSize(240, 24)
        self.lineedit_write_host.installEventFilter(self)
        self.label_write_host_hint = QtWidgets.QLabel('必填字段')
        self.label_write_host_hint.setObjectName('hint')
        label_username = QtWidgets.QLabel('用户名')
        label_username.setObjectName('title')
        self.lineedit_username = QtWidgets.QLineEdit()
        self.lineedit_username.setFixedSize(240, 24)
        self.lineedit_username.installEventFilter(self)
        self.label_username_hint = QtWidgets.QLabel('必填字段')
        self.label_username_hint.setObjectName('hint')
        label_passwd = QtWidgets.QLabel('密码')
        label_passwd.setObjectName('title')
        self.lineedit_passwd = QtWidgets.QLineEdit()
        self.lineedit_passwd.setFixedSize(240, 24)
        self.lineedit_passwd.setEchoMode(QtWidgets.QLineEdit.Password)
        self.lineedit_passwd.installEventFilter(self)
        self.label_passwd_hint = QtWidgets.QLabel('密码不能为空')
        self.label_passwd_hint.setObjectName('hint')
        self.button_save_env = QtWidgets.QPushButton('测试连接并保存')
        self.button_save_env.setObjectName('bottom')
        self.button_save_env.setFixedSize(150, 35)
        self.button_save_env.clicked.connect(self.save_env)
        self.button_unsave_env = QtWidgets.QPushButton('取消')
        self.button_unsave_env.setObjectName('bottom')
        self.button_unsave_env.setFixedSize(100, 35)
        self.button_unsave_env.clicked.connect(self.unsave_env)
        self.label_info = QtWidgets.QLabel()
        self.label_info.setObjectName('info')
        self.load_env_info()

        # 布局管理
        layout = QtWidgets.QVBoxLayout()
        groupbox_form = QtWidgets.QGroupBox()
        layout_form = QtWidgets.QGridLayout()
        layout_form.setSpacing(10)
        layout_envname = QtWidgets.QHBoxLayout()
        layout_form.addWidget(label_envname, 1, 1)
        layout_envname.addWidget(self.lineedit_envname)
        layout_envname.addWidget(self.button_save_envname)
        layout_envname.addWidget(self.button_unsave_envname)
        layout_envname.addStretch(1)
        layout_form.addLayout(layout_envname, 1, 2)
        layout_form.addWidget(label_read_host, 2, 1)
        layout_form.addWidget(self.lineedit_read_host, 2, 2)
        layout_form.addWidget(label_write_host, 3, 1)
        layout_write_host = QtWidgets.QHBoxLayout()
        layout_write_host.addWidget(self.lineedit_write_host)
        layout_write_host.addWidget(self.label_write_host_hint)
        layout_write_host.addStretch()
        layout_form.addLayout(layout_write_host, 3, 2)
        layout_form.addWidget(label_username, 4, 1)
        layout_username = QtWidgets.QHBoxLayout()
        layout_username.addWidget(self.lineedit_username)
        layout_username.addWidget(self.label_username_hint)
        layout_username.addStretch()
        layout_form.addLayout(layout_username, 4, 2)
        layout_form.addWidget(label_passwd, 5, 1)
        layout_passwd = QtWidgets.QHBoxLayout()
        layout_passwd.addWidget(self.lineedit_passwd)
        layout_passwd.addWidget(self.label_passwd_hint)
        layout_passwd.addStretch()
        layout_form.addLayout(layout_passwd, 5, 2)
        groupbox_form.setLayout(layout_form)
        layout.addStretch(1)
        layout.addWidget(groupbox_form)
        layout_info = QtWidgets.QHBoxLayout()
        layout_info.addStretch(1)
        layout_info.addWidget(self.label_info)
        layout_info.addStretch(1)
        layout.addLayout(layout_info)
        layout_buttons = QtWidgets.QHBoxLayout()
        layout_buttons.addStretch(1)
        layout_buttons.addWidget(self.button_save_env)
        layout_buttons.addWidget(self.button_unsave_env)
        layout_buttons.addStretch(1)
        layout.addLayout(layout_buttons)
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
                self.parent.children_windows['env_detail'] = None

        if (
            event.type() == QtCore.QEvent.MouseButtonDblClick and
            isinstance(source, QtWidgets.QLineEdit)
        ):
            source.setReadOnly(False)
            source.setStyleSheet(
                "QLineEdit{"
                "border:2px solid rgb(255,102,51)"
                "}"
            )
            if source == self.lineedit_envname:
                self.button_save_envname.setVisible(True)
                self.button_unsave_envname.setVisible(True)
            else:
                self.button_save_env.setVisible(True)
                self.button_unsave_env.setVisible(True)

        if (
            event.type() == QtCore.QEvent.FocusOut and
            source == self.lineedit_envname
        ):
            focusing_widget = QtWidgets.QApplication.focusWidget()
            if focusing_widget != self.button_save_envname:
                self.unsave_envname()
        return super().eventFilter(source, event)

    def load_env_info(self):
        self.label_write_host_hint.setVisible(False)
        self.label_username_hint.setVisible(False)
        self.label_passwd_hint.setVisible(False)
        self.lineedit_envname.setStyleSheet('QLineEdit{border:None}')
        self.lineedit_envname.setText(self.env['name'])
        self.lineedit_read_host.setStyleSheet('QLineEdit{border:None}')
        self.lineedit_read_host.setText(self.env['read_host'])
        self.lineedit_write_host.setStyleSheet('QLineEdit{border:None}')
        self.lineedit_write_host.setText(self.env['write_host'])
        self.lineedit_username.setStyleSheet('QLineEdit{border:None}')
        self.lineedit_username.setText(self.env['user'])
        self.lineedit_passwd.setStyleSheet('QLineEdit{border:None}')
        self.lineedit_passwd.setText(self.env['passwd'])
        self.label_info.setText('')

        # 设置初始状态
        self.lineedit_envname.setCursorPosition(0)
        self.lineedit_read_host.setCursorPosition(0)
        self.lineedit_write_host.setCursorPosition(0)
        self.lineedit_username.setCursorPosition(0)
        self.lineedit_passwd.setCursorPosition(0)
        self.lineedit_envname.setReadOnly(True)
        self.lineedit_read_host.setReadOnly(True)
        self.lineedit_write_host.setReadOnly(True)
        self.lineedit_username.setReadOnly(True)
        self.lineedit_passwd.setReadOnly(True)
        self.button_save_envname.setVisible(False)
        self.button_unsave_envname.setVisible(False)
        self.button_save_env.setVisible(False)
        self.button_unsave_env.setVisible(False)

    def save_envname(self):
        new_envname = self.lineedit_envname.text()
        if (
            new_envname != '<刷新环境配置......>' and
            new_envname and
            new_envname != self.env['name']
        ):
            update_result = self.parent.main_window.kos.root.update_env_name(
                self.parent.main_window.session_id,
                self.parent.main_window.token,
                self.env['name'],
                new_envname
            )
            if update_result:
                if update_result == -1:
                    # token失效
                    self.parent.main_window.set_enabled_cascade(False)
                    self.parent.main_window.login_window.show()
                else:
                    error_rename_env = WindowError(self)
                    error_rename_env.set_info('修改环境失败!')
                    self.children_windows['warning'] = error_rename_env
                    error_rename_env.exec()
                    self.children_windows['warning'] = None
            else:
                # 修改成功
                self.parent.update_envname_display(self.row, new_envname)
                self.unsave_envname()  # # 恢复只读状态
                self.lineedit_envname.setText(new_envname)
                self.env['name'] = new_envname

    def unsave_envname(self):
        self.lineedit_envname.setText(self.env['name'])
        self.button_save_envname.setVisible(False)
        self.button_unsave_envname.setVisible(False)
        self.lineedit_envname.setStyleSheet('QLineEdit{border:None}')
        self.lineedit_envname.setReadOnly(True)
        self.lineedit_read_host.setCursorPosition(0)

    def unsave_env(self):
        self.load_env_info()

    def save_env(self):
        is_form_valid = True
        self.label_write_host_hint.setVisible(False)
        self.label_username_hint.setVisible(False)
        self.label_passwd_hint.setVisible(False)
        write_host = self.lineedit_write_host.text()
        read_host = self.lineedit_read_host.text()
        user = self.lineedit_username.text()
        passwd = self.lineedit_passwd.text()
        if not write_host:
            self.label_write_host_hint.setVisible(True)
            is_form_valid = False
        if not user:
            self.label_username_hint.setVisible(True)
            is_form_valid = False
        if not passwd:
            self.label_passwd_hint.setVisible(True)
            is_form_valid = False

        if is_form_valid:
            result = 999
            try:
                result = self.parent.main_window.kos.root.update_env(
                    self.parent.main_window.session_id,
                    self.parent.main_window.token,
                    self.env['name'], read_host, write_host, user, passwd
                )
            except EOFError:
                # 正在尝试重新连接服务器
                pass
            if result == 0:
                self.close()
                self.parent.children_windows['env_detail'] = None
            elif result == 1:
                self.label_info.setText('读库或写库连接失败!')
            elif result == 2:
                self.label_info.setText('读库和写库均连接失败!')
            elif result == 3:
                self.label_info.setText('数据库发生错误!')
            elif result == 4:
                self.label_info.setText('权限不足!')
            elif result == -1:
                # token过期
                self.parent.main_window.set_enabled_cascade(False)
                self.parent.main_window.login_window.show()
            elif isinstance(result, str):
                self.label_info.setText('已存在重复的环境: {}'.format(result))
            else:
                self.label_info.setText('未知错误!')
