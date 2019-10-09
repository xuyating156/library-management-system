import sys
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
import qdarkstyle
from addBookDialog import addBookDialog
from dropBookDialog import dropBookDialog
from BookStorageViewer import BookStorageViewer
from UserManage import UserManage
from BookStorageViewer import BookStorageViewer
from borrowBookDialog import borrowBookDialog
from returnBookDialog import returnBookDialog
from BorrowStatusViewer import BorrowStatusViewer
from User import User#---
import sip

class AdminHome(QWidget):
    def __init__(self):
        super().__init__()
        self.userId = ''
        self.setUpUI()

    def setUpUI(self):
        self.resize(1400, 900)
        self.setWindowTitle("欢迎使用图书馆管理系统")
        self.layout = QHBoxLayout()
        self.buttonlayout = QVBoxLayout()
        self.setLayout(self.layout)

        font = QFont()
        font.setPixelSize(16)
        self.addBookButton = QPushButton("添加书籍")
        # self.dropBookButton = QPushButton("淘汰书籍")
        self.userButton = QPushButton("用户鉴权")
        self.userManageButton = QPushButton("删除用户")

        self.borrowBookButton = QPushButton("借书")
        self.returnBookButton = QPushButton("还书")
        self.myBookStatus = QPushButton("借阅状态")
        self.allBookButton = QPushButton("所有书籍")

        self.userManageButton.setFont(font)
        self.userButton.setFont(font)#--
        self.addBookButton.setFont(font)
        # self.dropBookButton.setFont(font)
        self.userManageButton.setFixedWidth(100)
        self.userManageButton.setFixedHeight(42)
        self.userButton.setFixedWidth(100)#--
        self.userButton.setFixedHeight(42)#--
        self.addBookButton.setFixedWidth(100)
        self.addBookButton.setFixedHeight(42)
        # self.dropBookButton.setFixedWidth(100)
        # self.dropBookButton.setFixedHeight(42)

        self.borrowBookButton.setFont(font)
        self.returnBookButton.setFont(font)  # --
        self.myBookStatus.setFont(font)
        self.allBookButton.setFont(font)
        self.borrowBookButton.setFixedWidth(100)
        self.borrowBookButton.setFixedHeight(42)
        self.returnBookButton.setFixedWidth(100)  # --
        self.returnBookButton.setFixedHeight(42)  # --
        self.myBookStatus.setFixedWidth(100)
        self.myBookStatus.setFixedHeight(42)
        self.allBookButton.setFixedWidth(100)
        self.allBookButton.setFixedHeight(42)

        self.buttonlayout.addWidget(self.addBookButton)
        # self.buttonlayout.addWidget(self.dropBookButton)
        self.buttonlayout.addWidget(self.userButton)#--
        self.buttonlayout.addWidget(self.userManageButton)

        self.buttonlayout.addWidget(self.borrowBookButton)
        self.buttonlayout.addWidget(self.returnBookButton)
        self.buttonlayout.addWidget(self.myBookStatus)  # --
        self.buttonlayout.addWidget(self.allBookButton)

        self.layout.addLayout(self.buttonlayout)
        self.storageView = BookStorageViewer()
        self.borrowStatusView = BorrowStatusViewer(self.userId)
        self.allBookButton.setEnabled(False)
        self.borrowBookButton.setEnabled(False)
        self.returnBookButton.setEnabled(False)
        self.myBookStatus.setEnabled(False)
        self.layout.addWidget(self.storageView)

        self.addBookButton.clicked.connect(self.addBookButtonClicked)
        # self.dropBookButton.clicked.connect(self.dropBookButtonClicked)
        self.userManageButton.clicked.connect(self.userManage)
        self.userButton.clicked.connect(self.UserButtonClicked)

        # 借书
        self.borrowBookButton.clicked.connect(self.borrowBookButtonClicked)
        # 还书
        self.returnBookButton.clicked.connect(self.returnBookButtonClicked)
        # 借阅状态
        self.myBookStatus.clicked.connect(self.myBookStatusClicked)
        # 所有书籍
        self.allBookButton.clicked.connect(self.allBookButtonClicked)

    def borrowBookButtonClicked(self):
        borrowDialog = borrowBookDialog(self.userId,self)
        borrowDialog.borrow_book_success_signal.connect(self.borrowStatusView.borrowedQuery)
        borrowDialog.borrow_book_success_signal.connect(self.storageView.searchButtonClicked)
        borrowDialog.show()
        borrowDialog.exec_()
        return

    def returnBookButtonClicked(self):
        returnDialog = returnBookDialog(self.userId,self)
        returnDialog.return_book_success_signal.connect(self.borrowStatusView.returnedQuery)
        returnDialog.return_book_success_signal.connect(self.borrowStatusView.borrowedQuery)
        returnDialog.return_book_success_signal.connect(self.storageView.searchButtonClicked)
        returnDialog.show()
        returnDialog.exec_()

    def myBookStatusClicked(self):
        self.layout.removeWidget(self.storageView)
        sip.delete(self.storageView)
        self.storageView = BookStorageViewer()
        self.borrowStatusView = BorrowStatusViewer(self.userId)
        self.layout.addWidget(self.borrowStatusView)
        self.allBookButton.setEnabled(True)
        self.myBookStatus.setEnabled(False)
        return

    def allBookButtonClicked(self):
        self.layout.removeWidget(self.borrowStatusView)
        sip.delete(self.borrowStatusView)
        self.borrowStatusView = BorrowStatusViewer(self.userId)
        self.storageView = BookStorageViewer()
        self.layout.addWidget(self.storageView)
        self.allBookButton.setEnabled(False)
        self.myBookStatus.setEnabled(True)
        return

    def addBookButtonClicked(self):
        addDialog = addBookDialog(self)
        addDialog.add_book_success_signal.connect(self.storageView.searchButtonClicked)
        addDialog.show()
        addDialog.exec_()
    #
    # def dropBookButtonClicked(self):
    #     dropDialog = dropBookDialog(self)
    #     dropDialog.drop_book_successful_signal.connect(self.storageView.searchButtonClicked)
    #     dropDialog.show()
    #     dropDialog.exec_()

    def UserButtonClicked(self):#---
        UserQuery=User(self)
        UserQuery.User_signal[str].connect(self.studentSignIn)
        UserQuery.show()
        UserQuery.exec_()
        # self.widget = SignUpUserWidget()
        # self.setCentralWidget(self.widget)
        #

    def studentSignIn(self, userId):
        self.userId = userId
        self.borrowBookButton.setEnabled(True)
        self.returnBookButton.setEnabled(True)
        self.myBookStatus.setEnabled(True)

    def userManage(self):
        UserDelete=UserManage(self)
        UserDelete.show()
        UserDelete.exec_()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    app.setWindowIcon(QIcon("./images/MainWindow_1.png"))
    app.setStyleSheet(qdarkstyle.load_stylesheet_pyqt5())
    mainMindow = AdminHome()
    mainMindow.show()
    sys.exit(app.exec_())
