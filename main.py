import sys
import os
from PyQt5.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QHBoxLayout, QGridLayout, QLabel,
    QScrollArea, QPushButton, QCheckBox, QComboBox, QFrame,
    QRadioButton, QButtonGroup, QSpinBox
)
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPalette, QColor, QPixmap

from BarChart import BarChart
from RadarChart import RadarChart
from RealTimePlot import RealTimePlot

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

        # Middle section
        middle_layout = QHBoxLayout()
        self.create_middle_section(middle_layout)
        self.scroll_layout.addLayout(middle_layout)

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
        pupil_image.setFixedSize(300, 200)
        image_path = "/Users/kritarth/code/PYQT5 Project/src/images/pupil-image.jpg"
        if os.path.exists(image_path):
            pixmap = QPixmap(image_path)
            pupil_image.setPixmap(pixmap.scaled(300, 200, Qt.KeepAspectRatio))
        else:
            pupil_image.setStyleSheet("background-color: lightgray; border: 1px solid black;")
            pupil_image.setText("Pupil Image Not Found")
            pupil_image.setAlignment(Qt.AlignCenter)
        pupil_layout.addWidget(pupil_image)
        layout.addLayout(pupil_layout)

        # Center: Two Tables with Random Data
        table_layout = QHBoxLayout()
        for i in range(2):
            table_content = "\n".join([f"Header {chr(65+i)}\nCell text {chr(65+i)}{j+1}" for j in range(3)])
            table = QLabel(table_content)
            table.setFixedSize(200, 100)
            table.setStyleSheet("background-color: white; border: 1px solid black; padding: 5px;")
            table_layout.addWidget(table)
        layout.addLayout(table_layout)

        # Right: Radar Chart
        radar_layout = QVBoxLayout()
        radar_layout.addWidget(RadarChart())
        layout.addLayout(radar_layout)

    def create_middle_section(self, layout):
        # Real-time plots (Pupil, Camera FPS, Model Confidence)
        real_time_plots_layout = QVBoxLayout()
        real_time_plots_layout.addWidget(RealTimePlot(title="Pupil"))
        real_time_plots_layout.addWidget(RealTimePlot(title="Camera FPS"))
        real_time_plots_layout.addWidget(RealTimePlot(title="Model Confidence"))
        layout.addLayout(real_time_plots_layout)

    def create_bottom_section(self, layout):
        # Left: Sound test controls
        controls_layout = QVBoxLayout()

        # Test Buttons
        self.dynamic_range_test_btn = QPushButton("Dynamic Range Test: OFF")
        self.loud_range_test_btn = QPushButton("Loud Range Test: OFF")
        self.digit_in_noise_test_btn = QPushButton("Digit in Noise Test: OFF")
        
        self.dynamic_range_test_btn.setStyleSheet("background-color: gray; color: white; padding: 10px 20px; border: none;")
        self.loud_range_test_btn.setStyleSheet("background-color: gray; color: white; padding: 10px 20px; border: none;")
        self.digit_in_noise_test_btn.setStyleSheet("background-color: gray; color: white; padding: 10px 20px; border: none;")
        
        self.dynamic_range_test_btn.clicked.connect(self.toggle_dynamic_range_test)
        self.loud_range_test_btn.clicked.connect(self.toggle_loud_range_test)
        self.digit_in_noise_test_btn.clicked.connect(self.toggle_digit_in_noise_test)
        
        controls_layout.addWidget(self.dynamic_range_test_btn)
        controls_layout.addWidget(self.loud_range_test_btn)
        controls_layout.addWidget(self.digit_in_noise_test_btn)

        # Repetitive Count and Baseline Time
        self.repetitive_count_spinbox = QSpinBox()
        self.repetitive_count_spinbox.setRange(1, 100)
        self.repetitive_count_spinbox.setValue(1)
        self.repetitive_count_spinbox.setPrefix("Repetitive Count: ")
        
        self.baseline_time_spinbox = QSpinBox()
        self.baseline_time_spinbox.setRange(1, 60)
        self.baseline_time_spinbox.setValue(1)
        self.baseline_time_spinbox.setPrefix("Baseline Time (s): ")
        
        controls_layout.addWidget(self.repetitive_count_spinbox)
        controls_layout.addWidget(self.baseline_time_spinbox)

        # Sound-related checkboxes
        self.sound_options_layout = QVBoxLayout()
        self.sound_checkbox_1 = QCheckBox("Sound Option 1")
        self.sound_checkbox_2 = QCheckBox("Sound Option 2")
        self.sound_checkbox_3 = QCheckBox("Sound Option 3")
        
        self.sound_options_layout.addWidget(self.sound_checkbox_1)
        self.sound_options_layout.addWidget(self.sound_checkbox_2)
        self.sound_options_layout.addWidget(self.sound_checkbox_3)
        
        controls_layout.addLayout(self.sound_options_layout)

        layout.addLayout(controls_layout)

        # Right: Bar chart
        chart_layout = QVBoxLayout()
        chart_layout.addWidget(BarChart())
        layout.addLayout(chart_layout)

    def toggle_dynamic_range_test(self):
        self.toggle_test(self.dynamic_range_test_btn, "Dynamic Range Test")

    def toggle_loud_range_test(self):
        self.toggle_test(self.loud_range_test_btn, "Loud Range Test")

    def toggle_digit_in_noise_test(self):
        self.toggle_test(self.digit_in_noise_test_btn, "Digit in Noise Test")

    def toggle_test(self, button, test_name):
        if button.text().endswith("OFF"):
            button.setText(f"{test_name}: ON")
            button.setStyleSheet("background-color: green; color: white; padding: 10px 20px; border: none;")
        else:
            button.setText(f"{test_name}: OFF")
            button.setStyleSheet("background-color: gray; color: white; padding: 10px 20px; border: none;")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = ApplicationWindow()
    window.show()
    sys.exit(app.exec_())
