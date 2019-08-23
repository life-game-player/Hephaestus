import sys
import uuid

from PyQt5 import QtWidgets

from views.window_login import WindowLogin


def main():
    app = QtWidgets.QApplication(sys.argv)

    # 获取屏幕大小
    screen_resolution = app.desktop().screenGeometry()
    width, height = screen_resolution.width(), screen_resolution.height()

    session_id = str(uuid.uuid4())
    window_login = WindowLogin(session_id, width, height)
    window_login.show()
    #window_main = WindowMain(width, height)
    #window_main.show()
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()
