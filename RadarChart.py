import numpy as np
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure


import random


class RadarChart(FigureCanvas):
    def __init__(self, parent=None):
        fig = Figure(figsize=(3, 3))  # Adjust size
        self.ax = fig.add_subplot(111, projection="polar")
        super(RadarChart, self).__init__(fig)

        # Data for the radar chart
        categories = ["Peak Value", "Valley Time", "Baseline", "Recovery Time (s)", "AUC"]
        values = [random.randint(50, 100) for _ in range(len(categories))]

        # Customize the radar chart
        angles = np.linspace(0, 2 * np.pi, len(categories), endpoint=False)
        values = np.concatenate((values, [values[0]]))
        angles = np.concatenate((angles, [angles[0]]))

        self.ax.plot(angles, values, 'b-')
        self.ax.fill(angles, values, 'b', alpha=0.25)

        # Set the theta grid with the correct number of labels
        self.ax.set_thetagrids(angles[:-1] * 180 / np.pi, categories)

        self.ax.set_rlabel_position(90)
        self.ax.set_rticks([25, 50, 75, 100])  # Customize radial ticks
        self.ax.set_title("Radar Plot", fontsize=10)
        self.draw()