import os
from PyQt5.QtWidgets import (
    QDialog, QVBoxLayout, QHBoxLayout, QTabWidget,
    QLabel, QPushButton, QWidget, QGroupBox
)
from PyQt5.QtCore import Qt
from ..widgets.visualizers import (
    WaveformVisualizer,
    SpectrogramVisualizer,
    ComparisonVisualizer
)
from core.analyzer import AudioAnalyzer

class AudioAnalysisDialog(QDialog):
    def __init__(self, file_path, reference_path=None, parent=None):
        super().__init__(parent)
        self.file_path = file_path
        self.reference_path = reference_path
        self.analyzer = AudioAnalyzer()
        self.initUI()
        self.analyze_audio()

    def initUI(self):
        self.setWindowTitle('Audio Analysis')
        self.setMinimumSize(800, 600)
        layout = QVBoxLayout(self)

        # Add filename at the top
        filename_layout = QHBoxLayout()
        filename_label = QLabel(f"File: {os.path.basename(self.file_path)}")
        filename_label.setStyleSheet("""
            QLabel {
                color: #E2E8F0;
                font-size: 14px;
                font-weight: bold;
                padding: 5px;
            }
        """)
        filename_layout.addWidget(filename_label)
        if self.reference_path:
            ref_filename_label = QLabel(f"Reference: {os.path.basename(self.reference_path)}")
            ref_filename_label.setStyleSheet("""
                QLabel {
                    color: #E2E8F0;
                    font-size: 14px;
                    font-weight: bold;
                    padding: 5px;
                }
            """)
            filename_layout.addWidget(ref_filename_label)
        layout.addLayout(filename_layout)

        # Create tab widget
        self.tab_widget = QTabWidget()
        
        # Overview tab
        overview_tab = QWidget()
        overview_layout = QVBoxLayout(overview_tab)
        
        # Basic info group
        info_group = QGroupBox("Audio Information")
        info_layout = QVBoxLayout()
        self.info_label = QLabel()
        info_layout.addWidget(self.info_label)
        info_group.setLayout(info_layout)
        overview_layout.addWidget(info_group)
        
        # Waveform
        waveform_group = QGroupBox("Waveform")
        waveform_layout = QVBoxLayout()
        self.waveform_viz = WaveformVisualizer()
        waveform_layout.addWidget(self.waveform_viz)
        waveform_group.setLayout(waveform_layout)
        overview_layout.addWidget(waveform_group)

        self.tab_widget.addTab(overview_tab, "Overview")

        # Spectrum tab
        spectrum_tab = QWidget()
        spectrum_layout = QVBoxLayout(spectrum_tab)
        self.spectrum_viz = SpectrogramVisualizer()
        spectrum_layout.addWidget(self.spectrum_viz)
        self.tab_widget.addTab(spectrum_tab, "Spectrum")

        # Comparison tab (if reference provided)
        if self.reference_path:
            comparison_tab = QWidget()
            comparison_layout = QVBoxLayout(comparison_tab)
            self.comparison_viz = ComparisonVisualizer()
            comparison_layout.addWidget(self.comparison_viz)
            self.tab_widget.addTab(comparison_tab, "Comparison")

        layout.addWidget(self.tab_widget)

        # Apply dark theme
        self.setStyleSheet("""
            QDialog, QWidget {
                background-color: #1A365D;
            }
            QLabel {
                color: #E2E8F0;
                font-size: 12px;
            }
            QGroupBox {
                color: #E2E8F0;
                font-weight: bold;
                border: 1px solid #4299E1;
                border-radius: 4px;
                margin-top: 1em;
                padding-top: 10px;
            }
            QTabWidget::pane {
                border: 1px solid #4299E1;
                background-color: #2D3748;
            }
            QTabBar::tab {
                background-color: #2D3748;
                color: #E2E8F0;
                padding: 8px 16px;
                border: 1px solid #4299E1;
                margin-right: 2px;
            }
            QTabBar::tab:selected {
                background-color: #4299E1;
            }
        """)

    def analyze_audio(self):
        analysis = self.analyzer.analyze_audio(self.file_path)
        if analysis:
            # Update info label
            info_text = f"""
            <b>Duration:</b> {analysis['duration']:.2f} seconds<br>
            <b>BPM:</b> {analysis['bpm']:.1f}<br>
            <b>Key:</b> {analysis['key']} {analysis['scale']}<br>
            <b>Average Loudness:</b> {analysis['loudness']['mean']:.2f} dB<br>
            <b>Dynamic Range:</b> {analysis['loudness']['dynamic_range']:.2f} dB
            """
            self.info_label.setText(info_text)
            
            # Update visualizations
            self.waveform_viz.plot_waveform(analysis['waveform'], self.analyzer._sr)
            self.spectrum_viz.plot_spectrogram(analysis['spectrogram'], self.analyzer._sr)
            
            # If reference provided, analyze and show comparison
            if self.reference_path:
                ref_analysis = self.analyzer.analyze_audio(self.reference_path)
                if ref_analysis:
                    self.comparison_viz.plot_comparison(
                        analysis['spectrogram'],
                        ref_analysis['spectrogram'],
                        self.analyzer._sr
                    )