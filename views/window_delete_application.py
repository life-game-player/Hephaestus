from PyQt5 import QtWidgets
from PyQt5 import QtCore
from PyQt5 import QtGui

from views.window_dragable import WindowDragable
from views.window_env_detail import WindowEnvDetail
from views.window_warning import WindowWarning
from views.window_error import WindowError
from qss.qss_setter import QSSSetter


class WindowDeleteApplication(WindowDragable):
    def __init__(self, main_window, tenant_id, env):
        super().__init__()

        self.main_window = main_window
        self.children_windows = dict()
        self.children_windows['env_detail'] = None
        self.validation_results = {'passed': [], 'failed': []}

        # 设置窗口无边框
        self.setWindowFlags(
            QtCore.Qt.FramelessWindowHint
        )
        # 设置窗口背景透明
        self.setAttribute(QtCore.Qt.WA_TranslucentBackground)

        # 设置窗口图标
        self.setWindowIcon(self.main_window.icon)

        # 设置窗口大小
        self.window_min_width = 300
        self.window_max_width = 300
        self.window_min_height = 250
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
        self.widget_body.setMinimumSize(
            self.window_min_width,
            self.window_min_height - 30
        )
        self.widget_body.setMaximumSize(
            self.window_max_width,
            self.window_max_height - 30
        )

        # 组件
        button_group = QtWidgets.QButtonGroup()
        radio_by_defkey = QtWidgets.QRadioButton("根据流程标识")
        radio_by_defkey.setChecked(True)
        radio_by_defkey.clicked.connect(self.select_by_defkey)
        radio_by_flowno = QtWidgets.QRadioButton("根据流程编号")
        radio_by_flowno.clicked.connect(self.select_by_flowno)
        button_group.addButton(radio_by_defkey)
        button_group.addButton(radio_by_flowno)
        self.label_validation_results = QtWidgets.QLabel()
        self.combobox_show_results = QtWidgets.QComboBox()
        list_show_results = [
            "显示全部结果",
            "仅显示失败结果",
            "仅显示成功结果"
        ]
        self.combobox_show_results.addItems(list_show_results)
        self.combobox_show_results.currentIndexChanged.connect(
            self.show_validation_results
        )
        self.text_edit_params = QtWidgets.QPlainTextEdit()
        self.text_edit_params.setFixedHeight(90)
        self.text_edit_params.setPlaceholderText('请填入需要删除的流程标识(如有多个，请用逗号隔开)')
        self.tree_validation = QtWidgets.QTreeWidget()
        self.tree_validation.setIndentation(0)
        self.tree_validation.setObjectName('validation')
        self.tree_validation.header().hide()
        self.button_validate = QtWidgets.QPushButton('验证')
        self.button_validate.setFixedSize(200, 30)
        self.button_validate.setObjectName('main')
        self.button_validate.clicked.connect(self.validate_params)
        self.button_delete = QtWidgets.QPushButton('确认删除')
        self.button_delete.setFixedSize(80, 30)
        self.button_delete.setObjectName('main')

        # 布局
        self.layout_main = QtWidgets.QVBoxLayout()
        groupbox_del_by = QtWidgets.QGroupBox()
        layout_del_by = QtWidgets.QVBoxLayout()
        layout_del_by.addWidget(radio_by_defkey)
        layout_del_by.addWidget(radio_by_flowno)
        groupbox_del_by.setLayout(layout_del_by)
        self.layout_main.addWidget(groupbox_del_by)
        self.layout_main.addWidget(self.text_edit_params)
        layout_validation_results = QtWidgets.QHBoxLayout()
        layout_validation_results.addWidget(self.label_validation_results)
        layout_validation_results.addStretch()
        layout_validation_results.addWidget(self.combobox_show_results)
        self.layout_main.addLayout(layout_validation_results)
        self.layout_main.addWidget(self.tree_validation)
        layout_buttons = QtWidgets.QHBoxLayout()
        layout_buttons.addStretch(1)
        layout_buttons.addWidget(self.button_validate)
        layout_buttons.addWidget(self.button_delete)
        layout_buttons.addStretch(1)
        self.layout_main.addLayout(layout_buttons)
        self.layout_main.addStretch(1)

        # 初始化
        self.label_validation_results.setVisible(False)
        self.combobox_show_results.setVisible(False)
        self.tree_validation.setVisible(False)
        self.button_delete.setVisible(False)

        self.widget_body.setLayout(self.layout_main)

    def close_window(self):
        self.close()
        self.main_window.children_windows['del_app'] = None

    def validate_params(self):
        self.tree_validation.setVisible(True)
        self.tree_validation.clear()
        self.validation_results = {'passed': [], 'failed': []}

        item_validation = QtWidgets.QTreeWidgetItem(self.tree_validation)
        item_validation.setText(0, '流程编号1')
        item_validation.setIcon(0, QtGui.QIcon('images/passed.png'))
        self.validation_results['passed'].append(0)

        item_validation1 = QtWidgets.QTreeWidgetItem(self.tree_validation)
        item_validation1.setText(0, '流程编号2')
        item_validation1.setIcon(0, QtGui.QIcon('images/failed.png'))
        self.validation_results['failed'].append(1)

        self.tree_validation.setFixedHeight(24 * 2)
        self.label_validation_results.setText(
            '验证结果: '
            '<span style="color:green">成功{}个</span>\t'
            '<span style="color:red">失败{}个</span>'.format(1, 1)
        )
        self.label_validation_results.setVisible(True)
        self.combobox_show_results.setVisible(True)

        self.button_validate.setText('重新验证')
        self.button_validate.setFixedWidth(80)
        self.button_delete.setVisible(True)

        self.setFixedSize(self.layout_main.sizeHint())

    def select_by_defkey(self):
        self.text_edit_params.setPlaceholderText('请填入需要删除的流程标识(如有多个，请用逗号隔开)')
        self.text_edit_params.setPlainText('')
        self.button_validate.setText('验证')
        self.button_validate.setFixedWidth(200)
        self.label_validation_results.setVisible(False)
        self.combobox_show_results.setVisible(False)
        self.tree_validation.setVisible(False)
        self.button_delete.setVisible(False)
        self.layout_main.activate()
        self.setFixedSize(self.window_min_width, self.window_min_height)

    def select_by_flowno(self):
        self.text_edit_params.setPlaceholderText('请填入需要删除的流程编号(如有多个，请用逗号隔开)')
        self.text_edit_params.setPlainText('')
        self.button_validate.setText('验证')
        self.button_validate.setFixedWidth(200)
        self.label_validation_results.setVisible(False)
        self.combobox_show_results.setVisible(False)
        self.tree_validation.setVisible(False)
        self.button_delete.setVisible(False)
        self.layout_main.activate()
        self.setFixedSize(self.window_min_width, self.window_min_height)

    def show_validation_results(self):
        results_option = self.combobox_show_results.currentText()
        root = self.tree_validation.invisibleRootItem()
        if results_option == '显示全部结果':
            for i in self.validation_results['passed']:
                root.child(i).setHidden(False)
            for i in self.validation_results['failed']:
                root.child(i).setHidden(False)
        elif results_option == '仅显示失败结果':
            for i in self.validation_results['passed']:
                root.child(i).setHidden(True)
            for i in self.validation_results['failed']:
                root.child(i).setHidden(False)
        elif results_option == '仅显示成功结果':
            for i in self.validation_results['passed']:
                root.child(i).setHidden(False)
            for i in self.validation_results['failed']:
                root.child(i).setHidden(True)
