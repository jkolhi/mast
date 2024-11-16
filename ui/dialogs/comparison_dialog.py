from PyQt5.QtWidgets import (
    QDialog, QVBoxLayout, QHBoxLayout, QLabel, 
    QPushButton, QTabWidget, QWidget, QGroupBox,
    QFileDialog, QScrollArea
)
from PyQt5.QtCore import Qt
from ..widgets.visualizers import WaveformVisualizer, SpectrogramVisualizer
from ..widgets.audio_player import AudioPlayer
from core.analyzer import AudioAnalyzer
import os
import mutagen
from PyQt5.QtCore import pyqtSignal

class AudioComparisonDialog(QDialog):
    # Add these signals
    file1_changed = pyqtSignal(str)  # Signal for song to master
    file2_changed = pyqtSignal(str)  # Signal for reference song

    def __init__(self, file1_path, file2_path=None, parent=None):
        super().__init__(parent)
        self.file1_path = file1_path
        self.file2_path = file2_path
        self.analyzer = AudioAnalyzer()
        self.initUI()
        self.analyze_files()

    def initUI(self):
        self.setWindowTitle('Audio Comparison')
        self.setMinimumSize(1200, 800)
        layout = QVBoxLayout(self)

        # File selection and info section
        file_section = QHBoxLayout()
        
        # First file
        self.file1_group = QGroupBox("Song to Master")
        file1_layout = QVBoxLayout()
        
        # File 1 selection
        file1_select = QHBoxLayout()
        self.file1_label = QLabel(os.path.basename(self.file1_path))
        file1_select_btn = QPushButton("Change File")
        file1_select_btn.clicked.connect(lambda: self.select_file(1))
        file1_select.addWidget(self.file1_label)
        file1_select.addWidget(file1_select_btn)
        file1_layout.addLayout(file1_select)
        
        # File 1 player
        self.player1 = AudioPlayer()
        self.player1.loadFile(self.file1_path)
        file1_layout.addWidget(self.player1)
        
        # File 1 metadata
        self.file1_metadata = QLabel()
        file1_layout.addWidget(self.file1_metadata)
        
        self.file1_group.setLayout(file1_layout)
        file_section.addWidget(self.file1_group)

        # Second file
        self.file2_group = QGroupBox("Reference Song")
        file2_layout = QVBoxLayout()
        
        # File 2 selection
        file2_select = QHBoxLayout()
        self.file2_label = QLabel(os.path.basename(self.file2_path) if self.file2_path else "No file selected")
        file2_select_btn = QPushButton("Change File")
        file2_select_btn.clicked.connect(lambda: self.select_file(2))
        file2_select.addWidget(self.file2_label)
        file2_select.addWidget(file2_select_btn)
        file2_layout.addLayout(file2_select)
        
        # File 2 player
        self.player2 = AudioPlayer()
        if self.file2_path:
            self.player2.loadFile(self.file2_path)
        file2_layout.addWidget(self.player2)
        
        # File 2 metadata
        self.file2_metadata = QLabel()
        file2_layout.addWidget(self.file2_metadata)
        
        self.file2_group.setLayout(file2_layout)
        file_section.addWidget(self.file2_group)
        
        layout.addLayout(file_section)

        # Visualization tabs
        tab_widget = QTabWidget()
        
        # Waveform tab
        waveform_tab = QWidget()
        waveform_layout = QVBoxLayout()
        self.waveform_viz1 = WaveformVisualizer()
        self.waveform_viz2 = WaveformVisualizer()
        waveform_layout.addWidget(QLabel("Song to Master"))
        waveform_layout.addWidget(self.waveform_viz1)
        waveform_layout.addWidget(QLabel("Reference"))
        waveform_layout.addWidget(self.waveform_viz2)
        waveform_tab.setLayout(waveform_layout)
        tab_widget.addTab(waveform_tab, "Waveforms")

        # Spectrum tab
        spectrum_tab = QWidget()
        spectrum_layout = QVBoxLayout()
        self.spectrum_viz1 = SpectrogramVisualizer()
        self.spectrum_viz2 = SpectrogramVisualizer()
        spectrum_layout.addWidget(QLabel("Song to Master"))
        spectrum_layout.addWidget(self.spectrum_viz1)
        spectrum_layout.addWidget(QLabel("Reference"))
        spectrum_layout.addWidget(self.spectrum_viz2)
        spectrum_tab.setLayout(spectrum_layout)
        tab_widget.addTab(spectrum_tab, "Spectrums")

        layout.addWidget(tab_widget)

        self.setStyleSheet("""
            QDialog, QWidget {
                background-color: #1A365D;
            }
            QLabel {
                color: #E2E8F0;
            }
            QGroupBox {
                color: #E2E8F0;
                font-weight: bold;
                border: 1px solid #4299E1;
                border-radius: 4px;
                margin-top: 1em;
                padding: 15px;
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

    def select_file(self, file_num):
        file_path, _ = QFileDialog.getOpenFileName(
            self,
            f'Select {"Song to Master" if file_num == 1 else "Reference Song"}',
            '',
            'Audio Files (*.mp3 *.wav *.aif *.flac *.m4a *.ogg)'
        )
        if file_path:
            if file_num == 1:
                self.file1_path = file_path
                self.file1_label.setText(os.path.basename(file_path))
                self.player1.loadFile(file_path)
                self.file1_changed.emit(file_path)  # Emit signal with new path
            else:
                self.file2_path = file_path
                self.file2_label.setText(os.path.basename(file_path))
                self.player2.loadFile(file_path)
                self.file2_changed.emit(file_path)  # Emit signal with new path
            self.analyze_files()
            
    def analyze_files(self):
        # Analyze first file
        analysis1 = self.analyzer.analyze_audio(self.file1_path)
        if analysis1:
            self.waveform_viz1.plot_waveform(analysis1['waveform'], analysis1['sample_rate'])
            self.spectrum_viz1.plot_spectrogram(analysis1['spectrogram'], analysis1['sample_rate'])
            self.update_metadata(1, analysis1)

        # Analyze second file if present
        if self.file2_path:
            analysis2 = self.analyzer.analyze_audio(self.file2_path)
            if analysis2:
                self.waveform_viz2.plot_waveform(analysis2['waveform'], analysis2['sample_rate'])
                self.spectrum_viz2.plot_spectrogram(analysis2['spectrogram'], analysis2['sample_rate'])
                self.update_metadata(2, analysis2)

    def update_metadata(self, file_num, analysis):
        metadata_text = f"""
        <b>Duration:</b> {analysis['duration']:.2f} seconds<br>
        <b>BPM:</b> {analysis['bpm']:.1f}<br>
        <b>Key:</b> {analysis['key']} {analysis['scale']}<br>
        <b>Average Loudness:</b> {analysis['loudness']['mean']:.2f} dB<br>
        <b>Dynamic Range:</b> {analysis['loudness']['dynamic_range']:.2f} dB
        """
        
        try:
            audio = mutagen.File(self.file1_path if file_num == 1 else self.file2_path)
            if audio and hasattr(audio, 'tags'):
                metadata_text += "<br><b>Tags:</b><br>"
                for key, value in audio.tags.items():
                    if not isinstance(value, bytes):
                        metadata_text += f"{key}: {value}<br>"
        except:
            pass

        if file_num == 1:
            self.file1_metadata.setText(metadata_text)
        else:
            self.file2_metadata.setText(metadata_text)