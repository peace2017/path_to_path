import os
import sys
from PyQt5 import QtWidgets, uic, QtCore


class ReadFileDialog(QtWidgets.QDialog):
    def __init__(self):
        super(QtWidgets.QDialog, self).__init__()
        uic.loadUi(os.path.join(os.path.split(__file__)
                                [0], "read_file_dialog.ui"), self)

        self.move(QtWidgets.QDesktopWidget().availableGeometry().center() -
                  self.rect().center())


def main():
    app = QtWidgets.QApplication(sys.argv)
    w = ReadFileDialog()
    w.show()
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()
