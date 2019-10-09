import sys
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
import qdarkstyle
from PyQt5.QtSql import *
import time
import sip
from StudentHome import StudentHome
from utils.SingletonTcpSocket import SingletonTcpSocket
import json


class logoutAdminWidget(QDialog):
    student_logoutAdmin_signal = pyqtSignal(str)

    def __init__(self, parent=None):
        super(logoutAdminWidget, self).__init__(parent)
        self.setUpUI()
        self.setWindowModality(Qt.WindowModal)
        self.setWindowTitle("注销管理员")

    def setUpUI(self):
        self.resize(300, 350)
        self.layout = QFormLayout()  # 表格布局
        self.setLayout(self.layout)

        # Label控件
        self.titlelabel = QLabel("注销管理员")
        self.UserIdLabel = QLabel("工    号:")

        # button控件
        self.UserButton = QPushButton("注销管理员")
        # lineEdit控件
        self.UserIdEdit = QLineEdit()

        self.UserIdEdit.setMaxLength(16)

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

        self.UserButton.clicked.connect(self.SignUp)

    def SignUp(self):
        studentId = self.UserIdEdit.text()
        if (studentId == ""):
            print(QMessageBox.warning(self, "警告", "表单不可为空，请重新输入", QMessageBox.Yes, QMessageBox.Yes))
            return
        else:
            # 组装json数据
            data = {'messageId': 1004, 'adminId': studentId}
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
                print(QMessageBox.information(self, "提醒", "您已成功注销管理员!", QMessageBox.Yes, QMessageBox.Yes))
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
    mainMindow = logoutAdminWidget()
    mainMindow.show()
    sys.exit(app.exec_())
