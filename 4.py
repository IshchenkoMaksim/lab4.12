#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from PySide2.QtSql import QSqlDatabase, QSqlQuery, QSqlTableModel
from PySide2.QtWidgets import (
    QTableView,
    QApplication,
    QHBoxLayout,
    QGridLayout,
    QPushButton,
    QWidget,
    QLineEdit,
    QFrame,
    QLabel,
    QHeaderView,
    QDateEdit,
    QTabWidget
)
from PySide2.QtCore import (
    QAbstractTableModel,
    Signal,
    Slot,
)
from PySide2.QtCore import QSortFilterProxyModel, Qt, QRect
import sys


class DateBase:
    def __init__(self, db_file) -> None:
        db = QSqlDatabase.addDatabase("QSQLITE")
        db.setDatabaseName(db_file)
        if not db.open():
            return False
        self.q = QSqlQuery()
        self.q.exec_(
            """
        CREATE TABLE IF NOT EXISTS Subscribers (
            "ФИО" text,
            "Статус" text,
            "Дата рождения" date,
            "Серия и номер паспорта" text PRIMARY KEY);"""
        )
        self.q.exec_(
            """
        CREATE TABLE IF NOT EXISTS Periodical (
            "Идентификатор" text PRIMARY KEY,
            "Название" text,
            "Дата начала выпуска" date,
            "Дата окончания выпуска" date);"""
        )
        self.q.exec_(
            """
        CREATE TABLE IF NOT EXISTS Subscriptions (
            "Серия номер паспорта" text,
            "Идентификатор изд." text,
            "Начало подписки" date,
            "Конец подписки" date);"""
        )
        self.q.exec_(
            """INSERT INTO Subscribers VALUES("Артур Хейли", "Обычный", "05.04.1920", "1212344556")"""
        )
        self.q.exec_(
            """INSERT INTO Subscribers VALUES("Барин Володимир", "Vip", "17.11.1985", "6412344556")"""
        )
        self.q.exec_(
            """INSERT INTO Subscribers VALUES("Эльдар Татар", "Писатель", "09.09.2009", "0399568675")"""
        )
        self.q.exec_(
            """INSERT INTO Periodical VALUES("#4537", "Аргументы и факты", "1.01.1999", "30.01.2030")"""
        )
        self.q.exec_(
            """INSERT INTO Periodical VALUES("#0004", "Анекдоты от", "08.08.2017", "08.08.2024")"""
        )
        self.q.exec_(
            """INSERT INTO Periodical VALUES("#1186", "Время", "11.11.1991", "11.11.2111")"""
        )
        self.q.exec_(
            """INSERT INTO Subscriptions VALUES("1212344556", "#0004", "01.01.2022", "01.01.2023")"""
        )
        self.q.exec_(
            """INSERT INTO Subscriptions VALUES("6412344556", "#4537", "20.12.2021", "20.06.2023")"""
        )
        self.q.exec_(
            """INSERT INTO Subscriptions VALUES("0399568675", "#1186", "11.11.2020", "11.11.2025")"""
        )


class TableView:
    tabBarClicked = Signal(int)

    def __init__(self, parent):
        self.parent = parent
        self.SetupUI()
        self.current_tab = "Subscribers"
        self.tab_id = "Серия и номер паспорта"

    def SetupUI(self):
        self.parent.setGeometry(50, 100, 750, 450)
        self.parent.setWindowTitle("Подписчики периодических изданий")
        self.main_conteiner = QGridLayout()
        self.frame1 = QFrame()
        self.frame2 = QFrame()
        self.frame2.setVisible(False)
        self.main_conteiner.addWidget(self.frame1, 0, 0)
        self.main_conteiner.addWidget(self.frame2, 0, 0)
        self.frame1.setStyleSheet(
            """
            font-size: 13px;
            """
        )
        self.frame2.setStyleSheet(
            """
            font-size: 13px;
            """
        )
        self.table_view = QTableView()
        self.table_view.setModel(self.tableSubscribers())
        self.table_view2 = QTableView()
        self.table_view2.setModel(self.tablePeriodical())
        self.table_view3 = QTableView()
        self.table_view3.setModel(self.tableSubscriptions())
        self.table_view.horizontalHeader().setSectionResizeMode(0, QHeaderView.Stretch)
        self.table_view.horizontalHeader().setSectionResizeMode(1, QHeaderView.Stretch)
        self.table_view.horizontalHeader().setSectionResizeMode(2, QHeaderView.Stretch)
        self.table_view.horizontalHeader().setSectionResizeMode(3, QHeaderView.Stretch)
        self.table_view2.horizontalHeader().setSectionResizeMode(0, QHeaderView.Stretch)
        self.table_view2.horizontalHeader().setSectionResizeMode(1, QHeaderView.Stretch)
        self.table_view2.horizontalHeader().setSectionResizeMode(2, QHeaderView.Stretch)
        self.table_view2.horizontalHeader().setSectionResizeMode(3, QHeaderView.Stretch)
        self.table_view3.horizontalHeader().setSectionResizeMode(0, QHeaderView.Stretch)
        self.table_view3.horizontalHeader().setSectionResizeMode(1, QHeaderView.Stretch)
        self.table_view3.horizontalHeader().setSectionResizeMode(2, QHeaderView.Stretch)
        self.table_view3.horizontalHeader().setSectionResizeMode(3, QHeaderView.Stretch)
        self.layout_main = QGridLayout(self.frame1)
        self.layh = QHBoxLayout()
        self.btn_add = QPushButton("Добавить")
        self.btn_del = QPushButton("Удалить")
        self.layh.addWidget(self.btn_add)
        self.layh.addWidget(self.btn_del)
        self.tab_conteiner = QTabWidget()
        self.tab_conteiner.setTabShape(QTabWidget.Rounded)
        self.tab_conteiner.setTabPosition(QTabWidget.South)
        self.tab_conteiner.addTab(self.table_view, "Подписчики")
        self.tab_conteiner.addTab(self.table_view2, "Издания")
        self.tab_conteiner.addTab(self.table_view3, "Подписки")
        self.layout_main.addWidget(self.tab_conteiner, 3, 0)
        self.layout_main.addLayout(self.layh, 0, 0)
        self.parent.setLayout(self.main_conteiner)
        self.btn_del.clicked.connect(self.delete)
        self.btn_add.clicked.connect(self.add)
        self.layout_grid = QGridLayout(self.frame2)
        self.btn_add2 = QPushButton("Добавить данные")
        self.btn_add2.setFixedWidth(300)
        self.btn_otmena = QPushButton("Отмена")
        self.name_line = QLineEdit()
        self.name = QLabel("ФИО: ")
        self.status_line = QLineEdit()
        self.status = QLabel("Статус: ")
        self.dateb_line = QDateEdit()
        self.dateb_line.setCalendarPopup(True)
        self.dateb_line.setTimeSpec(Qt.LocalTime)
        self.dateb_line.setGeometry(QRect(220, 31, 133, 20))
        self.dateb = QLabel("Дата рождения: ")
        self.pasport_line = QLineEdit()
        self.pasport = QLabel("Номер и серия паспорта: ")
        self.periodical_line = QLineEdit()
        self.periodical = QLabel("Издание: ")
        self.daten_line = QDateEdit()
        self.daten_line.setCalendarPopup(True)
        self.daten_line.setTimeSpec(Qt.LocalTime)
        self.daten_line.setGeometry(QRect(220, 31, 133, 20))
        self.daten = QLabel("Дата начала подписки: ")
        self.datek_line = QDateEdit()
        self.datek_line.setCalendarPopup(True)
        self.datek_line.setTimeSpec(Qt.LocalTime)
        self.datek_line.setGeometry(QRect(220, 31, 133, 20))
        self.datek = QLabel("Дата конца подписки: ")
        self.layout_grid.addWidget(self.name_line, 0, 1)
        self.layout_grid.addWidget(self.name, 0, 0)
        self.layout_grid.addWidget(self.status, 1, 0)
        self.layout_grid.addWidget(self.status_line, 1, 1)
        self.layout_grid.addWidget(self.dateb, 2, 0)
        self.layout_grid.addWidget(self.dateb_line, 2, 1)
        self.layout_grid.addWidget(self.pasport_line, 3, 1)
        self.layout_grid.addWidget(self.pasport, 3, 0)
        self.layout_grid.addWidget(self.periodical_line, 4, 1)
        self.layout_grid.addWidget(self.periodical, 4, 0)
        self.layout_grid.addWidget(self.daten, 5, 0)
        self.layout_grid.addWidget(self.daten_line, 5, 1)
        self.layout_grid.addWidget(self.datek, 6, 0)
        self.layout_grid.addWidget(self.datek_line, 6, 1)
        self.layout_grid.addWidget(self.btn_add2, 7, 1)
        self.layout_grid.addWidget(self.btn_otmena, 7, 0)
        self.btn_otmena.clicked.connect(self.back)
        self.btn_add2.clicked.connect(self.add_data)
        self.tab_conteiner.tabBarClicked.connect(self.handle_tabbar_clicked)

    def tableSubscribers(self):
        self.raw_model = QSqlTableModel()
        self.sqlquery = QSqlQuery()
        self.query = """SELECT * FROM Subscribers"""
        self.sqlquery.exec_(self.query)
        self.raw_model.setQuery(self.sqlquery)
        self.current_tab = "Subscribers"
        self.model = QSortFilterProxyModel()
        self.model.setSourceModel(self.raw_model)
        return self.model

    def tablePeriodical(self):
        self.raw_model = QSqlTableModel()
        self.sqlquery = QSqlQuery()
        self.query = """SELECT * FROM Periodical"""
        self.sqlquery.exec_(self.query)
        self.raw_model.setQuery(self.sqlquery)
        self.current_tab = "Periodical"
        self.model = QSortFilterProxyModel()
        self.model.setSourceModel(self.raw_model)
        return self.model

    def tableSubscriptions(self):
        self.raw_model = QSqlTableModel()
        self.sqlquery = QSqlQuery()
        self.query = """SELECT * FROM Subscriptions"""
        self.sqlquery.exec_(self.query)
        self.raw_model.setQuery(self.sqlquery)
        self.current_tab = "Subscriptions"
        self.tab_id = "Серия номер паспорта"
        self.model = QSortFilterProxyModel()
        self.model.setSourceModel(self.raw_model)
        return self.model

    def add(self):
        self.frame1.setVisible(False)
        self.frame2.setVisible(True)

    def back(self):
        self.frame1.setVisible(True)
        self.frame2.setVisible(False)

    def update(self):
        self.table_view.setModel(self.tableSubscribers())
        self.table_view2.setModel(self.tablePeriodical())
        self.table_view3.setModel(self.tableSubscriptions())

    def add_data(self):
        self.sqlquery = QSqlQuery()
        self.query = "INSERT INTO Subscribers VALUES('{}', '{}', '{}', '{}')".format(self.name_line.text(), self.status_line.text(), self.dateb_line.text(), self.pasport_line.text())
        self.sqlquery.exec_(self.query)
        self.query = "INSERT INTO Subscriptions VALUES('{}', '{}', '{}', '{}')".format(self.pasport_line.text(), self.periodical_line.text(), self.daten_line.text(), self.datek_line.text())
        self.sqlquery.exec_(self.query)
        self.update()
        self.frame1.setVisible(True)
        self.frame2.setVisible(False)

    def cell_click(self):
        if self.current_tab == "Subscribers":
            return self.table_view.model().data(self.table_view.currentIndex())
        if self.current_tab == "Periodical":
            return self.table_view2.model().data(self.table_view2.currentIndex())
        if self.current_tab == "Subscriptions":
            return self.table_view3.model().data(self.table_view3.currentIndex())

    def delete(self):
        self.sqlquery = QSqlQuery()
        self.query = f"""DELETE FROM {self.current_tab} WHERE ("{self.tab_id}" = "{self.cell_click()}")"""
        print(self.query)
        self.sqlquery.exec_(self.query)
        self.update()

    def handle_tabbar_clicked(self, index):
        if(index==0):
            self.current_tab = "Subscribers"
            self.tab_id = "Серия и номер паспорта"
        elif(index==1):
            self.current_tab = "Periodical"
            self.tab_id = "Идентификатор"
        else:
            self.current_tab = "Subscriptions"
            self.tab_id = "Серия номер паспорта"


class MainWindow(QWidget):
    def __init__(self) -> None:
        QWidget.__init__(self)
        self.my_datebase = DateBase("datebase.db")
        if not self.my_datebase:
            sys.exit(-1)
        self.main_view = TableView(self)


def main():
    app = QApplication(sys.argv)
    main_window = MainWindow()
    main_window.show()
    sys.exit(app.exec_())


if __name__ == "__main__":
    main()
