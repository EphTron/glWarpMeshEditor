#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on 09.01.18
@author: ephtron
"""

import random
from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QApplication, QWidget, QInputDialog, QLineEdit, QFileDialog
from PyQt5 import QtGui
from PyQt5 import QtCore


class Node(QtWidgets.QGraphicsEllipseItem):
    press_signal = QtCore.pyqtSignal()

    def __init__(self, point_idx, orig_x, orig_y, pos_x, pos_y, width, height, config_widget, parent=None):
        super(Node, self).__init__(pos_x, pos_y, width, height, parent)
        self.setFlag(QtWidgets.QGraphicsItem.ItemIsMovable, True)
        self.setFlag(QtWidgets.QGraphicsItem.ItemIsSelectable, True)

        self.point_idx = point_idx
        self.orig_x = orig_x
        self.orig_y = orig_y

        self.pos_x = pos_x
        self.pos_y = pos_y

        @QtCore.pyqtSlot()
        def update_node_position():
            self.update_position()

        config_widget.save_signal.connect(update_node_position)

    def mousePressEvent(self, QGraphicsSceneMouseEvent):
        super(Node, self).mousePressEvent(QGraphicsSceneMouseEvent)
        # self.press_signal.emit()
        print(self.point_idx)
        self.update_position()

    def update_position(self):
        print("update pos", self.x(), self.y())


class ConfigWidget(QtWidgets.QWidget):
    load_signal = QtCore.pyqtSignal()
    save_signal = QtCore.pyqtSignal()
    selection_signal = QtCore.pyqtSignal(int)

    def __init__(self, parent=None):
        super(ConfigWidget, self).__init__(parent)

        self.point_list = []
        self.point_item_list = []
        self.file_path = "texture_coords.txt"

        self.geometry_size = 1000
        self.scene_size = 900
        self.rings = 0
        self.lines = 0

        self.scene = None
        self.g_view = None

        self.init_ui()

    def init_ui(self):
        self.setGeometry(100, 100, self.geometry_size, self.geometry_size)
        self.setWindowTitle("Config Editor")

        # Init layout
        hbox = QtWidgets.QHBoxLayout()

        # Load button
        load_button = QtWidgets.QPushButton("Load dome configuration", self)
        hbox.addWidget(load_button)

        # Selection buttons
        single_selection_button = QtWidgets.QRadioButton("Single Selection", self)
        single_selection_button.setChecked(True)
        hbox.addWidget(single_selection_button)
        ring_selection_button = QtWidgets.QRadioButton("Ring Selection", self)
        hbox.addWidget(ring_selection_button)
        line_selection_button = QtWidgets.QRadioButton("Line Selection", self)
        hbox.addWidget(line_selection_button)

        # Save button
        save_button = QtWidgets.QPushButton("Save", self)
        hbox.addWidget(save_button)

        # Connect buttons
        load_button.clicked.connect(self.load_config)
        save_button.clicked.connect(self.save_config)

        # @QtCore.pyqtSlot()
        # def on_click_save():
        #     gesture_name = self.line_edit.text()
        #     if gesture_name:
        #         self.add_gesture_signal.emit(gesture_name)

        self.g_view = QtWidgets.QGraphicsView()
        self.scene = QtWidgets.QGraphicsScene(0, 0, self.scene_size, self.scene_size, self)

        vbox = QtWidgets.QVBoxLayout(self)
        vbox.addWidget(self.g_view)
        vbox.addLayout(hbox)
        self.setLayout(vbox)
        self.show()

    def setup_scene(self):
        min_max_x = [100.0, -100.0]
        min_max_y = [100.0, -100.0]
        border_size = 50

        for point in self.point_list:
            # get min x
            if point[0] < min_max_x[0]:
                min_max_x[0] = point[0]
            # get max x
            if point[0] > min_max_x[1]:
                min_max_x[1] = point[0]

            # get min y
            if point[1] < min_max_y[0]:
                min_max_y[0] = point[1]
            # get max y
            if point[1] > min_max_y[1]:
                min_max_y[1] = point[1]

        print(min_max_x, min_max_y)

        for idx, p in enumerate(self.point_list):
            # example
            # p = QtWidgets.QGraphicsEllipseItem(point[0] * 900 + 50, point[1] * 900 + 50, 10, 10)
            # p.setFlag(QtWidgets.QGraphicsItem.ItemIsMovable, True)
            # p.setFlag(QtWidgets.QGraphicsItem.ItemIsSelectable, True)
            point = [self.map_to_range(p[0], min_max_x[0], min_max_x[1], 0, 1),
                     self.map_to_range(p[1], min_max_y[0], min_max_y[1], 0, 1)]
            print(point)

            p = Node(idx, point[0], point[1],
                     point[0] * (self.scene_size - border_size) + border_size / 2,
                     point[1] * (self.scene_size - border_size) + border_size / 2,
                     10, 10, self)
            self.point_item_list.append(p)
            self.scene.addItem(p)

    def save_config(self):
        self.save_signal.emit()

        file_name = self.save_file_dialog()
        new_config_file = open(file_name, 'w')
        if new_config_file:
            for point_item in self.point_item_list:
                new_config_file.write("%f %f %f\n" % (point_item.pos_x, point_item.pos_y, 0.0))
            new_config_file.write("%f %f %f\n" % (self.rings, self.lines, len(self.point_item_list)))

    def load_config(self):
        self.reset_scene()
        if self.open_file_name_dialog():
            point_list = []

            # read points of dome config
            with open(self.file_path) as file:
                for line in file:
                    point_list.append([float(x) for x in line.split(" ")])

            # check if config file is correct
            print(len(point_list), "vs", point_list[-1][2] + 1)

            if len(point_list) == point_list[-1][2] + 1:
                self.rings = point_list[-1][0]
                self.lines = point_list[-1][1]
                del point_list[-1]
            else:
                point_list = []
                print("Error: Point count is wrong!")

            self.point_list = point_list
            print(self.point_list)
            self.setup_scene()

            self.g_view.setScene(self.scene)

    def open_file_name_dialog(self):
        self.load_signal.emit()
        options = QtWidgets.QFileDialog.Options()
        options |= QtWidgets.QFileDialog.DontUseNativeDialog
        file_name, _ = QtWidgets.QFileDialog.getOpenFileName(self, "QFileDialog.getOpenFileName()", "",
                                                             "All Files (*);;Text Files (*.txt)", options=options)
        if file_name:
            print(file_name)
            self.file_path = file_name
            return file_name
        else:
            return None

    def save_file_dialog(self):
        options = QtWidgets.QFileDialog.Options()
        options |= QtWidgets.QFileDialog.DontUseNativeDialog
        file_name, _ = QtWidgets.QFileDialog.getSaveFileName(self, "QFileDialog.getSaveFileName()", "",
                                                             "All Files (*);;Text Files (*.txt)", options=options)
        if file_name:
            print(file_name)
            return file_name
        else:
            return None

    def reset_scene(self):
        self.scene.clear()
        self.g_view.update()

    def map_to_range(self, val, in_min, in_max, out_min, out_max):
        return (val - in_min) * (out_max - out_min) / (in_max - in_min) + out_min
