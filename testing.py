import sys
import time

import numpy as np

from matplotlib.backends.qt_compat import QtWidgets
from matplotlib.backends.backend_qtagg import (
    FigureCanvas, NavigationToolbar2QT as NavigationToolbar)
from matplotlib.figure import Figure



class _Widget(QtWidgets.QWidget):
    def __init__(self):
        super(_Widget, self).__init__()
        layout = QtWidgets.QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)

        fig_room = Figure(figsize=(5, 3))
        canvas = FigureCanvas(fig_room)
        toolbar = NavigationToolbar(canvas, self)

        layout.addWidget(toolbar)
        layout.addWidget(canvas)

        self._dynamic_ax = canvas.figure.subplots()
        t = np.linspace(0, 10, 101)
        self._line, = self._dynamic_ax.plot(t, np.sin(t + time.time()))

    """"
    def _update_canvas(self):
        t = np.linspace(0, 10, 101)
        # Shift the sinusoid as a function of time.
        self._line.set_data(t, np.sin(t + time.time()))
        self._line.figure.canvas.draw()
    """""


class CanvasWidget(QtWidgets.QWidget):
    def __init__(self):
        super(CanvasWidget, self).__init__()
        self.layout = QtWidgets.QVBoxLayout(self)
        self.layout.setContentsMargins(0, 0, 0, 0)
        self.canvas = _Widget()
        self.layout.addWidget(self.canvas)

    def update(self):
        self.layout.removeWidget(self.canvas)
        self.canvas = _Widget()
        self.layout.addWidget(self.canvas)


class ApplicationWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        self.canvas = CanvasWidget()
        self.button = QtWidgets.QPushButton("UPDATE")
        self.lay = QtWidgets.QVBoxLayout()
        self.lay.setContentsMargins(0, 0, 0, 0)
        self.lay.addWidget(self.canvas)
        self.lay.addWidget(self.button)
        self.button.clicked.connect(self.update_)
        w = QtWidgets.QWidget()
        w.setLayout(self.lay)
        self.setCentralWidget(w)

    def update_(self):
        self.canvas.update()


if __name__ == "__main__":
    # Check whether there is already a running QApplication (e.g., if running
    # from an IDE).
    qapp = QtWidgets.QApplication.instance()
    if not qapp:
        qapp = QtWidgets.QApplication(sys.argv)

    app = ApplicationWindow()
    app.show()
    app.activateWindow()
    app.raise_()
    qapp.exec()

