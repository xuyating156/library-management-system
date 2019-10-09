# -*- coding: utf-8 -*-
import sys
from utils.SingletonTcpSocket import SingletonTcpSocket
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import Qt
import qdarkstyle
from PyQt5.QtSql import *
import json


class BookStorageViewer(QWidget):
    def __init__(self):
        super(BookStorageViewer, self).__init__()
        self.resize(700, 500)
        self.setWindowTitle("欢迎使用图书馆管理系统")
        # 查询模型
        self.queryModel = None
        # 数据表
        self.tableView = None
        # 当前页
        self.currentPage = 0
        # 总页数
        self.totalPage = 0
        # 总记录数
        self.totalRecord = 0
        # 每页数据数
        self.pageRecord = 10
        self.setUpUI()

    def disply(self,currentPage,recv_dictionaries):
        line = 0
        for one in range(0,10):
            self.queryModel.setItem(line, 0, QStandardItem(0))
            self.queryModel.setItem(line, 1, QStandardItem(0))
            self.queryModel.setItem(line, 2, QStandardItem(0))
            self.queryModel.setItem(line, 3, QStandardItem(0))
            self.queryModel.setItem(line, 4, QStandardItem(0))
            self.queryModel.setItem(line, 5, QStandardItem(0))
            self.queryModel.setItem(line, 6, QStandardItem(0))
            self.queryModel.setItem(line, 7, QStandardItem(0))
            self.queryModel.setItem(line, 8, QStandardItem(0))
            line += 1

        line = 0

        for one in recv_dictionaries:
            if 0 <= line and line < 10:
                if one and 'bookName' in one.keys():
                    self.queryModel.setItem(line, 0, QStandardItem(one['bookName']))
                if one and 'bookId' in one.keys():
                    self.queryModel.setItem(line, 1, QStandardItem(one['bookId']))
                if one and 'bookAuthor' in one.keys():
                    self.queryModel.setItem(line, 2, QStandardItem(one['bookAuthor']))
                if one and 'bookCategory' in one.keys():
                    self.queryModel.setItem(line, 3, QStandardItem(one['bookCategory']))
                if one and 'bookPublisher' in one.keys():
                    self.queryModel.setItem(line, 4, QStandardItem(one['bookPublisher']))
                if one and 'bookPublicationDate' in one.keys():
                    self.queryModel.setItem(line, 5, QStandardItem(one['bookPublicationDate']))
                if one and 'bookStock' in one.keys():
                    self.queryModel.setItem(line, 6, QStandardItem(str(one['bookStock'])))
                if one and 'bookRemain' in one.keys():
                    self.queryModel.setItem(line, 7, QStandardItem(str(one['bookRemain'])))
                if one and 'bookTimes' in one.keys():
                    self.queryModel.setItem(line, 8, QStandardItem(str(one['bookTimes'])))
                line += 1
        return

    def disply_condition(self, recv_dictionaries):
        line = 0
        for one in range(0, 10):
            self.queryModel.setItem(line, 0, QStandardItem(0))
            self.queryModel.setItem(line, 1, QStandardItem(0))
            self.queryModel.setItem(line, 2, QStandardItem(0))
            self.queryModel.setItem(line, 3, QStandardItem(0))
            self.queryModel.setItem(line, 4, QStandardItem(0))
            self.queryModel.setItem(line, 5, QStandardItem(0))
            self.queryModel.setItem(line, 6, QStandardItem(0))
            self.queryModel.setItem(line, 7, QStandardItem(0))
            self.queryModel.setItem(line, 8, QStandardItem(0))
            line += 1

        line = 0
        line1 = 0
        for one in recv_dictionaries:
            if line1 >= (self.currentPage-1) * 10 and line < 10:
                if one and 'bookName' in one.keys():
                    self.queryModel.setItem(line, 0, QStandardItem(one['bookName']))
                if one and 'bookId' in one.keys():
                    self.queryModel.setItem(line, 1, QStandardItem(one['bookId']))
                if one and 'bookAuthor' in one.keys():
                    self.queryModel.setItem(line, 2, QStandardItem(one['bookAuthor']))
                if one and 'bookCategory' in one.keys():
                    self.queryModel.setItem(line, 3, QStandardItem(one['bookCategory']))
                if one and 'bookPublisher' in one.keys():
                    self.queryModel.setItem(line, 4, QStandardItem(one['bookPublisher']))
                if one and 'bookPublicationDate' in one.keys():
                    self.queryModel.setItem(line, 5, QStandardItem(one['bookPublicationDate']))
                if one and 'bookStock' in one.keys():
                    self.queryModel.setItem(line, 6, QStandardItem(str(one['bookStock'])))
                if one and 'bookRemain' in one.keys():
                    self.queryModel.setItem(line, 7, QStandardItem(str(one['bookRemain'])))
                if one and 'bookTimes' in one.keys():
                    self.queryModel.setItem(line, 8, QStandardItem(str(one['bookTimes'])))
                line += 1
            line1 += 1
        return line1


    def setUpUI(self):
        self.layout = QVBoxLayout()
        self.Hlayout1 = QHBoxLayout()
        self.Hlayout2 = QHBoxLayout()

        # Hlayout1控件的初始化
        self.searchEdit = QLineEdit()
        self.searchEdit.setFixedHeight(32)
        font = QFont()
        font.setPixelSize(15)
        self.searchEdit.setFont(font)

        self.searchButton = QPushButton("查询")
        self.searchButton.setFixedHeight(32)
        self.searchButton.setFont(font)
        self.searchButton.setIcon(QIcon(QPixmap("./images/search.png")))

        self.condisionComboBox = QComboBox()
        searchCondision = ['按书名查询', '按书号查询', '按作者查询']
        self.condisionComboBox.setFixedHeight(32)
        self.condisionComboBox.setFont(font)
        self.condisionComboBox.addItems(searchCondision)

        self.Hlayout1.addWidget(self.searchEdit)
        self.Hlayout1.addWidget(self.searchButton)
        self.Hlayout1.addWidget(self.condisionComboBox)

        # Hlayout2初始化
        self.jumpToLabel = QLabel("跳转到第")
        self.pageEdit = QLineEdit()
        self.pageEdit.setFixedWidth(30)
        s = "/" + str(self.totalPage) + "页"
        self.pageLabel = QLabel(s)
        self.jumpToButton = QPushButton("跳转")
        self.prevButton = QPushButton("前一页")
        self.prevButton.setFixedWidth(60)
        self.backButton = QPushButton("后一页")
        self.backButton.setFixedWidth(60)

        Hlayout = QHBoxLayout()
        Hlayout.addWidget(self.jumpToLabel)
        Hlayout.addWidget(self.pageEdit)
        Hlayout.addWidget(self.pageLabel)
        Hlayout.addWidget(self.jumpToButton)
        Hlayout.addWidget(self.prevButton)
        Hlayout.addWidget(self.backButton)
        widget = QWidget()
        widget.setLayout(Hlayout)
        widget.setFixedWidth(300)
        self.Hlayout2.addWidget(widget)

        # tableView
        # 序号，书名，书号，作者，分类，出版社，出版时间，库存，剩余可借
        # self.db = QSqlDatabase.addDatabase("QSQLITE")
        # self.db.setDatabaseName('./db/LibraryManagement.db')
        # self.db.open()

        self.tableView = QTableView()
        self.tableView.horizontalHeader().setStretchLastSection(True)
        self.tableView.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.tableView.setEditTriggers(QAbstractItemView.NoEditTriggers)
        # self.queryModel = QSqlQueryModel()

        # SingletonTcpSocket().connect("10.2.8.3", 9999)
        data = {"messageId": 2001, "start": self.currentPage * 10, "end": (self.currentPage + 1) * 10}
        send_str = json.dumps(data)

        # 发送接收消息
        # self.recv_str = ''
        # self.recv_dictionaries = ''
        if (SingletonTcpSocket().send(bytes(send_str, encoding="utf8")) > 0):
            # 获取json数据
            strs = SingletonTcpSocket().recv(40960)
            if strs:
                self.recv_str = json.loads(strs.decode('utf8'))
                print('recv from server:%s' % strs)
        if self.recv_str and ('item' in self.recv_str.keys()) and ('total' in self.recv_str.keys()):
            self.recv_dictionaries = self.recv_str['item']
            self.totalRecord = self.recv_str['total']
        print(self.recv_dictionaries)

        self.queryModel = QStandardItemModel(10, 9)
        self.searchButtonClicked()
        self.tableView.setModel(self.queryModel)

        if self.recv_dictionaries:
            self.disply(self.currentPage,self.recv_dictionaries)

        self.queryModel.setHeaderData(0, Qt.Horizontal, "书名")
        self.queryModel.setHeaderData(1, Qt.Horizontal, "书号")
        self.queryModel.setHeaderData(2, Qt.Horizontal, "作者")
        self.queryModel.setHeaderData(3, Qt.Horizontal, "分类")
        self.queryModel.setHeaderData(4, Qt.Horizontal, "出版社")
        self.queryModel.setHeaderData(5, Qt.Horizontal, "出版时间")
        self.queryModel.setHeaderData(6, Qt.Horizontal, "库存")
        self.queryModel.setHeaderData(7, Qt.Horizontal, "剩余可借")
        self.queryModel.setHeaderData(8, Qt.Horizontal, "总借阅次数")

        self.layout.addLayout(self.Hlayout1)
        self.layout.addWidget(self.tableView)
        self.layout.addLayout(self.Hlayout2)
        self.setLayout(self.layout)
        self.searchButton.clicked.connect(self.searchButtonClicked)
        self.prevButton.clicked.connect(self.prevButtonClicked)
        self.backButton.clicked.connect(self.backButtonClicked)
        self.jumpToButton.clicked.connect(self.jumpToButtonClicked)
        self.searchEdit.returnPressed.connect(self.searchButtonClicked)

    def setButtonStatus(self):
        if(self.currentPage==self.totalPage):
            self.prevButton.setEnabled(True)
            self.backButton.setEnabled(False)
        if(self.currentPage==1):
            self.backButton.setEnabled(True)
            self.prevButton.setEnabled(False)
        if(self.currentPage<self.totalPage and self.currentPage>1):
            self.prevButton.setEnabled(True)
            self.backButton.setEnabled(True)

    # 得到记录数
    # def getTotalRecordCount(self):
    #     # self.queryModel.setQuery("SELECT * FROM Book")
    #     # self.totalRecord = self.queryModel.rowCount()
    #     sum = 0
    #     for one in self.recv_dictionaries:
    #         sum +=1
    #     self.totalRecord = sum
    #     return

    # 得到总页数
    def getPageCount(self):
        if (self.searchEdit.text() == ""):
            self.totalPage
        # self.getTotalRecordCount()
        # 上取整
        self.totalPage = int((self.totalRecord + self.pageRecord - 1) / self.pageRecord)
        return

    # 分页记录查询

    # 点击查询
    def searchButtonClicked(self):
        self.currentPage = 0
        self.currentPage += 1
        self.pageEdit.setText(str(self.currentPage))
        self.getPageCount()
        s = "/" + str(int(self.totalPage)) + "页"
        self.pageLabel.setText(s)
        index = (self.currentPage - 1) * self.pageRecord
        #self.recordQuery(index)
        queryCondition = ""
        conditionChoice = self.condisionComboBox.currentText()
        temp = self.searchEdit.text()
        if temp == "":
            data = {"messageId": 2001, "start": 0, "end":10}
            send_str = json.dumps(data)
            SingletonTcpSocket().send(bytes(send_str, encoding="utf8"))
            self.recv_str = json.loads(SingletonTcpSocket().recv(10240).decode('utf8'))
            self.recv_dictionaries = self.recv_str['item']
            self.totalRecord = self.recv_str['total']
            print(self.recv_dictionaries)

            self.disply(self.currentPage, self.recv_dictionaries)

            self.setButtonStatus()
            self.getPageCount()
            s = "/" + str(int(self.totalPage)) + "页"
            self.pageLabel.setText(s)

        else:
            if (conditionChoice == "按书名查询"):
                conditionChoice = 'bookName'
                type = 1
            elif (conditionChoice == "按书号查询"):
                conditionChoice = 'bookId'
                type = 0
            elif (conditionChoice == "按作者查询"):
                conditionChoice = 'bookAuthor'
                type = 2
            else:
                conditionChoice = 'Publisher'
            temp = self.searchEdit.text()
            data = {"messageId": 2003, "bookSearch": temp, "type": type}
            print(data)
            send_str = json.dumps(data)
            SingletonTcpSocket().sock.send(bytes(send_str, encoding="utf8"))
            recv_str = json.loads(SingletonTcpSocket().sock.recv(10240).decode('utf8'))
            self.recv_dictionaries = recv_str['item']
            print(self.recv_dictionaries)
            self.totalRecord  = self.disply_condition(self.recv_dictionaries)
            self.setButtonStatus()
            self.getPageCount()
            s = "/" + str(int(self.totalPage)) + "页"
            self.pageLabel.setText(s)
            return
        return



    # 向前翻页
    def prevButtonClicked(self):
        if self.currentPage <=1:
            return
        self.currentPage -= 1
        self.pageEdit.setText(str(self.currentPage))
        # index = (self.currentPage - 1) * self.pageRecord
        # self.recordQuery(index,currentPage)

        if (self.searchEdit.text() == ""):
            self.totalPage = int((self.totalRecord + self.pageRecord - 1) / self.pageRecord)
            label = "/" + str(int(self.totalPage)) + "页"
            self.pageLabel.setText(label)
            data = {"messageId": 2001, "start": (self.currentPage-1) * 10, "end": (self.currentPage) * 10}
            send_str = json.dumps(data)
            SingletonTcpSocket().sock.send(bytes(send_str, encoding="utf8"))
            recv_str = json.loads(SingletonTcpSocket().sock.recv(10240).decode('utf8'))
            self.recv_dictionaries = recv_str['item']
            self.totalRecord = self.recv_str['total']
            print(self.recv_dictionaries)

            self.disply(self.currentPage, self.recv_dictionaries)

            self.setButtonStatus()
        else:
            conditionChoice = self.condisionComboBox.currentText()
            if (conditionChoice == "按书名查询"):
                conditionChoice = 'bookName'
                type = 1
            elif (conditionChoice == "按书号查询"):
                conditionChoice = 'bookId'
                type = 0
            elif (conditionChoice == "按作者查询"):
                conditionChoice = 'bookAuthor'
                type = 2
            else:
                conditionChoice = 'Publisher'
            temp = self.searchEdit.text()
            data = {"messageId": 2003, "bookSearch": temp, "type": type}
            print(data)
            send_str = json.dumps(data)
            SingletonTcpSocket().sock.send(bytes(send_str, encoding="utf8"))
            recv_str = json.loads(SingletonTcpSocket().sock.recv(10240).decode('utf8'))
            self.recv_dictionaries = recv_str['item']
            print(self.recv_dictionaries)
            self.totalRecord = self.disply_condition(self.recv_dictionaries)
            self.setButtonStatus()
            self.getPageCount()
            s = "/" + str(int(self.totalPage)) + "页"
            self.pageLabel.setText(s)
        return

    # 向后翻页
    def backButtonClicked(self):
        if self.currentPage >=3:
            return
        self.currentPage += 1
        if (self.currentPage >= int(self.totalPage)):
            self.currentPage = int(self.totalPage)
        self.pageEdit.setText(str(self.currentPage))
        # index = (self.currentPage - 1) * self.pageRecord
        # self.recordQuery(index,currentPage)
        if (self.searchEdit.text() == ""):
            self.totalPage = int((self.totalRecord + self.pageRecord - 1) / self.pageRecord)
            label = "/" + str(int(self.totalPage)) + "页"
            self.pageLabel.setText(label)

            data = {"messageId":2001,"start":(self.currentPage-1)*10,"end":self.currentPage*10}
            print(data)
            send_str = json.dumps(data)
            SingletonTcpSocket().sock.send(bytes(send_str, encoding="utf8"))
            recv_str = json.loads(SingletonTcpSocket().sock.recv(10240).decode('utf8'))
            self.recv_dictionaries = recv_str['item']
            self.totalRecord = self.recv_str['total']
            print(self.recv_dictionaries)

            self.disply(self.currentPage, self.recv_dictionaries)

            self.setButtonStatus()
        else:
            conditionChoice = self.condisionComboBox.currentText()
            if (conditionChoice == "按书名查询"):
                conditionChoice = 'bookName'
                type = 1
            elif (conditionChoice == "按书号查询"):
                conditionChoice = 'bookId'
                type = 0
            elif (conditionChoice == "按作者查询"):
                conditionChoice = 'bookAuthor'
                type = 2
            else:
                conditionChoice = 'Publisher'
            temp = self.searchEdit.text()
            data = {"messageId": 2003, "bookSearch": temp, "type": type}
            print(data)
            send_str = json.dumps(data)
            SingletonTcpSocket().sock.send(bytes(send_str, encoding="utf8"))
            recv_str = json.loads(SingletonTcpSocket().sock.recv(10240).decode('utf8'))
            self.recv_dictionaries = recv_str['item']
            print(self.recv_dictionaries)
            self.totalRecord = self.disply_condition(self.recv_dictionaries)
            self.setButtonStatus()
            self.getPageCount()
            s = "/" + str(int(self.totalPage)) + "页"
            self.pageLabel.setText(s)

        return


    # 点击跳转
    def jumpToButtonClicked(self):
        if (self.pageEdit.text().isdigit()):
            self.currentPage = int(self.pageEdit.text())
            if (self.currentPage > self.totalPage):
                self.currentPage = self.totalPage
            if (self.currentPage <= 1):
                self.currentPage = 1
        else:
            self.currentPage = 1
        index = (self.currentPage - 1) * self.pageRecord
        self.pageEdit.setText(str(self.currentPage))
        # self.recordQuery(index)
        if (self.searchEdit.text() == ""):
            data = {"messageId": 2001, "start": index, "end": index + 10}
            print(data)
            send_str = json.dumps(data)
            SingletonTcpSocket().send(bytes(send_str, encoding="utf8"))
            recv_str = json.loads(SingletonTcpSocket().recv(10240).decode('utf8'))
            self.recv_dictionaries = recv_str['item']
            print(self.recv_dictionaries)

            self.disply(self.currentPage, self.recv_dictionaries)

            self.setButtonStatus()
        else:
            self.totalRecord = self.disply_condition(self.recv_dictionaries)

            self.setButtonStatus()
        return


if __name__ == "__main__":
    app = QApplication(sys.argv)
    app.setWindowIcon(QIcon("./images/MainWindow_1.png"))
    app.setStyleSheet(qdarkstyle.load_stylesheet_pyqt5())
    mainMindow = BookStorageViewer()
    mainMindow.show()
    sys.exit(app.exec_())
