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

        self.lineEdit.setText('/media/smironenko/423661C53661BA95/TOPCON/Research/AGI-2/Report/2019_01_08_egnos_kinematic/AGI_0/1_agi0_egnos.gga')
        self.lineEdit_2.setText('File 1')
        self.lineEdit_Ax.setText('44,9198160966666667')
        self.lineEdit_Ay.setText('11,007728795')
        self.lineEdit_Az.setText('58,0493')
        self.lineEdit_Bx.setText('44,920421265')
        self.lineEdit_By.setText('11,0081744883333333')
        self.lineEdit_Bz.setText('58,2422')

    @QtCore.pyqtSlot(bool)
    def on_pushButton_clicked(self, checked):
        self.fname = QtWidgets.QFileDialog.getOpenFileName(
            self, 'Open file', '/home')[0]
        self.lineEdit.insert(self.fname)

    @QtCore.pyqtSlot(bool)
    def on_checkBox_clicked(self, checked):
        print('checkbox')


def main():
    app = QtWidgets.QApplication(sys.argv)
    w = FileView()
    w.show()
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()
