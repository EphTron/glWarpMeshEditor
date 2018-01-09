#!/usr/bin/python3

import sys
import PyQt5
from PyQt5 import QtWidgets

from lib.ConfigWidget import ConfigWidget


def main():
    app = PyQt5.QtWidgets.QApplication(sys.argv)

    point_list = read_config_points("texture_coords.txt")
    print(point_list)

    cw = ConfigWidget([])

    sys.exit(app.exec_())

def read_config_points(file_path):
    point_list = []
    with open(file_path) as file:
        for line in file:
            point_list.append([float(x) for x in line.split(" ")])

    return point_list


if __name__ == "__main__":
    main()