# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'ya_maps.ui'
#
# Created by: PyQt5 UI code generator 5.15.4
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_ya_maps(object):
    def setupUi(self, ya_maps):
        ya_maps.setObjectName("ya_maps")
        ya_maps.resize(600, 450)
        self.map = QtWidgets.QLabel(ya_maps)
        self.map.setGeometry(QtCore.QRect(0, 0, 600, 450))
        self.map.setText("")
        self.map.setObjectName("map")

        self.retranslateUi(ya_maps)
        QtCore.QMetaObject.connectSlotsByName(ya_maps)

    def retranslateUi(self, ya_maps):
        _translate = QtCore.QCoreApplication.translate
        ya_maps.setWindowTitle(_translate("ya_maps", "ya_maps"))
