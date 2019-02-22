#!/usr/bin/python3
# -*- coding: utf-8 -*-
import os
import sys
from PyQt5 import QtWidgets, uic, QtCore


class MainWindow(QtWidgets.QMainWindow):
    update_view_state_changed = QtCore.pyqtSignal(int)

    def __init__(self, *args, **kwargs):
        super(QtWidgets.QMainWindow, self).__init__(*args, **kwargs)
        uic.loadUi(
            os.path.join(os.path.split(__file__)[0], "main.ui"),
            self)

        self.resize(
            QtWidgets.QDesktopWidget().availableGeometry().size() * 0.75)
        self.move(
            QtWidgets.QDesktopWidget().availableGeometry().center() -
            self.rect().center())

    @QtCore.pyqtSlot(bool)
    def on_actionOpen_triggered(self, checked):
        self.graph_view.open_files()

    # decorator or exist 2 times
    @QtCore.pyqtSlot(bool)
    def on_actionExit_triggered(self, checked):
        self.close()

    def closeEvent(self, event):
        reply = QtWidgets.QMessageBox.question(
            self,
            'Message',
            "Are you sure to quit?",
            QtWidgets.QMessageBox.Yes, QtWidgets.QMessageBox.No)

        if reply == QtWidgets.QMessageBox.Yes:
            event.accept()
        else:
            event.ignore()


def main():
    app = QtWidgets.QApplication(sys.argv)
    w = MainWindow()
    w.show()
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()
