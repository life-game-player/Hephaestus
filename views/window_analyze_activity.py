from PyQt5 import QtWidgets
from PyQt5 import QtCore
from PyQt5 import QtGui

from views.window_dragable import WindowDragable
from views.window_warning import WindowWarning
from views.window_info import WindowInfo
from views.window_error import WindowError
from qss.qss_setter import QSSSetter
from models.activity import Activity


class WindowAnalyzeActivity(WindowDragable):
    def __init__(self, parent, activity):
        super().__init__()
        self.parent = parent
        self.parent_activity = activity

        self.installEventFilter(self)
        self.activated = False

        # 设置窗口无边框
        self.setWindowFlags(
            QtCore.Qt.FramelessWindowHint
        )
        # 设置窗口背景透明
        self.setAttribute(QtCore.Qt.WA_TranslucentBackground)

        # 设置窗口大小
        self.window_min_width = 660
        self.window_max_width = 660
        self.window_min_height = 150
        self.window_max_height = 800
        self.setMinimumSize(self.window_min_width, self.window_min_height)
        self.setMaximumSize(self.window_max_width, self.window_max_height)

        # 设置窗口图标
        self.setWindowIcon(self.parent.parent.main_window.icon)

        # 设置窗口子部件
        self.set_body_widget()

        # 窗口组装
        self.layout_main = QtWidgets.QVBoxLayout()
        self.layout_main.addWidget(self.widget_body)
        self.layout_main.setSpacing(0)
        self.layout_main.setContentsMargins(0, 0, 0, 0)
        self.setLayout(self.layout_main)

        parent_pos = self.parent.pos()
        self.move(
            parent_pos.x() + self.parent.width(),
            parent_pos.y() + self.parent.parent.height()
        )

        # 设置样式
        QSSSetter.set_qss(self, __file__)

    def set_body_widget(self):
        self.widget_body = QtWidgets.QWidget(self)
        self.widget_body.setMinimumSize(
            self.window_min_width,
            self.window_min_height
        )
        self.widget_body.setMaximumSize(
            self.window_max_width,
            self.window_max_height
        )
        self.widget_body.setMouseTracking(True)
        self.widget_body.setObjectName('body')

        # 组件
        self.widget_activityinfo = QtWidgets.QWidget()
        layout_info = QtWidgets.QVBoxLayout()
        layout_info.setContentsMargins(0, 0, 0, 0)
        layout_info.setSpacing(0)
        groupbox_info = QtWidgets.QGroupBox()
        layout_activity = QtWidgets.QGridLayout()
        layout_activity.setHorizontalSpacing(30)

        self.splitter_line = QtWidgets.QFrame()
        self.splitter_line.setFrameShape(QtWidgets.QFrame.HLine)
        self.splitter_line.setFrameShadow(QtWidgets.QFrame.Sunken)
        label_id = QtWidgets.QLabel('ActivityID')
        label_id.setObjectName('title')
        self.label_id_value = QtWidgets.QLabel()
        self.label_id_value.setTextInteractionFlags(
            QtCore.Qt.TextSelectableByMouse
        )
        label_defid = QtWidgets.QLabel('ActivityDefID')
        label_defid.setObjectName('title')
        self.label_defid_value = QtWidgets.QLabel()
        self.label_defid_value.setFixedWidth(200)
        self.label_defid_value.setTextInteractionFlags(
            QtCore.Qt.TextSelectableByMouse
        )
        label_executionid = QtWidgets.QLabel('ExecutionID')
        label_executionid.setObjectName('title')
        self.label_executionid_value = QtWidgets.QLabel()
        self.label_executionid_value.setTextInteractionFlags(
            QtCore.Qt.TextSelectableByMouse
        )
        label_procdefid = QtWidgets.QLabel('ProcDefID')
        label_procdefid.setObjectName('title')
        self.label_procdefid_value = QtWidgets.QLabel()
        self.label_procdefid_value.setTextInteractionFlags(
            QtCore.Qt.TextSelectableByMouse
        )
        self.label_taskid = QtWidgets.QLabel('TaskID')
        self.label_taskid.setObjectName('title')
        self.label_taskid_value = QtWidgets.QLabel()
        self.label_taskname = QtWidgets.QLabel('任务名称')
        self.label_taskname.setObjectName('title')
        self.label_taskname_value = QtWidgets.QLabel()
        self.label_taskstart = QtWidgets.QLabel('任务开始时间')
        self.label_taskstart.setObjectName('title')
        self.label_taskstart_value = QtWidgets.QLabel()
        self.label_taskend = QtWidgets.QLabel('任务结束时间')
        self.label_taskend.setObjectName('title')
        self.label_taskend_value = QtWidgets.QLabel()
        self.label_task_deletereason = QtWidgets.QLabel('DeleteReason')
        self.label_task_deletereason.setObjectName('title')
        self.label_task_deletereason_value = QtWidgets.QLabel()
        self.label_task_outcome = QtWidgets.QLabel('Outcome')
        self.label_task_outcome.setObjectName('title')
        self.label_task_outcome_value = QtWidgets.QLabel()

        layout_activity.addWidget(label_procdefid, 1, 1)
        layout_activity.addWidget(self.label_procdefid_value, 1, 2)
        layout_activity.addWidget(label_executionid, 1, 3)
        layout_activity.addWidget(self.label_executionid_value, 1, 4)
        layout_activity.addWidget(label_id, 2, 1)
        layout_activity.addWidget(self.label_id_value, 2, 2)
        layout_activity.addWidget(label_defid, 3, 1)
        layout_activity.addWidget(self.label_defid_value, 3, 2)

        layout_activity.addWidget(self.splitter_line, 4, 1, 1, 4)
        layout_activity.addWidget(self.label_taskid, 5, 1)
        layout_activity.addWidget(self.label_taskid_value, 5, 2)
        layout_activity.addWidget(self.label_taskname, 5, 3)
        layout_activity.addWidget(self.label_taskname_value, 5, 4)
        layout_activity.addWidget(self.label_taskstart, 6, 1)
        layout_activity.addWidget(self.label_taskstart_value, 6, 2)
        layout_activity.addWidget(self.label_taskend, 6, 3)
        layout_activity.addWidget(self.label_taskend_value, 6, 4)
        layout_activity.addWidget(self.label_task_deletereason, 7, 1)
        layout_activity.addWidget(
            self.label_task_deletereason_value, 7, 2)
        layout_activity.addWidget(self.label_task_outcome, 7, 3)
        layout_activity.addWidget(self.label_task_outcome_value, 7, 4)

        self.widget_activityinfo.setLayout(layout_activity)
        layout_info.addWidget(self.widget_activityinfo)
        groupbox_info.setLayout(layout_info)

        self.tree_child_instance = QtWidgets.QTreeWidget()
        self.tree_child_instance.setFixedSize(642, 168)
        self.tree_child_instance.setHeaderLabels(
            [
                '名称/值',
                '类型',
                '创建时间',
                '修改时间',
                '状态'
            ]
        )
        self.tree_child_instance.setColumnCount(5)
        self.tree_child_instance.header().resizeSection(0, 200)
        self.tree_child_instance.header().resizeSection(1, 90)
        self.tree_child_instance.header().resizeSection(2, 150)
        self.tree_child_instance.header().resizeSection(3, 150)
        self.tree_child_instance.header().resizeSection(4, 10)

        # 布局
        layout_main = QtWidgets.QVBoxLayout()
        layout_main.addWidget(groupbox_info)
        layout_main.addWidget(self.tree_child_instance)

        # 初始化
        self.load_activity(self.parent_activity)

        self.widget_body.setLayout(layout_main)

    def eventFilter(self, source, event):
        if (
            event.type() == QtCore.QEvent.ActivationChange and
            source == self
        ):
            self.activated = not self.activated
            if (
                not self.activated
            ):
                self.close()
                self.parent.children_windows['activity'] = None
        return super().eventFilter(source, event)

    def set_taskinfo_visible(self, is_visible):
        self.splitter_line.setVisible(is_visible)
        self.label_taskid.setVisible(is_visible)
        self.label_taskid_value.setVisible(is_visible)
        self.label_taskname.setVisible(is_visible)
        self.label_taskname_value.setVisible(is_visible)
        self.label_taskstart.setVisible(is_visible)
        self.label_taskstart_value.setVisible(is_visible)
        self.label_taskend.setVisible(is_visible)
        self.label_taskend_value.setVisible(is_visible)
        self.label_task_deletereason.setVisible(is_visible)
        self.label_task_deletereason_value.setVisible(is_visible)
        self.label_task_outcome.setVisible(is_visible)
        self.label_task_outcome_value.setVisible(is_visible)

    def load_activity(self, activity, from_child=False):
        self.label_id_value.setText(str(activity.id))
        self.label_defid_value.setText(str(activity.defid))
        self.label_executionid_value.setText(str(activity.executionid))
        self.label_procdefid_value.setText(str(activity.procdefid))

        if activity.taskid > 0:
            task_results = self.parent.parent.main_window.kos.root.\
                get_task(
                    self.parent.parent.main_window.session_id,
                    self.parent.parent.main_window.token,
                    self.parent.parent.env,
                    self.parent.parent.tenant_id,
                    activity.taskid
                )
            if isinstance(task_results, int):
                if task_results == -1:
                    # token失效
                    self.setEnabled(False)
                    self.parent.parent.main_window.set_enabled_cascade(False)
                    self.parent.parent.main_window.login_window.show()
                return
            elif task_results:
                task = task_results[0]
                self.label_taskid_value.setText(str(activity.taskid))
                self.label_taskname_value.setText(task['Name'])
                self.label_taskstart_value.setText(str(task['StartTime']))
                self.label_taskend_value.setText(str(task['EndTime']))
                self.label_task_deletereason_value.setText(
                    task['DeleteReason'])
                self.label_task_outcome_value.setText(task['Outcome'])
                self.set_taskinfo_visible(True)
            else:
                self.set_taskinfo_visible(False)
        else:
            self.set_taskinfo_visible(False)

        if not from_child:
            if activity.child_procinstid:
                item_child_instance_node = QtWidgets.QTreeWidgetItem(
                    self.tree_child_instance)
                item_child_instance_node.setText(0, '流程子实例')

                instance_results = self.parent.parent.main_window.kos.root.\
                    get_instance(
                        self.parent.parent.main_window.session_id,
                        self.parent.parent.main_window.token,
                        self.parent.parent.env,
                        self.parent.parent.tenant_id,
                        activity.child_procinstid
                    )
                if isinstance(instance_results, int):
                    if instance_results == -1:
                        # token失效
                        self.setEnabled(False)
                        self.parent.parent.main_window.set_enabled_cascade(
                            False)
                        self.parent.parent.main_window.login_window.show()
                    return
                elif instance_results:
                    child_instance = instance_results[0]
                    item_child_instance = QtWidgets.QTreeWidgetItem(
                        item_child_instance_node)
                    item_child_instance.setText(0, child_instance['Name'])
                    item_child_instance.setText(1, 'Instance')
                    item_child_instance.setText(
                        2, str(child_instance['Created']))
                    item_child_instance.setText(
                        3, str(child_instance['Modified']))
                    item_child_instance.setData(
                        4,
                        QtCore.Qt.BackgroundRole,
                        self.parent.status_brush[child_instance['Status']]['brush']
                    )
                    item_child_instance_id = QtWidgets.QTreeWidgetItem(
                        item_child_instance
                    )
                    item_child_instance_id.setText(
                        0,
                        str(child_instance['ProcInstID'])
                    )
                    item_child_instance_id.setText(1, 'ProcInstID')
                    item_child_instance_msg = QtWidgets.QTreeWidgetItem(
                        item_child_instance)
                    item_child_instance_msg.setText(
                        0,
                        child_instance['Comment']
                        if child_instance['Comment'] else '(无)'
                    )
                    item_child_instance_msg.setText(1, 'Comment')
                    item_child_instance_activity_node = QtWidgets.QTreeWidgetItem(
                        item_child_instance_node
                    )
                    item_child_instance_activity_node.setText(0, '流程节点')
                    current_running_activities = list()
                    execution_results = self.parent.parent.main_window.kos.root.\
                        get_executions(
                            self.parent.parent.main_window.session_id,
                            self.parent.parent.main_window.token,
                            self.parent.parent.env,
                            self.parent.parent.tenant_id,
                            activity.child_procinstid
                        )
                    if isinstance(current_running_activities, int):
                        if execution_results == -1:
                            # token失效
                            self.setEnabled(False)
                            self.parent.parent.main_window.\
                                set_enabled_cascade(False)
                            self.parent.parent.main_window.login_window.show()
                        return
                    elif execution_results:
                        for e in execution_results:
                            current_running_activities.append(e['ActivityID'])
                    activity_results = self.parent.parent.main_window.kos.root.\
                        get_activities(
                            self.parent.parent.main_window.session_id,
                            self.parent.parent.main_window.token,
                            self.parent.parent.env,
                            child_instance['ProcInstID'],
                            self.parent.parent.tenant_id
                        )
                    if isinstance(activity_results, int):
                        if activity_results == -1:
                            # token失效
                            self.setEnabled(False)
                            self.parent.parent.main_window.\
                                set_enabled_cascade(False)
                            self.parent.parent.main_window.login_window.show()
                        return
                    elif activity_results:
                        dict_activities = {
                            0: item_child_instance_activity_node
                        }
                        for a in activity_results:
                            item_prev_activity = \
                                dict_activities[a['PrevActivityID']]
                            item_activity = QtWidgets.QTreeWidgetItem(
                                item_prev_activity)
                            item_activity.setText(0, a['Name'])
                            if a['ActivityID'] in current_running_activities:
                                item_activity.setIcon(
                                    0,
                                    QtGui.QIcon('images/running.svg')
                                )
                            activity_data = Activity(
                                a['ActivityID'],
                                a['ActivityDefID'],
                                a['ExecutionID'],
                                a['ProcDefID'],
                                a['CallProcInstID'],
                                a['TaskID']
                            )
                            item_activity.setData(
                                0,
                                QtCore.Qt.UserRole,
                                activity_data
                            )
                            item_activity.setText(1, a['ActivityType'])
                            item_activity.setText(2, str(a['Created']))
                            item_activity.setText(3, str(a['Modified']))
                            item_activity.setData(
                                4,
                                QtCore.Qt.BackgroundRole,
                                self.parent.status_brush[a['Status']]['brush']
                            )
                            dict_activities[a['ActivityID']] = item_activity
                    self.tree_child_instance.expandAll()
                    self.tree_child_instance.itemClicked.connect(
                        self.show_activity_details)
                else:
                    self.tree_child_instance.setVisible(False)
            else:
                self.tree_child_instance.setVisible(False)

    def show_activity_details(self, item, col):
        data = item.data(0, QtCore.Qt.UserRole)
        if data:
            if isinstance(data, Activity):
                self.load_activity(data, True)
        elif item.text(0) == '流程节点':
            self.load_activity(self.parent_activity)
