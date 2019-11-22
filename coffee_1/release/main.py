import sys
import sqlite3
from PyQt5.QtWidgets import QApplication, QMainWindow, QTableWidget, \
    QTableWidgetItem
from PyQt5 import QtCore, QtGui, QtWidgets
from addEditCoffeeForm import UiAdd
from widget import Ui_MainWindow


class MainTable(QMainWindow, Ui_MainWindow):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.update_table()
        self.pushButton.clicked.connect(self.run)

    def update_table(self):
        con = sqlite3.connect('data\coffee.db')
        cur = con.cursor()
        head = [x[1] for x in cur.execute(
            """PRAGMA table_info(coffee_info)""").fetchall()]
        table_values = cur.execute(
            '''select * from coffee_info''').fetchall()

        con.close()
        self.tableWidget.setColumnCount(len(head))
        self.tableWidget.setHorizontalHeaderLabels(head)
        self.tableWidget.setRowCount(0)
        for i, row in enumerate(table_values):
            self.tableWidget.setRowCount(self.tableWidget.rowCount() + 1)
            for j, elem in enumerate(row):
                self.tableWidget.setItem(i, j,
                                         QTableWidgetItem(str(elem)))
        self.tableWidget.resizeColumnsToContents()

    def run(self):
        self.new_win = AddTable()
        self.new_win.show()


class AddTable(QMainWindow, UiAdd):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.con = sqlite3.connect("data\coffee.db")
        self.update_table()
        self.modified = {}

        self.tableWidget.itemChanged.connect(self.item_changed)
        self.pushButton.clicked.connect(self.save_results)
        self.pushButton_2.clicked.connect(self.add_to_db)

    def update_table(self):
        con = sqlite3.connect('data\coffee.db')
        cur = con.cursor()
        head = [x[1] for x in cur.execute(
            """PRAGMA table_info(coffee_info)""").fetchall()]
        table_values = cur.execute(
            '''select * from coffee_info''').fetchall()
        self.titles = [description[0] for description in cur.description]
        con.close()
        self.tableWidget.setColumnCount(len(head))
        self.tableWidget.setHorizontalHeaderLabels(head)
        self.tableWidget.setRowCount(0)
        for i, row in enumerate(table_values):
            self.tableWidget.setRowCount(self.tableWidget.rowCount() + 1)
            for j, elem in enumerate(row):
                self.tableWidget.setItem(i, j,
                                         QTableWidgetItem(str(elem)))
        self.tableWidget.resizeColumnsToContents()

    def item_changed(self, item):
        self.modified[self.titles[item.column()]] = item.text()

    def save_results(self):
        if self.modified:
            print(self.modified)
            cur = self.con.cursor()
            que = "UPDATE coffee_info SET\n"
            for key in self.modified.keys():
                que += "{}='{}'\n".format(key, self.modified.get(key))
            que += "WHERE name = ?"
            cur.execute(que, (self.lineEdit.text(),))
            self.con.commit()
            self.update_table()

    def add_to_db(self):
        cur = self.con.cursor()
        name = self.lineEdit.text()
        roast = self.lineEdit_2.text()
        ground_grains = self.lineEdit_3.text()
        taste = self.lineEdit_4.text()
        price = self.lineEdit_5.text()
        volume = self.lineEdit_6.text()
        cur.execute(
            '''insert into coffee_info(name, roast, ground_grains, taste, 
            price, volume)
                values(?, ?, ?, ?, ?, ?)''',
            (name, roast, ground_grains, taste,
             price, volume))
        self.con.commit()
        self.update_table()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = MainTable()
    ex.show()
    sys.exit(app.exec())
