#-*- coding: utf-8 -*-

from ya_maps import Ui_ya_maps
import sys
from PyQt5.QtWidgets import QApplication, QMainWindow
from PyQt5.QtGui import QPixmap


class MainFunc(QMainWindow, Ui_ya_maps):
    def __init__(self):
        super().__init__()
        self.setupUi(self)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = MainFunc()
    ex.show()
    sys.exit(app.exec_())