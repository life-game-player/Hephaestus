from PyQt5 import QtWidgets
from PyQt5 import QtCore
from PyQt5 import QtGui

from views.window_dragable import WindowDragable
from views.window_user_detail import WindowUserDetail
from qss.qss_setter import QSSSetter


class WindowManageUser(WindowDragable):
    def __init__(self, main_window):
        super().__init__()

        self.main_window = main_window
        self.children_windows = dict()
        self.children_windows['user_detail'] = None

        # 设置窗口无边框
        self.setWindowFlags(
            QtCore.Qt.FramelessWindowHint
        )
        # 设置窗口背景透明
        self.setAttribute(QtCore.Qt.WA_TranslucentBackground)

        # 设置窗口大小
        self.window_min_width = 302
        self.window_max_width = 302
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
        lineedit_search = QtWidgets.QLineEdit()
        lineedit_search.setPlaceholderText('用户搜索')
        lineedit_search.setObjectName('search')
        lineedit_search.setFixedSize(self.window_min_width - 30, 30)
        self.table_users = QtWidgets.QTableWidget()
        self.table_users.setSelectionBehavior(
            QtWidgets.QAbstractItemView.SelectRows
        )
        self.table_users.horizontalHeader().setHighlightSections(False)
        self.table_users.horizontalHeader().setSectionResizeMode(
            QtWidgets.QHeaderView.Fixed
        )
        self.table_users.setColumnCount(3)
        self.table_users.setHorizontalHeaderLabels(['ID', '用户', '操作'])
        self.table_users.verticalHeader().setVisible(False)
        self.table_users.setColumnWidth(0, 50)
        self.table_users.setColumnWidth(1, 200)
        self.table_users.setColumnWidth(2, 50)
        self.table_users.itemClicked.connect(self.show_user_detail)
        self.table_users.setEditTriggers(QtWidgets.QTableWidget.NoEditTriggers)
        self.load_users()

        # 布局管理
        layout = QtWidgets.QVBoxLayout()
        layout.setSpacing(0)
        layout.setContentsMargins(0, 0, 0, 0)
        layout_h = QtWidgets.QHBoxLayout()
        layout_h.setSpacing(0)
        layout_h.setContentsMargins(0, 0, 0, 0)
        layout_h.addWidget(button_search)
        layout_h.addWidget(lineedit_search)
        self.table_users.setObjectName('users')
        layout.addLayout(layout_h)
        layout.addWidget(self.table_users)

        self.widget_body.setLayout(layout)

    def close_window(self):
        self.close()
        self.main_window.children_windows['manage_user'] = None

    def load_users(self):
        item_font = QtGui.QFont()
        item_font.setFamily("微软雅黑")
        item_font.setPixelSize(14)

        users = self.main_window.kos.root.get_users(
            self.main_window.session_id,
            self.main_window.token
        )
        if isinstance(users, list) and users:
            self.table_users.setRowCount(len(users))
            for row, u in enumerate(users):
                item_user_id = QtWidgets.QTableWidgetItem(str(u['id']))
                item_user_id.setFont(item_font)
                item_user_name = QtWidgets.QTableWidgetItem(u['name'])
                item_user_name.setFont(item_font)
                self.table_users.setItem(row, 0, item_user_id)
                self.table_users.setItem(row, 1, item_user_name)
                if not int.from_bytes(u['dominated'], 'big'):
                    button_del_user = QtWidgets.QPushButton()
                    button_del_user.setObjectName('del_user')
                    button_del_user.setFixedSize(30, 30)
                    widget_del_user = QtWidgets.QWidget()
                    layout_del_user = QtWidgets.QHBoxLayout(widget_del_user)
                    layout_del_user.addWidget(button_del_user)
                    layout_del_user.setAlignment(QtCore.Qt.AlignCenter)
                    layout_del_user.setContentsMargins(0, 0, 0, 0)
                    self.table_users.setCellWidget(row, 2, widget_del_user)
                self.table_users.setRowHeight(row, 40)
        elif isinstance(users, int) and users == -1:
            self.setEnabled(False)
            self.main_window.login_window.show()

    def show_user_detail(self, item):
        y = self.table_users.currentRow() * 40 + 30 + 30 + 25
        window_pos = self.pos()
        window_user_detail = self.children_windows['user_detail']
        if not window_user_detail:
            window_user_detail = WindowUserDetail(
                self, window_pos.x(), window_pos.y() + y
            )
            self.children_windows['user_detail'] = window_user_detail
        window_user_detail.show()
        window_user_detail.activateWindow()
