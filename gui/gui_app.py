import sys
from PyQt6.QtWidgets import QApplication, QMainWindow, QPushButton, QVBoxLayout, QWidget, QHBoxLayout

from gui_working_catalogs import open_catalog, dict_for_buttons
DICT_ = dict_for_buttons()
# from test_dict import test_dict
# DICT_ = test_dict

# Создание приложения
app = QApplication(sys.argv)

# Создание главного окна
central_widget = QWidget()
central_widget.setWindowTitle("Интерфейс PH каталогов")
central_widget.setGeometry(200, 200, 300, 100)

# Создание макета и добавление кнопки в него
layout = QVBoxLayout()

def open_catalog_values(key_):
    path_ = DICT_.get(key_)[0]
    open_catalog(path_)
    # return path_

opn_cat = lambda path: open_catalog_values(path)

for key, value in DICT_.items():
    button = QPushButton(f"{key} ({value[1]})")  # имя кнопки вида 'model (10,5 ГБ)'
    # button.clicked.connect(lambda checked, name=values: open_catalog_values(key_=key))
    button.clicked.connect(lambda checked, path=key: opn_cat(path))
    # button.clicked(open_catalog_values(key_=key))
    layout.addWidget(button)


# button = QPushButton("Привет, мир!")
# layout.addWidget(button)

central_widget.setLayout(layout)

# Установка центрального виджета
main_window = QMainWindow()
main_window.setCentralWidget(central_widget)
main_window.show()

sys.exit(app.exec())
