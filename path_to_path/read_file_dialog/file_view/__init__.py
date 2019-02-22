#!/usr/bin/python3
# -*- coding: utf-8 -*-
import os
import sys
from PyQt5 import QtWidgets, uic, QtCore


class FileView(QtWidgets.QWidget):

    def __init__(self, *args, **kwargs):
        super(QtWidgets.QWidget, self).__init__(*args, **kwargs)
        uic.loadUi(
            os.path.join(os.path.split(__file__)[0], "file_widget.ui"),
            self)

        self.fname = ''

        self.doubleSpinBox_Ax.setValue(1.0)
        self.doubleSpinBox_Ay.setValue(2.0)
        self.doubleSpinBox_Az.setValue(3.0)

        self.doubleSpinBox_Bx.setValue(1.0)
        self.doubleSpinBox_By.setValue(2.0)
        self.doubleSpinBox_Bz.setValue(3.0)

    @QtCore.pyqtSlot(bool)
    def on_pushButton_clicked(self, checked):
        self.fname = QtWidgets.QFileDialog.getOpenFileName(
            self, 'Open file', '/home')[0]
        self.lineEdit.insert(self.fname)


def main():
    app = QtWidgets.QApplication(sys.argv)
    w = FileView()
    w.show()
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()
