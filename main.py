#-*- coding: utf-8 -*-

import os
import const
from params import params_func
from ya_maps import Ui_ya_maps
import sys
from PyQt5.QtWidgets import QApplication, QMainWindow
from PyQt5.QtGui import QPixmap
from PyQt5.QtCore import Qt
import requests
import shutil


L = 'map'
SPN = 0.001


class MainFunc(QMainWindow, Ui_ya_maps):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.pos = [52.29723, 54.901171]
        self.step_ll = 0.001
        self.active_map_name = f'almet-{self.pos[0]}-{self.pos[1]}.png'

        if not os.path.exists('files//img'):
            os.mkdir('files//img')

        os.chdir('files//img')

        self.static_func()

    def static_func(self):
        params = params_func(ll=self.pos, spn=SPN, l=L)
        response = requests.get(const.STATIC_API_SERVER, params)
        with open(self.active_map_name, "wb") as file:
            file.write(response.content)

        self.map.setPixmap(QPixmap(self.active_map_name))

    def closeEvent(self, event):
        os.chdir('..')
        if os.path.exists('img'):
            shutil.rmtree('img')

    def keyPressEvent(self, event):
        if event.key() == Qt.Key_Up:
            self.pos[1] += self.step_ll
        if event.key() == Qt.Key_Down:
            self.pos[1] -= self.step_ll
        if event.key() == Qt.Key_Left:
            self.pos[0] -= self.step_ll
        if event.key() == Qt.Key_Right:
            self.pos[0] += self.step_ll

        if self.active_map_name != f'almet-{self.pos[0]}-{self.pos[1]}.png':
            self.active_map_name = f'almet-{self.pos[0]}-{self.pos[1]}.png'
            if os.access(self.active_map_name, os.F_OK):
                self.map.setPixmap(QPixmap(self.active_map_name))
            else:
                self.static_func()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = MainFunc()
    ex.show()
    sys.exit(app.exec_())
