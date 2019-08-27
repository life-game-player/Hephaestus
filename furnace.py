import sys
import uuid
import logging
import logging.handlers

from PyQt5 import QtWidgets
import rpyc

from views.window_login import WindowLogin


def main():
    app = QtWidgets.QApplication(sys.argv)

    # 日志设置
    logging_handler = logging.handlers.RotatingFileHandler(
        'logs/furnace.log',
        'a',
        1024 * 1024,
        10,
        'utf-8'
    )
    logging_format = logging.Formatter(
        '%(asctime)s [%(name)s - %(levelname)s] %(message)s'
    )
    logging_handler.setFormatter(logging_format)
    logger = logging.getLogger()
    logger.addHandler(logging_handler)
    logger.setLevel(logging.DEBUG)

    # 获取屏幕大小
    screen_resolution = app.desktop().screenGeometry()
    width, height = screen_resolution.width(), screen_resolution.height()

    session_id = str(uuid.uuid4())
    kos = None
    try:
        kos = rpyc.connect("localhost", 18861)
    except Exception as e:
        logging.error(
            "{} occured".format(type(e).__name__),
            exc_info=True
        )

    window_login = WindowLogin(session_id, kos, width, height)
    window_login.show()
    #window_main = WindowMain(width, height)
    #window_main.show()
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()
