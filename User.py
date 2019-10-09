import sys
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
import qdarkstyle
from utils.SerialComm import SerialCommThread
from PyQt5.QtSql import *
import time
import sip
from StudentHome import StudentHome
from utils.SingletonTcpSocket import SingletonTcpSocket
from utils.SerialComm import get_serial_card_number
import json
from BorrowStatusViewer import BorrowStatusViewer


class User(QDialog):
    User_signal = pyqtSignal(str)
    user_number_signal = pyqtSignal(str)

    def __init__(self, parent=None):
        super(User, self).__init__(parent)
        self.setUpUI()
        self.setWindowModality(Qt.WindowModal)
        self.setWindowTitle("输入卡号")

    def setUpUI(self):
        self.resize(300, 400)
        self.layout = QFormLayout()#表格布局
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
        self.user_number_signal[str].connect(self.addCardNumber)
        # self.close.connect(self.closeThread)
        # self.UserIdEdit.editingFinished().connect(self.ReadCardNumber)

        # 启动线程获取card_number
        self.thread = SerialCommThread(self.SignalEmit)
        self.thread.start()

    def SignalEmit(self, str):
        self.user_number_signal.emit(str)

    def addCardNumber(self,str):
        self.UserIdEdit.setText(str)

    def UserButtonCicked(self):
        UserId = self.UserIdEdit.text()
        if (UserId == ''):
            print(QMessageBox.warning(self, "警告", "有字段为空", QMessageBox.Yes, QMessageBox.Yes))
        else:
            # 组装json数据
            data = {'messageId': 5002, 'userNum': UserId}
            # SingletonTcpSocket().connect("10.2.8.3", 9999)
            # str = json.dumps(data, sort_keys=True, indent=4, separators=(',', ': ')
            str = json.dumps(data)
            print('json dumps:%s' % str)
            SingletonTcpSocket().send(bytes(str, encoding="utf8"))

            # 获取json数据
            str = SingletonTcpSocket().recv(1024)
            print('recv from server:%s' % str)

            # 解析json数据
            resData = json.loads(str.decode('utf8'))
            if (resData['errorCode'] == 0):
                print(QMessageBox.information(self, "提醒", "鉴权用户成功!", QMessageBox.Yes, QMessageBox.Yes))
                self.User_signal.emit(UserId)
                self.close()
                # self.clearEdit()
            else:
                print(QMessageBox.information(self, "提示", resData['errorDetail'], QMessageBox.Yes, QMessageBox.Yes))

            return


if __name__ == "__main__":
    app = QApplication(sys.argv)
    app.setWindowIcon(QIcon("./images/MainWindow_1.png"))
    app.setStyleSheet(qdarkstyle.load_stylesheet_pyqt5())
    mainMindow = User()
    mainMindow.show()
    sys.exit(app.exec_())