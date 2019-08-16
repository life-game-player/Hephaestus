from pathlib import Path


class QSSSetter:
    @staticmethod
    def set_qss(window, window_path):
        name = Path(window_path).stem
        qss_file = Path('./qss') / ("{}.qss").format(name)
        with open(qss_file, 'r', encoding='utf-8') as f:
            style = f.read()
        window.setStyleSheet(style)
