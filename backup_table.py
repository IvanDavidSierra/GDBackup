import json
import os
from PyQt5.QtCore import QUrl
from PyQt5.QtWidgets import QTableWidgetItem
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QDesktopServices

script_dir = os.path.dirname(os.path.abspath(__file__))
json_path = os.path.join(script_dir, "json", "table_data.json")

def handle_item_click(item, backup_folder_name, copy_thread):
    # Verificar si el clic se hizo en la columna 0 (nombre de la carpeta)
    if item.column() == 0:
        open_folder(copy_thread)

def open_folder(copy_thread):
    folder_path = copy_thread.destination_folder
    QDesktopServices.openUrl(QUrl.fromLocalFile(folder_path))

def save_table_data_to_json(table, json_file_path=json_path):
    data_dict = {'rows': []}

    for row in range(table.rowCount()):
        folder_name = table.item(row, 0).text()
        creation_time = table.item(row, 1).text()
        has_audio_files = table.item(row, 2).text()
        main_data = table.item(row, 3).text()

        data_dict['rows'].append({
            'folder_name': folder_name,
            'creation_time': creation_time,
            'has_audio_files': has_audio_files,
            'main_data': main_data
        })

    with open(json_file_path, 'w') as json_file:
        json.dump(data_dict, json_file, indent=3)

def load_table_data_from_json(table, json_file_path=json_path):
    try:
        with open(json_file_path, 'r') as json_file:
            data = json.load(json_file)

        for row_data in data.get('rows', []):
            folder_name = row_data.get('folder_name', '')
            creation_time = row_data.get('creation_time', '')
            has_audio_files = row_data.get('has_audio_files', '')
            main_data = row_data.get('main_data','')

            row_position = table.rowCount()
            table.setRowCount(row_position + 1)

            folder_item = QTableWidgetItem(folder_name)
            folder_item.setFlags(folder_item.flags() ^ Qt.ItemIsEditable)
            table.setItem(row_position, 0, folder_item)

            time_item = QTableWidgetItem(creation_time)
            time_item.setFlags(time_item.flags() ^ Qt.ItemIsEditable)
            table.setItem(row_position, 1, time_item)

            audio_item = QTableWidgetItem(has_audio_files)
            audio_item.setFlags(audio_item.flags() ^ Qt.ItemIsEditable)
            table.setItem(row_position, 2, audio_item)

            data_item = QTableWidgetItem(main_data)
            data_item.setFlags(data_item.flags() ^ Qt.ItemIsEditable)
            table.setItem(row_position, 3, data_item)

    except FileNotFoundError:
        print("El archivo JSON no se encontró.")
    except Exception as e:
        print(f"Error al cargar datos desde JSON: {e}")