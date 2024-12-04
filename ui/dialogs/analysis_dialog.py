from PyQt5.QtWidgets import (
    QDialog, QVBoxLayout, QHBoxLayout, QLabel, 
    QTabWidget, QWidget
)
from PyQt5.QtCore import Qt
from ..widgets.visualizers import WaveformVisualizer, SpectrogramVisualizer
from core.analyzer import AudioAnalyzer
import numpy as np
import librosa

class AudioAnalysisDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.file_path = None
        self.reference_path = None
        self.analyzer = AudioAnalyzer()
        self.setWindowModality(Qt.NonModal)
        self.setWindowFlags(Qt.Window | Qt.WindowSystemMenuHint | Qt.WindowCloseButtonHint)

    def loadFiles(self, file_path, reference_path=None):
        self.file_path = file_path
        self.reference_path = reference_path
        self.initUI()
        self.analyze_files()
        self.show()

    def initUI(self):
        if not self.file_path:
            return

        layout = QVBoxLayout(self)
        self.setWindowTitle('Audio Analysis')
        self.setMinimumSize(800, 600)

        tab_widget = QTabWidget()
        
        # Waveform tab
        waveform_tab = QWidget()
        waveform_layout = QVBoxLayout(waveform_tab)
        
        # Initialize waveform visualizers
        self.waveform_viz1 = WaveformVisualizer()
        self.waveform_viz2 = WaveformVisualizer()
        
        waveform_layout.addWidget(QLabel("Target Waveform"))
        waveform_layout.addWidget(self.waveform_viz1)
        if self.reference_path:
            waveform_layout.addWidget(QLabel("Reference Waveform"))
            waveform_layout.addWidget(self.waveform_viz2)
        
        # Initialize with dummy data
        dummy_data = np.zeros(1000)
        sr = 44100
        self.waveform_viz1.plot_waveform(dummy_data, sr)
        if self.reference_path:
            self.waveform_viz2.plot_waveform(dummy_data, sr)
        
        tab_widget.addTab(waveform_tab, "Waveforms")

        # Spectrum tab
        spectrum_tab = QWidget()
        spectrum_layout = QVBoxLayout(spectrum_tab)
        
        # Initialize spectrum visualizers
        self.spectrum_viz1 = SpectrogramVisualizer()
        self.spectrum_viz2 = SpectrogramVisualizer()
        
        spectrum_layout.addWidget(QLabel("Target Spectrum"))
        spectrum_layout.addWidget(self.spectrum_viz1)
        if self.reference_path:
            spectrum_layout.addWidget(QLabel("Reference Spectrum"))
            spectrum_layout.addWidget(self.spectrum_viz2)
        
        # Initialize with dummy spectrograms
        self.spectrum_viz1.plot_spectrogram(np.zeros((100,100)), sr)
        if self.reference_path:
            self.spectrum_viz2.plot_spectrogram(np.zeros((100,100)), sr)
        
        tab_widget.addTab(spectrum_tab, "Spectrums")
        
        # Info tab
        info_tab = QWidget()
        info_layout = QVBoxLayout(info_tab)
        self.info_label = QLabel()
        info_layout.addWidget(self.info_label)
        tab_widget.addTab(info_tab, "Audio Info")
        
        layout.addWidget(tab_widget)

        # Apply dark theme style
        self.setStyleSheet("""
            QDialog, QWidget {
                background-color: #1A365D;
            }
            QLabel {
                color: #E2E8F0;
                font-size: 12px;
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
            }
            QTabBar::tab:selected {
                background-color: #4299E1;
            }
        """)

    def analyze_files(self):
        """Analyze the loaded audio files"""
        try:
            y, sr = librosa.load(self.file_path)
            if len(y) == 0:
                print("Error: No audio data loaded")
                return

            # Calculate spectrogram
            spec = np.abs(librosa.stft(y))
            spec_db = librosa.amplitude_to_db(spec, ref=np.max)
            
            # Update visualizations
            self.waveform_viz1.plot_waveform(y, sr)
            self.spectrum_viz1.plot_spectrogram(spec_db, sr)
            
            # Calculate audio info
            tempo, beats = librosa.beat.beat_track(y=y, sr=sr)
            chroma = librosa.feature.chroma_cqt(y=y, sr=sr)
            rms = librosa.feature.rms(y=y)[0]
            
            analysis = {
                'duration': len(y) / sr,
                'bpm': float(tempo),
                'loudness': {
                    'mean': float(np.mean(rms)),
                    'max': float(np.max(rms)),
                    'min': float(np.min(rms)),
                    'dynamic_range': float(np.max(rms) - np.min(rms))
                }
            }
            
            self.update_info(1, analysis)
            
        except Exception as e:
            print(f"Error analyzing file: {str(e)}")
            
    def update_info(self, file_num, analysis):
        info_text = f"""
        <b>Duration:</b> {analysis['duration']:.2f} seconds<br>
        <b>BPM:</b> {analysis['bpm']:.1f}<br>
        <b>Loudness:</b><br>
        • Average: {analysis['loudness']['mean']:.2f} dB<br>
        • Peak: {analysis['loudness']['max']:.2f} dB<br>
        • Dynamic Range: {analysis['loudness']['dynamic_range']:.2f} dB
        """
        self.info_label.setText(info_text)
        self.info_label.setTextFormat(Qt.RichText)
