#!/usr/bin/python3

import sys
import PyQt5
from PyQt5 import QtWidgets

from lib.ConfigWidget import ConfigWidget


def main():
    app = PyQt5.QtWidgets.QApplication(sys.argv)

    cw = ConfigWidget()

    sys.exit(app.exec_())


if __name__ == "__main__":
    main()
