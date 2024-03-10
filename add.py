from functools import partial
from PyQt5 import QtCore, QtWidgets
import table
import sqlite3 as sl

con = sl.connect('durka.db')


class Ui_Dialog(object):
    widgets_dict = {
        "CLIENTS": {
            "ФИО:": "self.edit_1 = QtWidgets.QLineEdit(Dialog)",
            "Дата рождения:": "self.edit_2 = QtWidgets.QDateEdit(Dialog)",
            "Примечания:": "self.edit_3 = QtWidgets.QLineEdit(Dialog)",
            "Телефон:": "self.edit_4 = QtWidgets.QLineEdit(Dialog)"
        },
        "EMPLOYEES": {
            "ФИО:": "self.edit_1 = QtWidgets.QLineEdit(Dialog)",
            "Дата рождения:": "self.edit_2 = QtWidgets.QDateEdit(Dialog)",
            "Должность:": "self.edit_3 = QtWidgets.QComboBox(Dialog)\n"
                          """with con:
                              data = con.execute("SELECT name FROM POSITIONS").fetchall()
                              self.edit_3.addItems(str(*i) for i in data)""",
            "Телефон:": "self.edit_4 = QtWidgets.QLineEdit(Dialog)"
        },
        "SERVICES": {
            "Название:": "self.edit_1 = QtWidgets.QLineEdit(Dialog)",
            "Цена:": "self.edit_2 = QtWidgets.QDoubleSpinBox(Dialog)\nself.edit_2.setMaximum(100000)",
            "Длительность:": "self.edit_3 = QtWidgets.QTimeEdit(Dialog)",
            "Cпециальность врача:": "self.edit_4 = QtWidgets.QComboBox(Dialog)\n"
                                    """with con:
                                        data = con.execute("SELECT name FROM POSITIONS").fetchall()
                                        self.edit_4.addItems(str(*i) for i in data)"""
        },
        "EVENTS": {
            "Время:": "self.edit_1 = QtWidgets.QDateTimeEdit(Dialog)",
            "Клиент:": "self.edit_2 = QtWidgets.QComboBox(Dialog)\n"
                       """with con:
                          data = con.execute("SELECT name FROM CLIENTS").fetchall()
                          self.edit_2.addItems(str(*i) for i in data)""",
            "Врач:": "self.edit_3 = QtWidgets.QComboBox(Dialog)\n"
                     """with con:
                        data = con.execute("SELECT name FROM EMPLOYEES").fetchall()
                        self.edit_3.addItems(str(*i) for i in data)""",
            "Услуга:": "self.edit_4 = QtWidgets.QComboBox(Dialog)\n"
                       """with con:
                           data = con.execute("SELECT name FROM SERVICES").fetchall()
                           self.edit_4.addItems(str(*i) for i in data)"""
        },
        "POSITIONS": {
            "Название:": "self.edit_1 = QtWidgets.QLineEdit(Dialog)",
            "Зарплата:": "self.edit_2 = QtWidgets.QDoubleSpinBox(Dialog)\nself.edit_2.setMaximum(100000)",
            "Кабинет:": "self.edit_3 = QtWidgets.QLineEdit(Dialog)",
        }
    }

    def setupUi(self, Dialog):
        Dialog.setObjectName("Dialog")
        Dialog.resize(400, 400)
        self.pushButton = QtWidgets.QPushButton(Dialog)
        self.pushButton.setGeometry(QtCore.QRect(160, 350, 81, 31))
        self.pushButton.setObjectName("pushButton")
        self.pushButton.setText("Oк")
        position = [30, 20, 181, 22]
        widgets = self.widgets_dict[self.table[2]]
        edit_num = 1
        for k, v in widgets.items():
            self.label = QtWidgets.QLabel(Dialog)
            self.label.setGeometry(QtCore.QRect(*position))
            self.label.setObjectName("label")
            self.label.setText(k)
            exec(v)
            position[1] += 20
            exec(f"self.edit_{edit_num}.setGeometry(QtCore.QRect(*position))")
            exec(f"self.edit_{edit_num}.setObjectName('edit_{edit_num}')")
            position[1] += 30
            edit_num += 1

        self.pushButton.clicked.connect(partial(self.submit, Dialog))
        Dialog.setWindowTitle("Новая запись")

    def submit(self, Dialog):
        # Обработка нажатия кнопки "Ок"
        new_row = [len(self.table[0]) + 1]
        for i in range(1, len(self.widgets_dict[self.table[2]]) + 1):
            try:
                new_row.append(eval(f"self.edit_{i}.text()"))
            except AttributeError:
                new_row.append(eval(f"self.edit_{i}.currentText()"))
        self.table[0].append(tuple(new_row))
        Dialog.close()
        try:
            self.Dialog.close()
            Dialog1 = QtWidgets.QDialog()
            ui_2 = table.Ui_Dialog()
            ui_2.table = (self.table[0], self.table[1], self.table[2])
            ui_2.title = self.title
            ui_2.setupUi(Dialog1)
            Dialog1.show()
            Dialog1.exec_()
        except Exception as e:
            print(e)
