from PyQt5 import QtWidgets
from PyQt5 import QtCore

from qss.qss_setter import QSSSetter


class WindowMain(QtWidgets.QWidget):
    def __init__(self, screen_width, screen_height):
        super().__init__()

        # 设置窗口大小
        self.window_width = screen_width * 0.2
        self.window_height = screen_height * 0.8
        self.setMinimumSize(400, 760)
        self.setMaximumSize(400, 960)

        # 设置窗口透明度
        self.setWindowOpacity(0.7)
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
        self.setLayout(self.layout_main)

        # 设置样式
        QSSSetter.set_qss(self, __file__)

    def set_window_buttons_widget(self):
        self.widget_window_buttons = QtWidgets.QWidget()
        self.widget_window_buttons.setObjectName('window_buttons')
        self.widget_window_buttons.setFixedSize(self.window_width, 40)

        # 窗口按钮(最小化和关闭按钮)
        layout = QtWidgets.QHBoxLayout()
        layout.setSpacing(0)

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
        layout.addStretch(1)
        layout.addWidget(button_close_window)
        layout.addStretch(0.5)
        self.widget_window_buttons.setLayout(layout)

    def set_head_widget(self):
        self.widget_head = QtWidgets.QWidget()
        self.widget_head.setObjectName('head')
        self.widget_head.setFixedSize(384, 120)

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
        layout.addWidget(label_photo)
        layout_v = QtWidgets.QVBoxLayout()
        layout_v.setSpacing(0)
        layout.addLayout(layout_v)
        layout_v.addWidget(label_username)
        layout_v.addWidget(label_userinfo)
        self.widget_head.setLayout(layout)

    def set_body_widget(self):
        self.widget_body = QtWidgets.QWidget()
        self.widget_body.setObjectName('body')
        self.widget_body.setMinimumSize(384, 550)
        self.widget_body.setMaximumSize(384, self.window_height - 40 - 120)

        # 环境选择下拉框和商户搜索组件
        combobox_env = QtWidgets.QComboBox()
        combobox_env.setObjectName('env')
        combobox_env.setFixedSize(384, 30)
        label_search = QtWidgets.QLabel()
        label_search.setObjectName('search_icon')
        label_search.setFixedSize(30, 30)
        lineedit_search = QtWidgets.QLineEdit()
        lineedit_search.setObjectName('search_tenant')
        lineedit_search.setFixedSize(354, 30)

        # 常用商户分组
        button_fold_favourites = QtWidgets.QPushButton()
        button_fold_favourites.setObjectName('fold_button')
        button_fold_favourites.setFixedSize(30, 30)
        label_favourite = QtWidgets.QLabel('常用商户')
        label_favourite.setObjectName('group_name')

        # 所有商户分组
        button_fold_all = QtWidgets.QPushButton()
        button_fold_all.setObjectName('fold_button')
        button_fold_all.setFixedSize(30, 30)
        label_all = QtWidgets.QLabel('所有商户')
        label_all.setObjectName('group_name')

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
        layout.addLayout(layout_h)

        frame_favourite_tenants = QtWidgets.QFrame()
        layout_favourite_tenants = QtWidgets.QVBoxLayout()
        button_fold_favourites.clicked.connect(
            lambda: self.fold_frame(frame_favourite_tenants)
        )
        layout_favourite_tenants.setSpacing(0)
        layout_favourite_tenants.setContentsMargins(0, 10, 0, 0)
        layout_favourite_group = QtWidgets.QHBoxLayout()
        layout_favourite_group.setSpacing(0)
        layout_favourite_group.setContentsMargins(0, 0, 0, 0)
        layout_favourite_group.addWidget(button_fold_favourites)
        layout_favourite_group.addWidget(label_favourite)
        for i in range(5):
            label_tenant = QtWidgets.QLabel('商户{}'.format(i))
            label_tenant.setObjectName('tenant')
            label_tenant.setFixedSize(384, 30)
            layout_favourite_tenants.addWidget(label_tenant)
        frame_favourite_tenants.setLayout(layout_favourite_tenants)
        layout.addLayout(layout_favourite_group)
        layout.addWidget(frame_favourite_tenants)

        frame_all_tenants = QtWidgets.QFrame()
        layout_all_tenants = QtWidgets.QVBoxLayout()
        button_fold_all.clicked.connect(
            lambda: self.fold_frame(frame_all_tenants)
        )
        layout_all_tenants.setSpacing(0)
        layout_all_tenants.setContentsMargins(0, 10, 0, 0)
        layout_all_group = QtWidgets.QHBoxLayout()
        layout_all_group.setSpacing(0)
        layout_all_group.setContentsMargins(0, 0, 0, 0)
        layout_all_group.addWidget(button_fold_all)
        layout_all_group.addWidget(label_all)
        for i in range(5):
            label_tenant = QtWidgets.QLabel('商户{}'.format(i))
            label_tenant.setObjectName('tenant')
            label_tenant.setFixedSize(384, 30)
            layout_all_tenants.addWidget(label_tenant)
        frame_all_tenants.setLayout(layout_all_tenants)
        layout.addLayout(layout_all_group)
        layout.addWidget(frame_all_tenants)
        layout.addStretch()
        self.widget_body.setLayout(layout)

    def set_bottom_widget(self):
        self.widget_bottom = QtWidgets.QWidget()
        self.widget_bottom.setObjectName('bottom')
        self.widget_bottom.setFixedSize(384, 40)

        # 设置按钮
        button_setting = QtWidgets.QPushButton()
        button_setting.setObjectName('settings')
        button_setting.setFixedSize(20, 20)

        layout = QtWidgets.QHBoxLayout()
        layout.setSpacing(0)
        layout.setContentsMargins(10, 0, 0, 0)
        layout.addWidget(button_setting)
        layout.addStretch()
        self.widget_bottom.setLayout(layout)

    def fold_frame(self, frame):
        if frame.isHidden():
            frame.show()
        else:
            frame.hide()

    def mousePressEvent(self, event):
        if event.buttons() == QtCore.Qt.LeftButton:
            self.dragPos = event.globalPos()
            event.accept()

    def mouseMoveEvent(self, event):
        if event.buttons() == QtCore.Qt.LeftButton:
            self.move(self.pos() + event.globalPos() - self.dragPos)
            self.dragPos = event.globalPos()
            event.accept()
