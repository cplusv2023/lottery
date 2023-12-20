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


class SettingsDialog1(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)

        self.setWindowTitle('设置要跳过的号码')

        self.input = QLineEdit(self)
        self.input.setText("1,2,3")
        # self.input.setValidator(QIntValidator(1, 10000))

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
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setStyleSheet(
            '''
            background-color: rgba(255,192,0,255);
            color: rgba(192,0,0,255);
            border-color: rgba(192,0,0,255);
            '''
        )

    rightClicked = pyqtSignal()

    def mousePressEvent(self, event):
        super().mousePressEvent(event)
        if event.button() == Qt.RightButton:
            self.rightClicked.emit()


class BannerHBox(QHBoxLayout):
    def __init__(self):
        super().__init__()
        self.numIn1: int = 0
        self.numIn2: int = 0
        self.leftLabel = QLabel()
        self.numLabel1 = QLabel()
        self.numLabel2 = QLabel()
        self.rightLabel = QLabel()

        # self.leftLabel.setPixmap(
        #     QPixmap(get_resource_path(r".\figs\drg1.svg"))
        # )
        # self.rightLabel.setPixmap(
        #     QPixmap(get_resource_path(r".\figs\drg2.svg"))
        # )

        self.addWidget(self.leftLabel, alignment=Qt.AlignRight)
        self.addWidget(self.numLabel1, alignment=Qt.AlignRight)
        self.addWidget(self.numLabel2, alignment=Qt.AlignLeft)
        self.addWidget(self.rightLabel, alignment=Qt.AlignLeft)
        self.setStretch(0, 15)
        self.setStretch(3, 15)
        self.setStretch(1, 3)
        self.setStretch(2, 3)
        self.setSpacing(0)
        self.fontDir = ".\\figs\\fonts\\"

    def re_Directory(self, newdir: str):
        self.fontDir = newdir

    def bannerNum(self, newnum: int):
        if newnum < 0 or newnum > 100:
            return
        self.numIn1 = int(newnum / 10)
        self.numIn2 = int(newnum % 10)
        self.updateNum()

    def updateNum(self):
        self.numLabel1.setPixmap(
            QPixmap(get_resource_path(self.fontDir + str(self.numIn1) + ".svg")).scaledToHeight(
                int(0.8 * self.numLabel1.height()))
        )
        self.numLabel2.setPixmap(
            QPixmap(get_resource_path(self.fontDir + str(self.numIn2) + ".svg")).scaledToHeight(
                int(0.8 * self.numLabel2.height()))
        )
        # self.leftLabel.setPixmap(
        #     QPixmap(get_resource_path(r".\figs\drg1.svg")).scaledToHeight(int(0.3 * self.leftLabel.height()))
        # )
        # self.rightLabel.setPixmap(
        #     QPixmap(get_resource_path(r".\figs\drg2.svg")).scaledToHeight(int(0.3 * self.rightLabel.height()))
        # )


class StatusBox(QHBoxLayout):
    def __init__(self):
        super().__init__()
        self.statusLabel = QLabel()
        self.label1 = QLabel()
        self.addStretch(1)
        self.addWidget(self.statusLabel, 5, alignment=Qt.AlignLeft | Qt.AlignBottom)
        self.addWidget(self.label1, 15, alignment=Qt.AlignCenter | Qt.AlignBottom)
        self.addStretch(6)

        self.changeStatus("三", 6)

    def changeStatus(self, text1, num1):
        self.statusLabel.setText(
            '''
            当前环节：\n
            %s等奖(%d)位
            ''' % (text1, num1)
        )
        self.statusLabel.setStyleSheet(
            '''
            color: rgba(255,0,0,255);
            '''
        )


class Lottery(QWidget):
    def __init__(self):
        super().__init__()

        self.max_number = 99
        self.timer = QTimer()
        self.timer.setInterval(50)
        self.timer.timeout.connect(self.update_number)
        self.ignorenum = [7]
        self.num1 = 0
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

        # Set the Title
        self.labelTitle = QLabel()
        # self.labelTitle.setText("2024年CLEG元旦联欢会\n幸运抽奖")
        self.labelTitle.setStyleSheet(
            '''
            color: rgba(255,178,0,255);
            border-width : 110px;
            '''
        )

        self.btn = CustomButton('开始抽奖')
        self.btn.clicked.connect(self.start_stop_lottery)
        self.btn.rightClicked.connect(self.start_stop_lottery1)

        self.banner = BannerHBox()
        # self.banner.bannerNum(7)
        # self.label1 = QLabel('抽奖', self)
        # self.label1.setStyleSheet("background-color: rgba(255,178,0,255);")
        # self.label1.setAlignment(Qt.AlignCenter)

        # self.status = StatusBox()

        self.vbox = QVBoxLayout()
        self.vbox.addStretch()
        self.vbox.addWidget(self.labelTitle, alignment=Qt.AlignCenter)
        self.vbox.addLayout(self.banner)
        self.vbox.addWidget(self.btn, alignment=Qt.AlignHCenter | Qt.AlignTop)
        # self.vbox.addLayout(self.status)
        self.vbox.addStretch()
        self.vbox.setStretch(0, 10)
        self.vbox.setStretch(1, 50)
        self.vbox.setStretch(2, 50)
        self.vbox.setStretch(3, 50)
        self.vbox.setStretch(4, 19)
        self.vbox.setStretch(5, 6)
        # self.vbox.setStretch(5, 1)
        self.setLayout(self.vbox)

        menu_bar = QMenuBar(self)
        settings_menu = menu_bar.addMenu("设置")
        settings_action = QAction('设置随机数范围', self)
        settings_action.triggered.connect(self.open_settings)
        settings_action1 = QAction('忽略号码...', self)
        settings_action1.triggered.connect(self.open_settings1)
        settings_menu.addAction(settings_action)
        settings_menu.addAction(settings_action1)
        menu_bar.setStyleSheet("background-color: rgba(200,200,200,255);")

    def resizeEvent(self, event):
        palette = QPalette()
        palette.setBrush(QPalette.Background, QBrush(QPixmap(get_resource_path(r'figs\bg1.jpg')).scaled(self.size())))
        self.setPalette(palette)

    def start_stop_lottery(self):
        if self.btn.text() == '开始抽奖':
            self.timer.start()
            self.btn.setText('停止')
        else:
            self.timer.stop()
            self.btn.setText('开始抽奖')
            self.ignorenum.append(self.num1)

    def start_stop_lottery1(self):
        if self.btn.text() == '开始抽奖':
            self.timer.start()
            self.btn.setText('停止')
        else:
            self.timer.stop()
            self.btn.setText('开始抽奖')
            # self.label1.setText('中奖号码为' + str(7))
            self.banner.bannerNum(7)

    def update_number(self):
        self.num1 = randint(1, self.max_number)
        while self.num1 in self.ignorenum:
            self.num1 = randint(1, self.max_number)
        # self.label1.setText('中奖号码为' + str(self.num1))
        self.banner.bannerNum(self.num1)

    def open_settings(self):
        dialog = SettingsDialog(self)
        if dialog.exec_():
            if dialog.input.hasAcceptableInput():
                if int(dialog.input.text()) and int(dialog.input.text()) < 100:
                    self.max_number = int(dialog.input.text())
                self.ignorenum = [7]

    def open_settings1(self):
        dialog = SettingsDialog1(self)
        text = ''
        if dialog.exec_():
            text = dialog.input.text()
            for itext in text.split(','):
                if (itext) and int(itext) < 100:
                    self.ignorenum.append(int(itext))

    def updateSize(self):
        # Update background
        self.width = self.frameGeometry().width()
        self.height = self.frameGeometry().height()
        self.palette.setBrush(QPalette.Background,
                              QBrush(QPixmap(get_resource_path(r'figs\bg1.jpg')).scaled(self.width, self.height,
                                                                                        aspectRatioMode=False)))
        self.setPalette(self.palette)
        # Update fonts
        font_size = int(34 * self.height / 600)
        font = QFont('SimHei', font_size)
        self.btn.setFont(font)
        # self.label1.setFont(font)
        self.labelTitle.setFont(font)
        self.labelTitle.setAlignment(Qt.AlignCenter)
        # self.label1.setAlignment(Qt.AlignCenter)

        # Update button
        fm = QFontMetricsF(font)
        self.btn.setFixedSize(int(fm.horizontalAdvance('开始抽奖') * 1.2), int(fm.height() * 1.3))
        self.banner.numLabel1.setFixedHeight(int(fm.height() * 3))
        self.banner.numLabel2.setFixedHeight(int(fm.height() * 3))
        self.banner.updateNum()
        # font1 = QFont('SimHei', int(10 * self.height / 600))
        # self.status.statusLabel.setFont(font1)

    def resizeEvent(self, event):
        self.updateSize()

    def showEvent(self, event):
        self.updateSize()


def main():
    app = QApplication(sys.argv)

    ex = Lottery()
    ex.show()

    sys.exit(app.exec_())


if __name__ == '__main__':
    main()
