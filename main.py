import sys
import numpy as np
import random
from PyQt5.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QHBoxLayout, QGridLayout, QLabel,
    QScrollArea, QPushButton, QCheckBox, QComboBox, QLineEdit, QFrame,
    QRadioButton, QButtonGroup
)
from PyQt5.QtCore import Qt, QTimer
from PyQt5.QtGui import QPalette, QColor
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
from matplotlib import pyplot as plt

class RealTimePlot(FigureCanvas):
    def __init__(self, parent=None, title=""):
        fig = Figure(figsize=(5, 2))  # Set figure size
        self.ax = fig.add_subplot(111)
        super(RealTimePlot, self).__init__(fig)
        self.data = np.random.rand(100)
        self.title = title
        self.ax.set_title(self.title)
        self.ax.set_xlabel("Time")
        self.ax.set_ylabel("Value")
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
        self.ax.set_title(self.title)
        self.ax.set_xlabel("Time")
        self.ax.set_ylabel("Value")
        self.ax.set_ylim(0, 1.5)
        self.ax.set_yticks([0.5, 1.0, 1.5])
        self.ax.grid(True)
        self.draw()

class RadarChart(FigureCanvas):
    def __init__(self, parent=None):
        fig = Figure(figsize=(4, 4))
        self.ax = fig.add_subplot(111, projection="polar")
        super(RadarChart, self).__init__(fig)

        # Data for the radar chart
        categories = ["Peak Value", "Valley Time", "Baseline", "Recovery Time (s)", "AUC"]
        values = [random.randint(50, 100) for _ in range(len(categories))]

        # Customize the radar chart
        angles = np.linspace(0, 2 * np.pi, len(categories), endpoint=False)
        angles = np.concatenate((angles, [angles[0]]))
        values = np.concatenate((values, [values[0]]))
        self.ax.plot(angles, values, 'b-')
        self.ax.fill(angles, values, 'b', alpha=0.25)

        self.ax.set_thetagrids(angles * 180 / np.pi, categories)
        self.ax.set_rlabel_position(90)
        self.ax.set_rticks([25, 50, 75, 100])  # Customize radial ticks
        self.ax.set_title("Radar Plot")
        self.draw()

class BarChart(FigureCanvas):
    def __init__(self, parent=None, data=None):
        fig = Figure(figsize=(5, 2))  # Set figure size
        self.ax = fig.add_subplot(111)
        super(BarChart, self).__init__(fig)
        if data is None:
            data = [random.randint(1, 10) for _ in range(4)]
        self.ax.barh(["Disease 1", "Disease 2", "Disease 3", "Disease 4"], data, color='blue')
        self.ax.set_title("Disease Bar Chart")
        self.ax.set_xlabel("Value")
        self.ax.set_xlim(0, 12)  # Set x-axis limit
        self.ax.grid(True, axis='x')  # Add x-axis grid
        self.draw()

class ApplicationWindow(QWidget):
    def __init__(self):
        super().__init__()

        # Main layout
        self.setWindowTitle("Mockup UI")
        self.setGeometry(100, 100, 1200, 800)
        self.main_layout = QVBoxLayout()
        self.scroll_area = QScrollArea()
        self.scroll_area.setWidgetResizable(True)
        self.scroll_widget = QWidget()
        self.scroll_layout = QVBoxLayout(self.scroll_widget)
        self.scroll_area.setWidget(self.scroll_widget)

        self.main_layout.addWidget(self.scroll_area)
        self.setLayout(self.main_layout)

        # Theme selection
        self.create_theme_toggle()

        # Top section
        top_layout = QHBoxLayout()
        self.create_top_section(top_layout)
        self.scroll_layout.addLayout(top_layout)

        # Bottom section
        bottom_layout = QHBoxLayout()
        self.create_bottom_section(bottom_layout)
        self.scroll_layout.addLayout(bottom_layout)

    def create_theme_toggle(self):
        theme_layout = QHBoxLayout()
        light_theme_button = QRadioButton("Light Theme")
        dark_theme_button = QRadioButton("Dark Theme")
        light_theme_button.setChecked(True)
        light_theme_button.toggled.connect(lambda: self.apply_theme("light"))
        dark_theme_button.toggled.connect(lambda: self.apply_theme("dark"))
        theme_layout.addWidget(light_theme_button)
        theme_layout.addWidget(dark_theme_button)
        self.scroll_layout.addLayout(theme_layout)

    def apply_theme(self, theme):
        palette = QPalette()
        if theme == "light":
            palette.setColor(QPalette.Window, QColor(255, 255, 255))
            palette.setColor(QPalette.WindowText, QColor(0, 0, 0))
            palette.setColor(QPalette.Base, QColor(245, 245, 245))
        else:
            palette.setColor(QPalette.Window, QColor(53, 53, 53))
            palette.setColor(QPalette.WindowText, QColor(255, 255, 255))
            palette.setColor(QPalette.Base, QColor(25, 25, 25))
        self.setPalette(palette)

    def create_top_section(self, layout):
        # Left: Pupil Image (Placeholder)
        pupil_layout = QVBoxLayout()
        pupil_image = QLabel()
        pupil_image.setFixedSize(300, 300)
        pupil_image.setStyleSheet("background-image: url(pupil_image.jpg); background-repeat: no-repeat; background-position: center;")  # Replace with actual image
        pupil_layout.addWidget(pupil_image)
        layout.addLayout(pupil_layout)

        # Right: Real-time plots, radar plot, and tables
        right_layout = QVBoxLayout()
        plot_layout = QGridLayout()
        plot_layout.addWidget(RealTimePlot(title="Camera FPS"), 0, 0)
        plot_layout.addWidget(RealTimePlot(title="Model Confidence"), 1, 0)
        plot_layout.addWidget(RealTimePlot(title="Pupil Size"), 2, 0)
        right_layout.addLayout(plot_layout)

        radar_layout = QHBoxLayout()
        radar_layout.addWidget(RadarChart())
        right_layout.addLayout(radar_layout)

        # Additional tables
        table_layout = QHBoxLayout()
        table_1 = QLabel("Table 1")
        table_1.setFixedSize(200, 100)
        table_1.setStyleSheet("background-color: white; border: 1px solid black;")
        table_2 = QLabel("Table 2")
        table_2.setFixedSize(200, 100)
        table_2.setStyleSheet("background-color: white; border: 1px solid black;")
        table_layout.addWidget(table_1)
        table_layout.addWidget(table_2)
        right_layout.addLayout(table_layout)

        layout.addLayout(right_layout)

    def create_bottom_section(self, layout):
        # Left: Control buttons and checkboxes
        controls_layout = QVBoxLayout()
        button_labels = [
            "Check Camera", "Confirm Camera Setting", "Start Recording", "Stop Recording"
        ]
        for label in button_labels:
            button = QPushButton(label)
            button.setStyleSheet("background-color: blue; color: white; padding: 10px 20px; border: none;")
            controls_layout.addWidget(button)

        # Checkboxes
        checkbox_layout = QVBoxLayout()
        for label in ["Dynamic range test", "Loud range test", "Digit-in-noise test"]:
            checkbox = QCheckBox(label)
            checkbox_layout.addWidget(checkbox)
        controls_layout.addLayout(checkbox_layout)

        layout.addLayout(controls_layout)

        # Right: Sound selection and Disease Bars
        right_layout = QVBoxLayout()
        # Sound Selection
        sound_layout = QGridLayout()
        sound_layout.addWidget(QLabel("Select Sound"), 0, 0)
        for i in range(10):
            checkbox = QCheckBox()
            dropdown = QComboBox()
            dropdown.addItems(["1k 10dB.wav", "1k 5dB.wav", "1k 0dB.wav"])
            sound_layout.addWidget(checkbox, i + 1, 0)
            sound_layout.addWidget(dropdown, i + 1, 1)
        right_layout.addLayout(sound_layout)

        # Disease Bar Chart
        bar_chart_layout = QHBoxLayout()
        bar_chart = BarChart()
        bar_chart_layout.addWidget(bar_chart)
        right_layout.addLayout(bar_chart_layout)

        # Generate Report Button
        generate_report_button = QPushButton("Generate Report")
        generate_report_button.setStyleSheet("background-color: blue; color: white; padding: 10px 20px; border: none;")
        right_layout.addWidget(generate_report_button)

        layout.addLayout(right_layout)

def main():
    app = QApplication(sys.argv)
    window = ApplicationWindow()
    window.showMaximized()  # Window will maximize to fit any screen size
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()