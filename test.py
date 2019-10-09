import sys
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
import qdarkstyle
from PyQt5.QtSql import *
import time
import sip
from StudentHome import StudentHome

class User(QDialog):
    User_signal = pyqtSignal(str)

    def __init__(self, parent=None):
        super(User, self).__init__(parent)
        self.setUpUI()
        self.setWindowModality(Qt.WindowModal)
        self.setWindowTitle("输入卡号")
    def setUpUI(self):
        self.resize(300, 400)
        self.layout = QFormLayout()
        self.setLayout(self.layout)

        # Label控件
        self.titlelabel = QLabel("  输入卡号")
        self.UserIdLabel = QLabel("卡    号:")

        # button控件
        self.UserButton = QPushButton("进入")
        # lineEdit控件
        self.UserIdEdit = QLineEdit()

        self.UserIdEdit.setMaxLength(10)

        # 添加进formlayout
        self.layout.addRow("", self.titlelabel)
        self.layout.addRow(self.UserIdLabel, self.UserIdEdit)
        self.layout.addRow("", self.UserButton)

        # 设置字体
        font = QFont()
        font.setPixelSize(20)
        self.titlelabel.setFont(font)
        font.setPixelSize(14)
        self.UserIdLabel.setFont(font)
        self.UserIdEdit.setFont(font)

        # button设置
        font.setPixelSize(16)
        self.UserButton.setFont(font)
        self.UserButton.setFixedHeight(32)
        self.UserButton.setFixedWidth(140)

        # 设置间距
        self.titlelabel.setMargin(8)
        self.layout.setVerticalSpacing(10)

        self.UserButton.clicked.connect(self.UserButtonCicked)

        def studentSignIn(self, studentId):
            sip.delete(self.widget)
            self.widget = StudentHome(studentId)  # 学生登陆可以，但不会出现之后的界面
            self.setCentralWidget(self.widget)  # 显示登陆界面之后的内容
            self.changePasswordAction.setEnabled(False)
            self.signUpAction.setEnabled(True)
            self.signUpUserAction.setEnabled(True)
            self.signInAction.setEnabled(False)
            self.quitSignInAction.setEnabled(True)


        def addBookButtonCicked(self):
            UserId = self.UserIdEdit.text()
            if (UserId == ""):
                print(QMessageBox.warning(self, "警告", "有字段为空", QMessageBox.Yes, QMessageBox.Yes))
                return
            # 打开数据库连接
            db = QSqlDatabase.addDatabase("QSQLITE")
            db.setDatabaseName('./db/LibraryManagement.db')
            db.open()
            query = QSqlQuery()
            sql = "SELECT * FROM user WHERE StudentId='%s'" % (studentId)
            query.exec_(sql)
            db.close()

            hl = hashlib.md5()
            hl.update(password.encode(encoding='utf-8'))
            if (not query.next()):
                print(QMessageBox.information(self, "提示", "该账号不存在!", QMessageBox.Yes, QMessageBox.Yes))
            else:
                self.widget.is_student_signal[str].connect(self.studentSignIn)
