import sys

from PyQt5 import QtWidgets

from views.window_main import WindowMain


def main():
    app = QtWidgets.QApplication(sys.argv)

    # 获取屏幕大小
    screen_resolution = app.desktop().screenGeometry()
    width, height = screen_resolution.width(), screen_resolution.height()

    window_main = WindowMain(width, height)
    window_main.show()
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()
