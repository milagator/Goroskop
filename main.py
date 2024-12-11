import sys
from PyQt5 import QtWidgets, QtGui
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
class MainApp(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        self.db = Database()
        self.init_ui()

    def init_ui(self):
        self.setWindowTitle("Астрологическое приложение")
        self.setGeometry(100, 100, 500, 400)

        layout = QtWidgets.QVBoxLayout()

        # Заголовок
        label_title = QtWidgets.QLabel("Астрологическое приложение", self)
        label_title.setFont(QtGui.QFont("Arial", 16))
        layout.addWidget(label_title)

        # Кнопка для генерации гороскопа
        button_horoscope = QtWidgets.QPushButton("Генерация гороскопа", self)
        button_horoscope.clicked.connect(self.open_horoscope)
        layout.addWidget(button_horoscope)

        # Кнопка для проверки совместимости
        button_compatibility = QtWidgets.QPushButton("Проверка совместимости", self)
        button_compatibility.clicked.connect(self.open_compatibility)
        layout.addWidget(button_compatibility)

        # Кнопка для вывода пользователей
        self.button_show_users = QtWidgets.QPushButton("Показать пользователей", self)
        self.button_show_users.clicked.connect(self.show_users)
        layout.addWidget(self.button_show_users)

        # Кнопка для вывода совместимости
        self.button_show_compatibility = QtWidgets.QPushButton("Показать совместимость", self)
        self.button_show_compatibility.clicked.connect(self.show_compatibility)
        layout.addWidget(self.button_show_compatibility)

        self.setLayout(layout)

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
            self.show_table("Список пользователей", ["ID", "Имя", "Дата рождения", "Знак зодиака"], users)
        else:
            QtWidgets.QMessageBox.information(self, "Пользователи", "Пользователи не найдены.")

    def show_compatibility(self):
        """Вывод информации о совместимости из базы данных в таблице."""
        results = self.db.load_compatibility_results()
        if results:
            self.show_table("Результаты совместимости", ["ID", "Имя 1", "Имя 2", "Совместимость"], results)
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