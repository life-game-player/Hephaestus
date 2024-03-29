from PyQt5 import QtWidgets
from PyQt5 import QtCore
from PyQt5 import QtGui

from views.window_dragable import WindowDragable
from views.window_warning import WindowWarning
from views.window_info import WindowInfo
from views.window_error import WindowError
from qss.qss_setter import QSSSetter


class WindowDeleteApplication(WindowDragable):
    def __init__(self, main_window, tenant_id, env):
        super().__init__()

        self.main_window = main_window
        self.env = env
        self.tenant_id = tenant_id
        self.validation_results = {'passed': [], 'failed': []}
        self.application_id_list = []

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
        self.window_min_height = 320
        self.window_max_height = 550
        self.setMinimumSize(self.window_min_width, self.window_min_height)
        self.setMaximumSize(self.window_max_width, self.window_max_height)

        # 设置窗口子部件
        self.set_head_widget()
        self.set_body_widget()

        # 窗口组装
        self.layout_main = QtWidgets.QVBoxLayout(self)
        self.layout_main.addWidget(self.widget_head)
        self.layout_main.addWidget(self.widget_body)
        self.layout_main.setSpacing(0)
        self.layout_main.setContentsMargins(0, 0, 0, 0)
        self.setLayout(self.layout_main)

        # 设置样式
        QSSSetter.set_qss(self, __file__)

    def set_head_widget(self):
        self.widget_head = QtWidgets.QWidget(self)
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
        self.widget_body = QtWidgets.QWidget(self)
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
        label_env = QtWidgets.QLabel('环境: {}'.format(self.env))
        label_env.setObjectName('env')
        self.button_group = QtWidgets.QButtonGroup()
        radio_by_defkey = QtWidgets.QRadioButton(self.widget_body)
        radio_by_defkey.setText("根据流程标识")
        radio_by_defkey.setChecked(True)
        radio_by_defkey.clicked.connect(self.select_by_defkey)
        radio_by_flowno = QtWidgets.QRadioButton(self.widget_body)
        radio_by_flowno.setText("根据流程编号")
        radio_by_flowno.clicked.connect(self.select_by_flowno)
        self.button_group.addButton(radio_by_defkey, 1)
        self.button_group.addButton(radio_by_flowno, 2)
        self.label_validation_results = QtWidgets.QLabel(self.widget_body)
        self.combobox_show_results = QtWidgets.QComboBox(self.widget_body)
        list_show_results = [
            "显示全部结果",
            "仅显示失败结果",
            "仅显示成功结果"
        ]
        self.combobox_show_results.addItems(list_show_results)
        self.combobox_show_results.currentIndexChanged.connect(
            self.show_validation_results
        )
        self.text_edit_params = QtWidgets.QPlainTextEdit(self.widget_body)
        self.text_edit_params.setFixedHeight(90)
        self.text_edit_params.setPlaceholderText('请填入需要删除的流程标识(如有多个，请用逗号隔开)')
        self.label_info = QtWidgets.QLabel(self.widget_body)
        self.label_info.setObjectName('hint')
        self.tree_validation = QtWidgets.QTreeWidget(self.widget_body)
        self.tree_validation.setIndentation(0)
        self.tree_validation.setObjectName('validation')
        self.tree_validation.header().hide()
        self.button_validate = QtWidgets.QPushButton(self.widget_body)
        self.button_validate.setText('验证')
        self.button_validate.setFixedSize(200, 30)
        self.button_validate.setObjectName('main')
        self.button_validate.clicked.connect(self.validate_params)
        self.button_delete = QtWidgets.QPushButton(self.widget_body)
        self.button_delete.setText('确认删除')
        self.button_delete.setFixedSize(80, 30)
        self.button_delete.setObjectName('main')
        self.button_delete.clicked.connect(self.delete_application)

        # 布局
        layout_main = QtWidgets.QVBoxLayout(self.widget_body)
        groupbox_del_by = QtWidgets.QGroupBox(self.widget_body)
        layout_del_by = QtWidgets.QVBoxLayout(groupbox_del_by)
        layout_del_by.addWidget(radio_by_defkey)
        layout_del_by.addWidget(radio_by_flowno)
        groupbox_del_by.setLayout(layout_del_by)
        layout_main.addWidget(groupbox_del_by)
        layout_env = QtWidgets.QHBoxLayout()
        layout_env.addWidget(label_env)
        layout_env.addStretch()
        layout_main.addLayout(layout_env)
        layout_main.addWidget(self.text_edit_params)
        layout_main.addWidget(self.label_info)
        layout_validation_results = QtWidgets.QHBoxLayout()
        layout_validation_results.addWidget(self.label_validation_results)
        layout_validation_results.addStretch()
        layout_validation_results.addWidget(self.combobox_show_results)
        layout_main.addLayout(layout_validation_results)
        layout_main.addWidget(self.tree_validation)
        layout_buttons = QtWidgets.QHBoxLayout()
        layout_buttons.addStretch(1)
        layout_buttons.addWidget(self.button_validate)
        layout_buttons.addWidget(self.button_delete)
        layout_buttons.addStretch(1)
        layout_main.addLayout(layout_buttons)

        # 初始化
        self.label_validation_results.setVisible(False)
        self.combobox_show_results.setVisible(False)
        self.tree_validation.setVisible(False)
        self.button_delete.setVisible(False)

        self.widget_body.setLayout(layout_main)

    def close_window(self):
        self.close()
        self.main_window.children_windows['del_app'] = None

    def validate_params(self):
        self.validation_results = {'passed': [], 'failed': []}
        self.label_info.setText('')
        self.application_id_list = []

        checked_button_id = self.button_group.checkedId()
        params = self.text_edit_params.toPlainText()
        if params:
            param_list = [i.strip() for i in params.split(',')]
            if checked_button_id == 1:  # 按流程标识验证
                param_type = 'KEY'
            elif checked_button_id == 2:  # 按流程编号验证
                param_type = 'FLOWNO'
            validate_results = self.main_window.kos.root.\
                validate_application(
                    self.env,
                    self.main_window.session_id,
                    self.main_window.token,
                    param_list,
                    param_type,
                    self.tenant_id
                )
            if isinstance(validate_results, int):
                if validate_results == -1:
                    # token失效
                    self.main_window.set_enabled_cascade(False)
                    self.main_window.login_window.show()
                else:
                    # 报错
                    error_validate_param = WindowError(self)
                    if validate_results == 1:
                        err_msg = "环境无效或没有访问权限!"
                    elif validate_results == 2:
                        err_msg = "找不到商户数据库!"
                    else:
                        err_msg = "未知错误!"
                    error_validate_param.set_info(err_msg)
                    error_validate_param.exec()
                return
            elif validate_results:
                self.tree_validation.setVisible(True)
                self.tree_validation.clear()
                for i, p in enumerate(param_list):
                    for r in validate_results:
                        if p == r['validate_param']:
                            item_validation = QtWidgets.QTreeWidgetItem(
                                self.tree_validation
                            )
                            item_validation.setText(0, p)
                            item_validation.setIcon(
                                0, QtGui.QIcon('images/passed.png')
                            )
                            self.validation_results['passed'].append(i)
                            break
                    else:
                        item_validation = QtWidgets.QTreeWidgetItem(
                            self.tree_validation
                        )
                        item_validation.setText(0, p)
                        item_validation.setIcon(
                            0, QtGui.QIcon('images/failed.png')
                        )
                        self.validation_results['failed'].append(i)
            else:
                # 所有都验证失败
                self.tree_validation.setVisible(True)
                self.tree_validation.clear()
                for i, p in enumerate(param_list):
                    item_validation = QtWidgets.QTreeWidgetItem(
                        self.tree_validation
                    )
                    item_validation.setText(0, p)
                    item_validation.setIcon(
                        0, QtGui.QIcon('images/failed.png')
                    )
                    self.validation_results['failed'].append(i)

            total_cnt = len(param_list)
            passed_cnt = len(self.validation_results['passed'])
            if total_cnt == passed_cnt:
                # 所有验证都通过
                self.button_delete.setVisible(True)
                for r in validate_results:
                    self.application_id_list.append(r['ApplicationID'])
            self.tree_validation.setFixedHeight(24 * min([total_cnt, 10]))
            self.label_validation_results.setText(
                '验证结果: '
                '<span style="color:green">成功{}个</span>\t'
                '<span style="color:red">失败{}个</span>'.format(
                    len(self.validation_results['passed']),
                    len(self.validation_results['failed'])
                )
            )
            self.label_validation_results.setVisible(True)
            self.combobox_show_results.setVisible(True)

            self.button_validate.setText('重新验证')
            self.button_validate.setFixedWidth(80)

            self.setFixedSize(self.layout_main.sizeHint())
        else:
            # 没有填写参数
            self.label_info.setText('请先按要求填入参数')
            self.setFixedSize(self.layout_main.sizeHint())

    def select_by_defkey(self):
        self.text_edit_params.setPlaceholderText('请填入需要删除的流程标识(如有多个，请用逗号隔开)')
        self.text_edit_params.setPlainText('')
        self.label_info.setText('')
        self.set_ui_before_validation()

    def select_by_flowno(self):
        self.text_edit_params.setPlaceholderText('请填入需要删除的流程编号(如有多个，请用逗号隔开)')
        self.text_edit_params.setPlainText('')
        self.label_info.setText('')
        self.set_ui_before_validation()

    def set_ui_before_validation(self):
        self.button_validate.setText('验证')
        self.button_validate.setFixedWidth(200)
        self.label_validation_results.setVisible(False)
        self.combobox_show_results.setVisible(False)
        self.tree_validation.setVisible(False)
        self.button_delete.setVisible(False)
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

    def delete_application(self):
        warning_del_application = WindowWarning(self)
        warning_del_application.set_info(
            "确定要删除以上申请吗?"
        )
        is_confirmed = warning_del_application.exec()
        if is_confirmed:
            # 正式删除
            if self.application_id_list:
                delete_result = self.main_window.kos.root.\
                    delete_application(
                        self.env,
                        self.main_window.session_id,
                        self.main_window.token,
                        self.application_id_list,
                        self.tenant_id
                    )
                if delete_result == 0:
                    # 删除成功
                    self.application_id_list = []
                    info_succeeded = WindowInfo(self)
                    info_succeeded.set_info('删除成功!')
                    info_succeeded.exec()
                    self.select_by_flowno()
                elif delete_result == -1:
                    # token失效
                    self.main_window.set_enabled_cascade(False)
                    self.main_window.login_window.show()
                else:
                    # 删除失败
                    error_failed = WindowError(self)
                    error_failed.set_info('删除失败!')
                    error_failed.exec()

    def setEnabled(self, enabled):
        super().setEnabled(enabled)
        self.setFixedSize(self.layout_main.sizeHint())
