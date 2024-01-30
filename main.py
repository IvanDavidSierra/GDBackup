from PyQt5.QtWidgets import QApplication
from main_window import mainGUI
from backup_table import save_table_data_to_json, load_table_data_from_json

class AppController:
    def __init__(self):
        self.app = QApplication([])
        self.main_gui = mainGUI()
        load_table_data_from_json(self.main_gui.tableBackups)

    def open_main_gui(self):
        # Abre la ventana principal
        self.main_gui.show()

if __name__ == '__main__':
    app_controller = AppController()
    app_controller.open_main_gui()

    def save_data_on_close():
        save_table_data_to_json(app_controller.main_gui.tableBackups)
    
    app_controller.app.aboutToQuit.connect(save_data_on_close)
    app_controller.app.exec_()


