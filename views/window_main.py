from PyQt5 import QtWidgets
from PyQt5 import QtCore
from PyQt5 import QtGui

from qss.qss_setter import QSSSetter
from models.tenant import Tenant
from views.window_config import WindowConfig
from views.window_dragable import WindowDragable

import logging
import logging.handlers


class WindowMain(WindowDragable):
    def __init__(self, session_id, token, service, login_window):
        super().__init__()

        self.session_id = session_id
        self.token = token
        self.login_window = login_window
        self.children_windows = dict()
        self.children_windows['config'] = None
        self.tenants = dict()

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
        button_close_window.clicked.connect(self.close_main)
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
        button_view_tenants.setObjectName('tab1')
        button_view_tenants.setCheckable(True)
        button_view_tenants.setChecked(True)
        button_view_tenants.clicked.connect(
            lambda: self.swith_tenants_tools('tenants')
        )
        button_view_tools = QtWidgets.QPushButton('工具')
        button_view_tools.setFixedSize(192, 40)
        button_view_tools.setObjectName('tab2')
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

        # 商户信息
        self.tree_tenants = QtWidgets.QTreeWidget()
        #self.tree_tenants.itemClicked.connect(self.show_tenant_details)
        self.tree_tenants.setContextMenuPolicy(QtCore.Qt.CustomContextMenu)
        self.tree_tenants.customContextMenuRequested.connect(
            self.show_tenant_menu
        )
        self.tree_tenants.setObjectName('tenants')
        self.tree_tenants.setMinimumSize(
            self.window_min_width, 550 - 30 - 30 - 40 - 30
        )
        size_policy_tree_tenants = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.Fixed,
            QtWidgets.QSizePolicy.Expanding
        )
        self.tree_tenants.setSizePolicy(size_policy_tree_tenants)
        self.tree_tenants.header().hide()

        self.item_root_favourite_tenants = QtWidgets.QTreeWidgetItem(
            self.tree_tenants)
        self.item_root_favourite_tenants.setText(0, '常用商户')
        self.tenants['常用商户'] = list()
        self.item_root_favourite_tenants.setFont(
            0,
            QtGui.QFont("微软雅黑", 11, QtGui.QFont.Bold)
        )

        self.item_root_all_tenants = QtWidgets.QTreeWidgetItem(
            self.tree_tenants)
        self.item_root_all_tenants.setText(0, '所有商户')
        self.tenants['所有商户'] = list()
        self.item_root_all_tenants.setFont(
            0,
            QtGui.QFont("微软雅黑", 11, QtGui.QFont.Bold)
        )

        layout_tenants.addWidget(self.tree_tenants)

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

        self.refresh_tenants()  # 加载商户信息

        layout.addWidget(self.frame_tenants)
        layout.addWidget(self.frame_tools)
        layout.addWidget(self.label_message)
        self.label_message.setVisible(False)
        self.widget_body.setLayout(layout)

    def set_bottom_widget(self):
        self.widget_bottom = QtWidgets.QWidget()
        self.widget_bottom.setMouseTracking(True)
        self.widget_bottom.setObjectName('bottom')
        self.widget_bottom.setFixedSize(self.window_min_width, 45)

        # 设置按钮
        self.button_setting = QtWidgets.QPushButton('管理')
        self.button_setting.setIcon(QtGui.QIcon('images/settings.png'))
        self.button_setting.setIconSize(QtCore.QSize(30, 30))
        self.button_setting.setObjectName('settings')
        self.button_setting.clicked.connect(self.popup_menu_settings)
        self.menu_setting = QtWidgets.QMenu()
        self.menu_setting.setStyleSheet(
            "QMenu{"
            "background-color:qlineargradient("
            "spread:pad,x1:0,y1:0,x2:1,y2:0,stop:0 rgb(255,153,102),"
            "stop:1 rgb(255,255,255));"
            "} "
            "QMenu::item{"
            "background-color:transparent;"
            "padding:8px 20px;"
            "margin:0px 1px;"
            "font-size:12px;"
            "font-family:\"微软雅黑\";"
            "} "
            "QMenu::item::selected{"
            "background-color:rgba(192,192,192,50%)"
            "}"
        )
        menu_users = self.menu_setting.addMenu('用户管理')
        menu_users.addAction('用户创建')
        menu_users.addAction('用户修改')
        menu_envs = self.menu_setting.addMenu('环境配置')
        menu_envs.addAction('环境创建', self.show_config_window)
        menu_envs.addAction('环境修改', self.show_setting_window)
        self.menu_setting.addAction('历史审查')

        layout = QtWidgets.QHBoxLayout()
        layout.setSpacing(0)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.addWidget(self.button_setting)
        layout.addStretch()
        self.widget_bottom.setLayout(layout)

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
        self.label_message.setText(message)

    def close_main(self):
        if self.kos:
            try:
                self.kos.root.logout(self.session_id)
            except Exception as e:
                logging.error(
                    "{} occured".format(type(e).__name__),
                    exc_info=True
                )
        QtWidgets.qApp.quit()

    def refresh_tenants(self):
        self.item_root_favourite_tenants.takeChildren()
        self.item_root_all_tenants.takeChildren()
        self.tenants['常用商户'].clear()
        self.tenants['所有商户'].clear()
        if self.kos:
            try:
                favourite_tenants = self.kos.root.get_tenants(
                    self.session_id, self.token, 10
                )
                all_tenants = self.kos.root.get_tenants(
                    self.session_id, self.token
                )
                if (
                    isinstance(favourite_tenants, list) and
                    isinstance(all_tenants, list)
                ):
                    for t in favourite_tenants:
                        item_favourite_tenants = QtWidgets.QTreeWidgetItem()
                        item_favourite_tenants.setText(0, t['name'])
                        item_favourite_tenants.setToolTip(0, t['name'])
                        self.item_root_favourite_tenants.addChild(
                            item_favourite_tenants
                        )
                        self.tenants['常用商户'].append(Tenant(t['id'], t['name']))
                    for t in all_tenants:
                        item_all_tenants = QtWidgets.QTreeWidgetItem()
                        item_all_tenants.setText(0, t['name'])
                        item_all_tenants.setToolTip(0, t['name'])
                        self.item_root_all_tenants.addChild(item_all_tenants)
                        self.tenants['所有商户'].append(Tenant(t['id'], t['name']))
                else:
                    # 锁定界面，要求重新登录
                    self.setEnabled(False)
                    self.login_window.show()
            except Exception as e:
                self.show_message('服务器连接失败!')
                logging.error(
                    "{} occured".format(type(e).__name__),
                    exc_info=True
                )
        else:
            self.show_message('服务器连接失败!')

    def renew_token(self, token):
        self.token = token

    def set_enabled_cascade(self, enabled):
        for k, v in self.children_windows.items():
            if v:
                v.setEnabled(enabled)

    def popup_menu_settings(self):
        pos = QtCore.QPoint()
        pos.setX(0)
        pos.setY(
            -105
        )
        self.menu_setting.exec(
            self.button_setting.mapToGlobal(pos)
        )

    def show_tenant_menu(self, pos):
        selected_items = self.tree_tenants.selectedItems()
        if selected_items:
            selected_item = selected_items[0]
            parent = selected_item.parent()
            if parent:
                # 排除一级节点
                group = parent.text(0)
                index = parent.indexOfChild(selected_item)
                curr_tenant = self.tenants[group][index]
                menu_tenant = QtWidgets.QMenu()
                menu_list = menu_tenant.addMenu('内容列表')
                menu_workflow = menu_tenant.addMenu('流程管理')
                menu_list.addAction('完全删除')
                menu_list.addAction('数据清理')
                menu_list.addAction('重置ES数据')
                menu_list.addAction('重置GP数据')
                menu_list.addAction('重建索引')
                menu_workflow.addAction('删除流程')
                menu_workflow.addAction('清理数据')
                menu_report = menu_workflow.addMenu('流程报表')
                menu_report.addAction('重建索引')
                menu_workflow.addAction('流程修复')
                menu_tenant.setStyleSheet(
                    "QMenu::item{"
                    "background-color:transparent;"
                    "padding:8px 20px;"
                    "margin:0px 1px;"
                    "font-size:12px;"
                    "font-family:\"微软雅黑\";"
                    "} "
                    "QMenu::item::selected{"
                    "background-color:rgba(192,192,192,50%)"
                    "}"
                )
                print('ID: {}, Name: {}'.format(curr_tenant.id, curr_tenant.name))
                menu_tenant.exec(self.tree_tenants.mapToGlobal(pos))
            elif selected_item.text(0) == '所有商户':
                # 所有商户的操作菜单
                menu_tenant_group = QtWidgets.QMenu()
                menu_tenant_group.addAction('刷新', self.refresh_tenants)
                menu_tenant_group.setStyleSheet(
                    "QMenu::item{"
                    "background-color:transparent;"
                    "padding:4px 10px;"
                    "margin:0px 1px;"
                    "font-size:12px;"
                    "font-family:\"微软雅黑\";"
                    "} "
                    "QMenu::item::selected{"
                    "background-color:rgba(192,192,192,50%)"
                    "}"
                )
                menu_tenant_group.exec(self.tree_tenants.mapToGlobal(pos))

    def show_config_window(self):
        config_window = self.children_windows['config']
        if not config_window:
            config_window = WindowConfig(self)
            self.children_windows['config'] = config_window
        config_window.show()
        config_window.activateWindow()

    def show_setting_window(self):
        pass
