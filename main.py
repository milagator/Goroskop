import sys
from PyQt5 import QtWidgets, QtGui, QtCore
import sqlite3

from one import AstrologyApp as AstrologyApp1
from two import AstrologyApp as AstrologyApp2


# Класс для работы с базой данных
class Database:
    def __init__(self, user_db_path="db/user.db", compatibility_db_path="db/sinas.db"):
        self.user_connection = sqlite3.connect(user_db_path)
        self.compatibility_connection = sqlite3.connect(compatibility_db_path)
        self.create_tables()

    def create_tables(self):
        cursor = self.user_connection.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY,
                name TEXT,
                date_of_birth TEXT,
                zodiac_sign TEXT
            )
        ''')
        self.user_connection.commit()

        cursor = self.compatibility_connection.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS compatibility_results (
                id INTEGER PRIMARY KEY,
                name1 TEXT,
                name2 TEXT,
                compatibility TEXT
            )
        ''')
        self.compatibility_connection.commit()

    def load_users(self):
        cursor = self.user_connection.cursor()
        cursor.execute("SELECT * FROM users")
        return cursor.fetchall()

    def load_compatibility_results(self):
        cursor = self.compatibility_connection.cursor()
        cursor.execute("SELECT * FROM compatibility_results")
        return cursor.fetchall()

    def close(self):
        self.user_connection.close()
        self.compatibility_connection.close()


# Основное приложение
class MainApp(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        self.db = Database()
        self.init_ui()

    def init_ui(self):
        self.setWindowTitle("G-Lune")
        self.setGeometry(100, 100, 1920, 1080)

        # Центральный виджет
        self.centralwidget = QtWidgets.QWidget(self)
        self.setCentralWidget(self.centralwidget)
        self.centralwidget.setStyleSheet("background-image: url('static/ui/fon.png');")

        # Фон
        self.label = QtWidgets.QLabel(self.centralwidget)
        self.label.setGeometry(QtCore.QRect(0, 0, 1921, 1051))
        self.label.setStyleSheet("background-image: url(:/background/fon.png);")
        self.label.setText("")
        self.label.setObjectName("label")

        # Кнопка "Выход"
        self.button_exit = QtWidgets.QPushButton("Выход", self.centralwidget)
        self.button_exit.setGeometry(QtCore.QRect(20, 20, 100, 40))  # Позиция в левом верхнем углу
        font = QtGui.QFont("Roboto Light", 14)
        self.button_exit.setFont(font)
        self.button_exit.setStyleSheet("background-color: transparent; color: black; border: none;")  # Прозрачный фон и убрана обводка
        self.button_exit.clicked.connect(QtWidgets.qApp.quit)  # Закрыть приложение при нажатии на кнопку

        # Кнопка для генерации гороскопа
        self.pushButton = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton.setGeometry(QtCore.QRect(419, 333, 1081, 138))
        font = QtGui.QFont("Roboto Light", 28)
        self.pushButton.setFont(font)
        self.pushButton.setStyleSheet(
            "background: linear-gradient(90deg, rgba(238, 240, 252, 0) 0%, rgba(255, 255, 255, 0.2) 50%, rgba(238, 240, 252, 0) 100%), #E8CAEC;\n"
            "box-shadow: 0px 4px 3.8px rgba(0, 0, 0, 0.25);\n"
            "border-radius: 28px;")
        self.pushButton.setObjectName("pushButton")
        self.pushButton.setText("Генерация гороскопа")
        self.pushButton.clicked.connect(self.open_horoscope)

        # Кнопка для проверки совместимости
        self.pushButton_2 = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_2.setGeometry(QtCore.QRect(419, 518, 1081, 138))
        self.pushButton_2.setFont(font)
        self.pushButton_2.setStyleSheet(
            "background: linear-gradient(90deg, rgba(238, 240, 252, 0) 0%, rgba(255, 255, 255, 0.2) 50%, rgba(238, 240, 252, 0) 100%), #E8CAEC;\n"
            "box-shadow: 0px 4px 3.8px rgba(0, 0, 0, 0.25);\n"
            "border-radius: 28px;")
        self.pushButton_2.setObjectName("pushButton_2")
        self.pushButton_2.setText("Проверка совместимости")
        self.pushButton_2.clicked.connect(self.open_compatibility)

        # Кнопка для вывода пользователей
        self.pushButton_3 = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_3.setGeometry(QtCore.QRect(635, 703, 650, 83))
        font = QtGui.QFont("Roboto Light", 20)
        self.pushButton_3.setFont(font)
        self.pushButton_3.setStyleSheet(
            "background: linear-gradient(90deg, rgba(238, 240, 252, 0) 0%, rgba(255, 255, 255, 0.2) 50%, rgba(238, 240, 252, 0) 100%), #E8CAEC;\n"
            "box-shadow: 0px 4px 4px rgba(0, 0, 0, 0.25);\n"
            "border-radius: 28px;")
        self.pushButton_3.setObjectName("pushButton_3")
        self.pushButton_3.setText("Все пользователи")
        self.pushButton_3.clicked.connect(self.show_users)

        # Кнопка для вывода совместимости
        self.pushButton_4 = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_4.setGeometry(QtCore.QRect(635, 833, 650, 83))
        self.pushButton_4.setFont(font)
        self.pushButton_4.setStyleSheet(
            "background: linear-gradient(90deg, rgba(238, 240, 252, 0) 0%, rgba(255, 255, 255, 0.2) 50%, rgba(238, 240, 252, 0) 100%), #E8CAEC;\n"
            "box-shadow: 0px 4px 4px rgba(0, 0, 0, 0.25);\n"
            "border-radius: 28px;")
        self.pushButton_4.setObjectName("pushButton_4")
        self.pushButton_4.setText("Все совместимости")
        self.pushButton_4.clicked.connect(self.show_compatibility)

        # Меню и статус
        self.menubar = QtWidgets.QMenuBar(self)
        self.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(self)
        self.setStatusBar(self.statusbar)

    def open_horoscope(self):
        self.horoscope_app = AstrologyApp1()  # Поставьте вашу реализацию
        self.horoscope_app.show()

    def open_compatibility(self):
        self.compatibility_app = AstrologyApp2()  # Поставьте вашу реализацию
        self.compatibility_app.show()

    def show_users(self):
        """Вывод информации о пользователях из базы данных в таблице."""
        users = self.db.load_users()
        if users:
            # Создание диалогового окна
            table_dialog = QtWidgets.QDialog(self)
            table_dialog.setWindowTitle("Список пользователей")

            # Установка размера диалогового окна
            table_dialog.setFixedSize(760, 600)  # Устанавливаем фиксированный размер

            # Установка сиреневого фона
            table_dialog.setStyleSheet("background-color: #E8CAEC;")  # Розовый цвет

            layout = QtWidgets.QVBoxLayout()

            # Создание таблицы
            table = QtWidgets.QTableWidget()
            table.setRowCount(len(users))  # Количество строк
            table.setColumnCount(4)  # Четыре столбца: ID, Имя, Дата рождения, Знак зодиака
            table.setHorizontalHeaderLabels(["ID", "Имя", "Дата рождения", "Знак зодиака"])  # Заголовки столбцов

            # Установка шрифта Roboto Light и размера для заголовков таблицы
            font_header = QtGui.QFont("Roboto", 18, QtGui.QFont.Bold)  # Установка шрифта для заголовков
            table.horizontalHeader().setFont(font_header)

            # Установка шрифта Roboto Light и размера для ячеек таблицы
            font = QtGui.QFont("Roboto Light", 14)  # Установка шрифта и размера текста ячеек
            table.setFont(font)

            # Заполнение таблицы данными
            for row_index, row_data in enumerate(users):
                for column_index, column_data in enumerate(row_data):
                    table.setItem(row_index, column_index, QtWidgets.QTableWidgetItem(str(column_data)))

            # Автоматическая настройка ширины столбцов под содержимое
            for column_index in range(table.columnCount()):
                table.resizeColumnToContents(column_index)

            # Добавление таблицы в макет
            layout.addWidget(table)
            table_dialog.setLayout(layout)  # Установка макета

            # Отображение диалогового окна
            table_dialog.exec_()  # Модальный вызов
        else:
            QtWidgets.QMessageBox.information(self, "Пользователи", "Пользователи не найдены.")

    def show_compatibility(self):
        """Вывод информации о совместимости из базы данных в таблице."""
        results = self.db.load_compatibility_results()
        if results:
            # Создание диалогового окна
            table_dialog = QtWidgets.QDialog(self)
            table_dialog.setWindowTitle("Результаты совместимости")

            # Установка размера диалогового окна
            table_dialog.setFixedSize(900, 600)  # Устанавливаем фиксированный размер

            # Установка сиреневого фона
            table_dialog.setStyleSheet("background-color: #E8CAEC;")  # Сиреневый цвет

            layout = QtWidgets.QVBoxLayout()

            # Создание таблицы
            table = QtWidgets.QTableWidget()
            table.setRowCount(len(results))  # Количество строк
            table.setColumnCount(4)  # Четыре столбца: ID, Имя 1, Имя 2, Совместимость
            table.setHorizontalHeaderLabels(["ID", "Имя 1", "Имя 2", "Совместимость"])  # Заголовки столбцов

            # Установка шрифта Roboto Light и размера для заголовков таблицы
            font_header = QtGui.QFont("Roboto", 18, QtGui.QFont.Bold)  # Установка шрифта для заголовков
            table.horizontalHeader().setFont(font_header)

            # Установка шрифта Roboto Light и размера для ячеек таблицы
            font = QtGui.QFont("Roboto Light", 14)  # Установка шрифта и размера текста ячеек
            table.setFont(font)

            # Заполнение таблицы данными
            for row_index, row_data in enumerate(results):
                for column_index, column_data in enumerate(row_data):
                    table.setItem(row_index, column_index, QtWidgets.QTableWidgetItem(str(column_data)))

            # Автоматическая настройка ширины столбцов под содержимое
            for column_index in range(table.columnCount()):
                table.resizeColumnToContents(column_index)

            # Добавление таблицы в макет
            layout.addWidget(table)
            table_dialog.setLayout(layout)  # Установка макета

            # Отображение диалогового окна
            table_dialog.exec_()  # Модальный вызов
        else:
            QtWidgets.QMessageBox.information(self, "Результаты", "Совместимость не найдена.")

    def show_table(self, title, headers, data):
        """Создает и показывает окно с таблицей."""
        table_dialog = QtWidgets.QDialog(self)
        table_dialog.setWindowTitle(title)
        layout = QtWidgets.QVBoxLayout()

        table = QtWidgets.QTableWidget()
        table.setRowCount(len(data))
        table.setColumnCount(len(headers))
        table.setHorizontalHeaderLabels(headers)

        # Заполнение таблицы данными
        for row_index, row_data in enumerate(data):
            for column_index, column_data in enumerate(row_data):
                table.setItem(row_index, column_index, QtWidgets.QTableWidgetItem(str(column_data)))

        layout.addWidget(table)
        table_dialog.setLayout(layout)
        table_dialog.exec_()  # Отображение диалогового окна с таблицей

    def closeEvent(self, event):
        self.db.close()  # Закрытие соединений с базой данных при завершении приложения
        event.accept()


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    main_app = MainApp()
    main_app.show()
    sys.exit(app.exec_())