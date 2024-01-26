import os
import shutil
from PyQt5 import uic
from PyQt5.QtWidgets import *
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import QThread, pyqtSignal
from PyQt5.QtGui import QPixmap

class ThreadBackup(QThread):
    progress_updated = pyqtSignal(int, int)
    finished = pyqtSignal(bool)

    def __init__(self, source_folder, file_extensions, destination_folder):
        super().__init__()
        self.source_folder = source_folder
        self.file_extensions = file_extensions
        self.destination_folder = destination_folder
        self.success = False
    def run(self):
        files_to_copy = []

        if self.file_extensions is not None:
            files_to_copy = [f for f in os.listdir(self.source_folder) if os.path.splitext(f)[-1] in self.file_extensions]
        else:
            files_to_copy = os.listdir(self.source_folder)

        total_files = len(files_to_copy)
        copied_files = 0

        try:
            for file_name in files_to_copy:
                source_path = os.path.join(self.source_folder, file_name)
                destination_path = os.path.join(self.destination_folder, file_name)
                shutil.copy(source_path, destination_path)
                copied_files += 1
                self.progress_updated.emit(total_files, copied_files)
                print(f"Copiado exitosamente: {file_name}")

            # Si llega hasta aquí, la operación fue exitosa
            self.success = True
        except Exception as e:
            print(f"Error en la operación de copia: {str(e)}")
            self.success = False
        finally:
            self.finished.emit(self.success)

class mainGUI(QMainWindow):
    def __init__(self):
        super().__init__()

        self.selectFolder = self.findChild(QPushButton, 'selectFolder')
        self.backupData = self.findChild(QPushButton, 'backupData')

        self.confirmation_dialog = QMessageBox(self)
        self.confirmation_dialog.setWindowTitle("Message")
        self.confirmation_dialog.setText("Backup done successfully!")

        script_dir = os.path.dirname(os.path.abspath(__file__))
        gui_path = os.path.join(script_dir, "GUI", "main_window.ui")
        icon_path = os.path.join(script_dir, "icon", "icon.jpeg")
        img_path = os.path.join(script_dir, "img", "mojon.jpeg")
        self.setWindowIcon(QIcon(icon_path))
        self.copy_thread = None
        uic.loadUi(gui_path, self)

        # Code for progress bar
        self.progress_bar = QProgressBar(self)
        self.progress_bar.setGeometry(20, 400, 425, 25)
        self.progress_bar.setValue(0)

        self.status_label = QLabel(self)
        self.status_label.setGeometry(20, 430, 200, 20)
        self.status_label.setText("")

        self.status_files = QLabel(self)
        self.status_files.setGeometry(130, 430, 200, 20)
        self.status_files.setText("")

        self.img_bakop = QLabel(self)

        # Verifica si el widget se encontró correctamente
        if self.img_bakop:
            # Establece la imagen en el QLabel
            pixmap = QPixmap(img_path)  # Reemplaza con la ruta de tu imagen
            self.img_bakop.setPixmap(pixmap)
            self.img_bakop.setGeometry(620, 30, 100, 30)
            self.img_bakop.setScaledContents(True)  # Ajusta la imagen al tamaño del QLabel
        else:
            print("Error: No se encontró el QLabel 'imageLabel'")

        self.init_ui()

        self.setFixedSize(722, 456)
        self.show()

    def init_ui(self):
        selectFolder = self.findChild(QPushButton, 'selectFolder')
        backupData = self.findChild(QPushButton, 'backupData')
        assetsCheckbox = self.findChild(QCheckBox, 'assetsCheckbox')
        backupLocation = self.findChild(QLabel, 'backupLocation')
        if selectFolder and backupData and assetsCheckbox and backupLocation:
            selectFolder.clicked.connect(self.select_location)
            backupData.clicked.connect(lambda: self.backup_button_clicked(assetsCheckbox.isChecked()))
        else:
            print("Error: Al menos uno de los elementos no fue encontrado.")
    

    def select_location(self):
        folder_path = QFileDialog.getExistingDirectory(self, 'Select backup location')
        if folder_path:
            # Carpeta seleccionada correctamente
            backupLocation = self.findChild(QLabel, 'backupLocation')
            backupLocation.setText(folder_path)
        else:
            # Carpeta no seleccionada (puede deberse a que el usuario canceló el diálogo)
            QMessageBox.warning(self, "Please, select a folder")

    def backup_button_clicked(self, assets_checked):
        backupLocation = self.findChild(QLabel, 'backupLocation')

        self.selectFolder.setEnabled(False)
        self.backupData.setEnabled(False)
        self.status_label.setText("Backup in progress...")

        folder_path = backupLocation.text()
        user_name = os.getlogin()
        source_folder = f'C:/Users/{user_name}/AppData/Local/GeometryDash'
        file_extension = None if assets_checked else '.dat'
        if self.copy_thread and self.copy_thread.isRunning():
            print("Operación de copia ya en progreso.")
            return
        # Crear una instancia de threadBackup y conectar las señales
        self.copy_thread = ThreadBackup(source_folder, [file_extension] if file_extension else None, folder_path)
        self.copy_thread.progress_updated.connect(self.update_progress)
        self.copy_thread.finished.connect(self.handle_thread_finished)
        self.copy_thread.start()  # Iniciar el hilo de copia

    def handle_thread_finished(self, success):
        self.selectFolder.setEnabled(True)
        self.backupData.setEnabled(True)
        self.reset_progress()
        if success:
            self.show_confirmation_dialog()
            self.status_label.setText("")
            self.status_files.setText("")
        else:
            QMessageBox.warning(self, "Backup error!")


    # Método para actualizar la barra de progreso
    def update_progress(self, total_files, copied_files):
        self.progress_bar.setMaximum(total_files)
        self.progress_bar.setValue(copied_files)
        # Puedes actualizar también el texto del QLabel para mostrar la cantidad actual de archivos copiados
        self.status_files.setText(f"{copied_files} / {total_files} files")

    # Método para mostrar la ventana de confirmación
    def show_confirmation_dialog(self):
        self.confirmation_dialog.setIcon(QMessageBox.Information)
        self.confirmation_dialog.show()


    # Método para restablecer la barra de progreso
    def reset_progress(self):
        self.progress_bar.setValue(0)
