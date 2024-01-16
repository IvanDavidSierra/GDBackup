import os
from PyQt5 import uic
from PyQt5.QtWidgets import QMainWindow
class mainGUI(QMainWindow):
    def __init__(self):
        super().__init__()
        script_dir = os.path.dirname(os.path.abspath(__file__))
        ui_path = os.path.join(script_dir, "GUI", "design.ui")
        uic.loadUi(ui_path, self)
        self.show()


if __name__ == '__main__':
    import sys
    from PyQt5.QtWidgets import QApplication
    app = QApplication(sys.argv)
    ventana = mainGUI()
    sys.exit(app.exec_()