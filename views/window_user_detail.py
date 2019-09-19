from PyQt5 import QtWidgets
from PyQt5 import QtCore
from PyQt5 import QtGui

from views.window_dragable import WindowDragable
from qss.qss_setter import QSSSetter


class WindowUserDetail(WindowDragable):
    def __init__(self, parent, x, y):
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
        self.window_min_width = 392
        self.window_max_width = 392
        self.window_min_height = 370
        self.window_max_height = 370
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
        layout_form.addWidget(label_created, 2, 1)
        layout_form.addWidget(self.label_created_value, 2, 2)
        layout_form.addWidget(label_modified, 3, 1)
        layout_form.addWidget(self.label_modified_value, 3, 2)
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
        layout_form.addLayout(layout_edit_permission, 5, 1, 1, 2)
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
            if not self.activated:
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
        self.lineedit_username.setText('Bill Guo')
        self.button_save_username.setVisible(False)
        self.button_unsave_username.setVisible(False)
        self.lineedit_username.setStyleSheet('QLineEdit{border:None}')
        self.lineedit_username.setReadOnly(True)
        self.label_created_value.setText('2001-01-01 00:00:00')
        self.label_modified_value.setText('2001-01-01 00:00:00')
        self.table_permission.setEnabled(False)
        self.table_permission.setRowCount(
            len(self.parent.main_window.enviroments)
        )
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
        for row, e in enumerate(self.parent.main_window.enviroments):
            item_env = QtWidgets.QTableWidgetItem(e)
            item_env.setFlags(QtCore.Qt.ItemIsEnabled)
            combox_permission = QtWidgets.QComboBox()
            combox_permission.addItem('无权限')
            combox_permission.addItem('只读权限')
            combox_permission.addItem('读写权限')
            combox_permission.addItem('管理权限')
            self.table_permission.setItem(row, 0, item_env)
            self.table_permission.setCellWidget(row, 1, combox_permission)

    def unsave_username(self):
        self.lineedit_username.setText('Bill Guo')
        self.button_save_username.setVisible(False)
        self.button_unsave_username.setVisible(False)
        self.lineedit_username.setStyleSheet('QLineEdit{border:None}')
        self.lineedit_username.setReadOnly(True)
        self.button_reset_passwd.setVisible(True)
