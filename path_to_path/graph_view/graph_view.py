#!/usr/bin/python3
# -*- coding: utf-8 -*-
import os
import sys
import copy
import pyqtgraph as pg
import re
from PyQt5 import QtWidgets, uic, QtGui, QtCore
from path_to_path.read_file_dialog import read_file_dialog as dialog
from path_to_path.path_calculation import path_calculation as path_calc


pg.setConfigOption("background", "w")
pg.setConfigOption("foreground", "k")

COLOURS = [QtGui.QColor(QtCore.Qt.red),
           QtGui.QColor(QtCore.Qt.green),
           QtGui.QColor(QtCore.Qt.blue),
           QtGui.QColor(QtCore.Qt.black),
           QtGui.QColor(QtCore.Qt.magenta),
           ]


class GraphView(QtWidgets.QWidget):

    def __init__(self, *args, **kwargs):
        super(QtWidgets.QWidget, self).__init__(*args, **kwargs)
        uic.loadUi(
            os.path.join(os.path.split(__file__)[0], "graph_view.ui"),
            self)

        self.widget_xtrack.showGrid(True, True, 1)
        self.widget_xtrack.setTitle('Xtrack graphs')
        self.widget_xtrack.setLabel('left', 'Xtrack, (m)')
        self.widget_xtrack.setLabel('bottom', 'Time, (h:m:s)')

        self.widget_path_to_path.showGrid(True, True, 1)
        self.widget_path_to_path.setTitle('Path-to-path graphs')
        self.widget_path_to_path.setLabel('left', 'Path-to-path, (m)')
        self.widget_path_to_path.setLabel('bottom', 'Time, (h:m:s)')

        self.legend_xtrack = pg.LegendItem()
        self.legend_xtrack.setParentItem(
            self.widget_xtrack.graphicsItem())

        self.legend_path_to_path = pg.LegendItem()
        self.legend_path_to_path.setParentItem(
            self.widget_path_to_path.graphicsItem())

        self.names_path_to_path = []
        self.plots_path_to_path = []
        self.names_xtrack = []
        self.plots_xtrack = []

        self.dialog = dialog.ReadFileDialog()

        self.desc = {'Name': None,
                     'Short_name': None,
                     'Message': None,
                     'System': None,
                     'Path': None,
                     'Points': {
                         'A': {
                             'X_lat': 0.0,
                             'Y_lon': 0.0,
                             'Z_alt': 0.0},
                         'B': {
                             'X_lat': 0.0,
                             'Y_lon': 0.0,
                             'Z_alt': 0.0}}
                     }

        self.guis = [self.dialog.file_widget_1,
                     self.dialog.file_widget_2,
                     self.dialog.file_widget_3,
                     self.dialog.file_widget_4,
                     self.dialog.file_widget_5
                     ]

        self.items_desc = []
        self.pairs = {}

    def open_files(self):
        if self.names_xtrack or self.names_path_to_path:
            [self.legend_xtrack.removeItem(_) for _ in self.names_xtrack]
            [self.legend_path_to_path.removeItem(_)
                for _ in self.names_path_to_path]
            self.names_xtrack = []
            self.names_path_to_path = []
            self.plots_xtrack = []

            self.widget_xtrack.clear()
            self.widget_path_to_path.clear()

            self.items_desc = []

        desc = copy.deepcopy(self.desc)
        if QtWidgets.QDialog.Accepted == self.dialog.exec_():
            for idx, val in enumerate(self.guis):
                if val.lineEdit.text():
                    desc['Name'] = val.lineEdit.text()
                    desc['Short_name'] = val.lineEdit_2.text()
                    desc['Message'] = val.comboBox_calc.currentText()
                    desc['System'] = val.comboBox_system.currentText()

                    desc['Points']['A']['X_lat'] = self.str2float(
                        val.lineEdit_Ax.text())
                    desc['Points']['A']['Y_lon'] = self.str2float(
                        val.lineEdit_Ay.text())
                    desc['Points']['A']['Z_alt'] = self.str2float(
                        val.lineEdit_Az.text())

                    desc['Points']['B']['X_lat'] = self.str2float(
                        val.lineEdit_Bx.text())
                    desc['Points']['B']['Y_lon'] = self.str2float(
                        val.lineEdit_By.text())
                    desc['Points']['B']['Z_alt'] = self.str2float(
                        val.lineEdit_Bz.text())

                    self.items_desc.append(desc)
                    desc = copy.deepcopy(self.desc)

            ptp = self.path_to_path_calc(self.items_desc)

            description_xt = ""
            description_ptp = ""

            for i, p in enumerate(ptp):
                pen = pg.mkPen(color=COLOURS[i], width=1)
                y_xt = p[1].xtrack_AB
                x = [(i, t.strftime('%H:%M:%S'))
                     for i, t in enumerate(p[1].time_AB)]

                pw_xt = self.widget_xtrack
                pw_xt.setWindowTitle('Path-to-Path')
                plot_xt = pw_xt.plot(range(len(y_xt)), y_xt, pen=pen)
                pw_xt.getAxis('bottom').setTicks([x])
                ran = range(0, len(x), int(len(x) / 10))
                dx = [x[v] for v in ran]
                pw_xt.getAxis('bottom').setTicks([dx, []])

                self.legend_xtrack.addItem(plot_xt, p[0])
                self.names_xtrack.append(p[0])
                self.plots_xtrack.append(plot_xt)

                y_p2p = p[1].p2p_AB
                pw_p2p = self.widget_path_to_path
                pw_p2p.setWindowTitle('Path-to-Path')
                plot_p2p = pw_p2p.plot(range(len(y_p2p)), y_p2p, pen=pen)
                x_p2p = x[:-900]
                pw_p2p.getAxis('bottom').setTicks([x_p2p])
                ran = range(0, len(x_p2p), int(len(x_p2p) / 10))
                dx_p2p = [x_p2p[v] for v in ran]
                pw_p2p.getAxis('bottom').setTicks([dx_p2p, []])

                self.legend_path_to_path.addItem(plot_p2p, p[0])
                self.names_path_to_path.append(p[0])
                self.plots_path_to_path.append(plot_p2p)

                description_xt += str(i + 1) + ') '
                description_xt += p[0] + ':'
                description_xt += 'Number of points = '
                description_xt += str(len(p[1].xtrack_AB)) + '\n'
                description_xt += '\tXtrack statistics:' + '\n'
                description_xt += '\tMean = ' + str(p[1].xt_mean) + '\n'
                description_xt += '\tRMS x 2 = ' + str(p[1].xt_rms) + '\n\n'

                description_ptp += str(i + 1) + ') '
                description_ptp += p[0] + ':'
                description_ptp += 'Number of points = '
                description_ptp += str(len(p[1].xtrack_AB)) + '\n'
                description_ptp += '\tPath-to-path statistics:' + '\n'
                description_ptp += '\tMean = ' + str(p[1].ptp_mean) + '\n'
                description_ptp += '\tRMS x 2 = ' + str(p[1].ptp_rms) + '\n\n'

            self.plainTextEdit.setPlainText(description_xt)
            self.plainTextEdit_2.setPlainText(description_ptp)

    def path_to_path_calc(self, items):
        paths = [(_['Short_name'], path_calc.PathCalc(_)) for _ in items]
        return paths

    def str2float(self, val):
        if not re.search('[a-zA-Z]+', val):
            return float(".".join(val.split(",")))
        else:
            raise RuntimeError('XYZ should not have letters')


def main():
    app = QtWidgets.QApplication(sys.argv)
    w = GraphView()
    w.show()
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()
