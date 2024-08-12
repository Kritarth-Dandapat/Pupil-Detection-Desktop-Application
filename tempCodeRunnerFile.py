import sys
from PyQt5.QtWidgets import (
    QApplication, QLabel, QMainWindow, QTableWidget, QTableWidgetItem, QVBoxLayout, QWidget,
    QPushButton, QComboBox, QCheckBox, QSpinBox, QHBoxLayout, QScrollArea, QGridLayout
)
from PyQt5.QtGui import QColor, QPalette
from PyQt5.QtCore import Qt
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
import numpy as np


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Pupil Detection")
        self.setGeometry(100, 100, 1200, 600)
        self.setMinimumSize(800, 600)


        # Initialize with light theme
        self.is_dark_theme = False

        scroll = QScrollArea()
        central_widget = QWidget()
        scroll.setWidget(central_widget)
        scroll.setWidgetResizable(True)
        self.setCentralWidget(scroll)

        layout = QVBoxLayout(central_widget)

        # Top layout
        top_layout = QHBoxLayout()

        # Theme Toggle Button
        self.theme_toggle_button = QPushButton("Switch to Dark Theme")
        self.theme_toggle_button.clicked.connect(self.toggle_theme)
        layout.addWidget(self.theme_toggle_button)
        
        # Image label
        self.image_label = QLabel("Pupil Image Here")
        self.image_label.setFixedSize(320, 240)
        top_layout.addWidget(self.image_label)

        # Tables layout
        tables_layout = QVBoxLayout()

        # Table A
        self.table_a = QTableWidget(5, 3)
        self.table_a.setHorizontalHeaderLabels(['Header A', 'Header B', 'Header C'])
        for i in range(5):
            for j in range(3):
                self.table_a.setItem(i, j, QTableWidgetItem(f"Cell text {chr(65+i)}{j+1}"))
        tables_layout.addWidget(self.table_a)

        # Table B
        self.table_b = QTableWidget(5, 2)
        self.table_b.setHorizontalHeaderLabels(['Header A', 'Header B'])
        for i in range(5):
            for j in range(2):
                self.table_b.setItem(i, j, QTableWidgetItem(f"Cell text {chr(65+i)}{j+1}"))
        tables_layout.addWidget(self.table_b)

        top_layout.addLayout(tables_layout)

        # Radar chart
        self.radar_canvas = FigureCanvas(Figure(figsize=(4, 3)))
        radar_ax = self.radar_canvas.figure.add_subplot(111, polar=True)
        theta = np.linspace(0, 2 * np.pi, 5)
        values = np.random.rand(5)
        radar_ax.plot(theta, values)
        radar_ax.fill(theta, values, 'b', alpha=0.3)
        top_layout.addWidget(self.radar_canvas)

        layout.addLayout(top_layout)

        

        # Apply the initial theme
        self.set_theme()

        # Graphs and Controls layout
        graphs_and_controls_layout = QHBoxLayout()

        # Graphs layout
        graphs_layout = QVBoxLayout()
        for _ in range(3):
            graph_canvas = FigureCanvas(Figure(figsize=(3, 2)))
            ax = graph_canvas.figure.add_subplot(111)
            t = np.arange(0.0, 2.0, 0.01)
            s = np.sin(2 * np.pi * t)
            ax.plot(t, s)
            graphs_layout.addWidget(graph_canvas)
        graphs_and_controls_layout.addLayout(graphs_layout)

        # Controls layout
        controls_layout = QVBoxLayout()

        # Buttons
        self.check_camera_button = QPushButton("Check Camera")
        self.confirm_camera_button = QPushButton("Confirm Camera Setting")
        self.start_recording_button = QPushButton("Start Recording")
        self.stop_recording_button = QPushButton("Stop Recording")
        controls_layout.addWidget(self.check_camera_button)
        controls_layout.addWidget(self.confirm_camera_button)
        controls_layout.addWidget(self.start_recording_button)
        controls_layout.addWidget(self.stop_recording_button)

        # Checkboxes and SpinBox
        self.dynamic_range_test = QCheckBox("Dynamic range test")
        self.loud_range_test = QCheckBox("Loud range test")
        self.digit_in_noise_test = QCheckBox("Digit-in-noise test")
        controls_layout.addWidget(self.dynamic_range_test)
        controls_layout.addWidget(self.loud_range_test)
        controls_layout.addWidget(self.digit_in_noise_test)

        self.repetition_count = QSpinBox()
        self.repetition_count.setValue(1)
        controls_layout.addWidget(QLabel("Repetition Count:"))
        controls_layout.addWidget(self.repetition_count)

        self.baseline_time = QSpinBox()
        self.baseline_time.setValue(5)
        controls_layout.addWidget(QLabel("Baseline Time:"))
        controls_layout.addWidget(self.baseline_time)

        # Sound selection with checkboxes
        sound_grid = QGridLayout()
        for i in range(8):
            checkbox = QCheckBox(f"Sound {i+1}")
            combo = QComboBox()
            combo.addItems([f"10dB.wav", f"20dB.wav", f"30dB.wav"])
            sound_grid.addWidget(checkbox, i, 0)
            sound_grid.addWidget(combo, i, 1)
        controls_layout.addLayout(sound_grid)

        graphs_and_controls_layout.addLayout(controls_layout)

        layout.addLayout(graphs_and_controls_layout)

        # Disease report layout
        disease_report_layout = QHBoxLayout()

        # Generate Report button
        self.generate_report_button = QPushButton("Generate Report")
        disease_report_layout.addWidget(self.generate_report_button)

        # Disease bar chart
        self.disease_canvas = FigureCanvas(Figure(figsize=(7, 1)))
        disease_ax = self.disease_canvas.figure.add_subplot(111)
        self.disease_canvas.setFixedSize(650, 200)
        disease_data = [1, 2, 3, 4]
        disease_ax.barh([f"Disease {i+1}" for i in range(4)], disease_data, color='#5B9BD5')
        disease_report_layout.addWidget(self.disease_canvas)


        layout.addLayout(disease_report_layout)

    def set_theme(self):
        palette = self.palette()
        if self.is_dark_theme:
            # Dark theme
            palette.setColor(QPalette.Window, QColor(53, 53, 53))
            palette.setColor(QPalette.WindowText, QColor(255, 255, 255))
            palette.setColor(QPalette.Base, QColor(25, 25, 25))
            palette.setColor(QPalette.AlternateBase, QColor(53, 53, 53))
            palette.setColor(QPalette.ToolTipBase, QColor(255, 255, 255))
            palette.setColor(QPalette.ToolTipText, QColor(255, 255, 255))
            palette.setColor(QPalette.Text, QColor(255, 255, 255))
            palette.setColor(QPalette.Button, QColor(53, 53, 53))
            palette.setColor(QPalette.ButtonText, QColor(255, 255, 255))
            palette.setColor(QPalette.BrightText, QColor(255, 0, 0))
            palette.setColor(QPalette.Highlight, QColor(142, 45, 197))
            palette.setColor(QPalette.HighlightedText, QColor(0, 0, 0))
            self.theme_toggle_button.setText("Switch to Light Theme")
        else:
            # Light theme
            palette.setColor(QPalette.Window, QColor(245, 245, 245))
            palette.setColor(QPalette.WindowText, QColor(50, 50, 50))
            palette.setColor(QPalette.Base, QColor(255, 255, 255))
            palette.setColor(QPalette.AlternateBase, QColor(240, 240, 240))
            palette.setColor(QPalette.ToolTipBase, QColor(255, 255, 255))
            palette.setColor(QPalette.ToolTipText, QColor(50, 50, 50))
            palette.setColor(QPalette.Text, QColor(50, 50, 50))
            palette.setColor(QPalette.Button, QColor(220, 220, 220))
            palette.setColor(QPalette.ButtonText, QColor(50, 50, 50))
            palette.setColor(QPalette.BrightText, QColor(255, 0, 0))
            palette.setColor(QPalette.Highlight, QColor(91, 155, 213))
            palette.setColor(QPalette.HighlightedText, QColor(255, 255, 255))
            self.theme_toggle_button.setText("Switch to Dark Theme")

        self.setPalette(palette)

    def toggle_theme(self):
        self.is_dark_theme = not self.is_dark_theme
        self.set_theme()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())
