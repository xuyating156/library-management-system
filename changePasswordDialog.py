import sys
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
import qdarkstyle
import time
from PyQt5.QtSql import *
import hashlib
import json
from utils.SingletonTcpSocket import SingletonTcpSocket
class changePasswordDialog(QDialog):
    def __init__(self, parent=None):
        super(changePasswordDialog, self).__init__(parent)
        self.setWindowModality(Qt.WindowModal)
        self.setWindowTitle("修改密码")
        self.setUpUI()

    def setUpUI(self):
        self.resize(300, 280)
        self.layout = QFormLayout()
        self.setLayout(self.layout)

        self.titlelabel = QLabel(" 修改密码")
        self.studentIdLabel = QLabel("工    号：")
        # self.studentNameLabel=QLabel("姓    名：")
        self.oldPasswordLabel = QLabel("旧 密 码：")
        self.passwordLabel = QLabel("新 密 码：")
        self.confirmPasswordLabel = QLabel("确认密码：")

        self.studentIdEdit = QLineEdit()
        # self.studentNameEdit=QLineEdit()
        self.oldPasswordEdit = QLineEdit()
        self.passwordEdit = QLineEdit()
        self.confirmPasswordEdit = QLineEdit()

        self.changePasswordButton = QPushButton("确认修改")
        self.changePasswordButton.setFixedWidth(140)
        self.changePasswordButton.setFixedHeight(32)

        self.layout.addRow("", self.titlelabel)
        self.layout.addRow(self.studentIdLabel, self.studentIdEdit)
        # self.layout.addRow(self.studentNameLabel,self.studentNameEdit)
        self.layout.addRow(self.oldPasswordLabel, self.oldPasswordEdit)
        self.layout.addRow(self.passwordLabel, self.passwordEdit)
        self.layout.addRow(self.confirmPasswordLabel, self.confirmPasswordEdit)
        self.layout.addRow("", self.changePasswordButton)

        font = QFont()
        font.setPixelSize(20)
        self.titlelabel.setFont(font)
        font.setPixelSize(16)
        self.studentIdLabel.setFont(font)
        # self.studentNameLabel.setFont(font)
        self.oldPasswordLabel.setFont(font)
        self.passwordLabel.setFont(font)
        self.confirmPasswordLabel.setFont(font)

        font.setPixelSize(16)
        self.studentIdEdit.setFont(font)
        self.changePasswordButton.setFont(font)
        # self.studentNameEdit.setFont(font)
        font.setPixelSize(10)
        self.oldPasswordEdit.setFont(font)
        self.passwordEdit.setFont(font)
        self.confirmPasswordEdit.setFont(font)

        self.titlelabel.setMargin(8)
        self.layout.setVerticalSpacing(10)

        # 设置长度
        self.studentIdEdit.setMaxLength(10)
        self.oldPasswordEdit.setMaxLength(16)
        self.passwordEdit.setMaxLength(16)
        self.confirmPasswordEdit.setMaxLength(16)
        # 设置密码掩膜
        self.oldPasswordEdit.setEchoMode(QLineEdit.Password)
        self.passwordEdit.setEchoMode(QLineEdit.Password)
        self.confirmPasswordEdit.setEchoMode(QLineEdit.Password)

        # 设置校验
        reg = QRegExp("PB[0~9]{8}")
        pValidator = QRegExpValidator(self)
        pValidator.setRegExp(reg)
        self.studentIdEdit.setValidator(pValidator)

        reg = QRegExp("[a-zA-z0-9]+$")
        pValidator.setRegExp(reg)
        self.oldPasswordEdit.setValidator(pValidator)
        self.passwordEdit.setValidator(pValidator)
        self.confirmPasswordEdit.setValidator(pValidator)

        # 设置信号与槽
        self.changePasswordButton.clicked.connect(self.changePasswordButtonClicked)

    def changePasswordButtonClicked(self):
        studentId = self.studentIdEdit.text()
        oldPassword = self.oldPasswordEdit.text()
        password = self.passwordEdit.text()
        confirmPassword = self.confirmPasswordEdit.text()
        if (studentId == "" or oldPassword == "" or password == "" or confirmPassword == ""):
            print(QMessageBox.warning(self, "警告", "输入不可为空，请重新输入", QMessageBox.Yes, QMessageBox.Yes))
            return

        if(password!=confirmPassword):
            print(QMessageBox.warning(self,"警告","两次输入密码不同,请确认输入",QMessageBox.Yes,QMessageBox.Yes))
            self.passwordEdit.clear()
            self.confirmPasswordEdit.clear()

            return


        # 组装json数据
        data = {'messageId': 1003, 'adminId': studentId, 'adminOldPasswd': oldPassword, 'adminName': '','adminNewPasswd':password}
        # SingletonTcpSocket().connect("10.2.8.96", 9999)
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
            print(QMessageBox.information(self, "提醒", "修改密码成功", QMessageBox.Yes, QMessageBox.Yes))
            self.close()
        else:
            if ('errorDetail' in resData.keys()):
                print(QMessageBox.information(self, "提示", resData['errorDetail'], QMessageBox.Yes,
                                              QMessageBox.Yes))
            else:
                print(QMessageBox.information(self, "提示", '数据获取格式错误', QMessageBox.Yes, QMessageBox.Yes))

        return


if __name__ == "__main__":
    app = QApplication(sys.argv)
    app.setWindowIcon(QIcon("./images/MainWindow_1.png"))
    app.setStyleSheet(qdarkstyle.load_stylesheet_pyqt5())
    mainMindow = changePasswordDialog()
    mainMindow.show()
    sys.exit(app.exec_())
