from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure


import random


class BarChart(FigureCanvas):
    def __init__(self, parent=None, data=None):
        fig = Figure(figsize=(3, 2))  # Adjust size
        self.ax = fig.add_subplot(111)
        super(BarChart, self).__init__(fig)
        if data is None:
            data = [random.randint(1, 10) for _ in range(4)]
        self.ax.barh(["Disease 1", "Disease 2", "Disease 3", "Disease 4"], data, color='blue')
        self.ax.set_title("Disease Bar Chart", fontsize=8)
        self.ax.set_xlabel("Value", fontsize=8)
        self.ax.set_xlim(0, 12)  # Set x-axis limit
        self.ax.grid(True, axis='x')  # Add x-axis grid
        self.draw()