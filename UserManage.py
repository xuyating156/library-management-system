import sys
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
import qdarkstyle
from PyQt5.QtSql import *
import time
import sip
import json
from utils.SingletonTcpSocket import SingletonTcpSocket
class UserManage(QDialog):
    UserManage_signal = pyqtSignal(str)


    def __init__(self, parent=None):
        super(UserManage, self).__init__(parent)
        self.setUpUI()
        self.setWindowModality(Qt.WindowModal)
        self.setWindowTitle("删除用户")

    def setUpUI(self):
        self.resize(300, 400)
        self.layout = QFormLayout()#表格布局
        self.setLayout(self.layout)

        # Label控件
        self.titlelabel = QLabel("  输入卡号")
        self.UserIdLabel = QLabel("卡    号:")

        # button控件
        self.UserButton = QPushButton("删除")
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

        self.UserButton.clicked.connect(self.deleteUserclicked)



    def deleteUserclicked(self):
        UserId = self.UserIdEdit.text()
        if(UserId == "" ):
            print(QMessageBox.warning(self, "警告", "请输入要删除的用户", QMessageBox.Yes, QMessageBox.Yes))
            return
        #直接删了········································
        else:

            # 组装json数据
            data = {'messageId' : 5003, 'userNum' : UserId}
            # SingletonTcpSocket().connect("192.168.126.130", 9999)
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
                print(QMessageBox.information(self, "提醒", "删除用户成功!", QMessageBox.Yes, QMessageBox.Yes))
                # self.updateUI()
                self.close()
            else:
                print(QMessageBox.information(self, "提示", resData['errorDetail'], QMessageBox.Yes, QMessageBox.Yes))

            return


if __name__ == "__main__":
    app = QApplication(sys.argv)
    app.setWindowIcon(QIcon("./images/MainWindow_1.png"))
    app.setStyleSheet(qdarkstyle.load_stylesheet_pyqt5())
    mainMindow = UserManage()
    mainMindow.show()
    sys.exit(app.exec_())
