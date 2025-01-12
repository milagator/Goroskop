import sys
import sqlite3
from PyQt5 import QtWidgets, QtCore, QtGui
from PyQt5.QtGui import QPixmap

# Основные данные
ZODIAC_SIGNS = [
    ("Овен", (3, 21), (4, 19), "static/img/aries.png"),
    ("Телец", (4, 20), (5, 20), "static/img/taurus.png"),
    ("Близнецы", (5, 21), (6, 20), "static/img/gemini.png"),
    ("Рак", (6, 21), (7, 22), "static/img/cancer.png"),
    ("Лев", (7, 23), (8, 22), "static/img/leo.png"),
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

# Класс для работы с базой данных
class Database:
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
        font.setPointSize(24)
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

class AstrologyApp(QtWidgets.QMainWindow, Ui_MainWindow):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.zodiac_sign = None  # Для хранения текущего знака
        self.db = Database()

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

# Запуск приложения
if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    window = AstrologyApp()
    window.show()
    sys.exit(app.exec_())