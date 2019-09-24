from PyQt5 import QtWidgets
from PyQt5 import QtCore
from PyQt5 import QtGui

from views.window_dragable import WindowDragable
from views.window_warning import WindowWarning
from qss.qss_setter import QSSSetter


class WindowUserDetail(WindowDragable):
    def __init__(self, parent, user, x, y):
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
        if int.from_bytes(self.user['dominated'], 'big') == 0:
            self.window_min_height = 410
            self.window_max_height = 410
        else:
            self.window_min_height = 205
            self.window_max_height = 205
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
        label_username = QtWidgets.QLabel('用户名')
        label_username.setObjectName('title')
        self.lineedit_username = QtWidgets.QLineEdit()
        self.lineedit_username.setFixedWidth(160)
        self.lineedit_username.installEventFilter(self)
        self.button_save_username = QtWidgets.QPushButton()
        self.button_save_username.setFixedSize(24, 24)
        self.button_save_username.setObjectName('save_username')
        self.button_unsave_username = QtWidgets.QPushButton()
        self.button_unsave_username.setFixedSize(24, 24)
        self.button_unsave_username.setObjectName('unsave_username')
        self.button_unsave_username.clicked.connect(self.unsave_username)
        self.button_reset_passwd = QtWidgets.QPushButton('重置密码')
        self.button_reset_passwd.setFixedSize(70, 30)
        self.button_reset_passwd.setObjectName('reset')
        label_status = QtWidgets.QLabel('用户状态')
        self.label_status_value = QtWidgets.QLabel()
        self.label_status_value.setObjectName('value')
        label_last_login = QtWidgets.QLabel('上次登录时间')
        self.label_last_login_value = QtWidgets.QLabel()
        self.label_last_login_value.setObjectName('value')
        self.button_lock_user = QtWidgets.QPushButton()
        self.button_lock_user.setObjectName('lock')
        self.button_lock_user.clicked.connect(self.lock_user)
        self.button_unlock_user = QtWidgets.QPushButton()
        self.button_unlock_user.setObjectName('unlock')
        self.button_unlock_user.clicked.connect(self.unlock_user)
        self.button_lock_user.setFixedSize(24, 24)
        self.button_unlock_user.setFixedSize(24, 24)
        label_created = QtWidgets.QLabel('创建时间')
        label_created.setObjectName('title')
        self.label_created_value = QtWidgets.QLabel()
        self.label_created_value.setObjectName('value')
        label_modified = QtWidgets.QLabel('修改时间')
        label_modified.setObjectName('title')
        self.label_modified_value = QtWidgets.QLabel()
        self.label_modified_value.setObjectName('value')
        self.table_permission = QtWidgets.QTableWidget()
        self.table_permission.setColumnCount(2)
        self.table_permission.setHorizontalHeaderLabels(['环境', '用户权限'])
        self.table_permission.setColumnWidth(0, 200)
        self.table_permission.setColumnWidth(1, 150)
        self.table_permission.horizontalHeader().setHighlightSections(False)
        self.table_permission.setFixedSize(352, 180)
        self.load_user_info()
        self.button_edit_permission = QtWidgets.QPushButton()
        self.button_edit_permission.setFixedSize(30, 30)
        self.button_edit_permission.setObjectName('permission')
        self.button_edit_permission.clicked.connect(self.edit_permission)
        self.button_confirm_edit = QtWidgets.QPushButton()
        self.button_confirm_edit.setFixedSize(30, 30)
        self.button_confirm_edit.setObjectName('confirm')
        self.button_confirm_edit.clicked.connect(self.update_permission)
        self.button_cancel_edit = QtWidgets.QPushButton()
        self.button_cancel_edit.setFixedSize(30, 30)
        self.button_cancel_edit.setObjectName('cancel')
        self.button_confirm_edit.setVisible(False)
        self.button_cancel_edit.setVisible(False)
        self.button_cancel_edit.clicked.connect(self.cancel_edit)

        # 布局管理
        layout = QtWidgets.QVBoxLayout()
        groupbox_form = QtWidgets.QGroupBox()
        layout_form = QtWidgets.QGridLayout()
        layout_form.setSpacing(10)
        layout_username = QtWidgets.QHBoxLayout()
        layout_form.addWidget(label_username, 1, 1)
        layout_username.addWidget(self.lineedit_username)
        layout_username.addWidget(self.button_save_username)
        layout_username.addWidget(self.button_unsave_username)
        layout_username.addWidget(self.button_reset_passwd)
        layout_username.addStretch(1)
        layout_form.addLayout(layout_username, 1, 2)
        layout_form.addWidget(label_status, 2, 1)
        layout_userstatus = QtWidgets.QHBoxLayout()
        layout_userstatus.addWidget(self.label_status_value)
        layout_userstatus.addWidget(self.button_lock_user)
        layout_userstatus.addWidget(self.button_unlock_user)
        layout_userstatus.addStretch()
        layout_form.addLayout(layout_userstatus, 2, 2)
        layout_form.addWidget(label_last_login, 3, 1)
        layout_form.addWidget(self.label_last_login_value, 3, 2)
        layout_form.addWidget(label_created, 4, 1)
        layout_form.addWidget(self.label_created_value, 4, 2)
        layout_form.addWidget(label_modified, 5, 1)
        layout_form.addWidget(self.label_modified_value, 5, 2)
        layout_edit_permission = QtWidgets.QVBoxLayout()
        layout_edit_permission.setSpacing(0)
        layout_edit_permission.setContentsMargins(0, 0, 0, 0)
        layout_edit_button = QtWidgets.QHBoxLayout()
        layout_edit_button.addStretch(100)
        layout_edit_button.addWidget(self.button_confirm_edit)
        layout_edit_button.addStretch(3)
        layout_edit_button.addWidget(self.button_cancel_edit)
        layout_edit_button.addWidget(self.button_edit_permission)
        layout_edit_permission.addLayout(layout_edit_button)
        layout_edit_permission.addWidget(self.table_permission)
        if int.from_bytes(self.user['dominated'], 'big') == 0:
            layout_form.addLayout(layout_edit_permission, 6, 1, 1, 2)
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
                self.parent.children_windows['user_detail'] = None

        if (
            event.type() == QtCore.QEvent.MouseButtonDblClick and
            source == self.lineedit_username
        ):
            self.lineedit_username.setReadOnly(False)
            self.lineedit_username.setStyleSheet(
                "QLineEdit{"
                "border:1px solid rgb(175,222,255)"
                "}"
            )
            self.button_save_username.setVisible(True)
            self.button_unsave_username.setVisible(True)
            self.button_reset_passwd.setVisible(False)

        if (
            event.type() == QtCore.QEvent.FocusOut and
            source == self.lineedit_username
        ):
            self.unsave_username()
        return super().eventFilter(source, event)

    def load_user_info(self):
        self.lineedit_username.setText(self.user['name'])
        self.load_user_status(self.user['status'])
        self.button_save_username.setVisible(False)
        self.button_unsave_username.setVisible(False)
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
        self.table_permission.setEnabled(False)
        self.table_permission.setRowCount(
            len(self.parent.main_window.enviroments)
        )
        if int.from_bytes(self.user['dominated'], 'big') == 0:
            self.load_permission_table()

    def edit_permission(self):
        # 只读->编辑
        self.table_permission.setEnabled(True)
        self.button_edit_permission.setVisible(False)
        self.button_confirm_edit.setVisible(True)
        self.button_cancel_edit.setVisible(True)

    def cancel_edit(self):
        self.table_permission.setEnabled(False)
        self.load_permission_table()
        self.button_confirm_edit.setVisible(False)
        self.button_cancel_edit.setVisible(False)
        self.button_edit_permission.setVisible(True)
        self.lineedit_username.setSelection(0, 0)

    def load_permission_table(self):
        self.table_permission.clearContents()
        permission_results = self.parent.main_window.kos.root.\
            get_permission_by_user(
                self.parent.main_window.session_id,
                self.parent.main_window.token,
                self.user['id']
            )
        if (
            isinstance(permission_results, list) or
            isinstance(permission_results, tuple)
        ):
            for row, e in enumerate(self.parent.main_window.enviroments):
                item_env = QtWidgets.QTableWidgetItem(e)
                item_env.setFlags(QtCore.Qt.ItemIsEnabled)
                combox_permission = QtWidgets.QComboBox()
                combox_permission.addItem('无权限')
                combox_permission.addItem('只读权限')
                combox_permission.addItem('读写权限')
                combox_permission.addItem('管理权限')
                if permission_results:
                    for p in permission_results:
                        if e == p['island_name']:
                            combox_permission.setCurrentIndex(
                                p['access_level']
                            )
                            break
                    else:
                        combox_permission.setCurrentIndex(0)
                else:
                    combox_permission.setCurrentIndex(0)
                self.table_permission.setItem(row, 0, item_env)
                self.table_permission.setCellWidget(row, 1, combox_permission)
        elif isinstance(permission_results, int) and permission_results == -1:
            # token过期
            self.parent.main_window.set_enabled_cascade(False)
            self.parent.main_window.login_window.show()

    def unsave_username(self):
        self.lineedit_username.setText(self.user['name'])
        self.button_save_username.setVisible(False)
        self.button_unsave_username.setVisible(False)
        self.lineedit_username.setStyleSheet('QLineEdit{border:None}')
        self.lineedit_username.setReadOnly(True)
        self.button_reset_passwd.setVisible(True)

    def lock_user(self):
        self.update_user_status(1)

    def unlock_user(self):
        self.update_user_status(0)

    def update_user_status(self, user_status):
        display_user = (self.user['name'][:10] + '...')\
            if len(self.user['name']) > 10 else self.user['name']
        warning_update_user_status = WindowWarning(self)
        warning_update_user_status.set_info(
            "确定要{}用户[{}]吗?".format(
                '禁用' if user_status else '启用',
                display_user
            )
        )
        self.children_windows['warning'] = warning_update_user_status
        is_update_confirmed = warning_update_user_status.exec()
        self.children_windows['warning'] = None
        if is_update_confirmed:
            result = self.parent.main_window.kos.root.update_user_status(
                self.parent.main_window.session_id,
                self.parent.main_window.token,
                user_status,
                self.user['id']
            )
            if result:
                if result == -1:
                    # token失效
                    self.parent.main_window.set_enabled_cascade(False)
                    self.parent.main_window.login_window.show()
            else:
                self.load_user_status(user_status)

    def load_user_status(self, user_status):
        if user_status:
            # 禁用
            self.label_status_value.setStyleSheet(
                "QLabel{background-color:rgba(255,0,0,50%);"
                "border-radius:2px;}"
            )
        else:
            # 启用
            self.label_status_value.setStyleSheet(
                "QLabel{background-color:rgba(51,204,0,50%);"
                "border-radius:2px;}"
            )
        self.label_status_value.setText('已锁定' if user_status else '正常')
        self.button_unlock_user.setVisible(True if user_status else False)
        self.button_lock_user.setVisible(False if user_status else True)

    def update_permission(self):
        # 遍历TableWidget获取权限信息
        user_permisson = list()
        for row in range(self.table_permission.rowCount()):
            up = dict()
            up['env'] = self.table_permission.item(row, 0).text()
            up['permission'] = self.table_permission.\
                cellWidget(row, 1).currentIndex()
            user_permisson.append(up)

        result = self.parent.main_window.kos.root.update_permission_by_user(
            self.parent.main_window.session_id,
            self.parent.main_window.token,
            user_permisson,
            self.user['id']
        )
        self.cancel_edit()  # 刷新权限表并取消编辑状态
        print(result)
        if result and result == -1:
            # token失效
            self.parent.main_window.set_enabled_cascade(False)
            self.parent.main_window.login_window.show()
