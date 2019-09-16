import sys
import uuid

from PyQt5 import QtWidgets
import rpyc

from views.window_login import WindowLogin
from clio import logger


def main():
    app = QtWidgets.QApplication(sys.argv)

    # 获取屏幕大小
    screen_resolution = app.desktop().screenGeometry()
    width, height = screen_resolution.width(), screen_resolution.height()

    session_id = str(uuid.uuid4())
    kos = None
    try:
        kos = rpyc.connect("localhost", 18861)
    except Exception as e:
        logger.error(
            "{} occured".format(type(e).__name__),
            exc_info=True
        )

    window_login = WindowLogin(session_id, kos, width, height)
    window_login.show()
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()
