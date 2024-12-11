import sys
import sqlite3
from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QMessageBox, QComboBox

# Основные данные (например, знаки зодиака и совместимость)
ZODIAC_SIGNS = [
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
def get_zodiac_sign(day, month):
    for sign, start_date, end_date in ZODIAC_SIGNS:
        if (month == start_date[0] and day >= start_date[1]) or \
                (month == end_date[0] and day <= end_date[1]):
            return sign
    return "Неизвестный знак"

# Функция для проверки совместимости
def check_compatibility(sign1, sign2):
    if sign2 in COMPATIBILITY.get(sign1, []):
        return f"Знаки {sign1} и {sign2} совместимы!"
    return f"Знаки {sign1} и {sign2} несовместимы."

# Класс для работы с базами данных
class Database:
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
        zodiac_sign = get_zodiac_sign(day, month)

        cursor.execute("INSERT INTO users (name, date_of_birth, zodiac_sign) VALUES (?, ?, ?)",
                       (name, date_of_birth, zodiac_sign))
        self.user_connection.commit()

    def load_users(self):
        cursor = self.user_connection.cursor()
        cursor.execute("SELECT id, name FROM users")
        return cursor.fetchall()

    def save_compatibility(self, name1, name2, compatibility):
        cursor = self.compatibility_connection.cursor()
        cursor.execute("INSERT INTO compatibility_results (name1, name2, compatibility) VALUES (?, ?, ?)",
                       (name1, name2, compatibility))
        self.compatibility_connection.commit()

    def close(self):
        self.user_connection.close()
        self.compatibility_connection.close()

# Основное приложение
class AstrologyApp(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Астрологическое приложение")
        self.setGeometry(100, 100, 400, 300)

        # Создаем базу данных
        self.db = Database()

        # UI компоненты
        self.name_input = QtWidgets.QLineEdit(self)
        self.name_input.setPlaceholderText("Введите ваше имя")

        self.dob_input = QtWidgets.QLineEdit(self)
        self.dob_input.setPlaceholderText("Введите дату рождения (дд.мм.гггг)")

        self.add_user_button = QtWidgets.QPushButton("Добавить пользователя", self)
        self.add_user_button.clicked.connect(self.add_user)

        self.user1_combo = QComboBox(self)
        self.user2_combo = QComboBox(self)
        self.load_users()

        self.check_compatibility_button = QtWidgets.QPushButton("Проверить совместимость", self)
        self.check_compatibility_button.clicked.connect(self.check_compatibility)

        # Расположение
        layout = QtWidgets.QVBoxLayout()
        layout.addWidget(self.name_input)
        layout.addWidget(self.dob_input)
        layout.addWidget(self.add_user_button)
        layout.addWidget(QtWidgets.QLabel("Выберите первого пользователя:"))
        layout.addWidget(self.user1_combo)
        layout.addWidget(QtWidgets.QLabel("Выберите второго пользователя:"))
        layout.addWidget(self.user2_combo)
        layout.addWidget(self.check_compatibility_button)

        self.setLayout(layout)

    def load_users(self):
        self.user1_combo.clear()
        self.user2_combo.clear()
        users = self.db.load_users()
        for user in users:
            self.user1_combo.addItem(user[1], user[0])  # добавляем имя с ID
            self.user2_combo.addItem(user[1], user[0])

    def add_user(self):
        name = self.name_input.text()
        date_of_birth = self.dob_input.text()

        # Валидация
        if not name or not date_of_birth:
            QMessageBox.critical(self, "Ошибка", "Пожалуйста, заполните все поля")
            return

        # Проверка формата ввода даты
        try:
            day, month, year = map(int, date_of_birth.split('.'))
            if not (1 <= day <= 31 and 1 <= month <= 12):
                raise ValueError("Недопустимая дата")
        except Exception as e:
            QMessageBox.critical(self, "Ошибка", "Формат даты должен быть дд.мм.гггг")
            return

        # Добавление пользователя
        try:
            self.db.add_user(name, date_of_birth)
            QMessageBox.information(self, "Успех", f"Пользователь {name} добавлен!")
            self.load_users()
            self.name_input.clear()
            self.dob_input.clear()
        except Exception as e:
            QMessageBox.critical(self, "Ошибка", str(e))

    def check_compatibility(self):
        user1_id = self.user1_combo.currentData()
        user2_id = self.user2_combo.currentData()

        if user1_id is None or user2_id is None:
            QMessageBox.critical(self, "Ошибка", "Выберите обоих пользователей для проверки совместимости")
            return

        # Получение имен и знаков зодиака
        user1 = self.db.user_connection.execute("SELECT name, zodiac_sign FROM users WHERE id = ?", (user1_id,)).fetchone()
        user2 = self.db.user_connection.execute("SELECT name, zodiac_sign FROM users WHERE id = ?", (user2_id,)).fetchone()

        if user1 and user2:
            name1, sign1 = user1
            name2, sign2 = user2
            result = check_compatibility(sign1, sign2)
            QMessageBox.information(self, "Результат совместимости", result)

            # Сохранение результата совместимости в базу данных
            self.db.save_compatibility(name1, name2, result)
        else:
            QMessageBox.critical(self, "Ошибка", "Не удалось получить информацию о пользователях")

    def closeEvent(self, event):
        self.db.close()
        event.accept()

if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    mainWin = AstrologyApp()
    mainWin.show()
    sys.exit(app.exec_())