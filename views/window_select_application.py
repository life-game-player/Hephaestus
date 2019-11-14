from PyQt5 import QtWidgets
from PyQt5 import QtCore

from qss.qss_setter import QSSSetter


class WindowSelectApplication(QtWidgets.QDialog):
    def __init__(self, parent, applications):
        super().__init__(parent, QtCore.Qt.FramelessWindowHint)
        self.parent = parent
        self.applications = applications

        # 设置窗口大小
        self.window_min_width = 500
        self.window_max_width = 500
        self.window_min_height = 220
        self.window_max_height = 220
        self.setMinimumSize(self.window_min_width, self.window_min_height)
        self.setMaximumSize(self.window_max_width, self.window_max_height)

        # 设置窗口背景透明
        self.setAttribute(QtCore.Qt.WA_TranslucentBackground)

        # 组件
        widget_applications = QtWidgets.QWidget()
        widget_applications.setObjectName('applications')
        widget_applications.setMinimumSize(
            self.window_min_width, self.window_min_height
        )
        widget_applications.setMaximumSize(
            self.window_max_width, self.window_max_height
        )
        button_box = QtWidgets.QDialogButtonBox(
            QtWidgets.QDialogButtonBox.Ok
        )
        button_box.accepted.connect(self.accept)
        button_ok = button_box.button(QtWidgets.QDialogButtonBox.Ok)
        button_ok.setText('确 定')
        button_ok.setFixedSize(70, 30)
        button_ok.setStyleSheet(
            'QPushButton{'
            'border-radius:2px;'
            'font-size:14px;'
            'font-family:"微软雅黑";'
            'color:white;'
            'background-color:rgba(255,102,51,90%);'
            '}'
        )
        self.table_applications = QtWidgets.QTableWidget()
        self.table_applications.setSelectionBehavior(
            QtWidgets.QAbstractItemView.SelectRows
        )
        self.table_applications.setSelectionMode(
            QtWidgets.QAbstractItemView.SingleSelection
        )
        self.table_applications.horizontalHeader().setHighlightSections(False)
        self.table_applications.horizontalHeader().setSectionResizeMode(
            QtWidgets.QHeaderView.Fixed
        )
        self.table_applications.setColumnCount(6)
        self.table_applications.setHorizontalHeaderLabels(
            ['ID', '流程标识', '申请人', '状态', '创建时间', '修改时间']
        )
        self.table_applications.setFixedHeight(100)
        self.table_applications.setRowCount(len(self.applications))
        self.table_applications.verticalHeader().setVisible(False)
        self.table_applications.setColumnWidth(0, 150)
        self.table_applications.setColumnWidth(1, 100)
        self.table_applications.setColumnWidth(2, 100)
        self.table_applications.setColumnWidth(3, 30)
        self.table_applications.setColumnWidth(4, 180)
        self.table_applications.setColumnWidth(5, 180)
        self.table_applications.setEditTriggers(
            QtWidgets.QTableWidget.NoEditTriggers)
        for row, a in enumerate(self.applications):
            item_id = QtWidgets.QTableWidgetItem(str(a['ApplicationID']))
            item_defkey = QtWidgets.QTableWidgetItem(a['DefKey'])
            item_user = QtWidgets.QTableWidgetItem(a['ApplicantUserName'])
            item_status = QtWidgets.QTableWidgetItem(str(a['Status']))
            item_created = QtWidgets.QTableWidgetItem(str(a['Created']))
            item_modified = QtWidgets.QTableWidgetItem(str(a['Modified']))
            self.table_applications.setItem(row, 0, item_id)
            self.table_applications.setItem(row, 1, item_defkey)
            self.table_applications.setItem(row, 2, item_user)
            self.table_applications.setItem(row, 3, item_status)
            self.table_applications.setItem(row, 4, item_created)
            self.table_applications.setItem(row, 5, item_modified)

        label_hint = QtWidgets.QLabel('当前流程编号对应多个流程，请选择一个进行分析')
        label_hint.setObjectName('hint')
        self.label_info = QtWidgets.QLabel()
        self.label_info.setObjectName('info')
        self.label_info.setVisible(False)

        # 组件布局
        layout = QtWidgets.QVBoxLayout()
        layout.setSpacing(10)
        layout.setContentsMargins(10, 15, 10, 15)
        layout.addWidget(label_hint)
        layout.addWidget(self.table_applications)
        layout_info = QtWidgets.QHBoxLayout()
        layout_info.addStretch(1)
        layout_info.addWidget(self.label_info)
        layout_info.addStretch(1)
        layout.addLayout(layout_info)
        layout.addWidget(button_box)
        widget_applications.setLayout(layout)

        # 主布局
        layout_main = QtWidgets.QVBoxLayout()
        layout_main.setSpacing(0)
        layout_main.setContentsMargins(0, 0, 0, 0)
        layout_main.addWidget(widget_applications)
        self.setLayout(layout_main)

        # 设置样式
        QSSSetter.set_qss(self, __file__)

    def accept(self):
        selected_items = self.table_applications.selectedItems()
        if selected_items:
            selected_id = int(selected_items[0].text())
            for a in self.applications:
                if a['ApplicationID'] == selected_id:
                    self.parent.application = a
                    break
            root_instances_results = self.parent.main_window.kos.root.\
                get_root_instances(
                    self.parent.main_window.session_id,
                    self.parent.main_window.token,
                    self.parent.env,
                    self.parent.application['ApplicationID'],
                    self.parent.tenant_id
                )
            result = 0
            if isinstance(root_instances_results, int):
                if root_instances_results == -1:
                    # token失效
                    result = 1
                else:
                    result = 2
            elif root_instances_results:
                self.parent.root_instances = root_instances_results
            self.parent.children_windows['select_application'] = None
            self.done(result)
        else:
            # 提示未选择任何申请
            self.label_info.setText('请选中一个流程!')
            self.label_info.setVisible(True)
