import sys
import sqlite3
from PyQt5 import QtWidgets, QtCore
from PyQt5.QtGui import QPixmap

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
            return sign
    return "Неизвестный знак"

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
class AstrologyApp(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        self.zodiac_sign = None  # Для хранения текущего знака
        self.init_ui()
        self.db = Database()

    def init_ui(self):
        self.setWindowTitle("Астрологическое приложение")
        self.setGeometry(100, 100, 400, 400)

        layout = QtWidgets.QVBoxLayout()

        self.label_title = QtWidgets.QLabel("Астрологическое приложение", self)
        self.label_title.setStyleSheet("font-size: 20px;")
        layout.addWidget(self.label_title)

        self.label_name = QtWidgets.QLabel("Имя:", self)
        layout.addWidget(self.label_name)
        self.text_name = QtWidgets.QLineEdit(self)
        layout.addWidget(self.text_name)

        self.label_dob = QtWidgets.QLabel("Дата рождения (ДД.ММ.ГГГГ):", self)
        layout.addWidget(self.label_dob)
        self.text_dob = QtWidgets.QLineEdit(self)
        layout.addWidget(self.text_dob)

        self.button_generate = QtWidgets.QPushButton("Сгенерировать гороскоп", self)
        self.button_generate.clicked.connect(self.generate_horoscope)
        layout.addWidget(self.button_generate)

        self.label_result = QtWidgets.QLabel("Ваш гороскоп:", self)
        layout.addWidget(self.label_result)

        self.result_text = QtWidgets.QLabel("", self)
        layout.addWidget(self.result_text)

        # Кнопка для получения подробностей
        self.button_details = QtWidgets.QPushButton("Узнать подробней", self)
        self.button_details.setEnabled(False)  # Неактивна, пока знак не определен
        self.button_details.clicked.connect(self.show_details)
        layout.addWidget(self.button_details)

        # Элементы управления для загрузки и изменения данных пользователя
        self.label_user_name = QtWidgets.QLabel("Найти пользователя:", self)
        layout.addWidget(self.label_user_name)

        self.text_user_name = QtWidgets.QLineEdit(self)
        layout.addWidget(self.text_user_name)

        self.button_load = QtWidgets.QPushButton("Загрузить данные", self)
        self.button_load.clicked.connect(self.load_user_data)
        layout.addWidget(self.button_load)

        self.button_update = QtWidgets.QPushButton("Изменить данные", self)
        self.button_update.clicked.connect(self.update_user_data)
        layout.addWidget(self.button_update)

        self.image_label = QtWidgets.QLabel(self)
        self.image_label.setAlignment(QtCore.Qt.AlignCenter)
        layout.addWidget(self.image_label)

        self.setLayout(layout)

    def generate_horoscope(self):
        name = self.text_name.text()
        dob = self.text_dob.text()

        try:
            # Парсинг даты рождения
            day, month, year = map(int, dob.split('.'))
            self.zodiac_sign = get_zodiac_sign(day, month)  # Получаем знак зодиака и сохраняем его
            horoscope = generate_horoscope(self.zodiac_sign)  # Генерируем гороскоп

            # Сохранение данных пользователя в базу данных
            self.db.insert_user(name, dob, self.zodiac_sign)

            # Вывод результата
            self.result_text.setText(f"Привет, {name}! Ваш знак зодиака: {self.zodiac_sign}.\n{horoscope}")
            self.update_image(self.zodiac_sign)  # Обновляем изображение знака
            self.button_details.setEnabled(True)  # Активируем кнопку "Узнать подробней"

        except ValueError:
            QtWidgets.QMessageBox.critical(self, "Ошибка", "Введите дату в формате ДД.ММ.ГГГГ.")
        except Exception as e:
            QtWidgets.QMessageBox.critical(self, "Ошибка", f"Произошла ошибка: {str(e)}")

    def show_details(self):
        if self.zodiac_sign is None:
            QtWidgets.QMessageBox.warning(self, "Предупреждение", "Сначала сгенерируйте гороскоп.")
            return

        try:
            # Формируем путь к файлу
            file_path = f"static/files/{self.zodiac_sign}.txt"
            print(f"Открывается файл: {file_path}")

            # Открываем файл и читаем содержимое
            with open(file_path, "r", encoding="utf-8") as file:
                details = file.read()

            # Показать информацию в новом окне
            detail_window = QtWidgets.QMessageBox(self)
            detail_window.setWindowTitle(f"Подробности о знаке {self.zodiac_sign}")
            detail_window.setText(details)
            detail_window.exec_()

        except FileNotFoundError:
            QtWidgets.QMessageBox.critical(self, "Ошибка", f"Файл '{file_path}' не найден.")
        except Exception as e:
            QtWidgets.QMessageBox.critical(self, "Ошибка", f"Произошла ошибка: {str(e)}")

    def update_image(self, zodiac_sign):
        for sign, start_date, end_date, image in ZODIAC_SIGNS:
            if sign == zodiac_sign:
                pixmap = QPixmap(image)
                self.image_label.setPixmap(pixmap.scaled(300, 300, QtCore.Qt.KeepAspectRatio))
                break

    def closeEvent(self, event):
        self.db.close()

    def load_user_data(self):
        user_name = self.text_user_name.text()
        try:
            user_data = self.db.get_user(user_name)
            if user_data:
                name, dob, zodiac_sign = user_data
                self.text_name.setText(name)
                self.text_dob.setText(dob)
                self.result_text.setText(f"Знак зодиака: {zodiac_sign}.")
                self.update_image(zodiac_sign)  # Обновить изображение знака

                # Обновляем текущий знак зодиака для вызова подробностей
                self.zodiac_sign = zodiac_sign

                # Активируем кнопку для получения подробностей
                self.button_details.setEnabled(True)
                self.button_details.setEnabled(True)
            else:
                QtWidgets.QMessageBox.critical(self, "Ошибка", "Пользователь не найден.")
        except Exception as e:
            QtWidgets.QMessageBox.critical(self, "Ошибка", f"Произошла ошибка: {str(e)}")

    def update_user_data(self):
        user_name = self.text_user_name.text().strip()  # Удаляет пробелы
        dob = self.text_dob.text().strip()  # Удаляет пробелы

        try:
            # Проверка на пустые значения
            if not user_name or not dob:
                QtWidgets.QMessageBox.critical(self, "Ошибка", "Пожалуйста, введите имя пользователя и дату рождения.")
                return

            # Парсинг даты рождения
            day, month, year = map(int, dob.split('.'))
            zodiac_sign = get_zodiac_sign(day, month)

            # Проверка, существует ли пользователь перед обновлением
            existing_user = self.db.get_user(user_name)
            if not existing_user:
                QtWidgets.QMessageBox.critical(self, "Ошибка", "Пользователь не найден.")
                return

            # Обновление данных в базе данных
            self.db.update_user(user_name, dob, zodiac_sign)
            QtWidgets.QMessageBox.information(self, "Успех", "Данные пользователя успешно обновлены.")
        except ValueError:
            QtWidgets.QMessageBox.critical(self, "Ошибка", "Введите дату в формате ДД.ММ.ГГГГ.")
        except Exception as e:
            QtWidgets.QMessageBox.critical(self, "Ошибка", f"Произошла ошибка: {str(e)}")

# Запуск приложения
if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    window = AstrologyApp()
    window.show()
    sys.exit(app.exec_())