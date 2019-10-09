import sys
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
import qdarkstyle
from PyQt5.QtSql import *
import hashlib
import json
from utils.SingletonTcpSocket import SingletonTcpSocket
from utils.SerialComm import SerialCommThread
#
# class SignUpUserWidget(QWidget):
#     student_signupuser_signal = pyqtSignal(str)
#
#     def __init__(self):
#         super().__init__()
#         self.setUpUI()
#
#     def setUpUI(self):
#         self.resize(900, 600)
#         self.setWindowTitle("欢迎登陆图书馆管理系统")
#         self.signUpUserLabel = QLabel("添加用户")
#         self.signUpUserLabel.setAlignment(Qt.AlignCenter)
#         # self.signUpLabel.setFixedWidth(300)
#         self.signUpUserLabel.setFixedHeight(100)
#         font = QFont()
#         font.setPixelSize(36)
#         lineEditFont = QFont()
#         lineEditFont.setPixelSize(20)
#         self.signUpUserLabel.setFont(font)
#
#         self.layout = QVBoxLayout()
#         self.layout.addWidget(self.signUpUserLabel, Qt.AlignHCenter)
#         self.setLayout(self.layout)
#         # 表单，包括学号，姓名，密码，确认密码
#         self.formlayout = QFormLayout()
#         font.setPixelSize(20)
#         # Row1
#         self.studentIdLabel = QLabel("卡    号: ")
#         self.studentIdLabel.setFont(font)
#         self.studentIdLineEdit = QLineEdit()
#         self.studentIdLineEdit.setFixedWidth(180)
#         self.studentIdLineEdit.setFixedHeight(32)
#         self.studentIdLineEdit.setFont(lineEditFont)
#         self.studentIdLineEdit.setMaxLength(10)
#         self.formlayout.addRow(self.studentIdLabel, self.studentIdLineEdit)
#
#         # Row2
#         self.studentNameLabel = QLabel("姓    名: ")
#         self.studentNameLabel.setFont(font)
#         self.studentNameLineEdit = QLineEdit()
#         self.studentNameLineEdit.setFixedHeight(32)
#         self.studentNameLineEdit.setFixedWidth(180)
#         self.studentNameLineEdit.setFont(lineEditFont)
#         self.studentNameLineEdit.setMaxLength(10)
#         self.formlayout.addRow(self.studentNameLabel, self.studentNameLineEdit)
#
#         lineEditFont.setPixelSize(20)
#         # Row3
#         self.studentsexLabel = QLabel("性   别: ")
#         self.studentsexLabel.setFont(font)
#         self.studentsexLineEdit = QLineEdit()
#         self.studentsexLineEdit.setFixedHeight(32)
#         self.studentsexLineEdit.setFixedWidth(180)
#         self.studentsexLineEdit.setFont(lineEditFont)
#         self.studentsexLineEdit.setMaxLength(10)
#         self.formlayout.addRow(self.studentsexLabel, self.studentsexLineEdit)
#
#
#         # Row4
#         self.studentReamrkLabel = QLabel("备   注: ")
#         self.studentReamrkLabel.setFont(font)
#         self.studentReamrkLineEdit = QLineEdit()
#         self.studentReamrkLineEdit.setFixedHeight(32)
#         self.studentReamrkLineEdit.setFixedWidth(180)
#         self.studentReamrkLineEdit.setFont(lineEditFont)
#         self.studentReamrkLineEdit.setMaxLength(10)
#         self.formlayout.addRow(self.studentReamrkLabel, self.studentReamrkLineEdit)
#
#         # Row5
#         self.signUpbutton = QPushButton("添加用户")
#         self.signUpbutton.setFixedWidth(120)
#         self.signUpbutton.setFixedHeight(30)
#         self.signUpbutton.setFont(font)
#         self.formlayout.addRow("", self.signUpbutton)
#         widget = QWidget()
#         widget.setLayout(self.formlayout)
#         widget.setFixedHeight(250)
#         widget.setFixedWidth(300)
#         self.Hlayout = QHBoxLayout()
#         self.Hlayout.addWidget(widget, Qt.AlignCenter)
#         widget = QWidget()
#         widget.setLayout(self.Hlayout)
#         self.layout.addWidget(widget, Qt.AlignHCenter)
#
#         # 设置验证
#
#         self.signUpbutton.clicked.connect(self.SignUp)
#         self.studentIdLineEdit.returnPressed.connect(self.SignUp)
#         self.studentNameLineEdit.returnPressed.connect(self.SignUp)
#         self.studentsexLineEdit.returnPressed.connect(self.SignUp)#--
#         self.studentReamrkLineEdit.returnPressed.connect(self.SignUp)#--
#
#     def SignUp(self):
#         studentId = self.studentIdLineEdit.text()
#         studentName = self.studentNameLineEdit.text()
#         sex = self.studentsexLineEdit.text()
#         remark = self.studentReamrkLineEdit.text()
#         if (studentId == "" or studentName == "" or sex == "" ):
#             print(QMessageBox.warning(self, "警告", "表单不可为空(备注除外)，请重新输入", QMessageBox.Yes, QMessageBox.Yes))
#             return
#         elif( sex != "男" and sex != "女" ):
#             print(QMessageBox.warning(self, "警告", "性别输入男/女，请重新输入", QMessageBox.Yes, QMessageBox.Yes))
#             return
#         else:  # 需要处理逻辑，1.账号已存在;2.密码不匹配;3.插入user表
#
#             if(sex=='男'):
#                 userSex = '0'
#             else:
#                 userSex = '1'
#             # 组装json数据
#             data = {'messageId': 5001, 'userNum': studentId, 'userName': studentName, 'userSex': userSex,
#                     'userRemark': remark}
#             # str = json.dumps(data, sort_keys=True, indent=4, separators=(',', ': ')
#             # SingletonTcpSocket().connect("10.2.8.96", 9999)
#             str = json.dumps(data)
#             print('json dumps:%s' % str)
#             SingletonTcpSocket().send(bytes(str, encoding="utf8"))
#
#             # 获取json数据
#             str = SingletonTcpSocket().recv(1024)
#             print('recv from server:%s' % str)
#
#             # 解析json数据
#             resData = json.loads(str.decode('utf8'))
#             if (resData['errorCode'] == 0):
#                 print(QMessageBox.information(self, "提醒", "您已成功添加用户!", QMessageBox.Yes, QMessageBox.Yes))
#                 # self.is_admin_signal.emit()
#                 self.close()
#             else:
#                 print(QMessageBox.information(self, "提示", resData['errorDetail'], QMessageBox.Yes, QMessageBox.Yes))
#
#             return
#
#
# if __name__ == "__main__":
#     app = QApplication(sys.argv)
#     app.setWindowIcon(QIcon("./images/MainWindow_1.png"))
#     app.setStyleSheet(qdarkstyle.load_stylesheet_pyqt5())
#     mainMindow = SignUpUserWidget()
#     mainMindow.show()
#     sys.exit(app.exec_())


class SignUpUserWidget(QDialog):
    user_number_signal = pyqtSignal(str)

    def __init__(self, parent=None):
        super(SignUpUserWidget, self).__init__(parent)
        self.setWindowModality(Qt.WindowModal)
        self.setWindowTitle("添加用户")
        self.setUpUI()

    def setUpUI(self):
        self.resize(300, 350)
        self.layout = QFormLayout()
        self.setLayout(self.layout)

        self.titlelabel = QLabel(" 添加用户")
        self.studentIdLabel = QLabel("卡号：")
        self.studentNameLabel = QLabel("姓名：")
        self.sexLabel = QLabel("性别：")
        self.studentReamrkLabel = QLabel("备注：")



        self.studentIdEdit = QLineEdit()
        self.studentNameEdit = QLineEdit()
        self.sexEdit = QLineEdit()
        self.studentReamrkEdit = QLineEdit()


        self.changePasswordButton = QPushButton("确认添加")
        self.changePasswordButton.setFixedWidth(140)
        self.changePasswordButton.setFixedHeight(32)

        self.layout.addRow("", self.titlelabel)
        self.layout.addRow(self.studentIdLabel, self.studentIdEdit)
        self.layout.addRow(self.studentNameLabel, self.studentNameEdit)
        self.layout.addRow(self.sexLabel, self.sexEdit)
        self.layout.addRow(self.studentReamrkLabel, self.studentReamrkEdit)

        self.layout.addRow("", self.changePasswordButton)

        font = QFont()
        font.setPixelSize(20)
        self.titlelabel.setFont(font)
        font.setPixelSize(16)
        self.studentIdLabel.setFont(font)
        self.studentNameLabel.setFont(font)
        self.sexLabel.setFont(font)
        self.studentReamrkLabel.setFont(font)


        font.setPixelSize(16)
        self.studentIdEdit.setFont(font)
        self.changePasswordButton.setFont(font)
        font.setPixelSize(18)
        self.studentNameEdit.setFont(font)

        self.titlelabel.setMargin(16)
        self.layout.setVerticalSpacing(16)

        # 设置长度
        self.studentIdEdit.setMaxLength(10)
        self.studentNameEdit.setMaxLength(16)

        self.changePasswordButton.clicked.connect(self.SignUp)
        self.user_number_signal[str].connect(self.add_card_number)

        # 启动线程获取card_number
        self.thread = SerialCommThread(self.signal_emit)
        self.thread.start()

    def signal_emit(self, string):
        self.user_number_signal.emit(string)

    def add_card_number(self, string):
        self.studentIdEdit.setText(string)

    def SignUp(self):
        studentId = self.studentIdEdit.text()
        studentName = self.studentNameEdit.text()
        sex = self.sexEdit.text()
        remark = self.studentReamrkEdit.text()
        if (studentId == "" or studentName == "" or sex == "" ):
            print(QMessageBox.warning(self, "警告", "表单不可为空(备注除外)，请重新输入", QMessageBox.Yes, QMessageBox.Yes))
            return
        elif( sex != "男" and sex != "女" ):
            print(QMessageBox.warning(self, "警告", "性别输入男/女，请重新输入", QMessageBox.Yes, QMessageBox.Yes))
            return
        else:  # 需要处理逻辑，1.账号已存在;2.密码不匹配;3.插入user表

            if(sex=='男'):
                userSex = '0'
            else:
                userSex = '1'
            # 组装json数据
            data = {'messageId': 5001, 'userNum': studentId, 'userName': studentName, 'userSex': userSex,
                    'userRemark': remark}
            # str = json.dumps(data, sort_keys=True, indent=4, separators=(',', ': ')
            SingletonTcpSocket().connect("10.2.8.3", 9999)
            str = json.dumps(data)
            print('json dumps:%s' % str)
            SingletonTcpSocket().send(bytes(str, encoding="utf8"))

            # 获取json数据
            str = SingletonTcpSocket().recv(1024)
            print('recv from server:%s' % str)

            # 解析json数据
            resData = json.loads(str.decode('utf8'))
            if (resData['errorCode'] == 0):
                print(QMessageBox.information(self, "提醒", "您已成功添加用户!", QMessageBox.Yes, QMessageBox.Yes))
                self.close()
            else:
                print(QMessageBox.information(self, "提示", resData['errorDetail'], QMessageBox.Yes, QMessageBox.Yes))

            return


if __name__ == "__main__":
    app = QApplication(sys.argv)
    app.setWindowIcon(QIcon("./images/MainWindow_1.png"))
    app.setStyleSheet(qdarkstyle.load_stylesheet_pyqt5())
    mainMindow = SignUpUserWidget()
    mainMindow.show()
    sys.exit(app.exec_())
