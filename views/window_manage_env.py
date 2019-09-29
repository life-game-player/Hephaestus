from PyQt5 import QtWidgets
from PyQt5 import QtCore
from PyQt5 import QtGui

from views.window_dragable import WindowDragable
from views.window_env_detail import WindowEnvDetail
from views.window_warning import WindowWarning
from views.window_error import WindowError
from qss.qss_setter import QSSSetter

import re


class WindowManageEnv(WindowDragable):
    def __init__(self, main_window):
        super().__init__()

        self.main_window = main_window
        self.children_windows = dict()
        self.children_windows['env_detail'] = None

        # 设置窗口无边框
        self.setWindowFlags(
            QtCore.Qt.FramelessWindowHint
        )
        # 设置窗口背景透明
        self.setAttribute(QtCore.Qt.WA_TranslucentBackground)

        # 设置窗口大小
        self.window_min_width = 282
        self.window_max_width = 282
        self.window_min_height = 550
        self.window_max_height = 550
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
        button_search = QtWidgets.QPushButton()
        button_search.setObjectName('search_icon')
        button_search.setFixedSize(30, 30)
        button_search.setShortcut('Return')
        button_search.clicked.connect(self.search_env)
        self.lineedit_search = QtWidgets.QLineEdit()
        self.lineedit_search.setPlaceholderText('环境搜索')
        self.lineedit_search.setObjectName('search')
        self.lineedit_search.setFixedSize(self.window_min_width - 30, 30)
        self.table_envs = QtWidgets.QTableWidget()
        self.table_envs.setSelectionBehavior(
            QtWidgets.QAbstractItemView.SelectRows
        )
        self.table_envs.horizontalHeader().setHighlightSections(False)
        self.table_envs.horizontalHeader().setSectionResizeMode(
            QtWidgets.QHeaderView.Fixed
        )
        self.table_envs.setColumnCount(2)
        self.table_envs.setHorizontalHeaderLabels(['环境', '操作'])
        self.table_envs.verticalHeader().setVisible(False)
        self.table_envs.setColumnWidth(0, 200)
        self.table_envs.setColumnWidth(1, 80)
        self.table_envs.itemClicked.connect(self.show_env_detail)
        self.table_envs.setEditTriggers(QtWidgets.QTableWidget.NoEditTriggers)
        self.load_envs()

        # 布局管理
        layout = QtWidgets.QVBoxLayout()
        layout.setSpacing(0)
        layout.setContentsMargins(0, 0, 0, 0)
        layout_h = QtWidgets.QHBoxLayout()
        layout_h.setSpacing(0)
        layout_h.setContentsMargins(0, 0, 0, 0)
        layout_h.addWidget(button_search)
        layout_h.addWidget(self.lineedit_search)
        self.table_envs.setObjectName('envs')
        layout.addLayout(layout_h)
        layout.addWidget(self.table_envs)

        self.widget_body.setLayout(layout)

    def close_window(self):
        self.close()
        self.main_window.children_windows['manage_env'] = None

    def load_envs(self):
        item_font = QtGui.QFont()
        item_font.setFamily("微软雅黑")
        item_font.setPixelSize(14)

        envs = self.main_window.kos.root.get_environments(
            self.main_window.session_id,
            self.main_window.token
        )
        if isinstance(envs, list) and envs:
            self.table_envs.clearContents()
            self.table_envs.setRowCount(len(envs))
            for row, e in enumerate(envs):
                item_env_name = QtWidgets.QTableWidgetItem(e['name'])
                item_env_name.setFont(item_font)
                item_env_name.setTextAlignment(QtCore.Qt.AlignCenter)
                self.table_envs.setItem(row, 0, item_env_name)
                button_del_env = QtWidgets.QPushButton()
                button_del_env.setObjectName('del_env')
                button_del_env.setFixedSize(30, 30)
                button_del_env.clicked.connect(
                    lambda: self.del_env(e['name'])
                )
                widget_del_env = QtWidgets.QWidget()
                layout_del_env = QtWidgets.QHBoxLayout(widget_del_env)
                layout_del_env.addWidget(button_del_env)
                layout_del_env.setAlignment(QtCore.Qt.AlignCenter)
                layout_del_env.setContentsMargins(0, 0, 0, 0)
                self.table_envs.setCellWidget(row, 1, widget_del_env)
                self.table_envs.setRowHeight(row, 40)
        elif isinstance(envs, int) and envs == -1:
            self.main_window.set_enabled_cascade(False)
            self.main_window.login_window.show()

    def show_env_detail(self, item):
        curr_row = self.table_envs.currentRow()
        y = curr_row * 40 + 30 + 30 + 25
        window_pos = self.pos()
        window_env_detail = self.children_windows['env_detail']
        query_env = self.main_window.kos.root.get_environment(
            self.main_window.session_id,
            self.main_window.token,
            self.table_envs.item(curr_row, 0).text()
        )
        if isinstance(query_env, list) and query_env:
            window_env_detail = WindowEnvDetail(
                self,
                query_env[0],
                window_pos.x(), window_pos.y() + y,
                curr_row
            )
            self.children_windows['env_detail'] = window_env_detail
            window_env_detail.show()
            window_env_detail.activateWindow()
        elif isinstance(query_env, int) and query_env == -1:
            # token过期
            self.main_window.set_enabled_cascade(False)
            self.main_window.login_window.show()

    def update_envname_display(self, row, new_name):
        self.table_envs.item(row, 0).setText(new_name)

    def del_env(self, env_name):
        warning_del_env = WindowWarning(self)
        warning_del_env.set_info("确定要删除环境[{}]吗?".format(
            (env_name[:10] + '...') if len(env_name) > 10 else env_name)
        )
        is_confirmed = warning_del_env.exec()
        if is_confirmed:
            del_result = self.main_window.kos.root.delete_env(
                self.main_window.session_id,
                self.main_window.token,
                env_name
            )
            if del_result == 0:
                self.load_envs()
            elif del_result == -1:
                # token过期
                self.main_window.set_enabled_cascade(False)
                self.main_window.login_window.show()
            else:
                # 删除失败
                error_del_env = WindowError(self)
                error_del_env.set_info('环境删除失败!')
                error_del_env.exec()

    def search_env(self):
        focusing_widget = QtWidgets.QApplication.focusWidget()
        keyword = self.lineedit_search.text()
        if (
            not focusing_widget.objectName() in
            ['search', 'search_icon']
        ):
            return  # 避免快捷键的不当触发
        if keyword:
            env_search = re.compile(r'{}'.format(keyword))
            for row in range(self.table_envs.rowCount()):
                curr_env = self.table_envs.item(row, 0).text()
                if not env_search.search(curr_env):
                    self.table_envs.hideRow(row)
        else:  # 恢复默认显示
            for row in range(self.table_envs.rowCount()):
                self.table_envs.showRow(row)
