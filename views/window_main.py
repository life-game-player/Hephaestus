from PyQt5 import QtWidgets
from PyQt5 import QtCore
from PyQt5 import QtGui
from PyQt5.QtGui import QCursor
import rpyc

from qss.qss_setter import QSSSetter

import logging
import logging.handlers


class WindowMain(QtWidgets.QWidget):
    def __init__(self, session_id, token, service):
        super().__init__()

        self.session_id = session_id

        # 日志设置
        logging_handler = logging.handlers.RotatingFileHandler(
            'logs/main.log',
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

        # 连接服务
        self.kos = service

        # 公用标记
        self.tab = 'tenants'

        # 设置窗口大小
        self.window_min_width = 384
        self.window_max_width = 384
        self.window_min_height = 760
        self.window_max_height = 960
        self.setMinimumSize(self.window_min_width, self.window_min_height)
        self.setMaximumSize(self.window_max_width, self.window_max_height)

        # 设置窗口透明度
        #self.setWindowOpacity(0.8)

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
        self.set_bottom_widget()

        # 窗口组装
        self.layout_main = QtWidgets.QVBoxLayout()
        self.layout_main.addWidget(self.widget_window_buttons)
        self.layout_main.addWidget(self.widget_head)
        self.layout_main.addWidget(self.widget_body)
        self.layout_main.addWidget(self.widget_bottom)
        self.layout_main.setSpacing(0)
        self.layout_main.setContentsMargins(0, 0, 0, 0)
        self.setLayout(self.layout_main)

        # 鼠标状态
        self.setMouseTracking(True)
        self.edge_range = 4
        self.mouse_pos = None  # 鼠标相对于窗口的位置
        self.is_left_button_pressed = False

        # 设置样式
        QSSSetter.set_qss(self, __file__)

    def set_window_buttons_widget(self):
        self.widget_window_buttons = QtWidgets.QWidget()
        self.widget_window_buttons.setMouseTracking(True)
        self.widget_window_buttons.setObjectName('window_buttons')
        self.widget_window_buttons.setFixedSize(self.window_min_width, 40)

        # 窗口按钮(最小化和关闭按钮)
        layout = QtWidgets.QHBoxLayout()
        layout.setSpacing(0)
        layout.setContentsMargins(0, 0, 0, 0)

        button_min_window = QtWidgets.QPushButton()
        button_min_window.clicked.connect(self.showMinimized)
        button_min_window.setObjectName('button_min_window')
        button_min_window.setFixedSize(25, 25)
        button_close_window = QtWidgets.QPushButton()
        button_close_window.clicked.connect(QtWidgets.qApp.quit)
        button_close_window.setFixedSize(25, 25)
        button_close_window.setObjectName('button_close_window')

        layout.addStretch(30)
        layout.addWidget(button_min_window)
        layout.addStretch(1.5)
        layout.addWidget(button_close_window)
        layout.addStretch(1)
        self.widget_window_buttons.setLayout(layout)

    def set_head_widget(self):
        self.widget_head = QtWidgets.QWidget()
        self.widget_head.setMouseTracking(True)
        self.widget_head.setObjectName('head')
        self.widget_head.setFixedSize(self.window_min_width, 120)

        # 用户头像和用户信息组件
        label_photo = QtWidgets.QLabel()
        label_photo.setFixedSize(80, 80)
        label_photo.setObjectName('user_photo')
        label_username = QtWidgets.QLabel('Bill Guo')
        label_username.setObjectName('user_name')
        label_userinfo = QtWidgets.QLabel('Administrator')
        label_userinfo.setObjectName('user_info')

        # 布局
        layout = QtWidgets.QHBoxLayout()
        layout.setSpacing(0)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.addStretch(1)
        layout.addWidget(label_photo)
        layout_v = QtWidgets.QVBoxLayout()
        layout_v.setSpacing(0)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.addLayout(layout_v)
        layout.addStretch(10)
        layout_v.addStretch(2)
        layout_v.addWidget(label_username)
        layout_v.addStretch(1)
        layout_v.addWidget(label_userinfo)
        layout_v.addStretch(2)
        self.widget_head.setLayout(layout)

    def set_body_widget(self):
        self.widget_body = QtWidgets.QWidget()
        self.widget_body.setMouseTracking(True)
        self.widget_body.setObjectName('body')
        self.widget_body.setMinimumSize(self.window_min_width, 550)
        self.widget_body.setMaximumSize(
            self.window_min_width,
            self.window_max_height - 45 - 120
        )

        # 环境选择下拉框和商户搜索组件
        combobox_env = QtWidgets.QComboBox()
        listview_combobox = QtWidgets.QListView()
        listview_combobox.setObjectName('env_list')
        combobox_env.setView(listview_combobox)
        if self.kos:
            try:
                combobox_env.addItems(self.kos.root.get_environments())
            except Exception as e:
                self.show_message('服务器连接失败!')
                logging.error(
                    "{} occured".format(type(e).__name__),
                    exc_info=True
                )
        else:
            self.show_message('服务器连接失败!')
        combobox_env.setObjectName('env')
        combobox_env.setFixedSize(self.window_min_width, 30)
        label_search = QtWidgets.QLabel()
        label_search.setObjectName('search_icon')
        label_search.setFixedSize(30, 30)
        lineedit_search = QtWidgets.QLineEdit()
        lineedit_search.setPlaceholderText('搜索')
        lineedit_search.setObjectName('search_tenant')
        lineedit_search.setFixedSize(self.window_min_width - 30, 30)

        # Tab切换
        self.frame_tenants = QtWidgets.QFrame()
        layout_tenants = QtWidgets.QVBoxLayout()
        layout_tenants.setSpacing(0)
        layout_tenants.setContentsMargins(0, 0, 0, 0)
        self.frame_tools = QtWidgets.QFrame()
        layout_tools = QtWidgets.QVBoxLayout()
        self.frame_tools.hide()

        # 布局
        layout = QtWidgets.QVBoxLayout()
        layout.setSpacing(0)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.addWidget(combobox_env)
        layout_h = QtWidgets.QHBoxLayout()
        layout_h.setSpacing(0)
        layout_h.setContentsMargins(0, 0, 0, 0)
        layout_h.addWidget(label_search)
        layout_h.addWidget(lineedit_search)
        layout_tab = QtWidgets.QHBoxLayout()
        button_group_view = QtWidgets.QButtonGroup(self)
        button_view_tenants = QtWidgets.QPushButton('商户')
        button_view_tenants.setFixedSize(192, 40)
        button_view_tenants.setObjectName('tab')
        button_view_tenants.setCheckable(True)
        button_view_tenants.setChecked(True)
        button_view_tenants.clicked.connect(
            lambda: self.swith_tenants_tools('tenants')
        )
        button_view_tools = QtWidgets.QPushButton('工具')
        button_view_tools.setFixedSize(192, 40)
        button_view_tools.setObjectName('tab')
        button_view_tools.setCheckable(True)
        button_view_tools.clicked.connect(
            lambda: self.swith_tenants_tools('tools')
        )
        button_group_view.addButton(button_view_tenants)
        button_group_view.addButton(button_view_tools)
        layout_tab.setSpacing(0)
        layout_tab.setContentsMargins(0, 0, 0, 0)
        layout_tab.addWidget(button_view_tenants)
        layout_tab.addWidget(button_view_tools)
        layout.addLayout(layout_h)
        layout.addLayout(layout_tab)

        # 常用商户
        tree_tenants = QtWidgets.QTreeWidget()
        tree_tenants.setObjectName('tenants')
        tree_tenants.setMinimumSize(self.window_min_width, 550 - 30 - 30 - 40)
        size_policy_tree_tenants = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.Fixed,
            QtWidgets.QSizePolicy.Expanding
        )
        tree_tenants.setSizePolicy(size_policy_tree_tenants)
        tree_tenants.header().hide()
        item_root_favourite_tenants = QtWidgets.QTreeWidgetItem(
            tree_tenants)
        item_root_favourite_tenants.setText(0, '常用商户')
        item_root_favourite_tenants.setFont(
            0,
            QtGui.QFont("微软雅黑", 11, QtGui.QFont.Bold)
        )
        for i in range(100):
            item_favourite_tenants = QtWidgets.QTreeWidgetItem()
            item_favourite_tenants.setText(0, '商户{}'.format(i))
            item_favourite_tenants.setToolTip(0, '商户{}'.format(i))
            item_root_favourite_tenants.addChild(item_favourite_tenants)

        # 所有商户
        item_root_all_tenants = QtWidgets.QTreeWidgetItem(
            tree_tenants)
        item_root_all_tenants.setText(0, '所有商户')
        item_root_all_tenants.setFont(
            0,
            QtGui.QFont("微软雅黑", 11, QtGui.QFont.Bold)
        )
        for i in range(5):
            item_all_tenants = QtWidgets.QTreeWidgetItem()
            item_all_tenants.setText(0, '商户{}'.format(i))
            item_all_tenants.setToolTip(0, '商户{}'.format(i))
            item_root_all_tenants.addChild(item_all_tenants)
        layout_tenants.addWidget(tree_tenants)

        '''
        layout_scroll_tenants = QtWidgets.QVBoxLayout()
        scroll_tenants = QtWidgets.QScrollArea()
        scroll_tenants.setLayout(layout_tenants)
        scroll_tenants.setWidgetResizable(True)
        layout_scroll_tenants.addWidget(scroll_tenants)
        self.frame_tenants.setLayout(layout_scroll_tenants)
        '''

        self.frame_tenants.setLayout(layout_tenants)

        self.label_message = QtWidgets.QLabel()
        self.label_message.setFixedSize(self.window_min_width, 20)
        self.label_message.setObjectName('message')
        self.label_message.setAlignment(QtCore.Qt.AlignCenter)

        layout.addWidget(self.frame_tenants)
        layout.addWidget(self.frame_tools)
        layout.addStretch()
        layout.addWidget(self.label_message)
        self.label_message.setVisible(False)
        self.widget_body.setLayout(layout)

    def set_bottom_widget(self):
        self.widget_bottom = QtWidgets.QWidget()
        self.widget_bottom.setMouseTracking(True)
        self.widget_bottom.setObjectName('bottom')
        self.widget_bottom.setFixedSize(self.window_min_width, 45)

        # 设置按钮
        button_setting = QtWidgets.QPushButton('管理')
        button_setting.setIcon(QtGui.QIcon('images/settings.png'))
        button_setting.setIconSize(QtCore.QSize(30, 30))
        button_setting.setObjectName('settings')
        #button_setting.setFixedSize(45, 45)

        layout = QtWidgets.QHBoxLayout()
        layout.setSpacing(0)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.addWidget(button_setting)
        layout.addStretch()
        self.widget_bottom.setLayout(layout)

    def mousePressEvent(self, event):
        if event.button() == QtCore.Qt.LeftButton:
            self.is_left_button_pressed = True
            mouse_x = event.globalPos().x()
            mouse_y = event.globalPos().y()
            rect_window = self.rect()
            topleft_point = self.mapToGlobal(rect_window.topLeft())
            rightbottom_point = self.mapToGlobal(rect_window.bottomRight())
            if (
                (topleft_point.x() - self.edge_range) <= mouse_x and
                mouse_x <= (topleft_point.x() + self.edge_range) and
                (topleft_point.y() - self.edge_range) <= mouse_y and
                mouse_y <= (topleft_point.y() + self.edge_range)
            ):
                self.mouse_pos = 'LEFTTOP'  # 鼠标位于窗口左上角
            elif (
                (rightbottom_point.x() - self.edge_range) <= mouse_x and
                mouse_x <= (rightbottom_point.x() + self.edge_range) and
                (topleft_point.y() - self.edge_range) <= mouse_y and
                mouse_y <= (topleft_point.y() + self.edge_range)
            ):
                self.mouse_pos = 'RIGHTTOP'
            elif (
                (topleft_point.x() - self.edge_range) <= mouse_x and
                mouse_x <= (topleft_point.x() + self.edge_range) and
                (rightbottom_point.y() - self.edge_range) <= mouse_y and
                mouse_y <= (rightbottom_point.y() + self.edge_range)
            ):
                self.mouse_pos = 'LEFTBOTTOM'
            elif (
                (rightbottom_point.x() - self.edge_range) <= mouse_x and
                mouse_x <= (rightbottom_point.x() + self.edge_range) and
                (rightbottom_point.y() - self.edge_range) <= mouse_y and
                mouse_y <= (rightbottom_point.y() + self.edge_range)
            ):
                self.mouse_pos = 'RIGHTBOTTOM'
            elif (
                (topleft_point.x() + self.edge_range) < mouse_x and
                mouse_x < (rightbottom_point.x() - self.edge_range) and
                (topleft_point.y() - self.edge_range) <= mouse_y and
                mouse_y <= (topleft_point.y() + self.edge_range)
            ):
                self.mouse_pos = 'TOP'
            elif (
                (topleft_point.x() + self.edge_range) < mouse_x and
                mouse_x < (rightbottom_point.x() - self.edge_range) and
                (rightbottom_point.y() - self.edge_range) <= mouse_y and
                mouse_y <= (rightbottom_point.y() + self.edge_range)
            ):
                self.mouse_pos = 'BOTTOM'
            else:
                self.drag_pos = event.globalPos()  # 拖拽起始点坐标
                self.setCursor(
                    QCursor(QtCore.Qt.OpenHandCursor)
                )
            event.accept()

    def mouseMoveEvent(self, event):
        mouse_x = event.globalPos().x()
        mouse_y = event.globalPos().y()
        rect_window = self.rect()
        topleft_point = self.mapToGlobal(rect_window.topLeft())
        rightbottom_point = self.mapToGlobal(rect_window.bottomRight())
        if not self.is_left_button_pressed:
            # 仅改变鼠标形状
            if (
                (topleft_point.x() - self.edge_range) <= mouse_x and
                mouse_x <= (topleft_point.x() + self.edge_range) and
                (topleft_point.y() - self.edge_range) <= mouse_y and
                mouse_y <= (topleft_point.y() + self.edge_range)
            ):
                # 左上
                self.setCursor(
                    QCursor(QtCore.Qt.SizeFDiagCursor)
                )  # 设置鼠标形状
            elif (
                (rightbottom_point.x() - self.edge_range) <= mouse_x and
                mouse_x <= (rightbottom_point.x() + self.edge_range) and
                (topleft_point.y() - self.edge_range) <= mouse_y and
                mouse_y <= (topleft_point.y() + self.edge_range)
            ):
                # 右上
                self.setCursor(
                    QCursor(QtCore.Qt.SizeBDiagCursor)
                )  # 设置鼠标形状
            elif (
                (topleft_point.x() - self.edge_range) <= mouse_x and
                mouse_x <= (topleft_point.x() + self.edge_range) and
                (rightbottom_point.y() - self.edge_range) <= mouse_y and
                mouse_y <= (rightbottom_point.y() + self.edge_range)
            ):
                # 左下
                self.setCursor(
                    QCursor(QtCore.Qt.SizeBDiagCursor)
                )  # 设置鼠标形状
            elif (
                (rightbottom_point.x() - self.edge_range) <= mouse_x and
                mouse_x <= (rightbottom_point.x() + self.edge_range) and
                (rightbottom_point.y() - self.edge_range) <= mouse_y and
                mouse_y <= (rightbottom_point.y() + self.edge_range)
            ):
                # 右下
                self.setCursor(
                    QCursor(QtCore.Qt.SizeFDiagCursor)
                )  # 设置鼠标形状
            elif (
                (topleft_point.x() + self.edge_range) < mouse_x and
                mouse_x < (rightbottom_point.x() - self.edge_range) and
                (topleft_point.y() - self.edge_range) <= mouse_y and
                mouse_y <= (topleft_point.y() + self.edge_range)
            ):
                # 上
                self.setCursor(
                    QCursor(QtCore.Qt.SizeVerCursor)
                )  # 设置鼠标形状
            elif (
                (topleft_point.x() + self.edge_range) < mouse_x and
                mouse_x < (rightbottom_point.x() - self.edge_range) and
                (rightbottom_point.y() - self.edge_range) <= mouse_y and
                mouse_y <= (rightbottom_point.y() + self.edge_range)
            ):
                # 下
                self.setCursor(
                    QCursor(QtCore.Qt.SizeVerCursor)
                )  # 设置鼠标形状
            else:
                self.setCursor(
                    QCursor(QtCore.Qt.ArrowCursor)
                )  # 设置鼠标形状
        elif self.mouse_pos is None:
            # 拖拽改变窗口位置
            self.move(self.pos() + event.globalPos() - self.drag_pos)
            self.drag_pos = event.globalPos()
            event.accept()
        else:
            rect_new = QtCore.QRect(topleft_point, rightbottom_point)
            if self.mouse_pos == 'LEFTTOP':
                if (
                    self.window_min_width <
                    rightbottom_point.x() - mouse_x <
                    self.window_max_width
                ):
                    rect_new.setX(mouse_x)

                if (
                    self.window_min_height <
                    rightbottom_point.y() - mouse_y <
                    self.window_max_height
                ):
                    rect_new.setY(mouse_y)

            if self.mouse_pos == 'TOP':
                if (
                    self.window_min_height <
                    rightbottom_point.y() - mouse_y <
                    self.window_max_height
                ):
                    rect_new.setY(mouse_y)

            if self.mouse_pos == 'RIGHTBOTTOM':
                if (
                    self.window_min_width <
                    mouse_x - topleft_point.x() <
                    self.window_max_width
                ):
                    rect_new.setX(mouse_x)
                if (
                    self.window_min_height <
                    mouse_y - topleft_point.y() <
                    self.window_max_height
                ):
                    rect_new.setY(mouse_y)

            if self.mouse_pos == 'BOTTOM':
                if (
                    self.window_min_height <
                    mouse_y - topleft_point.y() <
                    self.window_max_height
                ):
                    rect_new.setY(mouse_y)

            if self.mouse_pos == 'RIGHTTOP':
                if (
                    self.window_min_width <
                    mouse_x - topleft_point.x() <
                    self.window_max_width
                ):
                    rect_new.setX(mouse_x)
                if (
                    self.window_min_height <
                    rightbottom_point.y() - mouse_y <
                    self.window_max_height
                ):
                    rect_new.setY(mouse_y)

            if self.mouse_pos == 'LEFTBOTTOM':
                if (
                    self.window_min_width <
                    rightbottom_point.x() - mouse_x <
                    self.window_max_width
                ):
                    rect_new.setX(mouse_x)
                if (
                    self.window_min_height <
                    mouse_y - topleft_point.y() <
                    self.window_max_height
                ):
                    rect_new.setY(mouse_y)

            self.setGeometry(rect_new)

    def mouseReleaseEvent(self, event):
        if event.button() == QtCore.Qt.LeftButton:
            self.mouse_pos = None
            self.is_left_button_pressed = False
            self.setCursor(
                QCursor(QtCore.Qt.ArrowCursor)
            )
            event.accept()

    def swith_tenants_tools(self, tab):
        if tab == 'tenants':
            self.frame_tenants.show()
            self.frame_tools.hide()
            self.tab = tab
        elif tab == 'tools':
            self.frame_tenants.hide()
            self.frame_tools.show()
            self.tab = tab

    def show_message(self, message):
        self.label_message.setVisible(True)
        self.label_message.setText('服务器连接失败')
