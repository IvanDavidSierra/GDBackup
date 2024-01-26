import sys
from PyQt5.QtWidgets import QApplication
from main_window import mainGUI

class AppController:
    def __init__(self):
        self.app = QApplication([])
        self.main_gui = mainGUI()

    def open_main_gui(self):
        # Abre la ventana principal
        self.main_gui.show()

if __name__ == '__main__':
    app_controller = AppController()
    app_controller.open_main_gui()
    app_controller.app.exec_()


