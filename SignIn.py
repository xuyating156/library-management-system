import sys
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from utils.SingletonTcpSocket import SingletonTcpSocket
import qdarkstyle
import hashlib
from PyQt5.QtSql import *
import json


class SignInWidget(QWidget):
    is_admin_signal = pyqtSignal()
    is_student_signal = pyqtSignal(str)

    def __init__(self):
        super(SignInWidget, self).__init__()
        self.resize(1400, 900)
        self.setWindowTitle("欢迎使用图书馆管理系统")
        self.setUpUI()

    def setUpUI(self):
        self.Vlayout = QVBoxLayout(self)
        self.Hlayout1 = QHBoxLayout()
        self.Hlayout2 = QHBoxLayout()
        self.formlayout = QFormLayout()

        self.label0 = QLabel("IP地址: ")
        labelFont = QFont()
        labelFont.setPixelSize(18)
        lineEditFont = QFont()
        lineEditFont.setPixelSize(16)
        self.label0.setFont(labelFont)
        self.lineEdit0 = QLineEdit()
        self.lineEdit0.setFixedHeight(32)
        self.lineEdit0.setFixedWidth(180)
        self.lineEdit0.setFont(lineEditFont)
        self.lineEdit0.setMaxLength(16)

        self.formlayout.addRow(self.label0, self.lineEdit0)

        self.label1 = QLabel("工号: ")
        # labelFont = QFont()
        # labelFont.setPixelSize(18)
        # lineEditFont = QFont()
        # lineEditFont.setPixelSize(16)
        self.label1.setFont(labelFont)
        self.lineEdit1 = QLineEdit()
        self.lineEdit1.setFixedHeight(32)
        self.lineEdit1.setFixedWidth(180)
        self.lineEdit1.setFont(lineEditFont)
        self.lineEdit1.setMaxLength(10)

        self.formlayout.addRow(self.label1, self.lineEdit1)

        self.label2 = QLabel("密码: ")
        self.label2.setFont(labelFont)
        self.lineEdit2 = QLineEdit()
        self.lineEdit2.setFixedHeight(32)
        self.lineEdit2.setFixedWidth(180)
        self.lineEdit2.setMaxLength(16)

        # 设置验证
        reg = QRegExp("PB[0~9]{8}")
        pValidator = QRegExpValidator(self)
        pValidator.setRegExp(reg)
        self.lineEdit1.setValidator(pValidator)

        reg = QRegExp("[a-zA-z0-9]+$")
        pValidator.setRegExp(reg)
        self.lineEdit2.setValidator(pValidator)

        passwordFont = QFont()
        passwordFont.setPixelSize(10)
        self.lineEdit2.setFont(passwordFont)

        self.lineEdit2.setEchoMode(QLineEdit.Password)
        self.formlayout.addRow(self.label2, self.lineEdit2)
        self.signIn = QPushButton("登 录")
        self.signIn.setFixedWidth(80)
        self.signIn.setFixedHeight(30)
        self.signIn.setFont(labelFont)
        self.formlayout.addRow("", self.signIn)

        self.label = QLabel("欢迎使用图书馆管理系统")
        fontlabel = QFont()
        fontlabel.setPixelSize(30)
        self.label.setFixedWidth(390)
        # self.label.setFixedHeight(80)
        self.label.setFont(fontlabel)
        self.Hlayout1.addWidget(self.label, Qt.AlignCenter)
        self.widget1 = QWidget()
        self.widget1.setLayout(self.Hlayout1)
        self.widget2 = QWidget()
        self.widget2.setFixedWidth(300)
        self.widget2.setFixedHeight(150)
        self.widget2.setLayout(self.formlayout)
        self.Hlayout2.addWidget(self.widget2, Qt.AlignCenter)
        self.widget = QWidget()
        self.widget.setLayout(self.Hlayout2)
        self.Vlayout.addWidget(self.widget1)
        self.Vlayout.addWidget(self.widget, Qt.AlignTop)

        self.signIn.clicked.connect(self.signInCheck)
        self.lineEdit2.returnPressed.connect(self.signInCheck)
        self.lineEdit1.returnPressed.connect(self.signInCheck)
        self.lineEdit0.returnPressed.connect(self.signInCheck)

        # self.setAutoFillBackground(True)
        # palette = QPalette()
        # palette.setBrush(self.backgroundRole(), QBrush(QPixmap("./images/MainWindow_1.png")))
        # self.setPalette(palette)

    def signInCheck(self):
        IP = self.lineEdit0.text()
        studentId = self.lineEdit1.text()
        password = self.lineEdit2.text()
        if (studentId == "" or password == "" or IP == ""):
            print(QMessageBox.warning(self, "警告", "表单不可为空!", QMessageBox.Yes, QMessageBox.Yes))
            return


        if not SingletonTcpSocket().connect(IP, 9999):
            print(QMessageBox.warning(self, "提示", "网络连接异常，请检查网络", QMessageBox.Yes, QMessageBox.Yes))
            return

        # 组装json数据
        data = {'messageId' : 1001, 'adminId' : studentId, 'adminPasswd' : password, 'adminName' : ''}
        # str = json.dumps(data, sort_keys=True, indent=4, separators=(',', ': ')
        str = json.dumps(data)
        print('json dumps:%s' % str)

        # 发送接收消息
        if (SingletonTcpSocket().send(bytes(str, encoding="utf8")) > 0):
            # 获取json数据
            str = SingletonTcpSocket().recv(4096)
            print('recv from server:%s' % str)
            if not str:
                print(QMessageBox.information(self, "提示", '数据获取不正确', QMessageBox.Yes, QMessageBox.Yes))
                return

        # 解析json数据
        resData = json.loads(str.decode('utf8'))
        if ('errorCode' in resData.keys() and resData['errorCode'] == 0):
            self.is_admin_signal.emit()
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
    mainMindow = SignInWidget()
    mainMindow.show()
    sys.exit(app.exec_())
