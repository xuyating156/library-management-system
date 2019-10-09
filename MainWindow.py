# coding=utf-8

import sys
from PyQt5.QtWidgets import *
from PyQt5.QtGui import QIcon, QFont, QPalette, QBrush, QPixmap
from PyQt5.QtCore import *
import qdarkstyle
from SignIn import SignInWidget
from SignUp import SignUpWidget

import sip
from AdminHome import AdminHome
from StudentHome import StudentHome
from changePasswordDialog import changePasswordDialog
from SignUpUser import SignUpUserWidget
from logoutAdmin import logoutAdminWidget
from User import User


class Main(QMainWindow):
    def __init__(self, parent=None):
        super(Main, self).__init__(parent)
        self.layout = QHBoxLayout()
        self.widget = SignInWidget()
        self.resize(1400, 900)
        self.setWindowTitle("欢迎登陆图书馆管理系统")
        self.setCentralWidget(self.widget)
        bar = self.menuBar()
        self.Menu = bar.addMenu("菜单栏")
        self.signUpAction = QAction("注册", self)
        self.signUpUserAction = QAction("添加用户", self)#---
        self.changePasswordAction =QAction("修改密码",self)
        self.signInAction = QAction("登录", self)
        self.logoutAdminAction = QAction("注销管理员", self)
        self.quitAction = QAction("退出", self)
        self.Menu.addAction(self.signUpAction)
        self.Menu.addAction(self.signUpUserAction)
        self.Menu.addAction(self.changePasswordAction)
        self.Menu.addAction(self.signInAction)
        self.Menu.addAction(self.logoutAdminAction)
        self.Menu.addAction(self.quitAction)
        self.signUpAction.setEnabled(True)
        self.signUpUserAction.setEnabled(False)
        self.changePasswordAction.setEnabled(False)
        self.signInAction.setEnabled(False)
        self.logoutAdminAction.setEnabled(True)
        self.widget.is_admin_signal.connect(self.adminSignIn)
        self.widget.is_student_signal[str].connect(self.studentSignIn)

        self.Menu.triggered[QAction].connect(self.menuTriggered)

        self.updateStatusBar('')

    def adminSignIn(self):
        sip.delete(self.widget)
        self.widget = AdminHome()
        self.setCentralWidget(self.widget)
        self.changePasswordAction.setEnabled(True)
        self.signUpAction.setEnabled(True)
        self.signUpUserAction.setEnabled(True)
        self.signInAction.setEnabled(False)
        self.logoutAdminAction.setEnabled(True)

    def studentSignIn(self, studentId):
        sip.delete(self.widget)
        self.widget = StudentHome(studentId)#学生登陆可以，但不会出现之后的界面
        self.setCentralWidget(self.widget)#显示登陆界面之后的内容
        self.changePasswordAction.setEnabled(False)
        self.signUpAction.setEnabled(True)
        self.signUpUserAction.setEnabled(True)
        self.signInAction.setEnabled(False)
        self.logoutAdminAction.setEnabled(True)

    def updateStatusBar(self, strs):
            self.statusBar().showMessage('用户卡号: %s' % strs)

    def menuTriggered(self, q):
        if(q.text()=="修改密码"):
            changePsdDialog=changePasswordDialog(self)
            changePsdDialog.show()
            changePsdDialog.exec_()
        if (q.text() == "注册"):
            sip.delete(self.widget)
            self.widget = SignUpWidget()
            self.setCentralWidget(self.widget)
            self.widget.student_signup_signal[str].connect(self.adminSignIn)
            self.signUpAction.setEnabled(False)
            self.changePasswordAction.setEnabled(True)
            self.signInAction.setEnabled(True)
            self.logoutAdminAction.setEnabled(False)

        if (q.text() == "添加用户"):
            # sip.delete(self.widget)
            # self.widget = SignUpUserWidget()
            # self.setCentralWidget(self.widget)
            # self.widget.student_signupuser_signal[str].connect(self.adminSignIn)
            # self.signUpUserAction.setEnabled(False)
            SingUpUserDialog = SignUpUserWidget(self)
            SingUpUserDialog.show()
            SingUpUserDialog.exec_()


        if (q.text() == "注销管理员"):
            # sip.delete(self.widget)
            # self.widget = logoutAdminWidget()
            # self.setCentralWidget(self.widget)
            # self.widget.student_logoutAdmin_signal[str].connect(self.adminSignIn)
            # self.signUpAction.setEnabled(True)
            # self.changePasswordAction.setEnabled(True)
            # self.signInAction.setEnabled(False)
            # self.logoutAdminAction.setEnabled(False)
            # qApp = QApplication.instance()
            # qApp.quit()
            logoutAdminDialog = logoutAdminWidget(self)
            logoutAdminDialog.show()
            logoutAdminDialog.exec_()
        if (q.text() == "登录"):
            sip.delete(self.widget)
            self.widget = SignInWidget()
            self.setCentralWidget(self.widget)
            self.widget.is_admin_signal.connect(self.adminSignIn)
            # self.widget.is_student_signal[str].connect(self.studentSignIn)
            self.signUpAction.setEnabled(True)
            self.changePasswordAction.setEnabled(True)
            self.signInAction.setEnabled(False)
            self.logoutAdminAction.setEnabled(False)
        if (q.text() == "退出"):
            qApp = QApplication.instance()
            qApp.quit()
        return


if __name__ == "__main__":
    app = QApplication(sys.argv)
    app.setWindowIcon(QIcon("./images/MainWindow_1.png"))
    app.setStyleSheet(qdarkstyle.load_stylesheet_pyqt5())
    mainMindow = Main()
    mainMindow.show()
    sys.exit(app.exec_())
