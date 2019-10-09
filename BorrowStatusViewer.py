# coding=utf8

import sys
from utils.SingletonTcpSocket import SingletonTcpSocket
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import Qt
import qdarkstyle
from PyQt5.QtSql import *
import json


class BorrowStatusViewer(QWidget):
    def __init__(self, studentId):
        super(BorrowStatusViewer, self).__init__()
        self.resize(1000, 800)
        self.studentId = studentId
        self.setWindowTitle("欢迎使用图书馆管理系统")
        self.setUpUI()

    def setUpUI(self):
        # 分为两块，上方是已借未归还书，下方是已归还书
        self.layout = QVBoxLayout(self)
        # Label设置
        self.borrowedLabel = QLabel("未归还:")
        self.returnedLabel = QLabel("已归还:")
        self.borrowedLabel.setFixedHeight(32)
        self.borrowedLabel.setFixedWidth(60)
        self.returnedLabel.setFixedHeight(32)
        self.returnedLabel.setFixedWidth(60)
        font = QFont()
        font.setPixelSize(18)
        self.borrowedLabel.setFont(font)
        self.returnedLabel.setFont(font)

        # Table和Model
        self.borrowedTableView = QTableView()
        self.borrowedTableView.horizontalHeader().setStretchLastSection(True)
        self.borrowedTableView.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.borrowedTableView.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.returnedTableView = QTableView()
        self.returnedTableView.horizontalHeader().setStretchLastSection(True)
        self.returnedTableView.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.returnedTableView.setEditTriggers(QAbstractItemView.NoEditTriggers)

        # self.borrowedQueryModel = QSqlQueryModel()
        self.borrowedQueryModel = QStandardItemModel(10,8)
        self.borrowedTableView.setModel(self.borrowedQueryModel)

        # self.returnedQueryModel = QSqlQueryModel()
        self.returnedQueryModel = QStandardItemModel(10,9)
        self.returnedTableView.setModel(self.returnedQueryModel)

        self.borrowedTableView.setModel(self.borrowedQueryModel)
        self.returnedTableView.setModel(self.returnedQueryModel)
        if self.studentId != '':
            self.borrowedQuery()


        self.borrowedQueryModel.setHeaderData(0, Qt.Horizontal, "书名")
        self.borrowedQueryModel.setHeaderData(1, Qt.Horizontal, "书号")
        self.borrowedQueryModel.setHeaderData(2, Qt.Horizontal, "作者")
        self.borrowedQueryModel.setHeaderData(3, Qt.Horizontal, "分类")
        self.borrowedQueryModel.setHeaderData(4, Qt.Horizontal, "出版社")
        self.borrowedQueryModel.setHeaderData(5, Qt.Horizontal, "出版时间")
        self.borrowedQueryModel.setHeaderData(6, Qt.Horizontal, "借出时间")
        self.borrowedQueryModel.setHeaderData(7, Qt.Horizontal, "最晚归还时间")

        if self.studentId != '':
            self.returnedQuery()
        self.returnedQueryModel.setHeaderData(0, Qt.Horizontal, "书名")
        self.returnedQueryModel.setHeaderData(1, Qt.Horizontal, "书号")
        self.returnedQueryModel.setHeaderData(2, Qt.Horizontal, "作者")
        self.returnedQueryModel.setHeaderData(3, Qt.Horizontal, "分类")
        self.returnedQueryModel.setHeaderData(4, Qt.Horizontal, "出版社")
        self.returnedQueryModel.setHeaderData(5, Qt.Horizontal, "出版时间")
        self.returnedQueryModel.setHeaderData(6, Qt.Horizontal, "借阅时间")
        self.returnedQueryModel.setHeaderData(7, Qt.Horizontal, "归还时间")
        self.returnedQueryModel.setHeaderData(8, Qt.Horizontal, "最晚归还时间")

        self.layout.addWidget(self.borrowedLabel)
        self.layout.addWidget(self.borrowedTableView)
        self.layout.addWidget(self.returnedLabel)
        self.layout.addWidget(self.returnedTableView)
        return
    #
    def borrowedQuery(self):
        data = {'messageId' : 3002, 'userNum' : self.studentId}
        # SingletonTcpSocket().connect("10.2.8.96", 9999)
        str = json.dumps(data)
        print('json dumps:%s' % str)
        SingletonTcpSocket().send(bytes(str, encoding="utf8"))

        # 获取json数据
        str = SingletonTcpSocket().recv(40960)
        print('recv from server:str%s' % str)

        # 解析json数据
        resData = json.loads(str.decode('utf8'))
        str_first = resData['item']
        print('recv from server:str_first%s' % str_first)
        if (resData['errorCode'] == 0):
            line = 0
            for one in str_first:
                if one and 'bookName' in one.keys():
                    self.borrowedQueryModel.setItem(line, 0, QStandardItem(one['bookName']))
                if one and 'bookId' in one.keys():
                    self.borrowedQueryModel.setItem(line, 1, QStandardItem(one['bookId']))
                if one and 'bookAuthor' in one.keys():
                    self.borrowedQueryModel.setItem(line, 2, QStandardItem(one['bookAuthor']))
                if one and 'bookCategory' in one.keys():
                    self.borrowedQueryModel.setItem(line, 3, QStandardItem(one['bookCategory']))
                if one and 'bookPublisher' in one.keys():
                    self.borrowedQueryModel.setItem(line, 4, QStandardItem(one['bookPublisher']))
                if one and 'bookPublicationDate' in one.keys():
                    self.borrowedQueryModel.setItem(line, 5, QStandardItem(one['bookPublicationDate']))
                if one and 'borDate' in one.keys():
                    self.borrowedQueryModel.setItem(line, 6, QStandardItem(one['borDate']))
                if one and 'borRetDateLimit' in one.keys():
                    self.borrowedQueryModel.setItem(line, 7, QStandardItem(one['borRetDateLimit']))

                print('111')
                line += 1

        else:
            print(QMessageBox.information(self, "提示", resData['errorDetail'], QMessageBox.Yes, QMessageBox.Yes))

        return

    def returnedQuery(self):
        # #组装json数据
        data = {'messageId' : 4002, 'userNum' : self.studentId}
        # SingletonTcpSocket().connect("10.2.8.96", 9999)
        str = json.dumps(data)
        print('json dumps:%s' % str)
        SingletonTcpSocket().send(bytes(str, encoding="utf8"))

        # 获取json数据
        str = SingletonTcpSocket().recv(40960)
        print('recv from server:str%s' % str)

        # 解析json数据
        resData = json.loads(str.decode('utf8'))
        str_first = resData['item']
        print('recv from server:str_first%s' % str_first)
        if (resData['errorCode'] == 0):
            line = 0

            for one in str_first:
                if one and 'bookName' in one.keys():
                    self.returnedQueryModel.setItem(line, 0, QStandardItem(one['bookName']))
                if one and 'bookId' in one.keys():
                    self.returnedQueryModel.setItem(line, 1, QStandardItem(one['bookId']))
                if one and 'bookAuthor' in one.keys():
                    self.returnedQueryModel.setItem(line, 2, QStandardItem(one['bookAuthor']))
                if one and 'bookCategory' in one.keys():
                    self.returnedQueryModel.setItem(line, 3, QStandardItem(one['bookCategory']))
                if one and 'bookPublisher' in one.keys():
                    self.returnedQueryModel.setItem(line, 4, QStandardItem(one['bookPublisher']))
                if one and 'bookPublicationDate' in one.keys():
                    self.returnedQueryModel.setItem(line, 5, QStandardItem(one['bookPublicationDate']))
                if one and 'borDate' in one.keys():
                    self.returnedQueryModel.setItem(line, 6, QStandardItem(one['borDate']))
                if one and 'retDate' in one.keys():
                    self.returnedQueryModel.setItem(line, 7, QStandardItem(one['retDate']))
                if one and 'borRetDateLimit' in one.keys():
                    self.returnedQueryModel.setItem(line, 8, QStandardItem(one['borRetDateLimit']))
                print('222')
                line += 1

        else:
            print(QMessageBox.information(self, "提示", resData['errorDetail'], QMessageBox.Yes, QMessageBox.Yes))

        return

if __name__ == "__main__":
    app = QApplication(sys.argv)
    app.setWindowIcon(QIcon("./images/MainWindow_1.png"))
    app.setStyleSheet(qdarkstyle.load_stylesheet_pyqt5())
    mainMindow = BorrowStatusViewer("0001")
    mainMindow.show()
    sys.exit(app.exec_())
