from PyQt5 import QtWidgets
from PyQt5 import QtCore
from PyQt5.QtGui import QCursor


class WindowDragable(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()

        # 鼠标状态
        self.setMouseTracking(True)
        self.edge_range = 4
        self.mouse_pos = None  # 鼠标相对于窗口的位置
        self.is_left_button_pressed = False

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
                    rect_new.setLeft(mouse_x)

                if (
                    self.window_min_height <
                    rightbottom_point.y() - mouse_y <
                    self.window_max_height
                ):
                    rect_new.setTop(mouse_y)

            if self.mouse_pos == 'TOP':
                if (
                    self.window_min_height <
                    rightbottom_point.y() - mouse_y <
                    self.window_max_height
                ):
                    rect_new.setTop(mouse_y)

            if self.mouse_pos == 'RIGHTBOTTOM':
                if (
                    self.window_min_width <
                    mouse_x - topleft_point.x() <
                    self.window_max_width
                ):
                    rect_new.setRight(mouse_x)
                if (
                    self.window_min_height <
                    mouse_y - topleft_point.y() <
                    self.window_max_height
                ):
                    rect_new.setBottom(mouse_y)

            if self.mouse_pos == 'BOTTOM':
                if (
                    self.window_min_height <
                    mouse_y - topleft_point.y() <
                    self.window_max_height
                ):
                    rect_new.setBottom(mouse_y)

            if self.mouse_pos == 'RIGHTTOP':
                if (
                    self.window_min_width <
                    mouse_x - topleft_point.x() <
                    self.window_max_width
                ):
                    rect_new.setRight(mouse_x)
                if (
                    self.window_min_height <
                    rightbottom_point.y() - mouse_y <
                    self.window_max_height
                ):
                    rect_new.setTop(mouse_y)

            if self.mouse_pos == 'LEFTBOTTOM':
                if (
                    self.window_min_width <
                    rightbottom_point.x() - mouse_x <
                    self.window_max_width
                ):
                    rect_new.setLeft(mouse_x)
                if (
                    self.window_min_height <
                    mouse_y - topleft_point.y() <
                    self.window_max_height
                ):
                    rect_new.setBottom(mouse_y)

            self.setGeometry(rect_new)

    def mouseReleaseEvent(self, event):
        if event.button() == QtCore.Qt.LeftButton:
            self.mouse_pos = None
            self.is_left_button_pressed = False
            self.setCursor(
                QCursor(QtCore.Qt.ArrowCursor)
            )
            event.accept()
