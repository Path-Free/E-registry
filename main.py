import sqlite3 as sl
import sys
from functools import partial

from PyQt5 import QtCore, QtGui, QtWidgets

import add
import table


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(800, 600)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 800, 21))
        self.menubar.setObjectName("menubar")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

        # Создание кнопок с помощью цикла и словаря
        buttons = {
            "pushButton": {"geometry": QtCore.QRect(20, 330, 751, 201), "font_size": 26, "bold": True,
                           "text": "ЗАПИСАТЬ КЛИЕНТА", "click": partial(self.add, "EVENTS")},
            "pushButton_2": {"geometry": QtCore.QRect(30, 22, 161, 281), "font_size": 20, "bold": False,
                             "text": "Услуги", "click": partial(self.table, "SERVICES", "Услуги")},
            "pushButton_3": {"geometry": QtCore.QRect(220, 20, 161, 281), "font_size": 20, "bold": False,
                             "text": "Должности", "click": partial(self.table, "POSITIONS", "Должности")},
            "pushButton_4": {"geometry": QtCore.QRect(410, 20, 161, 281), "font_size": 20, "bold": False,
                             "text": "Сотрудники", "click": partial(self.table, "EMPLOYEES", "Сотрудники")},
            "pushButton_5": {"geometry": QtCore.QRect(600, 20, 161, 281), "font_size": 20, "bold": False,
                             "text": "Пациенты", "click": partial(self.table, "CLIENTS", "Пациенты")},
        }

        for button_name, button_info in buttons.items():
            button = QtWidgets.QPushButton(self.centralwidget)
            button.setGeometry(button_info["geometry"])
            font = QtGui.QFont()
            font.setPointSize(button_info["font_size"])
            font.setBold(button_info["bold"])
            font.setWeight(75 if button_info["bold"] else 50)
            button.setFont(font)
            button.setObjectName(button_name)
            button.setText(button_info["text"])
            button.clicked.connect(button_info["click"])
            setattr(self, button_name, button)

        MainWindow.setWindowTitle("Электронная регистратура")

    # Функция для добавления записи
    def add(self, name):
        Dialog = QtWidgets.QDialog()
        ui_2 = add.Ui_Dialog()
        ui_2.table = self.table_info(name)
        ui_2.setupUi(Dialog)
        Dialog.show()
        Dialog.exec_()

    # Функция для отображения таблицы
    def table(self, name, title):
        Dialog = QtWidgets.QDialog()
        ui_2 = table.Ui_Dialog()
        ui_2.table = self.table_info(name)
        ui_2.title = title
        ui_2.setupUi(Dialog)
        Dialog.show()
        Dialog.exec_()

    # Функция для получения информации о таблице
    def table_info(self, name):
        with sl.connect("durka.db") as con:
            table_list = con.execute(f"SELECT * FROM {name}").fetchall()
            columns_info = con.execute(f"PRAGMA table_info({name});").fetchall()
            column_names = [x[1] for x in columns_info]
        return table_list, column_names, name


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())
