import sys
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
import qdarkstyle
from PyQt5.QtSql import *
import hashlib
import json
from utils.SingletonTcpSocket import SingletonTcpSocket

class SignUpWidget(QWidget):
    student_signup_signal = pyqtSignal(str)

    def __init__(self):
        super().__init__()
        self.setUpUI()

    def setUpUI(self):
        self.resize(900, 600)
        self.setWindowTitle("欢迎登陆图书馆管理系统")
        self.signUpLabel = QLabel("注   册")
        self.signUpLabel.setAlignment(Qt.AlignCenter)
        # self.signUpLabel.setFixedWidth(300)
        self.signUpLabel.setFixedHeight(100)
        font = QFont()
        font.setPixelSize(36)
        lineEditFont = QFont()
        lineEditFont.setPixelSize(16)
        self.signUpLabel.setFont(font)

        self.layout = QVBoxLayout()
        self.layout.addWidget(self.signUpLabel, Qt.AlignHCenter)
        self.setLayout(self.layout)
        # 表单，包括学号，姓名，密码，确认密码
        self.formlayout = QFormLayout()
        font.setPixelSize(18)
        # Row1
        self.studentIdLabel = QLabel("工    号: ")
        self.studentIdLabel.setFont(font)
        self.studentIdLineEdit = QLineEdit()
        self.studentIdLineEdit.setFixedWidth(180)
        self.studentIdLineEdit.setFixedHeight(32)
        self.studentIdLineEdit.setFont(lineEditFont)
        self.studentIdLineEdit.setMaxLength(10)
        self.formlayout.addRow(self.studentIdLabel, self.studentIdLineEdit)

        # Row2
        self.studentNameLabel = QLabel("姓    名: ")
        self.studentNameLabel.setFont(font)
        self.studentNameLineEdit = QLineEdit()
        self.studentNameLineEdit.setFixedHeight(32)
        self.studentNameLineEdit.setFixedWidth(180)
        self.studentNameLineEdit.setFont(lineEditFont)
        self.studentNameLineEdit.setMaxLength(10)
        self.formlayout.addRow(self.studentNameLabel, self.studentNameLineEdit)

        lineEditFont.setPixelSize(10)

        # Row3
        self.passwordLabel = QLabel("密    码: ")
        self.passwordLabel.setFont(font)
        self.passwordLineEdit = QLineEdit()
        self.passwordLineEdit.setFixedWidth(180)
        self.passwordLineEdit.setFixedHeight(32)
        self.passwordLineEdit.setFont(lineEditFont)
        self.passwordLineEdit.setEchoMode(QLineEdit.Password)
        self.passwordLineEdit.setMaxLength(16)
        self.formlayout.addRow(self.passwordLabel, self.passwordLineEdit)

        # Row4
        self.passwordConfirmLabel = QLabel("确认密码: ")
        self.passwordConfirmLabel.setFont(font)
        self.passwordConfirmLineEdit = QLineEdit()
        self.passwordConfirmLineEdit.setFixedWidth(180)
        self.passwordConfirmLineEdit.setFixedHeight(32)
        self.passwordConfirmLineEdit.setFont(lineEditFont)
        self.passwordConfirmLineEdit.setEchoMode(QLineEdit.Password)
        self.passwordConfirmLineEdit.setMaxLength(16)
        self.formlayout.addRow(self.passwordConfirmLabel, self.passwordConfirmLineEdit)

        # Row5
        self.signUpbutton = QPushButton("注 册")
        self.signUpbutton.setFixedWidth(120)
        self.signUpbutton.setFixedHeight(30)
        self.signUpbutton.setFont(font)
        self.formlayout.addRow("", self.signUpbutton)
        widget = QWidget()
        widget.setLayout(self.formlayout)
        widget.setFixedHeight(250)
        widget.setFixedWidth(300)
        self.Hlayout = QHBoxLayout()
        self.Hlayout.addWidget(widget, Qt.AlignCenter)
        widget = QWidget()
        widget.setLayout(self.Hlayout)
        self.layout.addWidget(widget, Qt.AlignHCenter)

        # 设置验证
        reg = QRegExp("PB[0~9]{8}")
        pValidator = QRegExpValidator(self)
        pValidator.setRegExp(reg)
        self.studentIdLineEdit.setValidator(pValidator)

        reg = QRegExp("[a-zA-z0-9]+$")
        pValidator.setRegExp(reg)
        self.passwordLineEdit.setValidator(pValidator)
        self.passwordConfirmLineEdit.setValidator(pValidator)
        self.signUpbutton.clicked.connect(self.SignUp)
        self.studentIdLineEdit.returnPressed.connect(self.SignUp)
        self.studentNameLineEdit.returnPressed.connect(self.SignUp)
        self.passwordLineEdit.returnPressed.connect(self.SignUp)
        self.passwordConfirmLineEdit.returnPressed.connect(self.SignUp)

    def SignUp(self):
        studentId = self.studentIdLineEdit.text()
        studentName = self.studentNameLineEdit.text()
        password = self.passwordLineEdit.text()
        confirmPassword = self.passwordConfirmLineEdit.text()
        if (studentId == "" or  password == "" or confirmPassword == ""):
            print(QMessageBox.warning(self, "警告", "表单不可为空（姓名除外），请重新输入", QMessageBox.Yes, QMessageBox.Yes))
            return
        else:
            if (confirmPassword != password):
                print(QMessageBox.warning(self, "警告", "两次输入密码不一致，请重新输入", QMessageBox.Yes, QMessageBox.Yes))
                return

            # 组装json数据
            data = {'messageId': 1002, 'adminId': studentId, 'adminPasswd': password, 'adminName': studentName}
            # SingletonTcpSocket().connect("10.2.8.96",9999)
            # str = json.dumps(data, sort_keys=True, indent=4, separators=(',', ': ')
            str = json.dumps(data)
            print('json dumps:%s' % str)

            # 发送接收消息
            if (SingletonTcpSocket().send(bytes(str, encoding="utf8")) > 0):
                # 获取json数据
                str = SingletonTcpSocket().recv(1024)
                print('recv from server:%s' % str)
                if not str:
                    print(QMessageBox.information(self, "提示", '数据获取不正确', QMessageBox.Yes, QMessageBox.Yes))
                    return

            # 解析json数据
            resData = json.loads(str.decode('utf8'))
            if ('errorCode' in resData.keys() and resData['errorCode'] == 0):
                print(QMessageBox.information(self, "提醒", "您已成功注册账号!请登录", QMessageBox.Yes, QMessageBox.Yes))
            else:
                if ('errorDetail' in resData.keys()):
                    print(QMessageBox.information(self, "提示", resData['errorDetail'], QMessageBox.Yes, QMessageBox.Yes))
                else:
                    print(QMessageBox.information(self, "提示", '数据获取格式错误', QMessageBox.Yes, QMessageBox.Yes))

            return

if __name__ == "__main__":
    app = QApplication(sys.argv)
    app.setWindowIcon(QIcon("./images/MainWindow_1.png"))
    app.setStyleSheet(qdarkstyle.load_stylesheet_pyqt5())
    mainMindow = SignUpWidget()
    mainMindow.show()
    sys.exit(app.exec_())
