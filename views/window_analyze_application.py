from PyQt5 import QtWidgets
from PyQt5 import QtCore
from PyQt5 import QtGui

from views.window_dragable import WindowDragable
from views.window_warning import WindowWarning
from views.window_info import WindowInfo
from views.window_error import WindowError
from views.window_analyze_results import WindowAnalyzeResults
from views.window_select_application import WindowSelectApplication

from qss.qss_setter import QSSSetter


class WindowAnalyzeApplication(WindowDragable):
    def __init__(self, main_window, tenant_id, tenant_name, env):
        super().__init__()

        self.main_window = main_window
        self.env = env
        self.tenant_id = tenant_id
        self.tenant_name = tenant_name
        self.application_status = {
            1: '运行中',
            2: '已结束',
            3: '已拒绝',
            4: '出错',
            5: '已撤回',
            51: '撤回中',
            6: '已取消',
            61: '取消中',
            999: '终止'
        }
        self.children_windows = dict()
        self.children_windows['anal_result'] = None
        self.children_windows['select_application'] = None

        # 设置窗口无边框
        self.setWindowFlags(
            QtCore.Qt.FramelessWindowHint
        )
        # 设置窗口背景透明
        self.setAttribute(QtCore.Qt.WA_TranslucentBackground)

        # 设置窗口图标
        self.setWindowIcon(self.main_window.icon)

        # 设置窗口大小
        self.window_min_width = 500
        self.window_max_width = 500
        self.window_min_height = 135
        self.window_max_height = 800
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
        label_tenant = QtWidgets.QLabel('商户')
        label_tenant.setObjectName('base')
        self.label_tenant_value = QtWidgets.QLabel(self.tenant_name)
        self.label_tenant_value.setObjectName('base')
        label_flowno = QtWidgets.QLabel('流程编号')
        label_flowno.setObjectName('base')
        self.lineedit_flowno = QtWidgets.QLineEdit()
        self.lineedit_flowno.setFixedWidth(300)
        button_analyze = QtWidgets.QPushButton('分   析')
        button_analyze.setObjectName('analyze')
        button_analyze.setFixedSize(80, 25)
        button_analyze.clicked.connect(self.analyze)
        self.label_info = QtWidgets.QLabel()
        self.label_info.setObjectName('info')

        self.widget_applicationinfo = QtWidgets.QWidget()
        layout_applicationinfo = QtWidgets.QVBoxLayout()
        layout_applicationinfo.setContentsMargins(0, 0, 0, 0)
        layout_applicationinfo.setSpacing(0)
        label_applicationid = QtWidgets.QLabel('ApplicationID')
        label_applicationid.setObjectName('title')
        self.label_applicationid_value = QtWidgets.QLabel()
        self.label_applicationid_value.setTextInteractionFlags(
            QtCore.Qt.TextSelectableByMouse
        )
        label_key = QtWidgets.QLabel('流程标识')
        label_key.setObjectName('title')
        self.label_key_value = QtWidgets.QLabel()
        self.label_key_value.setTextInteractionFlags(
            QtCore.Qt.TextSelectableByMouse
        )
        label_applicant = QtWidgets.QLabel('申请人')
        label_applicant.setObjectName('title')
        self.label_applicant_value = QtWidgets.QLabel()
        self.label_applicant_value.setTextInteractionFlags(
            QtCore.Qt.TextSelectableByMouse
        )
        label_status = QtWidgets.QLabel('状态')
        label_status.setObjectName('title')
        self.label_status_value = QtWidgets.QLabel()
        label_created = QtWidgets.QLabel('创建时间')
        label_created.setObjectName('title')
        self.label_created_value = QtWidgets.QLabel()
        self.label_created_value.setTextInteractionFlags(
            QtCore.Qt.TextSelectableByMouse
        )
        label_modified = QtWidgets.QLabel('修改时间')
        label_modified.setObjectName('title')
        self.label_modified_value = QtWidgets.QLabel()
        self.label_modified_value.setTextInteractionFlags(
            QtCore.Qt.TextSelectableByMouse
        )
        splitter_line = QtWidgets.QFrame()
        splitter_line.setFrameShape(QtWidgets.QFrame.HLine)
        splitter_line.setFrameShadow(QtWidgets.QFrame.Sunken)
        label_error = QtWidgets.QLabel('报错信息')
        label_error.setObjectName('title')
        self.label_error_value = QtWidgets.QPlainTextEdit()
        self.label_error_value.setFixedHeight(100)
        self.label_error_value.setReadOnly(True)
        groupbox_application = QtWidgets.QGroupBox()
        layout_application = QtWidgets.QGridLayout()
        layout_application.setHorizontalSpacing(30)
        layout_application.addWidget(label_applicationid, 1, 1)
        layout_application.addWidget(self.label_applicationid_value, 1, 2)
        layout_application.addWidget(label_status, 1, 3)
        layout_application.addWidget(self.label_status_value, 1, 4)
        layout_application.addWidget(label_key, 2, 1)
        layout_application.addWidget(self.label_key_value, 2, 2)
        layout_application.addWidget(label_applicant, 3, 1)
        layout_application.addWidget(self.label_applicant_value, 3, 2)
        layout_application.addWidget(label_created, 4, 1)
        layout_application.addWidget(self.label_created_value, 4, 2, 1, 3)
        layout_application.addWidget(label_modified, 5, 1)
        layout_application.addWidget(self.label_modified_value, 5, 2, 1, 3)
        layout_application.addWidget(splitter_line, 6, 1, 1, 4)
        layout_application.addWidget(label_error, 7, 1)
        layout_application.addWidget(self.label_error_value, 7, 2, 1, 3)
        groupbox_application.setLayout(layout_application)
        layout_applicationinfo.addWidget(groupbox_application)
        self.widget_applicationinfo.setLayout(layout_applicationinfo)

        # 布局
        layout_main = QtWidgets.QVBoxLayout()
        groupbox_baseinfo = QtWidgets.QGroupBox()
        layout_baseinfo = QtWidgets.QGridLayout()
        layout_baseinfo.setVerticalSpacing(15)
        layout_baseinfo.addWidget(label_tenant, 1, 1)
        layout_baseinfo.addWidget(self.label_tenant_value, 1, 2)
        layout_baseinfo.addWidget(label_flowno, 2, 1)
        layout_flowno = QtWidgets.QHBoxLayout()
        layout_flowno.addWidget(self.lineedit_flowno)
        layout_flowno.addStretch(1)
        layout_flowno.addWidget(button_analyze)
        layout_flowno.addStretch(1)
        layout_baseinfo.addLayout(layout_flowno, 2, 2)
        layout_baseinfo.addWidget(self.label_info, 3, 2)
        layout_baseinfo.setColumnMinimumWidth(1, 60)
        groupbox_baseinfo.setLayout(layout_baseinfo)
        layout_main.addWidget(groupbox_baseinfo)
        layout_main.addWidget(self.widget_applicationinfo)
        layout_main.addStretch()

        # 初始化
        self.widget_applicationinfo.setVisible(False)
        self.label_info.setVisible(False)

        self.widget_body.setLayout(layout_main)

    def close_window(self):
        if self.children_windows['anal_result']:
            self.children_windows['anal_result'].close()
        self.main_window.children_windows['anal_app'] = None
        self.close()

    def setEnabled(self, enabled):
        for c in self.children_windows.values():
            if c:
                c.setEnabled(enabled)
        super().setEnabled(enabled)

    def analyze(self):
        self.label_info.setVisible(False)
        self.widget_applicationinfo.setVisible(False)
        self.adjustSize()
        flowno = self.lineedit_flowno.text()
        if not flowno:
            self.label_info.setText('请填写流程编号!')
            self.label_info.setVisible(True)
            self.adjustSize()
            return
        self.application = None
        self.root_instances = None
        application_results = self.main_window.kos.root.get_application(
            self.main_window.session_id,
            self.main_window.token,
            self.env,
            flowno,
            self.tenant_id
        )
        if isinstance(application_results, int):
            if application_results == -1:
                # token失效
                self.main_window.set_enabled_cascade(False)
                self.main_window.login_window.show()
            else:
                # 报错
                if application_results == 1:
                    self.label_info.setText('环境无效或没有访问权限!')
                elif application_results == 2:
                    self.label_info.setText('找不到商户数据库!')
                else:
                    self.label_info.setText('未知错误!')
                self.label_info.setVisible(True)
            return
        elif application_results:
            if len(application_results) > 1:
                # 同一flowno对应多个申请,需要进一步指定
                window_select_application = self.children_windows[
                    'select_application'
                ]
                if window_select_application:
                    window_select_application.close()
                window_select_application = WindowSelectApplication(
                    self,
                    application_results
                )
                self.children_windows['select_application'] = \
                    window_select_application
                result = window_select_application.exec()
                if result == 1:
                    # token失效
                    self.main_window.set_enabled_cascade(False)
                    self.main_window.login_window.show()
                    return
                elif result == 2:
                    # 查询root_instance错误
                    return
            else:
                self.application = application_results[0]
                root_instances_results = self.main_window.kos.root.\
                    get_root_instances(
                        self.main_window.session_id,
                        self.main_window.token,
                        self.env,
                        self.application['ApplicationID'],
                        self.tenant_id
                    )
                if (
                    not isinstance(root_instances_results, int) and
                    root_instances_results
                ):
                    self.root_instances = root_instances_results
            self.label_applicationid_value.setText(
                str(self.application['ApplicationID'])
            )
            self.label_applicant_value.setText(
                '{} ({})'.format(
                    self.application['ApplicantUserName'],
                    self.application['ApplicantUserID']
                )
            )
            self.label_status_value.setText(
                self.application_status[self.application['Status']]
            )
            self.label_key_value.setText(self.application['DefKey'])
            self.label_created_value.setText(
                str(self.application['Created'])
            )
            self.label_modified_value.setText(
                str(self.application['Modified'])
            )
            if self.application['Comment']:
                self.label_error_value.setPlainText(
                    self.application['Comment']
                )
            else:
                self.label_error_value.setPlainText('(无)')
            self.widget_applicationinfo.setVisible(True)
            self.adjustSize()
            window_analyze_results = self.children_windows['anal_result']
            if window_analyze_results:
                window_analyze_results.close()
            window_analyze_results = WindowAnalyzeResults(self)
            self.children_windows['anal_result'] = window_analyze_results
            window_analyze_results.show()
        else:
            # 找不到流程
            self.label_info.setText('找不到该流程!')
            self.label_info.setVisible(True)
            self.adjustSize()
