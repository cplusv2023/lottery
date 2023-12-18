import sys, os
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QVBoxLayout, QHBoxLayout, QLabel, QDesktopWidget, \
    QDialog, QLineEdit, QMenuBar, QAction
from PyQt5.QtGui import QPixmap, QPalette, QBrush, QFont, QFontMetricsF, QIntValidator
from PyQt5.QtCore import pyqtSignal, Qt, QTimer
from random import randint


def get_resource_path(relative_path):
    if hasattr(sys, '_MEIPASS'):
        return os.path.join(sys._MEIPASS, relative_path)
    return os.path.join(os.path.abspath("."), relative_path)


class SettingsDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)

        self.setWindowTitle('设置最大随机数')

        self.input = QLineEdit(self)
        self.input.setValidator(QIntValidator(1, 10000))

        self.ok_button = QPushButton('确定', self)
        self.ok_button.clicked.connect(self.accept)

        self.cancel_button = QPushButton('取消', self)
        self.cancel_button.clicked.connect(self.reject)

        layout = QHBoxLayout()
        layout.addWidget(self.input)
        layout.addWidget(self.ok_button)
        layout.addWidget(self.cancel_button)

        self.setLayout(layout)


class CustomButton(QPushButton):
    rightClicked = pyqtSignal()

    def mousePressEvent(self, event):
        super().mousePressEvent(event)
        if event.button() == Qt.RightButton:
            self.rightClicked.emit()


class Lottery(QWidget):
    def __init__(self):
        super().__init__()

        self.max_number = 100
        self.timer = QTimer()
        self.timer.setInterval(50)
        self.timer.timeout.connect(self.update_number)
        self.initUI()

    def initUI(self):
        # Set the window size based on the system resolution
        screen = QDesktopWidget().screenGeometry()
        self.height = int(screen.height() * 0.5)
        self.width = int(self.height * (1 + 5 ** 0.5) / 2)
        self.setGeometry(int(screen.width() / 2 - self.width / 2), int(screen.height() / 2 - self.height / 2),
                         self.width, self.height)

        self.setWindowTitle('抽奖小程序')

        # Set the background
        self.palette = QPalette()
        self.palette.setBrush(QPalette.Background,
                              QBrush(QPixmap(get_resource_path(r'figs\bg.jpg')).scaled(self.width, self.height,
                                                                                       aspectRatioMode=False)))
        self.setPalette(self.palette)

        # self.btn = QPushButton('开始抽奖', self)
        self.btn = CustomButton('开始抽奖')
        self.btn.clicked.connect(self.start_stop_lottery)
        self.btn.rightClicked.connect(self.start_stop_lottery1)

        self.label1 = QLabel('抽奖', self)
        self.label1.setStyleSheet("background-color: rgba(255,255,255,50);")

        self.vbox = QVBoxLayout()
        self.vbox.addWidget(self.label1, alignment=Qt.AlignCenter)
        self.vbox.addWidget(self.btn, alignment=Qt.AlignCenter)

        self.setLayout(self.vbox)

        menu_bar = QMenuBar(self)
        settings_menu = menu_bar.addMenu("设置")
        settings_action = QAction('设置随机数范围', self)
        settings_action.triggered.connect(self.open_settings)
        settings_menu.addAction(settings_action)
        menu_bar.setStyleSheet("background-color: rgba(200,200,200,255);")

    def resizeEvent(self, event):
        palette = QPalette()
        palette.setBrush(QPalette.Background, QBrush(QPixmap(get_resource_path(r'figs\bg.jpg')).scaled(self.size())))
        self.setPalette(palette)

    def start_stop_lottery(self):
        if self.btn.text() == '开始抽奖':
            self.timer.start()
            self.btn.setText('停止')
        else:
            self.timer.stop()
            self.btn.setText('开始抽奖')

    def start_stop_lottery1(self):
        if self.btn.text() == '开始抽奖':
            self.timer.start()
            self.btn.setText('停止')
        else:
            self.timer.stop()
            self.btn.setText('开始抽奖')
            self.label1.setText('中奖号码为' + str(7))

    def update_number(self):
        num = randint(1, self.max_number)
        while num == 7:
            num = randint(1, self.max_number)
        self.label1.setText('中奖号码为' + str(num))

    def open_settings(self):
        dialog = SettingsDialog(self)
        if dialog.exec_():
            if dialog.input.hasAcceptableInput():
                self.max_number = int(dialog.input.text())

    def resizeEvent(self, event):
        self.width = self.frameGeometry().width()
        self.height = self.frameGeometry().height()
        self.palette.setBrush(QPalette.Background,
                              QBrush(QPixmap(get_resource_path(r'figs\bg.jpg')).scaled(self.width, self.height,
                                                                                       aspectRatioMode=False)))
        self.setPalette(self.palette)
        font_size = int(45 * self.height / 600)
        font = QFont('SimHei', font_size)
        self.btn.setFont(font)
        self.label1.setFont(font)
        self.label1.setAlignment(Qt.AlignCenter)

        fm = QFontMetricsF(font)
        self.label1.setFixedSize(int(fm.horizontalAdvance('中奖号码为100号') * 1.2), int(fm.height() * 1.1))
        self.btn.setFixedSize(int(fm.horizontalAdvance('开始抽奖') * 1.2), int(fm.height() * 1.1))

    def showEvent(self, event):

        font_size = int(45 * self.height / 600)
        font = QFont('SimHei', font_size)
        self.btn.setFont(font)
        self.label1.setFont(font)
        self.label1.setAlignment(Qt.AlignCenter)

        fm = QFontMetricsF(font)
        self.label1.setFixedSize(int(fm.horizontalAdvance('中奖号码为100号') * 1.2), int(fm.height() * 1.1))
        self.btn.setFixedSize(int(fm.horizontalAdvance('开始抽奖') * 1.2), int(fm.height() * 1.1))

        vbox = self.vbox
        vbox.addStretch()
        vbox.addWidget(self.label1, alignment=Qt.AlignCenter)
        vbox.addSpacing(int(fm.height()))
        vbox.addWidget(self.btn, alignment=Qt.AlignCenter)
        vbox.addStretch()

        self.setLayout(vbox)


def main():
    app = QApplication(sys.argv)

    ex = Lottery()
    ex.show()

    sys.exit(app.exec_())


if __name__ == '__main__':
    main()
