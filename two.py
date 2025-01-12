import sys
import sqlite3
from PyQt5 import QtWidgets, QtCore, QtGui
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

# Класс для работы с базой данных
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

# Основное приложение
class AstrologyApp(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        self.db = Database()  # Создаем соединение с базой данных
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
        self.pushButton.setStyleSheet("background: linear-gradient(90deg, rgba(238, 240, 252, 0) 0%, rgba(255, 255, 255, 0.2) 50%, rgba(238, 240, 252, 0) 100%), #E8CAEC;\n"
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
        self.comboBox.setStyleSheet("background: linear-gradient(90deg, rgba(238, 240, 252, 0) 0%, rgba(255, 255, 255, 0.2) 50%, rgba(238, 240, 252, 0) 100%), #E2E2E2;\n"
                                     "box-shadow: 0px 4px 3.8px rgba(0, 0, 0, 0.25);\n"
                                     "border-radius: 28px;")
        self.comboBox.setFont(QtGui.QFont("Roboto Light", 12))
        self.comboBox.setObjectName("comboBox")

        self.comboBox_2 = QtWidgets.QComboBox(self.centralwidget)
        self.comboBox_2.setGeometry(QtCore.QRect(157, 523, 601, 44))
        self.comboBox_2.setStyleSheet("background: linear-gradient(90deg, rgba(238, 240, 252, 0) 0%, rgba(255, 255, 255, 0.2) 50%, rgba(238, 240, 252, 0) 100%), #E2E2E2;\n"
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
        self.pushButton_2.setStyleSheet("background: linear-gradient(90deg, rgba(238, 240, 252, 0) 0%, rgba(255, 255, 255, 0.2) 50%, rgba(238, 240, 252, 0) 100%), #E8CAEC;\n"
                                         "box-shadow: 0px 4px 3.8px rgba(0, 0, 0, 0.25);\n"
                                         "border-radius: 20px;")
        self.pushButton_2.setObjectName("pushButton_2")

        # Поля ввода
        self.lineEdit = QtWidgets.QLineEdit(self.centralwidget)
        self.lineEdit.setGeometry(QtCore.QRect(1190, 400, 601, 44))
        font.setPointSize(12)
        self.lineEdit.setFont(font)
        self.lineEdit.setStyleSheet("background: linear-gradient(90deg, rgba(238, 240, 252, 0) 0%, rgba(255, 255, 255, 0.2) 50%, rgba(238, 240, 252, 0) 100%), #DFDFDF;\n"
                                    "box-shadow: 0px 4px 3.8px rgba(0, 0, 0, 0.25);\n"
                                    "border-radius: 28px; padding-left: 10px;")
        self.lineEdit.setObjectName("lineEdit")

        self.lineEdit_2 = QtWidgets.QLineEdit(self.centralwidget)
        self.lineEdit_2.setGeometry(QtCore.QRect(1190, 523, 601, 44))
        self.lineEdit_2.setStyleSheet("background: linear-gradient(90deg, rgba(238, 240, 252, 0) 0%, rgba(255, 255, 255, 0.2) 50%, rgba(238, 240, 252, 0) 100%), #DFDFDF;\n"
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
        self.centralwidget.setStyleSheet("background-image: url('static/ui/lune.png');")

    def load_users(self):
        self.comboBox.clear()
        self.comboBox_2.clear()
        users = self.db.load_users()
        for user in users:
            self.comboBox.addItem(user[1], user[0])  # добавляем имя с ID
            self.comboBox_2.addItem(user[1], user[0])

    def add_user(self):
        name = self.lineEdit.text()
        date_of_birth = self.lineEdit_2.text()

        # Валидация
        if not name or not date_of_birth:
            self.show_custom_message("Ошибка", "Пожалуйста, заполните все поля")
            return

        # Проверка формата ввода даты
        try:
            day, month, year = map(int, date_of_birth.split('.'))
            if not (1 <= day <= 31 and 1 <= month <= 12):
                raise ValueError("Недопустимая дата")
        except Exception:
            self.show_custom_message("Ошибка", "Формат даты должен быть дд.мм.гггг")
            return

        # Добавление пользователя в базу данных
        try:
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
    astrology_app = AstrologyApp()
    astrology_app.show()
    sys.exit(app.exec_())