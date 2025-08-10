import sys
from PyQt6.QtWidgets import QApplication, QMainWindow, QPushButton, QVBoxLayout, QWidget, QHBoxLayout

from gui_working_catalogs import open_catalog
# print(DICT_)

from test_dict import test_dict

# Создание приложения
app = QApplication(sys.argv)

# Создание главного окна
central_widget = QWidget()
central_widget.setWindowTitle("интерфейс PH каталогов")
central_widget.setGeometry(200, 200, 300, 100)

# Создание макета и добавление кнопки в него
layout = QHBoxLayout()
# layout = QVBoxLayout()

for i in range(3):  # Создаем три колонки
    column = QVBoxLayout()  # Вертикальный контейнер для каждой колонки

    for j in range(5):
        button = QPushButton(f"Кнопка {j + (i * 5)}")  # Создаем кнопку и добавляем ее в вертикальный контейнер
        column.addWidget(button)

    layout.addLayout(column)  # Добавляем колонки в основной горизонтальный контейнер

for key, values in test_dict.items():
    button = QPushButton(f"{key} ({values[1]})")
    button.clicked.connect(lambda checked, name=key: open_catalog(values[0]))
    layout.addWidget(button)


# button = QPushButton("Привет, мир!")
# layout.addWidget(button)

central_widget.setLayout(layout)

# Установка центрального виджета
main_window = QMainWindow()
main_window.setCentralWidget(central_widget)
main_window.show()

sys.exit(app.exec())
