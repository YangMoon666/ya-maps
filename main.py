#-*- coding: utf-8 -*-

import os
import const
from params import params_func
from ya_maps import Ui_ya_maps
import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QPushButton, QInputDialog, QWidget
from PyQt5.QtGui import QPixmap, QFont, QFocusEvent
from PyQt5.QtCore import Qt, QEvent
from PyQt5 import QtGui, QtCore
import requests
import shutil


class MainFunc(QMainWindow, Ui_ya_maps):
    def __init__(self):
        super().__init__()
        self.setupUi(self)

        self.search_place = 'Россия, Республика Татарстан, Альметьевск, улица Ленина, 1В'
        self.search_place_postal_code = ', 423458'
        self.search_place_postal_code_bool = True
        self.pt = ''
        self.l_dict = {'m': 'map', 's': 'sat', 'g': 'sat,skl'}
        self.l_dict_key = 'm'
        self.pos = [52.29723, 54.901171]
        self.step_ll = 0.001
        self.spn_lst = [0.002, 0.005, 0.01, 0.05, 0.1, 0.5, 1, 3, 6, 12, 23, 45]
        self.spn_lst_key = 0
        self.active_map_name = f'almet-{self.spn_lst[self.spn_lst_key]}-{self.pos[0]}-{self.pos[1]}-' \
                               f'{self.l_dict[self.l_dict_key]}.png'

        self.font_error = QtGui.QFont()
        self.font_error.setFamily("Ubuntu Medium")
        self.font_error.setPointSize(8)

        self.font_successful = QtGui.QFont()
        self.font_successful.setFamily("Ubuntu Medium")
        self.font_successful.setPointSize(19)

        self.status.setFont(self.font_successful)
        self.status.setText(self.search_place + self.search_place_postal_code
                            if self.search_place_postal_code_bool else self.search_place)
        self.status.setStyleSheet("color: #00a550;")

        if not os.path.exists('files//img'):
            os.mkdir('files//img')

        os.chdir('files//img')

        self.static_func()
        self.reset_search.clicked.connect(self.data_reset_func)
        self.postal_code_btn.clicked.connect(self.postal_code_btn_func)

    def postal_code_btn_func(self):
        self.search_place_postal_code_bool = False if self.search_place_postal_code_bool else True

        self.status.setFont(self.font_successful)
        self.status.setText(self.search_place + self.search_place_postal_code
                            if self.search_place_postal_code_bool else self.search_place)
        self.status.setStyleSheet("color: #00a550;")

    def focusInEvent(self, event: QFocusEvent):
        # фокус при разных обстоятельствах при нажатии на кнопки вверх, влево и тд, переходит к кнопке
        self.reset_search.clearFocus()

    def focusOutEvent(self, event: QFocusEvent):
        self.reset_search.clearFocus()

    def search_place_geocoder(self, search_place):
        # поиск данных о введенном пользователем месте

        params = params_func(search_place=search_place, params_type='geocoder')
        response = requests.get(const.GEOCODER_API_SERVER, params=params)

        try:
            json_response = response.json()
            toponym = json_response["response"]["GeoObjectCollection"]["featureMember"][0]["GeoObject"]
            toponym_address = toponym["metaDataProperty"]["GeocoderMetaData"]["text"]
            toponym_postal_code = toponym["metaDataProperty"]["GeocoderMetaData"]["Address"].get('postal_code', '')
            if toponym_postal_code:
                toponym_postal_code = f', {toponym_postal_code}'
            toponym_coodrinates = toponym["Point"]["pos"].split()

            return toponym_address, toponym_coodrinates, toponym_postal_code
        except Exception:
            pass

        return False

    def search_place_func(self):
        # ввод данных о месте для отображения карты

        search_place, ok_pressed = QInputDialog.getText(self, "Введите место",
                                                        "Введите место, карту которого вы хотите отобразить?")

        if ok_pressed:
            search_place_adress, search_place_coords, toponym_postal_code = self.search_place_geocoder(search_place)
            self.search_place = search_place_adress
            self.search_place_postal_code = toponym_postal_code

            # исключение ошибок поиска (не грамматических)
            if search_place_coords:
                self.pos = [float(search_place_coords[0]), float(search_place_coords[1])]
                self.pt = f'{",".join([str(self.pos[0]), str(self.pos[1])])},comma'

                # статус запроса
                self.status.setFont(self.font_successful)
                self.status.setText(self.search_place + self.search_place_postal_code
                                    if self.search_place_postal_code_bool else self.search_place)
                self.status.setStyleSheet("color: #00a550;")
            else:
                self.status.setFont(self.font_error)
                self.status.setText('Запрос отвергнут. Причина: ошибка')
                self.status.setStyleSheet("color: #ff6161;")

    def static_func(self):
        # поиск карты по определенным параметрам

        params = params_func(ll=self.pos, spn=self.spn_lst[self.spn_lst_key], l=self.l_dict[self.l_dict_key],
                             pt=self.pt, params_type='static')
        response = requests.get(const.STATIC_API_SERVER, params)
        with open(self.active_map_name, "wb") as file:
            file.write(response.content)

        self.map.setPixmap(QPixmap(self.active_map_name))

    def closeEvent(self, event):
        # после закрытия окна программы, все изображения безвозвратно удаляются

        os.chdir('..')
        if os.path.exists('img'):
            shutil.rmtree('img')

    def data_reset_func(self):
        # сброс данных

        self.search_place = 'Россия, Республика Татарстан, Альметьевск, улица Ленина, 1В'
        self.search_place_postal_code = ', 423458'
        self.search_place_postal_code_bool = True
        self.pt = ''
        self.pos = [52.29723, 54.901171]
        self.spn_lst_key = 0
        self.l_dict_key = 'm'

        self.status.setFont(self.font_successful)
        self.status.setText(self.search_place + self.search_place_postal_code
                            if self.search_place_postal_code_bool else self.search_place)
        self.status.setStyleSheet("color: #00a550;")

        self.data_change_func()

    def data_change_func(self):
        # функция для смены карты

        self.active_map_name = \
            f'almet-{self.spn_lst[self.spn_lst_key]}-{self.pos[0]}-{self.pos[1]}-' \
            f'{self.l_dict[self.l_dict_key]}.png'
        if os.access(self.active_map_name, os.F_OK):
            self.map.setPixmap(QPixmap(self.active_map_name))
        else:
            self.static_func()

    def keyPressEvent(self, event):
        # нажатие на ENTER, открытия окна для поиска места
        if event.key() == 16777220:
            self.search_place_func()

        # смена слоя карты
        if event.key() == Qt.Key_S:
            self.l_dict_key = 's'
        if event.key() == Qt.Key_G:
            self.l_dict_key = 'g'
        if event.key() == Qt.Key_M:
            self.l_dict_key = 'm'

        # передвижение карты
        if event.key() == Qt.Key_Up:
            self.pos[1] += self.step_ll
        if event.key() == Qt.Key_Down:
            self.pos[1] -= self.step_ll
        if event.key() == Qt.Key_Left:
            self.pos[0] -= self.step_ll
        if event.key() == Qt.Key_Right:
            self.pos[0] += self.step_ll

        # масштабирование карты
        if 0 <= self.spn_lst_key + 1 < len(self.spn_lst) and event.key() == Qt.Key_PageUp:
            self.spn_lst_key += 1
        if 0 <= self.spn_lst_key - 1 < len(self.spn_lst) and event.key() == Qt.Key_PageDown:
            self.spn_lst_key -= 1
        self.spn_lst_key %= len(self.spn_lst)

        # смена карты происходит только по нажатию на горячие клавишы
        if self.active_map_name != f'almet-{self.spn_lst[self.spn_lst_key]}-{self.pos[0]}-{self.pos[1]}-' \
                                   f'{self.l_dict[self.l_dict_key]}.png':
            self.data_change_func()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = MainFunc()
    ex.show()
    app.focusChanged.connect(
        lambda old, new: ex.focusInEvent(QFocusEvent(QFocusEvent.FocusIn)) if ex.isAncestorOf(
            new) else ex.focusOutEvent(QFocusEvent(QFocusEvent.FocusOut)))
    sys.exit(app.exec_())
