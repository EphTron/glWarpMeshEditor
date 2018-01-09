#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on 09.01.18
@author: ephtron
"""

import random
from PyQt5 import QtWidgets
from PyQt5 import QtGui
from PyQt5 import QtCore


class Node(QtWidgets.QGraphicsItem):
    def __init__(self, parent=None):
        super(Node, self).__init__(parent)
        self.setFlag(QtWidgets.QGraphicsItem.ItemIsMovable)

    def boundingRect(self):
        return

    def paint(self, qp, QStyleOptionGraphicsItem, widget=None):
        pen = QtGui.QPen(QtCore.Qt.black, 4, QtCore.Qt.SolidLine)
        qp.setPen(pen)
        qp.drawPoint(5, 5)


class ConfigWidget(QtWidgets.QWidget):
    def __init__(self, point_list, parent=None):
        super(ConfigWidget, self).__init__(parent)

        self.point_list = point_list
        self.point_item_list = []

        self.scene = None
        self.g_view = None

        self.init_ui()

    def init_ui(self):
        hbox = QtWidgets.QHBoxLayout()
        self.g_view = QtWidgets.QGraphicsView()
        self.g_view.setScene(self.scene)

        self.scene = QtWidgets.QGraphicsScene(0, 0, 1000, 1000, self)
        self.scene.addText("Dome Warp Config")
        self.setup_scene()

        hbox.addWidget(self.g_view)
        self.setLayout(hbox)
        self.show()

    def setup_scene(self):

        for point in self.point_list:
            p = QtWidgets.QGraphicsEllipseItem(10, 0, 20, 20)
            p.setFlag(QtWidgets.QGraphicsItem.ItemIsMovable, True)
            p.setFlag(QtWidgets.QGraphicsItem.ItemIsSelectable, True)
            self.point_item_list.append()

        self.item1 = QtWidgets.QGraphicsEllipseItem(10, 0, 20, 20)
        self.item1.setFlag(QtWidgets.QGraphicsItem.ItemIsMovable, True)
        self.item1.setFlag(QtWidgets.QGraphicsItem.ItemIsSelectable, True)
        self.scene.addItem(self.item1)

    # def paintEvent(self, e):
    #     qp = QtGui.QPainter()
    #     qp.begin(self)
    #     self.draw_points(qp)
    #     qp.end()
    #
    # def draw_points(self, qp):
    #     pen = QtGui.QPen(QtCore.Qt.black, 4, QtCore.Qt.SolidLine)
    #     qp.setPen(pen)
    #     size = self.size()
    #
    #     for i in range(100):
    #         x = random.randint(1, size.width() - 1)
    #         y = random.randint(1, size.height() - 1)
    #         qp.drawPoint(x, y)
