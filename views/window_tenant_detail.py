from PyQt5 import QtWidgets
from PyQt5 import QtCore
from PyQt5 import QtGui

from views.window_dragable import WindowDragable
from views.window_warning import WindowWarning
from views.window_error import WindowError
from views.window_update_passwd import WindowUpdatePass
from qss.qss_setter import QSSSetter


class WindowTenantDetail(WindowDragable):
    def __init__(self, parent, tenant):
        super().__init__()
        self.parent = parent
        self.children_windows = dict()
        self.tenant = tenant

        self.installEventFilter(self)
        self.activated = False

        # 设置窗口无边框
        self.setWindowFlags(
            QtCore.Qt.FramelessWindowHint
        )
        # 设置窗口背景透明
        self.setAttribute(QtCore.Qt.WA_TranslucentBackground)

        # 设置窗口大小
        self.window_min_width = 392
        self.window_max_width = 392
        self.window_min_height = 180
        self.window_max_height = 180
        self.setMinimumSize(self.window_min_width, self.window_min_height)
        self.setMaximumSize(self.window_max_width, self.window_max_height)

        # 设置窗口图标
        self.setWindowIcon(self.parent.icon)

        # 设置窗口子部件
        self.set_body_widget()

        # 窗口组装
        self.layout_main = QtWidgets.QVBoxLayout()
        self.layout_main.addWidget(self.widget_body)
        self.layout_main.setSpacing(0)
        self.layout_main.setContentsMargins(0, 0, 0, 0)
        self.setLayout(self.layout_main)

        parent_pos = parent.pos()
        self.setGeometry(
            parent_pos.x() - self.window_min_width,
            parent_pos.y(),
            self.window_min_width,
            self.window_min_height
        )

        # 设置样式
        QSSSetter.set_qss(self, __file__)

    def set_body_widget(self):
        self.widget_body = QtWidgets.QWidget()
        self.widget_body.setMouseTracking(True)
        self.widget_body.setObjectName('body')
        self.widget_body.setFixedSize(
            self.window_min_width,
            self.window_min_height
        )

        # 组件
        label_tenantid = QtWidgets.QLabel('商户ID')
        label_tenantid.setObjectName('title')
        self.label_tenantid_value = QtWidgets.QLabel()
        self.label_tenantid_value.setTextInteractionFlags(
            QtCore.Qt.TextSelectableByMouse
        )
        self.label_tenantid_value.setObjectName('value')
        label_tenantname = QtWidgets.QLabel('商户名称')
        label_tenantname.setObjectName('title')
        self.label_tenantname_value = QtWidgets.QLabel()
        self.label_tenantname_value.setTextInteractionFlags(
            QtCore.Qt.TextSelectableByMouse
        )
        self.label_tenantname_value.setObjectName('value')
        label_tenant_created = QtWidgets.QLabel('注册时间')
        label_tenant_created.setObjectName('title')
        self.label_tenant_created_value = QtWidgets.QLabel()
        self.label_tenant_created_value.setTextInteractionFlags(
            QtCore.Qt.TextSelectableByMouse
        )
        self.label_tenant_created_value.setObjectName('value')
        label_tenant_expired = QtWidgets.QLabel('过期时间')
        label_tenant_expired.setObjectName('title')
        self.label_tenant_expired_value = QtWidgets.QDateEdit()
        self.label_tenant_expired_value.setReadOnly(True)
        self.label_tenant_expired_value.setFocusPolicy(QtCore.Qt.NoFocus)
        self.label_tenant_expired_value.setDisplayFormat('yyyy-MM-dd')
        self.label_tenant_expired_value.setCalendarPopup(True)
        label_db = QtWidgets.QLabel('所在数据库')
        label_db.setObjectName('title')
        self.label_db_value = QtWidgets.QLabel()
        self.label_db_value.setTextInteractionFlags(
            QtCore.Qt.TextSelectableByMouse
        )
        self.label_db_value.setObjectName('value')
        self.load_tenant_info()

        # 布局管理
        layout = QtWidgets.QVBoxLayout()
        groupbox_form = QtWidgets.QGroupBox()
        layout_form = QtWidgets.QGridLayout()
        layout_form.setSpacing(10)
        layout_form.setColumnStretch(0, 1)
        layout_form.setColumnStretch(1, 10)
        layout_form.addWidget(label_tenantid, 1, 0)
        layout_form.addWidget(self.label_tenantid_value, 1, 1)
        layout_form.addWidget(label_tenantname, 2, 0)
        layout_form.addWidget(self.label_tenantname_value, 2, 1)
        layout_form.addWidget(label_tenant_created, 3, 0)
        layout_form.addWidget(self.label_tenant_created_value, 3, 1)
        layout_form.addWidget(label_tenant_expired, 4, 0)
        layout_form.addWidget(self.label_tenant_expired_value, 4, 1)
        layout_form.addWidget(label_db, 5, 0)
        layout_form.addWidget(self.label_db_value, 5, 1)
        groupbox_form.setLayout(layout_form)
        layout.addStretch(1)
        layout.addWidget(groupbox_form)
        layout.addStretch(1)

        self.widget_body.setLayout(layout)

    def eventFilter(self, source, event):
        if (
            event.type() == QtCore.QEvent.ActivationChange and
            source == self
        ):
            self.activated = not self.activated
            if (
                not self.activated and
                (
                    'warning' not in self.children_windows.keys() or
                    self.children_windows['warning'] is None
                )
            ):
                self.close()
                self.parent.children_windows['tenant_detail'] = None
        return super().eventFilter(source, event)

    def load_tenant_info(self):
        self.label_tenantid_value.setText(str(self.tenant['TenantID']))
        self.label_tenantname_value.setText(self.tenant['MerchantName'])
        self.label_tenant_created_value.setText(str(self.tenant['Created']))
        self.label_tenant_expired_value.setDate(
            QtCore.QDate.fromString(self.tenant['ExpireDate'], 'yyyy-MM-dd')
        )
        self.label_db_value.setText(self.tenant['tenant_db'])
