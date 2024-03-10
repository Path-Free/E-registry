from PyQt5 import QtCore, QtGui, QtWidgets
import add
import sqlite3 as sl
from functools import partial


class Ui_Dialog(object):
    def setupUi(self, Dialog):
        Dialog.setObjectName("Dialog")
        Dialog.resize(600, 500)
        self.tableWidget = QtWidgets.QTableWidget(Dialog)
        self.tableWidget.setGeometry(QtCore.QRect(20, 70, 551, 411))
        self.tableWidget.setObjectName("tableWidget")
        self.tableWidget.verticalHeader().setVisible(False)
        self.tableWidget.setSelectionBehavior(QtWidgets.QTableView.SelectRows)
        self.table_gen()
        QtCore.QMetaObject.connectSlotsByName(Dialog)

        # Создание кнопок с помощью цикла и словаря
        buttons = {
            "pushButton": {"geometry": QtCore.QRect(20, 20, 91, 31), "text": "Добавить",
                           "click": partial(self.add, Dialog)},
            "pushButton_2": {"geometry": QtCore.QRect(130, 20, 91, 31), "text": "Сохранить", "click": self.save},
            "pushButton_3": {"geometry": QtCore.QRect(240, 20, 91, 31), "text": "Удалить", "click": self.delete},
            "pushButton_4": {"geometry": QtCore.QRect(484, 20, 91, 31), "text": "Отменить",
                             "click": partial(self.cancel, Dialog)},
        }

        for button_name, button_info in buttons.items():
            button = QtWidgets.QPushButton(Dialog)
            button.setGeometry(button_info["geometry"])
            button.setObjectName(button_name)
            button.setText(button_info["text"])
            button.clicked.connect(button_info["click"])
            setattr(self, button_name, button)

        Dialog.setWindowTitle(self.title)

    # Функция для генерации таблицы
    def table_gen(self):
        table_list = self.table[0]
        column_names = self.table[1]
        self.tableWidget.setColumnCount(len(table_list[0]))
        self.tableWidget.setRowCount(len(table_list))
        self.tableWidget.setHorizontalHeaderLabels(column_names)
        for i in range(0, len(table_list)):
            for j in range(0, len(table_list[0])):
                item = QtWidgets.QTableWidgetItem
                self.tableWidget.setItem(i, j, item(str(table_list[i][j])))

    # Функция для добавления записи
    def add(self, Dialog):
        Dialog1 = QtWidgets.QDialog()
        ui_2 = add.Ui_Dialog()
        ui_2.table = self.table
        ui_2.title = self.title
        ui_2.Dialog = Dialog
        ui_2.setupUi(Dialog1)
        Dialog1.show()
        Dialog1.exec_()

    # Функция для сохранения изменений
    def save(self):
        con = sl.connect("durka.db")
        table = self.table
        quest_signs = "?"
        quest_signs += ", ?" * (len(table[1]) - 1)
        column_list = " ,".join(table[1])
        sql_insert = f"INSERT OR IGNORE INTO {table[2]} ({column_list}) values({quest_signs})"
        with con:
            con.execute(f"DELETE FROM {table[2]}")
            for i in range(0, len(table[0])):
                con.execute(sql_insert, list(table[0][i]))
            data = con.execute(f"SELECT * FROM {table[2]}").fetchall()
        print(data)

    # Функция для удаления записи
    def delete(self):
        selected = self.tableWidget.selectedItems()[0].row()
        self.tableWidget.removeRow(selected)
        print(selected)
        for x in self.table[0]:
            print(x)
            if x[0] == selected + 1:
                self.table[0].remove(x)
        print(self.table[0])

    # Функция для отмены действия и возврата к предыдущему диалогу
    def cancel(self, Dialog):
        Dialog.close()
        print(self.table)
        Dialog1 = QtWidgets.QDialog()
        ui_2 = Ui_Dialog()
        ui_2.table = self.table_info()
        ui_2.title = self.title
        ui_2.setupUi(Dialog1)
        Dialog1.show()
        Dialog1.exec_()

    # Функция для получения информации о таблице
    def table_info(self):
        with sl.connect("durka.db") as con:
            table_name = self.table[2]
            table_list = con.execute(f"SELECT * FROM {table_name}").fetchall()
            columns_info = con.execute(f"PRAGMA table_info({table_name});").fetchall()
            column_names = [x[1] for x in columns_info]
        return table_list, column_names, table_name
