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


POS = ['52.29723', '54.901171']
L = 'map'


class MainFunc(QMainWindow, Ui_ya_maps):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.spn_lst = [0.002, 0.005, 0.01, 0.05, 0.1, 0.5, 1, 3, 6, 12, 23, 45]
        self.spn_lst_key = 0
        self.active_map_name = f'almet-{self.spn_lst[self.spn_lst_key]}.png'

        if not os.path.exists('files//img'):
            os.mkdir('files//img')

        os.chdir('files//img')

        self.static_func()

    def static_func(self):
        params = params_func(ll=POS, spn=self.spn_lst[self.spn_lst_key], l=L)
        response = requests.get(const.STATIC_API_SERVER, params)
        with open(self.active_map_name, "wb") as file:
            file.write(response.content)

        self.map.setPixmap(QPixmap(self.active_map_name))

    def closeEvent(self, event):
        os.chdir('..')
        if os.path.exists('img'):
            shutil.rmtree('img')

    def keyPressEvent(self, event):
        if 0 <= self.spn_lst_key + 1 < len(self.spn_lst) and event.key() == Qt.Key_Up:
            self.spn_lst_key += 1
        if 0 <= self.spn_lst_key - 1 < len(self.spn_lst) and event.key() == Qt.Key_Down:
            self.spn_lst_key -= 1

        self.spn_lst_key %= len(self.spn_lst)

        if self.active_map_name != f"almet-{self.spn_lst[self.spn_lst_key]}.png":
            self.active_map_name = f"almet-{self.spn_lst[self.spn_lst_key]}.png"
            if os.access(self.active_map_name, os.F_OK):
                self.map.setPixmap(QPixmap(self.active_map_name))
            else:
                self.static_func()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = MainFunc()
    ex.show()
    sys.exit(app.exec_())
