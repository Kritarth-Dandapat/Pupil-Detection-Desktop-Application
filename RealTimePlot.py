import numpy as np
from PyQt5.QtCore import QTimer
from PyQt5.QtWidgets import QSizePolicy
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure

class RealTimePlot(FigureCanvas):
    def __init__(self, parent=None, title="", min_height=150):
        fig = Figure(figsize=(4, 2))  # Adjust figure size
        self.ax = fig.add_subplot(111)
        super(RealTimePlot, self).__init__(fig)
        self.data = np.random.rand(100)

        # Set title as y-axis label
        self.title = title
        self.ax.set_xlabel("Time", fontsize=8)
        self.ax.set_ylabel(self.title, fontsize=8)  # Title on y-axis
        self.ax.set_ylim(0, 1.5)
        self.ax.set_yticks([0.5, 1.0, 1.5])
        self.ax.grid(True)  # Add grid

        # Set minimum height
        self.setMinimumHeight(min_height)
        self.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.MinimumExpanding)

        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_plot)
        self.timer.start(100)

    def update_plot(self):
        self.data = np.roll(self.data, -1)
        self.data[-1] = np.random.rand()
        self.ax.clear()
        self.ax.plot(self.data, 'b-')
        self.ax.set_xlabel("Time", fontsize=8)
        self.ax.set_ylabel(self.title, fontsize=8)  # Title on y-axis
        self.ax.set_ylim(0, 1.5)
        self.ax.set_yticks([0.5, 1.0, 1.5])
        self.ax.grid(True)
        self.draw()
