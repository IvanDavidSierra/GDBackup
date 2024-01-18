import os
import sys
from PyQt5 import uic
from PyQt5.QtWidgets import QMainWindow, QApplication, QWidget, QPushButton, QFrame, QLabel, QFileDialog


class mainGUI(QMainWindow):
    def __init__(self):
        super().__init__()

        script_dir = os.path.dirname(os.path.abspath(__file__))
        gui_path = os.path.join(script_dir, "GUI", "design.ui")
        uic.loadUi(gui_path, self)

        self.init_ui()

        self.setFixedSize(722, 456)
        self.show()

    def init_ui(self):
        central_widget = self.findChild(QWidget, 'miCentralWidget')
        if central_widget:
            frame = central_widget.findChild(QFrame, 'frame')
            if frame:
                selectFolder = frame.findChild(QPushButton, 'selectFolder')
                if selectFolder:
                    selectFolder.clicked.connect(self.select_location)
                else:
                    print("Error: No se encontró el botón 'selectFolder'")
            else:
                print("Error: No se encontró el QFrame 'frame' dentro del QWidget 'miCentralWidget'")
        else:
            print("Error: No se encontró el QWidget 'miCentralWidget'")

    def select_location(self):
        folder_path = QFileDialog.getExistingDirectory(self, 'backupLocation')
        central_widget = self.findChild(QWidget, 'miCentralWidget')
        if central_widget:
            frame = central_widget.findChild(QFrame, 'frame')
            if frame:
                backupLocation = frame.findChild(QLabel, 'backupLocation')
                if backupLocation:
                    backupLocation.setText(folder_path)
                else:
                    print("Error: No se encontró el campo 'backupLocation'")
            else:
                print("Error: No se encontró el QFrame 'frame' dentro del QWidget 'miCentralWidget'")
        else:
            print("Error: No se encontró el QWidget 'miCentralWidget'")


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ventana = mainGUI()
    sys.exit(app.exec_())

