#-*- coding: utf-8 -*-

import os
import const
from params import params_func
from ya_maps import Ui_ya_maps
import sys
from PyQt5.QtWidgets import QApplication, QMainWindow
from PyQt5.QtGui import QPixmap
import requests
import shutil


POS = ['52.29723', '54.901171']
DELTA = '0.01'
SPN = 'map'


class MainFunc(QMainWindow, Ui_ya_maps):
    def __init__(self):
        super().__init__()
        self.setupUi(self)

        if not os.path.exists('files//img'):
            os.mkdir('files//img')

        self.static_func()

    def static_func(self):
        params = params_func(POS, DELTA, SPN)
        response = requests.get(const.STATIC_API_SERVER, params)

        static_name = 'almet'
        with open('files//img//' + static_name, "wb") as file:
            file.write(response.content)

        self.map.setPixmap(QPixmap('files//img//' + static_name))

    def closeEvent(self, event):
        if os.path.exists('files//img'):
            shutil.rmtree('files//img')


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = MainFunc()
    ex.show()
    sys.exit(app.exec_())
