from PyQt5 import QtWidgets
from PyQt5 import QtCore

from views.window_dragable import WindowDragable
from qss.qss_setter import QSSSetter


class WindowUpdatePass(WindowDragable):
    def __init__(self, parent):
        super().__init__()

        self.parent = parent

        # 设置窗口无边框
        self.setWindowFlags(
            QtCore.Qt.FramelessWindowHint
        )
        # 设置窗口背景透明
        self.setAttribute(QtCore.Qt.WA_TranslucentBackground)

        # 设置窗口大小
        self.window_min_width = 390
        self.window_max_width = 390
        self.window_min_height = 165
        self.window_max_height = 165
        self.setMinimumSize(self.window_min_width, self.window_min_height)
        self.setMaximumSize(self.window_max_width, self.window_max_height)

        # 设置窗口图标
        self.setWindowIcon(self.parent.main_window.icon)

        # 设置窗口子部件
        self.set_body_widget()

        # 窗口组装
        self.layout_main = QtWidgets.QVBoxLayout()
        self.layout_main.addWidget(self.widget_body)
        self.layout_main.setSpacing(0)
        self.layout_main.setContentsMargins(0, 0, 0, 0)
        self.setLayout(self.layout_main)

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

        label_passwd = QtWidgets.QLabel('新密码')
        self.lineedit_passwd = QtWidgets.QLineEdit()
        self.lineedit_passwd.setEchoMode(QtWidgets.QLineEdit.Password)
        self.label_passwd_hint = QtWidgets.QLabel('密码不能为空')
        self.label_passwd_hint.setObjectName('hint')
        label_confirm_passwd = QtWidgets.QLabel('确认密码')
        self.lineedit_confirm_passwd = QtWidgets.QLineEdit()
        self.lineedit_confirm_passwd.setEchoMode(QtWidgets.QLineEdit.Password)
        self.label_confirm_passwd_hint = QtWidgets.QLabel('两次密码输入不一致')
        self.label_confirm_passwd_hint.setObjectName('hint')
        self.label_info = QtWidgets.QLabel('密码修改失败!')
        self.label_info.setObjectName('hint')
        button_save = QtWidgets.QPushButton('修改')
        button_save.setObjectName('save')
        button_save.setFixedSize(100, 30)
        button_save.clicked.connect(self.update_passwd)
        button_cancel = QtWidgets.QPushButton('取消')
        button_cancel.setObjectName('cancel')
        button_cancel.setFixedSize(100, 30)
        button_cancel.clicked.connect(self.close_window)

        # 初始时提示不可见
        self.label_passwd_hint.setVisible(False)
        self.label_confirm_passwd_hint.setVisible(False)
        self.label_info.setVisible(False)

        # 布局管理
        layout = QtWidgets.QVBoxLayout()
        groupbox_form = QtWidgets.QGroupBox()
        layout_form = QtWidgets.QGridLayout()
        layout_form.addWidget(label_passwd, 2, 1)
        layout_form.addWidget(self.lineedit_passwd, 2, 2)
        layout_form.addWidget(self.label_passwd_hint, 2, 3)
        layout_form.addWidget(label_confirm_passwd, 3, 1)
        layout_form.addWidget(self.lineedit_confirm_passwd, 3, 2)
        layout_form.addWidget(self.label_confirm_passwd_hint, 3, 3)
        groupbox_form.setLayout(layout_form)
        layout_info = QtWidgets.QHBoxLayout()
        layout_info.addStretch(1)
        layout_info.addWidget(self.label_info)
        layout_info.addStretch(1)
        layout_button = QtWidgets.QHBoxLayout()
        layout_button.addStretch(1)
        layout_button.addWidget(button_save)
        layout_button.addWidget(button_cancel)
        layout_button.addStretch(1)
        layout.addWidget(groupbox_form)
        layout.addLayout(layout_info)
        layout.addLayout(layout_button)

        self.widget_body.setLayout(layout)

    def update_passwd(self):
        self.label_passwd_hint.setVisible(False)
        self.label_confirm_passwd_hint.setVisible(False)
        self.label_info.setVisible(False)
        passwd = self.lineedit_passwd.text()
        confirm_passwd = self.lineedit_confirm_passwd.text()
        if not passwd:
            self.label_passwd_hint.setVisible(True)
        if passwd != confirm_passwd:
            self.label_confirm_passwd_hint.setVisible(True)
            passwd = None  # 只有两次输入密码匹配时passwd才有效，否则置空，后面有判断

        if passwd:
            result = self.parent.parent.kos.root.update_own_passwd(
                self.parent.parent.session_id,
                self.parent.parent.token,
                passwd
            )
            if result == 0:
                self.close_window()
            elif result == -1:
                # token过期
                self.parent.parent.set_enabled_cascade(False)
                self.parent.parent.login_window.setWindowModality(2)
                self.parent.parent.login_window.show()
            else:
                # 报错
                self.label_info.setVisible(True)

    def close_window(self):
        self.parent.children_windows['warning'] = None
        self.close()
