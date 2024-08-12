import numpy as np
from PyQt5.QtCore import QTimer
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure


class RealTimePlot(FigureCanvas):
    def __init__(self, parent=None, title=""):
        fig = Figure(figsize=(4, 1))  # Adjust figure size
        self.ax = fig.add_subplot(111)
        super(RealTimePlot, self).__init__(fig)
        self.data = np.random.rand(100)
        self.title = title
        self.ax.set_title(self.title, fontsize=8)
        self.ax.set_xlabel("Time", fontsize=8)
        self.ax.set_ylabel("Value", fontsize=8)
        self.ax.set_ylim(0, 1.5)
        self.ax.set_yticks([0.5, 1.0, 1.5])
        self.ax.grid(True)  # Add grid

        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_plot)
        self.timer.start(100)

    def update_plot(self):
        self.data = np.roll(self.data, -1)
        self.data[-1] = np.random.rand()
        self.ax.clear()
        self.ax.plot(self.data, 'b-')
        self.ax.set_title(self.title, fontsize=8)
        self.ax.set_xlabel("Time", fontsize=8)
        self.ax.set_ylabel("Value", fontsize=8)
        self.ax.set_ylim(0, 1.5)
        self.ax.set_yticks([0.5, 1.0, 1.5])
        self.ax.grid(True)
        self.draw()