from PyQt5 import QtWidgets
from PyQt5 import QtCore
from PyQt5 import QtGui

from views.window_dragable import WindowDragable
from views.window_warning import WindowWarning
from views.window_info import WindowInfo
from views.window_error import WindowError
from views.window_analyze_activity import WindowAnalyzeActivity
from qss.qss_setter import QSSSetter
from models.activity import Activity


class WindowAnalyzeResults(WindowDragable):
    def __init__(self, parent):
        super().__init__()

        self.parent = parent
        self.children_windows = dict()
        self.children_windows['activity'] = None
        self.status_brush = {
            0: {
                'name': '未开始',
                'brush': QtGui.QBrush(QtGui.QColor(221, 221, 221))
            },
            1: {
                'name': '运行中',
                'brush': QtGui.QBrush(QtGui.QColor(255, 229, 153))
            },
            2: {
                'name': '已结束',
                'brush': QtGui.QBrush(QtGui.QColor(147, 196, 125))
            },
            3: {
                'name': '已拒绝',
                'brush': QtGui.QBrush(QtGui.QColor(255, 102, 51))
            },
            4: {
                'name': '出错',
                'brush': QtGui.QBrush(QtGui.QColor(255, 0, 0))
            },
            5: {
                'name': '已撤回',
                'brush': QtGui.QBrush(QtGui.QColor(102, 102, 102))
            },
            51: {
                'name': '撤回中',
                'brush': QtGui.QBrush(QtGui.QColor(102, 102, 102))
            },
            6: {
                'name': '已取消',
                'brush': QtGui.QBrush(QtGui.QColor(142, 124, 195))
            },
            61: {
                'name': '取消中',
                'brush': QtGui.QBrush(QtGui.QColor(142, 124, 195))
            },
            999: {
                'name': '终止',
                'brush': QtGui.QBrush(QtGui.QColor(111, 168, 220))
            }
        }

        # 设置窗口无边框
        self.setWindowFlags(
            QtCore.Qt.FramelessWindowHint
        )
        # 设置窗口背景透明
        self.setAttribute(QtCore.Qt.WA_TranslucentBackground)

        # 设置窗口图标
        self.setWindowIcon(self.parent.main_window.icon)

        # 设置窗口大小
        self.window_min_width = 650
        self.window_max_width = 650
        self.window_min_height = 734
        self.window_max_height = 900
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

        parent_pos = self.parent.pos()
        self.setGeometry(
            parent_pos.x() - self.window_min_width,
            parent_pos.y(),
            self.window_min_width,
            self.window_min_height
        )

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
        self.tree_analysis_results = QtWidgets.QTreeWidget(self)
        self.tree_analysis_results.itemClicked.connect(
            self.show_activity_details)
        self.tree_analysis_results.itemExpanded.connect(
            self.expand_analysis_result
        )
        self.tree_analysis_results.setHeaderLabels(
            [
                '名称/值',
                '类型',
                '创建时间',
                '修改时间',
                '状态'
            ]
        )
        self.tree_analysis_results.setColumnCount(5)
        self.tree_analysis_results.header().resizeSection(0, 200)
        self.tree_analysis_results.header().resizeSection(1, 90)
        self.tree_analysis_results.header().resizeSection(2, 150)
        self.tree_analysis_results.header().resizeSection(3, 150)
        self.tree_analysis_results.header().resizeSection(4, 10)
        self.tree_analysis_results.setFixedSize(630, 583)

        self.init_analysis_tree()

        # 布局
        layout_main = QtWidgets.QVBoxLayout()
        layout_legend = QtWidgets.QGridLayout()
        legend_grid_col_cnt = 6
        legend_grid_curr_col = 1
        legend_grid_curr_row = 1
        for dict_status in self.status_brush.values():
            pixmap_status_color = QtGui.QPixmap(20, 20)
            pixmap_status_color.fill(dict_status['brush'].color())
            label_status_name = QtWidgets.QLabel(dict_status['name'])
            label_status_color = QtWidgets.QLabel()
            label_status_color.setPixmap(pixmap_status_color)
            layout_legend.addWidget(
                label_status_name,
                legend_grid_curr_row,
                legend_grid_curr_col
            )
            layout_legend.addWidget(
                label_status_color,
                legend_grid_curr_row,
                legend_grid_curr_col + 1
            )
            legend_grid_curr_col += 2
            if legend_grid_curr_col > legend_grid_col_cnt:
                legend_grid_curr_row += 1
                legend_grid_curr_col = 1
        layout_main.addLayout(layout_legend)
        layout_main.addWidget(self.tree_analysis_results)
        layout_main.addStretch()
        self.widget_body.setLayout(layout_main)

    def close_window(self):
        self.close()
        self.parent.children_windows['anal_result'] = None

    def init_analysis_tree(self):
        self.tree_analysis_results.clear()
        item_variables = QtWidgets.QTreeWidgetItem(self.tree_analysis_results)
        item_variables.setText(0, '流程变量')
        item_variables.setChildIndicatorPolicy(
            QtWidgets.QTreeWidgetItem.ShowIndicator
        )
        item_variables_persistent = QtWidgets.QTreeWidgetItem(item_variables)
        item_variables_persistent.setText(0, '持久层')
        item_variables_persistent.setChildIndicatorPolicy(
            QtWidgets.QTreeWidgetItem.ShowIndicator
        )
        item_variables_runtime = QtWidgets.QTreeWidgetItem(item_variables)
        item_variables_runtime.setText(0, '运行时')
        item_variables_runtime.setChildIndicatorPolicy(
            QtWidgets.QTreeWidgetItem.ShowIndicator
        )
        item_variables_track = QtWidgets.QTreeWidgetItem(item_variables)
        item_variables_track.setText(0, '修改记录')
        item_variables_track.setChildIndicatorPolicy(
            QtWidgets.QTreeWidgetItem.ShowIndicator
        )
        self.tree_analysis_results.expandItem(item_variables)
        item_instances = QtWidgets.QTreeWidgetItem(self.tree_analysis_results)
        item_instances.setText(0, '流程主实例')
        if self.parent.root_instances:
            is_most_recent = True
            for i in self.parent.root_instances:
                item_instance_main = QtWidgets.QTreeWidgetItem(item_instances)
                item_instance_main.setText(0, i['Name'])
                item_instance_main.setText(1, 'Instance')
                item_instance_main.setText(2, str(i['Created']))
                item_instance_main.setText(3, str(i['Modified']))
                for c in range(4):
                    item_instance_main.setBackground(
                        c,
                        self.status_brush[i['Status']]['brush'].color()
                    )
                item_instance_main.setData(
                    4,
                    QtCore.Qt.BackgroundRole,
                    self.status_brush[i['Status']]['brush']
                )
                item_instance_main_detail = QtWidgets.QTreeWidgetItem(
                    item_instance_main
                )
                item_instance_main_detail.setText(0, str(i['ProcInstID']))
                item_instance_main_detail.setText(1, 'ProcInstID')
                item_instance_main_comment = QtWidgets.QTreeWidgetItem(
                    item_instance_main
                )
                item_instance_main_comment.setText(
                    0,
                    i['Comment'] if i['Comment'] else '(无)'
                )
                item_instance_main_comment.setText(1, 'Comment')
                item_init_variables = QtWidgets.QTreeWidgetItem(
                    item_instance_main
                )
                item_init_variables.setText(0, '提交时变量')
                item_init_variables.setChildIndicatorPolicy(
                    QtWidgets.QTreeWidgetItem.ShowIndicator
                )
                item_instance_detail = QtWidgets.QTreeWidgetItem(
                    item_instance_main
                )
                item_instance_detail.setText(0, '流程节点')
                item_instance_detail.setChildIndicatorPolicy(
                    QtWidgets.QTreeWidgetItem.ShowIndicator
                )
                if is_most_recent:
                    self.tree_analysis_results.expandItem(item_instance_main)
                    is_most_recent = False
        else:
            item_instance_main = QtWidgets.QTreeWidgetItem(item_instances)
            item_instance_main.setText(0, '(无)')
        self.tree_analysis_results.expandItem(item_instances)

    def expand_analysis_result(self, item):
        curr_item_text_0 = item.text(0)
        if curr_item_text_0 == '流程节点':
            self.get_instance_detail(
                item,
                int(item.parent().child(0).text(0))
            )
        if curr_item_text_0 == '提交时变量':
            pass
        if curr_item_text_0 == '持久层':
            self.get_persistent_variables(item)
        if curr_item_text_0 == '运行时':
            self.get_runtime_variables(item)
        if curr_item_text_0 == '修改记录':
            pass

    def expand_children(self, item):
        children_cnt = item.childCount()
        for i in range(children_cnt):
            child = item.child(i)
            self.tree_analysis_results.expandItem(child)
            self.expand_children(child)

    def get_runtime_variables(self, item):
        title_font = QtGui.QFont("微软雅黑", 9, QtGui.QFont.Bold)
        item.takeChildren()
        results = self.parent.main_window.kos.root.\
            get_runtime_variables(
                self.parent.main_window.session_id,
                self.parent.main_window.token,
                self.parent.env,
                self.parent.application['ApplicationID'],
                self.parent.tenant_id
            )
        if isinstance(results, int):
            if results == -1:
                # token失效
                self.tree_analysis_results.collapseItem(item)
                self.parent.main_window.set_enabled_cascade(False)
                self.parent.main_window.login_window.show()
                return
        elif results:
            for v in results:
                item_variable = QtWidgets.QTreeWidgetItem(item)
                item_variable.setText(0, v['Name'])
                item_variable.setFont(0, title_font)
                item_variable.setText(1, v['Type'])
                item_variable.setFont(1, title_font)
                item_variable.setText(2, str(v['Created']))
                item_variable.setFont(2, title_font)
                item_variable.setText(3, str(v['Modified']))
                item_variable.setFont(3, title_font)
                item_variable_value = QtWidgets.QTreeWidgetItem(
                    item_variable
                )
                item_variable_value.setText(0, v['Value'])
            self.expand_children(item)
        else:
            # 找不到变量
            item_variable = QtWidgets.QTreeWidgetItem(item)
            item_variable.setText(0, '(无)')
            self.expand_children(item)

    def get_persistent_variables(self, item):
        title_font = QtGui.QFont("微软雅黑", 9, QtGui.QFont.Bold)
        item.takeChildren()
        results = self.parent.main_window.kos.root.\
            get_persistent_variables(
                self.parent.main_window.session_id,
                self.parent.main_window.token,
                self.parent.env,
                self.parent.application['ApplicationID'],
                self.parent.tenant_id
            )
        if isinstance(results, int):
            if results == -1:
                # token失效
                self.tree_analysis_results.collapseItem(item)
                self.parent.main_window.set_enabled_cascade(False)
                self.parent.main_window.login_window.show()
                return
        elif results:
            for v in results:
                item_variable = QtWidgets.QTreeWidgetItem(item)
                item_variable.setText(0, v['Name'])
                item_variable.setFont(0, title_font)
                item_variable.setText(1, v['Type'])
                item_variable.setFont(1, title_font)
                item_variable.setText(2, str(v['Created']))
                item_variable.setFont(2, title_font)
                item_variable.setText(3, str(v['Modified']))
                item_variable.setFont(3, title_font)
                item_variable_value = QtWidgets.QTreeWidgetItem(
                    item_variable
                )
                item_variable_value.setText(0, v['Value'])
            self.expand_children(item)
        else:
            # 找不到变量
            item_variable = QtWidgets.QTreeWidgetItem(item)
            item_variable.setText(0, '(无)')
            self.expand_children(item)

    def get_instance_detail(self, item, instanceid):
        item.takeChildren()
        current_running_activities = list()
        execution_results = self.parent.main_window.kos.root.\
            get_executions(
                self.parent.main_window.session_id,
                self.parent.main_window.token,
                self.parent.env,
                self.parent.tenant_id,
                instanceid
            )
        if isinstance(execution_results, int):
            if execution_results == -1:
                # token失效
                self.tree_analysis_results.collapseItem(item)
                self.parent.main_window.set_enabled_cascade(False)
                self.parent.main_window.login_window.show()
            return
        elif execution_results:
            for e in execution_results:
                current_running_activities.append(e['ActivityID'])
        activity_results = self.parent.main_window.kos.root.\
            get_activities(
                self.parent.main_window.session_id,
                self.parent.main_window.token,
                self.parent.env,
                instanceid,
                self.parent.tenant_id
            )
        if isinstance(activity_results, int):
            if activity_results == -1:
                # token失效
                self.tree_analysis_results.collapseItem(item)
                self.parent.main_window.set_enabled_cascade(False)
                self.parent.main_window.login_window.show()
            return
        elif activity_results:
            dict_activities = {
                0: item
            }
            for a in activity_results:
                item_prev_activity = dict_activities[a['PrevActivityID']]
                item_activity = QtWidgets.QTreeWidgetItem(item_prev_activity)
                item_activity.setText(0, a['Name'])
                if a['ActivityID'] in current_running_activities:
                    item_activity.setIcon(0, QtGui.QIcon('images/running.svg'))
                activity_data = Activity(
                    a['ActivityID'],
                    a['ActivityDefID'],
                    a['ExecutionID'],
                    a['ProcDefID'],
                    a['CallProcInstID'],
                    a['TaskID']
                )
                item_activity.setData(0, QtCore.Qt.UserRole, activity_data)
                item_activity.setText(1, a['ActivityType'])
                item_activity.setText(2, str(a['Created']))
                item_activity.setText(3, str(a['Modified']))
                item_activity.setData(
                    4,
                    QtCore.Qt.BackgroundRole,
                    self.status_brush[a['Status']]['brush']
                )
                dict_activities[a['ActivityID']] = item_activity
            self.expand_children(item)
        else:
            # 找不到变量
            item_activity = QtWidgets.QTreeWidgetItem(item)
            item_activity.setText(0, '(无)')
            self.expand_children(item)

    def show_activity_details(self, item, col):
        data = item.data(0, QtCore.Qt.UserRole)
        if data:
            if isinstance(data, Activity):
                window_analyze_activity = self.children_windows['activity']
                if not window_analyze_activity:
                    window_analyze_activity = WindowAnalyzeActivity(
                        self,
                        data
                    )
                    self.children_windows['activity'] = window_analyze_activity
                window_analyze_activity.show()
