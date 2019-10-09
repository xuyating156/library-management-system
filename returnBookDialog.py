import sys
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
import qdarkstyle
import time
from PyQt5.QtSql import *
import json
from utils.SingletonTcpSocket import SingletonTcpSocket

class returnBookDialog(QDialog):
    return_book_success_signal=pyqtSignal()
    def __init__(self, StudentId, parent=None):
        super(returnBookDialog, self).__init__(parent)
        self.studentId = StudentId
        self.setUpUI()
        self.setWindowModality(Qt.WindowModal)
        self.setWindowTitle("归还书籍")

    def setUpUI(self):
        # 书名，书号，作者，分类，添加数量.出版社,出版日期
        # 书籍分类：哲学类、社会科学类、政治类、法律类、军事类、经济类、文化类、教育类、体育类、语言文字类、艺术类、历史类、地理类、天文学类、生物学类、医学卫生类、农业类
        self.resize(300, 400)
        self.layout = QFormLayout()
        self.setLayout(self.layout)

        # Label控件
        self.returnStudentLabel = QLabel("还 书 人:")
        self.returnStudentIdLabel = QLabel(self.studentId)
        self.titlelabel = QLabel("  归还书籍")
        self.bookIdLabel = QLabel("书    号:")

        # button控件
        self.returnBookButton = QPushButton("确认归还")

        # lineEdit控件
        self.bookIdEdit = QLineEdit()
        self.publishTime = QLineEdit()

        self.bookIdEdit.setMaxLength(20)

        # 添加进formlayout
        self.layout.addRow("", self.titlelabel)
        self.layout.addRow(self.returnStudentLabel, self.returnStudentIdLabel)
        self.layout.addRow(self.bookIdLabel, self.bookIdEdit)
        self.layout.addRow("", self.returnBookButton)

        # 设置字体
        font = QFont()
        font.setPixelSize(20)
        self.titlelabel.setFont(font)
        font.setPixelSize(16)
        self.returnStudentIdLabel.setFont(font)
        font.setPixelSize(14)
        self.returnStudentLabel.setFont(font)
        self.bookIdLabel.setFont(font)

        self.bookIdEdit.setFont(font)

        # button设置
        font.setPixelSize(16)
        self.returnBookButton.setFont(font)
        self.returnBookButton.setFixedHeight(32)
        self.returnBookButton.setFixedWidth(140)

        # 设置间距
        self.titlelabel.setMargin(8)
        self.layout.setVerticalSpacing(10)
        self.returnBookButton.clicked.connect(self.returnButtonClicked)
        # self.bookIdEdit.textChanged.connect(self.bookIdEditChanged)

    def returnButtonClicked(self):
        # 获取书号，书号为空或并未借阅，则弹出错误
        # 更新Book_User表User表以及Book表
        BookId = self.bookIdEdit.text()
        UserId = self.studentId
        # BookId为空的处理
        if (BookId == ""):
            print(QMessageBox.warning(self, "警告", "你所要还的书不存在，请查看输入", QMessageBox.Yes, QMessageBox.Yes))
            return

        # 组装json数据
        data = {'messageId': 4001, 'userNum': UserId, 'bookId': BookId}
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

        if (resData['errorCode'] == 0):
            print(resData['errorCode'])
            print(QMessageBox.information(self, "提醒", "您已成功归还!", QMessageBox.Yes, QMessageBox.Yes))
            # self.borrow_book_success_signal.emit()
            self.close()
        else:
            print(QMessageBox.information(self, "提示", resData['errorDetail'], QMessageBox.Yes, QMessageBox.Yes))

        return




if __name__ == "__main__":
    app = QApplication(sys.argv)
    app.setWindowIcon(QIcon("./images/MainWindow_1.png"))
    app.setStyleSheet(qdarkstyle.load_stylesheet_pyqt5())
    mainMindow = returnBookDialog("0001")
    mainMindow.show()
    sys.exit(app.exec_())
