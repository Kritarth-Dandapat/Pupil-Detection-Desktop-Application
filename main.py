import sys
import os
from PyQt5.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QHBoxLayout, QGridLayout, QLabel,
    QScrollArea, QPushButton, QCheckBox, QComboBox, QFrame,
    QRadioButton, QButtonGroup, QSpinBox, QSizePolicy, QTableWidget, QTableWidgetItem
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
        self.setWindowTitle("Pupil detection App")
        self.setGeometry(100, 100, 1600, 1200)
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
        
        # Create first table
        table_1 = QTableWidget()
        table_1.setRowCount(3)
        table_1.setColumnCount(2)
        table_1.setHorizontalHeaderLabels(['Header A', 'Header B'])
        table_1.setItem(0, 0, QTableWidgetItem('Data A1'))
        table_1.setItem(0, 1, QTableWidgetItem('Data B1'))
        table_1.setItem(1, 0, QTableWidgetItem('Data A2'))
        table_1.setItem(1, 1, QTableWidgetItem('Data B2'))
        table_1.setItem(2, 0, QTableWidgetItem('Data A3'))
        table_1.setItem(2, 1, QTableWidgetItem('Data B3'))
        
        # Create second table
        table_2 = QTableWidget()
        table_2.setRowCount(3)
        table_2.setColumnCount(2)
        table_2.setHorizontalHeaderLabels(['Header C', 'Header D'])
        table_2.setItem(0, 0, QTableWidgetItem('Data C1'))
        table_2.setItem(0, 1, QTableWidgetItem('Data D1'))
        table_2.setItem(1, 0, QTableWidgetItem('Data C2'))
        table_2.setItem(1, 1, QTableWidgetItem('Data D2'))
        table_2.setItem(2, 0, QTableWidgetItem('Data C3'))
        table_2.setItem(2, 1, QTableWidgetItem('Data D3'))

        # Add tables to the layout
        table_layout.addWidget(table_1)
        table_layout.addWidget(table_2)
        
        layout.addLayout(table_layout)
        self.setLayout(layout)

        # Right: Radar Chart
        radar_layout = QVBoxLayout()
        radar_layout.addWidget(RadarChart())
        layout.addLayout(radar_layout)

    def create_middle_section(self, layout):
        # Real-time plots (Pupil, Camera FPS, Model Confidence)
        real_time_plots_layout = QVBoxLayout()

        # Existing RealTimePlot widgets with visible titles
        pupil_plot = RealTimePlot(title="Pupil")
        fps_plot = RealTimePlot(title="Camera FPS")
        confidence_plot = RealTimePlot(title="Model Confidence")

        # Set size policy to control how the plots expand
        pupil_plot.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        fps_plot.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        confidence_plot.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)

        # Add the plots to the vertical layout
        real_time_plots_layout.addWidget(pupil_plot)
        real_time_plots_layout.addWidget(fps_plot)
        real_time_plots_layout.addWidget(confidence_plot)

        # Set stretch factors to adjust the relative size of each plot
        real_time_plots_layout.setStretch(0, 1)  # Pupil plot
        real_time_plots_layout.setStretch(1, 1)  # Camera FPS plot
        real_time_plots_layout.setStretch(2, 1)  # Model Confidence plot

        # New layout for additional RealTimePlot and button
        additional_plot_layout = QVBoxLayout()
        additional_plot = RealTimePlot(title="Additional Plot")  # New RealTimePlot widget
        additional_plot.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)

        generate_report_button = QPushButton("Generate Report")  # New button

        additional_plot_layout.addWidget(additional_plot)
        additional_plot_layout.addWidget(generate_report_button)

        # Add the additional layout to the right side of the middle section
        right_layout = QHBoxLayout()
        right_layout.addLayout(real_time_plots_layout)
        right_layout.addLayout(additional_plot_layout)

        # Set the stretch factors to control the width of each section
        right_layout.setStretch(0, 2)  # Left section (Real-time plots)
        right_layout.setStretch(1, 1)  # Right section (Additional plot and button)

        layout.addLayout(right_layout)






    def create_bottom_section(self, layout):
        # Set a maximum height for the bottom section to 1/3 of the viewable page height
        bottom_section_max_height = int(self.height() / 3)

        bottom_section_widget = QWidget()
        bottom_section_layout = QHBoxLayout(bottom_section_widget)
        bottom_section_widget.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Preferred)
        bottom_section_widget.setMaximumHeight(bottom_section_max_height)

        # Top Buttons
        top_buttons_layout = QVBoxLayout()
        self.check_camera_button = QPushButton("Check Camera")
        self.confirm_camera_button = QPushButton("Confirm Camera Setting")
        self.start_recording_button = QPushButton("Start Recording")
        self.stop_recording_button = QPushButton("Stop Recording")
        top_buttons_layout.addWidget(self.check_camera_button)
        top_buttons_layout.addWidget(self.confirm_camera_button)
        top_buttons_layout.addWidget(self.start_recording_button)
        top_buttons_layout.addWidget(self.stop_recording_button)


        # Checkboxes and Spinboxes
        controls_layout = QVBoxLayout()
        self.dynamic_range_test_btn = QCheckBox("Dynamic Range Test")
        self.loud_range_test_btn = QCheckBox("Loud Range Test")
        self.digit_in_noise_test_btn = QCheckBox("Digit in Noise Test")


        text_button_layout = QVBoxLayout()
        text_button_layout.addWidget(self.dynamic_range_test_btn)
        text_button_layout.addWidget(self.loud_range_test_btn)
        text_button_layout.addWidget(self.digit_in_noise_test_btn)

        repetitive_count_layout = QVBoxLayout()
        self.repetitive_count_spinbox = QSpinBox()
        self.repetitive_count_spinbox.setRange(1, 100)
        self.repetitive_count_spinbox.setValue(1)
        self.repetitive_count_spinbox.setPrefix("Repetitive Count: ")

        self.baseline_time_spinbox = QSpinBox()
        self.baseline_time_spinbox.setRange(1, 60)
        self.baseline_time_spinbox.setValue(1)
        self.baseline_time_spinbox.setPrefix("Baseline Time (s): ")

        repetitive_count_layout.addWidget(self.repetitive_count_spinbox)
        repetitive_count_layout.addWidget(self.baseline_time_spinbox)

        control_layout_2 = QHBoxLayout()
        control_layout_2.addLayout(text_button_layout)
        control_layout_2.addLayout(repetitive_count_layout)

        controls_layout.addLayout(top_buttons_layout)
        controls_layout.addLayout(control_layout_2)

        controls_widget = QWidget()
        controls_widget.setLayout(controls_layout)
        controls_widget.setMaximumWidth(400)  # 2/3 width

        # bottom_section_layout.addWidget(buttons_widget)
        bottom_section_layout.addWidget(controls_widget)

        # Sound Options
        scroll_area = QScrollArea()
        scroll_area.setWidgetResizable(True)
        scroll_content_widget = QWidget()
        self.sound_options_layout = QVBoxLayout(scroll_content_widget)
        self.sound_options_layout.setStretch(0, 1)

        for i in range(1, 11):
            sound_checkbox = QCheckBox()
            sound_combo_box = QComboBox()
            sound_combo_box.addItems(["Opt 1", "Opt 2", "Opt 3"])

            sound_option_layout = QHBoxLayout()
            sound_option_layout.setSpacing(0)  # Remove gap
            sound_option_layout.addWidget(sound_checkbox)
            sound_option_layout.addWidget(sound_combo_box)

            self.sound_options_layout.addLayout(sound_option_layout)

        scroll_area.setWidget(scroll_content_widget)
        sound_layout = QVBoxLayout()
        sound_layout.addWidget(QLabel("Sound Options", alignment=Qt.AlignLeft))
        sound_layout.addWidget(scroll_area)

        # Bar Chart
        chart_layout = QVBoxLayout()
        chart_layout.addWidget(BarChart())
        chart_layout.setStretch(0, 1)  # Ensure it takes 1/3 width

        bottom_section_layout.addLayout(sound_layout)
        bottom_section_layout.addLayout(chart_layout)

        layout.addWidget(bottom_section_widget)


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
