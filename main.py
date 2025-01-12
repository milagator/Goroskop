import sys
import sqlite3
from PyQt5 import QtWidgets, QtCore, QtGui
from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import QMessageBox, QComboBox
#from one import AstrologyApp as AstrologyApp1
#from two import AstrologyApp as AstrologyApp2

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
        self.label.setStyleSheet("background-image: url(:background/fon.png);")
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
# Основные данные
ZODIAC_SIGNS = [
    ("Овен", (3, 21), (4, 19), "static/img/aries.png"),
    ("Телец", (4, 20), (5, 20), "static/img/taurus.png"),
    ("Близнецы", (5, 21), (6, 20), "static/img/gemini.png"),
    ("Рак", (6, 21), (7, 22), "static/img/cancer.png"),
    ("Лев", (7, 23), (8, 22), "static/img/leole.png"),
    ("Дева", (8, 23), (9, 22), "static/img/virgo.png"),
    ("Весы", (9, 23), (10, 22), "static/img/libra.png"),
    ("Скорпион", (10, 23), (11, 21), "static/img/scorpio.png"),
    ("Стрелец", (11, 22), (12, 21), "static/img/sagittarius.png"),
    ("Козерог", (12, 22), (1, 19), "static/img/capricorn.png"),
    ("Водолей", (1, 20), (2, 18), "static/img/aquarius.png"),
    ("Рыбы", (2, 19), (3, 20), "static/img/pisces.png"),
]

# Функция для определения знака зодиака
def get_zodiac_sign(day, month):
    for sign, start_date, end_date, image in ZODIAC_SIGNS:
        if (month == start_date[0] and day >= start_date[1]) or \
                (month == end_date[0] and day <= end_date[1]):
            return sign, image
    return "Неизвестный знак", ""

# Функция для генерации гороскопа
def generate_horoscope(sign):
    horoscopes = {
        "Овен": "Сегодня ваш день! Время действовать.",
        "Телец": "Вас ждут приятные сюрпризы.",
        "Близнецы": "День подходит для общения.",
        "Рак": "Сосредоточьтесь на семье.",
        "Лев": "Сегодня вы будете в центре внимания.",
        "Дева": "Идеальное время для планирования.",
        "Весы": "Сохраняйте баланс во всем.",
        "Скорпион": "День будет наполнен эмоциями.",
        "Стрелец": "Пора подумать о путешествиях.",
        "Козерог": "Сосредоточьтесь на карьере.",
        "Водолей": "Хороший день для новых идей.",
        "Рыбы": "Слушайте свою интуицию.",
    }
    return horoscopes.get(sign, "Гороскоп отсутствует.")

class Database1:
    def __init__(self, db_name="db/user.db"):
        self.conn = sqlite3.connect(db_name)
        self.create_table()

    def create_table(self):
        with self.conn:
            self.conn.execute("""
                CREATE TABLE IF NOT EXISTS users (
                    id INTEGER PRIMARY KEY,
                    name TEXT,
                    date_of_birth TEXT,
                    zodiac_sign TEXT
                )
            """)

    def insert_user(self, name, date_of_birth, zodiac_sign):
        with self.conn:
            self.conn.execute("""
                INSERT INTO users (name, date_of_birth, zodiac_sign)
                VALUES (?, ?, ?)
            """, (name, date_of_birth, zodiac_sign))

    def update_user(self, name, date_of_birth, zodiac_sign):
        with self.conn:
            self.conn.execute("""
                UPDATE users SET date_of_birth = ?, zodiac_sign = ? WHERE name = ?
            """, (date_of_birth, zodiac_sign, name))

    def get_user(self, name):
        cursor = self.conn.cursor()
        cursor.execute("SELECT name, date_of_birth, zodiac_sign FROM users WHERE name = ?", (name,))
        return cursor.fetchone()

    def close(self):
        self.conn.close()

# Основное приложение
class Ui_MainWindow:
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(1920, 1080)
        font = QtGui.QFont()
        font.setFamily("Roboto Light")
        font.setPointSize(10)
        MainWindow.setFont(font)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")

        # Кнопка "Назад"
        self.button_back = QtWidgets.QPushButton(self.centralwidget)
        self.button_back.setGeometry(QtCore.QRect(30, 20, 100, 40))  # Установите положение и размер
        self.button_back.setFont(QtGui.QFont("Roboto Light", 14))
        self.button_back.setText("Назад")
        self.button_back.setStyleSheet("background-color: transparent; color: black; border: none;")  # Прозрачный фон
        self.button_back.clicked.connect(MainWindow.close)  # Закрыть окно при нажатии

        self.label = QtWidgets.QLabel(self.centralwidget)
        self.label.setGeometry(QtCore.QRect(80, 80, 1661, 291))
        self.label.setStyleSheet("background-image: url(image.png);")
        self.label.setText("")
        self.label.setObjectName("label")

        self.text_name = QtWidgets.QLineEdit(self.centralwidget)
        self.text_name.setGeometry(QtCore.QRect(151, 355, 601, 44))
        self.text_name.setStyleSheet(self.get_line_edit_style())
        self.text_name.setObjectName("text_name")

        self.text_dob = QtWidgets.QLineEdit(self.centralwidget)
        self.text_dob.setGeometry(QtCore.QRect(151, 444, 601, 44))
        self.text_dob.setStyleSheet(self.get_line_edit_style())
        self.text_dob.setObjectName("text_dob")

        self.text_user_name = QtWidgets.QLineEdit(self.centralwidget)
        self.text_user_name.setGeometry(QtCore.QRect(151, 710, 601, 44))
        self.text_user_name.setStyleSheet(self.get_line_edit_style())
        self.text_user_name.setObjectName("text_user_name")

        self.button_generate = QtWidgets.QPushButton(self.centralwidget)
        self.button_generate.setGeometry(QtCore.QRect(229, 526, 446, 51))
        font = QtGui.QFont()
        font.setFamily("Roboto Light")
        font.setPointSize(14)
        self.button_generate.setFont(font)
        self.button_generate.setStyleSheet(self.get_button_style())
        self.button_generate.setObjectName("button_generate")

        self.button_load = QtWidgets.QPushButton(self.centralwidget)
        self.button_load.setGeometry(QtCore.QRect(229, 782, 446, 51))
        self.button_load.setFont(font)
        self.button_load.setStyleSheet(self.get_button_style())
        self.button_load.setObjectName("button_load")

        self.button_update = QtWidgets.QPushButton(self.centralwidget)
        self.button_update.setGeometry(QtCore.QRect(229, 900, 446, 51))
        self.button_update.setFont(font)
        self.button_update.setStyleSheet(self.get_button_style())
        self.button_update.setObjectName("button_update")

        self.label_2 = QtWidgets.QLabel(self.centralwidget)
        self.label_2.setGeometry(QtCore.QRect(150, 260, 538, 65))
        font = QtGui.QFont()
        font.setFamily("Roboto Light")
        font.setPointSize(24)
        self.label_2.setFont(font)
        self.label_2.setObjectName("label_2")

        self.label_3 = QtWidgets.QLabel(self.centralwidget)
        self.label_3.setGeometry(QtCore.QRect(151, 325, 55, 16))
        font.setPointSize(14)
        self.label_3.setFont(font)
        self.label_3.setObjectName("label_3")

        self.label_4 = QtWidgets.QLabel(self.centralwidget)
        self.label_4.setGeometry(QtCore.QRect(151, 410, 444, 30))
        font.setPointSize(14)
        self.label_4.setFont(font)
        self.label_4.setObjectName("label_4")

        self.label_5 = QtWidgets.QLabel(self.centralwidget)
        self.label_5.setGeometry(QtCore.QRect(151, 600, 538, 65))
        font.setPointSize(24)
        self.label_5.setFont(font)
        self.label_5.setObjectName("label_5")

        self.label_6 = QtWidgets.QLabel(self.centralwidget)
        self.label_6.setGeometry(QtCore.QRect(151, 670, 151, 31))
        font.setPointSize(14)
        self.label_6.setFont(font)
        self.label_6.setObjectName("label_6")

        self.label_7 = QtWidgets.QLabel(self.centralwidget)
        self.label_7.setGeometry(QtCore.QRect(1080, 260, 801, 101))
        font.setPointSize(20)
        self.label_7.setFont(font)
        self.label_7.setObjectName("label_7")

        self.button_details = QtWidgets.QPushButton(self.centralwidget)
        self.button_details.setGeometry(QtCore.QRect(1200, 900, 446, 51))
        font.setPointSize(14)
        self.button_details.setFont(font)
        self.button_details.setStyleSheet(self.get_button_style())
        self.button_details.setObjectName("button_details")

        # Метка для изображения знака зодиака
        self.zodiac_image_label = QtWidgets.QLabel(self.centralwidget)
        self.zodiac_image_label.setGeometry(QtCore.QRect(1220, 370, 400, 500))  # Измените размеры по необходимости
        self.zodiac_image_label.setScaledContents(True)  # Сохранение соотношения сторон
        self.zodiac_image_label.setObjectName("zodiac_image_label")
        self.zodiac_image_label.setVisible(False)  # Скрыть метку по умолчанию

        MainWindow.setCentralWidget(self.centralwidget)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def get_line_edit_style(self):
        return """
            padding: 10px;  /* Отступ внутри поля ввода */
            background: linear-gradient(90deg, rgba(238, 240, 252, 0) 0%, rgba(255, 255, 255, 0.2) 50%, rgba(238, 240, 252, 0) 100%), #DFDFDF;
            box-shadow: 0px 4px 3.8px rgba(0, 0, 0, 0.25);
            border-radius: 28px;
        """

    def get_button_style(self):
        return """
            background: linear-gradient(90deg, rgba(238, 240, 252, 0) 0%, rgba(255, 255, 255, 0.2) 50%, rgba(238, 240, 252, 0) 100%), #E8CAEC;
            box-shadow: 0px 4px 3.8px rgba(0, 0, 0, 0.25);
            border-radius: 20px;
        """

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "G-Lune"))
        self.button_generate.setText(_translate("MainWindow", "Сгенерировать гороскоп"))
        self.button_load.setText(_translate("MainWindow", "Загрузить данные"))
        self.button_update.setText(_translate("MainWindow", "Изменить данные"))
        self.label_2.setText(_translate("MainWindow", "Генерация гороскопа"))
        self.label_3.setText(_translate("MainWindow", "Имя:"))
        self.label_4.setText(_translate("MainWindow", "Дата рождения: (ДД.ММ.ГГГГ)"))
        self.label_5.setText(_translate("MainWindow", "Найти пользователя "))
        self.label_6.setText(_translate("MainWindow", "Введите имя:"))
        self.label_7.setText(_translate("MainWindow", "Гороскоп:"))
        self.button_details.setText(_translate("MainWindow", "Узнать больше"))

        self.centralwidget.setStyleSheet("background-image: url('static/ui/lune.png');")

class AstrologyApp1(QtWidgets.QMainWindow, Ui_MainWindow):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.zodiac_sign = None  # Для хранения текущего знака
        self.db = Database1()

        # Подключение кнопок к методам
        self.button_generate.clicked.connect(self.generate_horoscope)
        self.button_load.clicked.connect(self.load_user_data)
        self.button_update.clicked.connect(self.update_user_data)
        self.button_details.clicked.connect(self.show_details)

    def generate_horoscope(self):
        name = self.text_name.text().strip()
        dob = self.text_dob.text().strip()

        try:
            day, month, year = map(int, dob.split('.'))
            self.zodiac_sign, image_path = get_zodiac_sign(day, month)
            horoscope = generate_horoscope(self.zodiac_sign)
            self.db.insert_user(name, dob, self.zodiac_sign)

            self.label_7.setText(f"Привет, {name}! Ваш знак зодиака: {self.zodiac_sign}.\n{horoscope}")
            self.button_details.setEnabled(True)

            # Загрузить и показать изображение знака зодиака
            if image_path:  # Проверка, что путь к изображению существует
                pixmap = QPixmap(image_path)
                self.zodiac_image_label.setPixmap(pixmap)
                self.zodiac_image_label.setVisible(True)  # Сделать метку видимой

        except ValueError:
            QtWidgets.QMessageBox.critical(self, "Ошибка", "Введите дату в формате ДД.ММ.ГГГГ.")
        except Exception as e:
            self.show_error_message(e)

    def load_user_data(self):
        user_name = self.text_user_name.text().strip()
        try:
            user_data = self.db.get_user(user_name)
            if user_data:
                name, dob, zodiac_sign = user_data
                self.text_name.setText(name)
                self.text_dob.setText(dob)
                self.label_7.setText(f"Знак зодиака: {zodiac_sign}.")

                # Обновляем изображение для текущего знака
                for sign, start_date, end_date, image in ZODIAC_SIGNS:
                    if zodiac_sign == sign:
                        pixmap = QPixmap(image)
                        self.zodiac_image_label.setPixmap(pixmap)
                        self.zodiac_image_label.setVisible(True)
                        break

                self.zodiac_sign = zodiac_sign
                self.button_details.setEnabled(True)

            else:
                QtWidgets.QMessageBox.critical(self, "Ошибка", "Пользователь не найден.")
        except Exception as e:
            self.show_error_message(e)

    def update_user_data(self):
        user_name = self.text_user_name.text().strip()
        dob = self.text_dob.text().strip()

        try:
            if not user_name or not dob:
                QtWidgets.QMessageBox.critical(self, "Ошибка", "Введите имя пользователя и дату рождения.")
                return

            day, month, year = map(int, dob.split('.'))
            zodiac_sign, _ = get_zodiac_sign(day, month)

            existing_user = self.db.get_user(user_name)
            if not existing_user:
                QtWidgets.QMessageBox.critical(self, "Ошибка", "Пользователь не найден.")
                return

            self.db.update_user(user_name, dob, zodiac_sign)
            self.show_success_message("Данные пользователя успешно обновлены.")
        except ValueError:
            QtWidgets.QMessageBox.critical(self, "Ошибка", "Введите дату в формате ДД.ММ.ГГГГ.")
        except Exception as e:
            self.show_error_message(e)

    def show_details(self):
        if self.zodiac_sign is None:
            QtWidgets.QMessageBox.warning(self, "Предупреждение", "Сначала сгенерируйте гороскоп.")
            return

        file_path = f"static/files/{self.zodiac_sign}.txt"
        try:
            with open(file_path, "r", encoding="utf-8") as file:
                details = file.read()

            detail_window = QtWidgets.QMessageBox(self)
            detail_window.setWindowTitle(f"Подробности о знаке {self.zodiac_sign}")
            detail_window.setText(details)
            detail_window.setStyleSheet("background-color: #E8CAEC;")  # фон
            font = QtGui.QFont("Roboto Light", 14)  # Шрифт Roboto Light
            detail_window.setFont(font)
            detail_window.exec_()

        except FileNotFoundError:
            QtWidgets.QMessageBox.critical(self, "Ошибка", f"Файл '{file_path}' не найден.")
        except Exception as e:
            self.show_error_message(e)

    def show_success_message(self, message):
        success_window = QtWidgets.QMessageBox(self)
        success_window.setWindowTitle("Успех")
        success_window.setText(message)
        success_window.setStyleSheet("background-color: #E8CAEC;")  # фон
        font = QtGui.QFont("Roboto Light", 14)  # Шрифт Roboto Light
        success_window.setFont(font)
        success_window.exec_()

    def show_error_message(self, error):
        error_window = QtWidgets.QMessageBox(self)
        error_window.setWindowTitle("Ошибка")
        error_window.setText(f"Произошла ошибка: {str(error)}")
        error_window.setStyleSheet("background-color: #E8CAEC;")  # фон
        font = QtGui.QFont("Roboto Light", 14)  # Шрифт Roboto Light
        error_window.setFont(font)
        error_window.exec_()

    def closeEvent(self, event):
        self.db.close()

# Основные данные
ZODIAC_SIGNS2 = [
    ("Овен", (3, 21), (4, 19)),
    ("Телец", (4, 20), (5, 20)),
    ("Близнецы", (5, 21), (6, 20)),
    ("Рак", (6, 21), (7, 22)),
    ("Лев", (7, 23), (8, 22)),
    ("Дева", (8, 23), (9, 22)),
    ("Весы", (9, 23), (10, 22)),
    ("Скорпион", (10, 23), (11, 21)),
    ("Стрелец", (11, 22), (12, 21)),
    ("Козерог", (12, 22), (1, 19)),
    ("Водолей", (1, 20), (2, 18)),
    ("Рыбы", (2, 19), (3, 20)),
]

COMPATIBILITY = {
    "Овен": ["Лев", "Стрелец", "Близнецы"],
    "Телец": ["Дева", "Козерог", "Рак"],
    "Близнецы": ["Весы", "Водолей", "Овен"],
    "Рак": ["Скорпион", "Рыбы", "Телец"],
    "Лев": ["Овен", "Стрелец", "Весы"],
    "Дева": ["Телец", "Козерог", "Рак", "Дева"],
    "Весы": ["Близнецы", "Водолей", "Лев"],
    "Скорпион": ["Рак", "Рыбы", "Козерог"],
    "Стрелец": ["Лев", "Овен", "Водолей"],
    "Козерог": ["Телец", "Дева", "Скорпион"],
    "Водолей": ["Близнецы", "Весы", "Стрелец"],
    "Рыбы": ["Рак", "Скорпион", "Козерог"],
}


# Функция для определения знака зодиака
def get_zodiac_sign2(day, month):
    for sign, start_date, end_date in ZODIAC_SIGNS2:
        if (month == start_date[0] and day >= start_date[1]) or \
                (month == end_date[0] and day <= end_date[1]):
            return sign
    return "Неизвестный знак"


# Функция для проверки совместимости
def check_compatibility(sign1, sign2):
    if sign2 in COMPATIBILITY.get(sign1, []):
        return f"Знаки {sign1} и {sign2} совместимы!"
    return f"Знаки {sign1} и {sign2} несовместимы."


class Database2:
    def __init__(self, user_db_path="db/user.db",
                 compatibility_db_path="db/sinas.db"):
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

        # Создание таблицы совместимости в sinas.db
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

    def add_user(self, name, date_of_birth):
        cursor = self.user_connection.cursor()
        day, month, year = map(int, date_of_birth.split('.'))
        zodiac_sign = get_zodiac_sign2(day, month)

        cursor.execute("INSERT INTO users (name, date_of_birth, zodiac_sign) VALUES (?, ?, ?)",
                       (name, date_of_birth, zodiac_sign))
        self.user_connection.commit()

    def load_users(self):
        cursor = self.user_connection.cursor()
        cursor.execute("SELECT id, name, zodiac_sign FROM users")
        return cursor.fetchall()

    def save_compatibility(self, name1, name2, compatibility):
        cursor = self.compatibility_connection.cursor()
        cursor.execute("INSERT INTO compatibility_results (name1, name2, compatibility) VALUES (?, ?, ?)",
                       (name1, name2, compatibility))
        self.compatibility_connection.commit()

    def close(self):
        self.user_connection.close()
        self.compatibility_connection.close()

    def is_user_exists(self, name):
        cursor = self.user_connection.cursor()
        cursor.execute("SELECT * FROM users WHERE name = ?", (name,))
        return cursor.fetchone() is not None


# Основное приложение
class AstrologyApp2(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        self.db = Database2()  # Создаем соединение с базой данных
        self.setupUi()

    def setupUi(self):
        self.setObjectName("MainWindow")
        self.resize(1920, 1080)
        self.centralwidget = QtWidgets.QWidget(self)
        self.centralwidget.setObjectName("centralwidget")

        # Кнопка "Назад"
        self.button_back = QtWidgets.QPushButton(self.centralwidget)
        self.button_back.setGeometry(QtCore.QRect(30, 20, 100, 40))  # Установите положение и размер
        self.button_back.setFont(QtGui.QFont("Roboto Light", 14))
        self.button_back.setText("Назад")
        self.button_back.setStyleSheet("background-color: transparent; color: black; border: none;")  # Прозрачный фон
        self.button_back.clicked.connect(self.close)  # Закрыть только текущее окно

        # Кнопки и метки
        self.pushButton = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton.setGeometry(QtCore.QRect(229, 630, 446, 51))
        font = QtGui.QFont()
        font.setFamily("Roboto Light")
        font.setPointSize(14)
        self.pushButton.setFont(font)
        self.pushButton.setStyleSheet(
            "background: linear-gradient(90deg, rgba(238, 240, 252, 0) 0%, rgba(255, 255, 255, 0.2) 50%, rgba(238, 240, 252, 0) 100%), #E8CAEC;\n"
            "box-shadow: 0px 4px 3.8px rgba(0, 0, 0, 0.25);\n"
            "border-radius: 20px;\n")
        self.pushButton.setObjectName("pushButton")

        self.label = QtWidgets.QLabel(self.centralwidget)
        self.label.setGeometry(QtCore.QRect(165, 250, 538, 65))
        font.setPointSize(24)
        self.label.setFont(font)
        self.label.setObjectName("label")

        self.label_2 = QtWidgets.QLabel(self.centralwidget)
        self.label_2.setGeometry(QtCore.QRect(165, 340, 444, 38))
        font.setPointSize(14)
        self.label_2.setFont(font)
        self.label_2.setObjectName("label_2")

        self.label_3 = QtWidgets.QLabel(self.centralwidget)
        self.label_3.setGeometry(QtCore.QRect(165, 470, 444, 38))
        font.setPointSize(14)
        self.label_3.setFont(font)
        self.label_3.setObjectName("label_3")

        # Настройка выпадающих списков
        self.comboBox = QtWidgets.QComboBox(self.centralwidget)
        self.comboBox.setGeometry(QtCore.QRect(157, 400, 601, 44))
        self.comboBox.setStyleSheet(
            "background: linear-gradient(90deg, rgba(238, 240, 252, 0) 0%, rgba(255, 255, 255, 0.2) 50%, rgba(238, 240, 252, 0) 100%), #E2E2E2;\n"
            "box-shadow: 0px 4px 3.8px rgba(0, 0, 0, 0.25);\n"
            "border-radius: 28px;")
        self.comboBox.setFont(QtGui.QFont("Roboto Light", 12))
        self.comboBox.setObjectName("comboBox")

        self.comboBox_2 = QtWidgets.QComboBox(self.centralwidget)
        self.comboBox_2.setGeometry(QtCore.QRect(157, 523, 601, 44))
        self.comboBox_2.setStyleSheet(
            "background: linear-gradient(90deg, rgba(238, 240, 252, 0) 0%, rgba(255, 255, 255, 0.2) 50%, rgba(238, 240, 252, 0) 100%), #E2E2E2;\n"
            "box-shadow: 0px 4px 3.8px rgba(0, 0, 0, 0.25);\n"
            "border-radius: 28px;")
        self.comboBox_2.setFont(QtGui.QFont("Roboto Light", 12))
        self.comboBox_2.setObjectName("comboBox_2")

        self.label_4 = QtWidgets.QLabel(self.centralwidget)
        self.label_4.setGeometry(QtCore.QRect(1190, 250, 538, 65))
        font.setPointSize(24)
        self.label_4.setFont(font)
        self.label_4.setObjectName("label_4")

        self.label_5 = QtWidgets.QLabel(self.centralwidget)
        self.label_5.setGeometry(QtCore.QRect(1190, 340, 444, 33))
        font.setPointSize(14)
        self.label_5.setFont(font)
        self.label_5.setObjectName("label_5")

        self.label_6 = QtWidgets.QLabel(self.centralwidget)
        self.label_6.setGeometry(QtCore.QRect(1190, 470, 444, 38))
        font.setPointSize(14)
        self.label_6.setFont(font)
        self.label_6.setObjectName("label_6")

        self.pushButton_2 = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_2.setGeometry(QtCore.QRect(1270, 630, 446, 51))
        self.pushButton_2.setFont(font)
        self.pushButton_2.setStyleSheet(
            "background: linear-gradient(90deg, rgba(238, 240, 252, 0) 0%, rgba(255, 255, 255, 0.2) 50%, rgba(238, 240, 252, 0) 100%), #E8CAEC;\n"
            "box-shadow: 0px 4px 3.8px rgba(0, 0, 0, 0.25);\n"
            "border-radius: 20px;")
        self.pushButton_2.setObjectName("pushButton_2")

        # Поля ввода
        self.lineEdit = QtWidgets.QLineEdit(self.centralwidget)
        self.lineEdit.setGeometry(QtCore.QRect(1190, 400, 601, 44))
        font.setPointSize(12)
        self.lineEdit.setFont(font)
        self.lineEdit.setStyleSheet(
            "background: linear-gradient(90deg, rgba(238, 240, 252, 0) 0%, rgba(255, 255, 255, 0.2) 50%, rgba(238, 240, 252, 0) 100%), #DFDFDF;\n"
            "box-shadow: 0px 4px 3.8px rgba(0, 0, 0, 0.25);\n"
            "border-radius: 28px; padding-left: 10px;")
        self.lineEdit.setObjectName("lineEdit")

        self.lineEdit_2 = QtWidgets.QLineEdit(self.centralwidget)
        self.lineEdit_2.setGeometry(QtCore.QRect(1190, 523, 601, 44))
        self.lineEdit_2.setStyleSheet(
            "background: linear-gradient(90deg, rgba(238, 240, 252, 0) 0%, rgba(255, 255, 255, 0.2) 50%, rgba(238, 240, 252, 0) 100%), #DFDFDF;\n"
            "box-shadow: 0px 4px 3.8px rgba(0, 0, 0, 0.25);\n"
            "border-radius: 28px; padding-left: 10px;")
        self.lineEdit_2.setFont(font)
        self.lineEdit_2.setObjectName("lineEdit_2")

        self.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(self)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 1920, 26))
        self.menubar.setObjectName("menubar")
        self.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(self)
        self.statusbar.setObjectName("statusbar")
        self.setStatusBar(self.statusbar)

        self.retranslateUi()
        QtCore.QMetaObject.connectSlotsByName(self)

        # Подключение слотов к кнопкам
        self.pushButton.clicked.connect(self.check_compatibility)
        self.pushButton_2.clicked.connect(self.add_user)
        self.load_users()

    def retranslateUi(self):
        _translate = QtCore.QCoreApplication.translate
        self.setWindowTitle(_translate("MainWindow", "G-Lune"))
        self.pushButton.setText(_translate("MainWindow", "Проверить совместимость"))
        self.label.setText(_translate("MainWindow", "Проверка совместимости"))
        self.label_2.setText(_translate("MainWindow", "Выберите первого пользователя"))
        self.label_3.setText(_translate("MainWindow", "Выберите второго пользователя"))
        self.label_4.setText(_translate("MainWindow", "Добавление пользователя"))
        self.label_5.setText(_translate("MainWindow", "Имя:"))
        self.label_6.setText(_translate("MainWindow", "Дата рождения: (ДД.ММ.ГГГГ)"))
        self.pushButton_2.setText(_translate("MainWindow", "Добавить пользователя"))
        self.centralwidget.setStyleSheet("background-image: url('_internal/static/ui/lune.png');")

    def load_users(self):
        self.comboBox.clear()
        self.comboBox_2.clear()
        users = self.db.load_users()
        for user in users:
            self.comboBox.addItem(user[1], user[0])  # добавляем имя с ID
            self.comboBox_2.addItem(user[1], user[0])

    def add_user(self):
        name = self.lineEdit.text().strip()
        date_of_birth = self.lineEdit_2.text().strip()

        # Валидация
        if not name or not date_of_birth:
            self.show_custom_message("Ошибка", "Пожалуйста, заполните все поля")
            return

        # Проверка формата ввода даты
        try:
            day, month, year = map(int, date_of_birth.split('.'))
            if not (1 <= day <= 31 and 1 <= month <= 12):
                raise ValueError("Недопустимая дата")
        except ValueError:
            self.show_custom_message("Ошибка", "Формат даты должен быть дд.мм.гггг")
            return

        # Добавление пользователя в базу данных
        try:
            if self.db.is_user_exists(name):
                self.show_custom_message("Ошибка", "Пользователь с таким именем уже существует.")
                return

            self.db.add_user(name, date_of_birth)
            self.show_custom_message("Успех", f"Пользователь {name} добавлен!")
            self.load_users()
            self.lineEdit.clear()
            self.lineEdit_2.clear()
        except Exception as e:
            self.show_custom_message("Ошибка", str(e))

    def check_compatibility(self):
        user1_id = self.comboBox.currentData()
        user2_id = self.comboBox_2.currentData()

        if user1_id is None or user2_id is None:
            self.show_custom_message("Ошибка", "Выберите обоих пользователей для проверки совместимости")
            return

        # Получение знаков зодиака
        users = self.db.load_users()
        user1 = users[user1_id - 1]  # получаем данные первого пользователя
        user2 = users[user2_id - 1]  # получаем данные второго пользователя

        if user1 and user2:
            name1, sign1 = user1[1], user1[2]  # Имя и знак зодиака первого пользователя
            name2, sign2 = user2[1], user2[2]  # Имя и знак зодиака второго пользователя
            result = check_compatibility(sign1, sign2)
            self.show_custom_message("Результат совместимости", result)

            # Сохранение результата совместимости в базу данных
            self.db.save_compatibility(name1, name2, result)
        else:
            self.show_custom_message("Ошибка", "Не удалось получить информацию о пользователях")

    def show_custom_message(self, title, message):
        msg_box = QMessageBox()
        msg_box.setWindowTitle(title)
        msg_box.setText(message)
        msg_box.setStyleSheet("background-color: #E8CAEC; color: black; font-family: 'Roboto Light'; font-size: 14px;")
        msg_box.exec_()

if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    main_app = MainApp()
    main_app.show()
    sys.exit(app.exec_())