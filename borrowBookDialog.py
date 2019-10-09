import sys
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
import qdarkstyle
import time
from PyQt5.QtSql import *
import json
from utils.SingletonTcpSocket import SingletonTcpSocket


class borrowBookDialog(QDialog):
    borrow_book_success_signal = pyqtSignal()

    def __init__(self, StudentId, parent=None):
        super(borrowBookDialog, self).__init__(parent)
        self.studentId = StudentId
        self.setUpUI()
        self.setWindowModality(Qt.WindowModal)
        self.setWindowTitle("借阅书籍")

    def setUpUI(self):
        # 书名，书号，作者，分类，添加数量.出版社,出版日期
        self.resize(300, 400)
        self.layout = QFormLayout()
        self.setLayout(self.layout)

        # Label控件
        self.borrowStudentLabel = QLabel("借 阅 人:")
        self.borrowStudentIdLabel = QLabel(self.studentId)
        self.titlelabel = QLabel("  借阅书籍")
        self.bookIdLabel = QLabel("书    号:")

        # button控件
        self.borrowBookButton = QPushButton("确认借阅")

        # lineEdit控件
        self.bookIdEdit = QLineEdit()
        # self.authNameEdit = QLineEdit()
        # self.categoryComboBox = QComboBox()
        # self.categoryComboBox.addItems(BookCategory)
        # self.publisherEdit = QLineEdit()
        # self.publishTime = QLineEdit()

        self.bookIdEdit.setMaxLength(20)
        # self.authNameEdit.setMaxLength(10)
        # self.publisherEdit.setMaxLength(10)

        # 添加进formlayout
        self.layout.addRow("", self.titlelabel)
        self.layout.addRow(self.borrowStudentLabel, self.borrowStudentIdLabel)
        self.layout.addRow(self.bookIdLabel, self.bookIdEdit)
        # self.layout.addRow(self.authNameLabel, self.authNameEdit)
        # self.layout.addRow(self.categoryLabel, self.categoryComboBox)
        # self.layout.addRow(self.publisherLabel, self.publisherEdit)
        # self.layout.addRow(self.publishDateLabel, self.publishTime)
        self.layout.addRow("", self.borrowBookButton)

        # 设置字体
        font = QFont()
        font.setPixelSize(20)
        self.titlelabel.setFont(font)
        font.setPixelSize(16)
        self.borrowStudentIdLabel.setFont(font)
        font.setPixelSize(14)
        self.borrowStudentLabel.setFont(font)
        self.bookIdLabel.setFont(font)
        # self.authNameLabel.setFont(font)
        # self.categoryLabel.setFont(font)
        # self.publisherLabel.setFont(font)
        # self.publishDateLabel.setFont(font)

        self.bookIdEdit.setFont(font)
        # self.authNameEdit.setFont(font)
        # self.authNameEdit.setReadOnly(True)
        # self.authNameEdit.setStyleSheet("background-color:#363636")
        # self.publisherEdit.setFont(font)
        # self.publisherEdit.setReadOnly(True)
        # self.publisherEdit.setStyleSheet("background-color:#363636")
        # self.publishTime.setFont(font)
        # self.publishTime.setStyleSheet("background-color:#363636")
        # self.categoryComboBox.setFont(font)
        # self.categoryComboBox.setStyleSheet("background-color:#363636")

        # button设置
        font.setPixelSize(16)
        self.borrowBookButton.setFont(font)
        self.borrowBookButton.setFixedHeight(32)
        self.borrowBookButton.setFixedWidth(140)

        # 设置间距
        self.titlelabel.setMargin(8)
        self.layout.setVerticalSpacing(10)
        self.borrowBookButton.clicked.connect(self.borrowButtonClicked)
        # self.bookIdEdit.textChanged.connect(self.bookIdEditChanged)
        self.bookIdEdit.returnPressed.connect(self.borrowButtonClicked)

    def borrowButtonClicked(self):
        # 获取书号，书号为空或不存在库中，则弹出错误
        # 向Book_User表插入记录，更新User表以及Book表
        BookId = self.bookIdEdit.text()
        useId = self.studentId
        # BookId为空的处理
        if (BookId == ""):
            print(QMessageBox.warning(self, "警告", "你所要借的书不存在，请查看输入", QMessageBox.Yes, QMessageBox.Yes))
            return

        # 组装json数据
        data = {"messageId":3001,"userNum":useId,"bookId":BookId}
        # SingletonTcpSocket().connect("10.2.8.96", 9999)
        # str = json.dumps(data, sort_keys=True, indent=4, separators=(',', ': ')
        str = json.dumps(data)
        print('json dumps:%s' % str)
        SingletonTcpSocket().send(bytes(str, encoding="utf8"))

        # 获取json数据
        str = SingletonTcpSocket().recv(4096)
        print('recv from server:%s' % str)
        print('222')

        # 解析json数据
        resData = json.loads(str.decode('utf8'))
        print('analysis:'%resData)

        print('111')
        if (resData['errorCode'] == 0):
            print(resData['errorCode'])
            print(QMessageBox.information(self, "提醒", "您已成功借阅!", QMessageBox.Yes, QMessageBox.Yes))
            # self.borrow_book_success_signal.emit()
            self.close()
        else:
            print(QMessageBox.information(self, "提示", resData['errorDetail'], QMessageBox.Yes, QMessageBox.Yes))

        return


if __name__ == "__main__":
    app = QApplication(sys.argv)
    app.setWindowIcon(QIcon("./images/MainWindow_1.png"))
    app.setStyleSheet(qdarkstyle.load_stylesheet_pyqt5())
    mainMindow = borrowBookDialog("0005")
    mainMindow.show()
    sys.exit(app.exec_())
