#!/usr/bin/python3
# -*- coding: utf-8 -*-
import os
import sys
from PyQt5 import QtWidgets, uic, QtCore
from path_to_path.read_file_dialog import read_file_dialog as dialog


class GraphView(QtWidgets.QWidget):

    def __init__(self, *args, **kwargs):
        super(QtWidgets.QWidget, self).__init__(*args, **kwargs)
        uic.loadUi(
            os.path.join(os.path.split(__file__)[0], "graph_view.ui"),
            self)

        self.dialog = dialog.ReadFileDialog()

        self.desc = {'Name': None,
                     'Message': None,
                     'System': None,
                     'Points': {
                         'A': {
                             'X': 0.0,
                             'Y': 0.0,
                             'Z': 0.0},
                         'B': {
                             'X': 0.0,
                             'Y': 0.0,
                             'Z': 0.0}}
                     }

        self.guis = [self.dialog.file_widget_1,
                     self.dialog.file_widget_2,
                     self.dialog.file_widget_3,
                     self.dialog.file_widget_4,
                     self.dialog.file_widget_5
                     ]

        self.items_desc = []

    def open_files(self):
        if QtWidgets.QDialog.Accepted == self.dialog.exec_():

            for idx, val in enumerate(self.settings):
                val['file_num'] = idx
                print('fname = ', val['widget'].fname)
                val['desc']['Name'] = val['widget'].fname
                print('')
            # self.dialog.file_widget_1.fname

            # self.dialog.file_widget_1.doubleSpinBox_Ax
            # self.dialog.file_widget_1.doubleSpinBox_Ay
            # self.dialog.file_widget_1.doubleSpinBox_Az

            # self.dialog.file_widget_1.doubleSpinBox_Bx
            # self.dialog.file_widget_1.doubleSpinBox_By
            # self.dialog.file_widget_1.doubleSpinBox_Bz

            # self.dialog.file_widget_1.comboBox_calc
        print(self.settings)

def main():
    app = QtWidgets.QApplication(sys.argv)
    w = GraphView()
    w.show()
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()
