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

        generate_report_button = QPushButton("Gene