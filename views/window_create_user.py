from PyQt5 import QtWidgets
from PyQt5 import QtCore

from views.window_dragable import WindowDragable
from qss.qss_setter import QSSSetter


class WindowCreateUser(WindowDragable):
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

        label_username = QtWidgets.QLabel('用户名')
        self.lineedit_username = QtWidgets.QLineEdit()
        self.label_username_hint = QtWidgets.QLabel('必填字段')
        self.label_username_hint.setObjectName('hint')
        label_passwd = QtWidgets.QLabel('密码')
        self.lineedit_passwd = QtWidgets.QLineEdit()
        self.lineedit_passwd.setEchoMode(QtWidgets.QLineEdit.Password)
        self.label_passwd_hint = QtWidgets.QLabel('密码不能为空')
        self.label_passwd_hint.setObjectName('hint')
        label_confirm_passwd = QtWidgets.QLabel('确认密码')
        self.lineedit_confirm_passwd = QtWidgets.QLineEdit()
        self.lineedit_confirm_passwd.setEchoMode(QtWidgets.QLineEdit.Password)
        self.label_confirm_passwd_hint = QtWidgets.QLabel('两次密码输入不一致')
        self.label_confirm_passwd_hint.setObjectName('hint')
        self.table_permission = QtWidgets.QTableWidget()
        self.table_permission.setColumnCount(2)
        self.table_permission.setHorizontalHeaderLabels(['环境', '用户权限'])
        self.table_permission.setColumnWidth(0, 200)
        self.table_permission.setColumnWidth(1, 150)
        self.table_permission.horizontalHeader().setHighlightSections(False)
        self.load_table_permission()
        button_save = QtWidgets.QPushButton('创建')
        button_save.setObjectName('save')
        button_save.setFixedSize(140, 30)
        button_save.clicked.connect(self.create_user)

        # 初始时提示不可见
        self.label_username_hint.setVisible(False)
        self.label_passwd_hint.setVisible(False)
        self.label_confirm_passwd_hint.setVisible(False)

        # 布局管理
        layout = QtWidgets.QVBoxLayout()
        groupbox_form = QtWidgets.QGroupBox()
        layout_form = QtWidgets.QGridLayout()
        layout_form.addWidget(label_username, 1, 1)
        layout_form.addWidget(self.lineedit_username, 1, 2)
        layout_form.addWidget(self.label_username_hint, 1, 3)
        layout_form.addWidget(label_passwd, 2, 1)
        layout_form.addWidget(self.lineedit_passwd, 2, 2)
        layout_form.addWidget(self.label_passwd_hint, 2, 3)
        layout_form.addWidget(label_confirm_passwd, 3, 1)
        layout_form.addWidget(self.lineedit_confirm_passwd, 3, 2)
        layout_form.addWidget(self.label_confirm_passwd_hint, 3, 3)
        layout_form.addWidget(self.table_permission, 4, 1, 1, 3)
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
        self.main_window.children_windows['create_user'] = None

    def load_table_permission(self):
        self.table_permission.setRowCount(
            len(self.main_window.enviroments)
        )
        for row, e in enumerate(self.main_window.enviroments):
            item_env = QtWidgets.QTableWidgetItem(e)
            combox_permission = QtWidgets.QComboBox()
            combox_permission.addItem('无权限')
            combox_permission.addItem('只读权限')
            combox_permission.addItem('读写权限')
            combox_permission.addItem('管理权限')
            self.table_permission.setItem(row, 0, item_env)
            self.table_permission.setCellWidget(row, 1, combox_permission)

    def create_user(self):
        self.label_username_hint.setVisible(False)
        self.label_passwd_hint.setVisible(False)
        self.label_confirm_passwd_hint.setVisible(False)
        username = self.lineedit_username.text()
        passwd = self.lineedit_passwd.text()
        confirm_passwd = self.lineedit_confirm_passwd.text()
        if not username:
            self.label_username_hint.setVisible(True)
        if not passwd:
            self.label_passwd_hint.setVisible(True)
        if passwd != confirm_passwd:
            self.label_confirm_passwd_hint.setVisible(True)
            passwd = None  # 只有两次输入密码匹配时passwd才有效，否则置空

        if username and passwd:
            result = 999

            # 遍历TableWidget获取权限信息
            user_permisson = list()
            for row in range(self.table_permission.rowCount()):
                up = dict()
                up['env'] = self.table_permission.item(row, 0).text()
                up['permission'] = self.table_permission.\
                    cellWidget(row, 1).currentIndex()
                user_permisson.append(up)

            try:
                result = self.main_window.kos.root.create_user(
                    self.main_window.session_id,
                    self.main_window.token,
                    username,
                    passwd,
                    user_permisson
                )
            except EOFError:
                # 正在尝试重新连接服务器
                pass
            if result == 0:  # 成功
                self.close_window()
            elif result == 1:
                self.label_info.setText('数据库发生错误!')
            elif result == 2:
                self.label_info.setText('权限不足!')
            elif result == -1:
                # token过期
                self.main_window.set_enabled_cascade(False)
                self.main_window.login_window.show()
            elif isinstance(result, str):
                self.label_info.setText('已存在同名用户: {}'.format(result))
            else:
                self.label_info.setText('未知错误!')
