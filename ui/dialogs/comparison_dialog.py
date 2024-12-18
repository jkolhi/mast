from PyQt5.QtWidgets import (
    QDialog, QVBoxLayout, QHBoxLayout, QLabel, 
    QTabWidget, QWidget
)
from PyQt5.QtCore import Qt, QThread, pyqtSignal
from PyQt5.QtGui import QPixmap
import librosa
import numpy as np
import os
from datetime import datetime
from ..widgets.visualizers import WaveformVisualizer, SpectrogramVisualizer
from core.analyzer import AudioAnalyzer

class AnalysisThread(QThread):
    analysis_complete = pyqtSignal(dict, int)  # Analysis results, file number
    error_occurred = pyqtSignal(str)
    
    def __init__(self, file_path, file_num):
        super().__init__()
        self.file_path = file_path
        self.file_num = file_num
        
    def run(self):
        try:
            y, sr = librosa.load(self.file_path)
            spec = np.abs(librosa.stft(y))
            spec_db = librosa.amplitude_to_db(spec, ref=np.max)
            
            tempo, beats = librosa.beat.beat_track(y=y, sr=sr)
            rms = librosa.feature.rms(y=y)[0]
            
            analysis = {
                'waveform': y,
                'sample_rate': sr,
                'spectrogram': spec_db,
                'duration': len(y) / sr,
                'bpm': float(tempo),
                'loudness': {
                    'mean': float(np.mean(rms)),
                    'max': float(np.max(rms)),
                    'min': float(np.min(rms)),
                    'dynamic_range': float(np.max(rms) - np.min(rms))
                }
            }
            self.analysis_complete.emit(analysis, self.file_num)
        except Exception as e:
            self.error_occurred.emit(str(e))

class AudioComparisonDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.file1_path = None
        self.file2_path = None
        self.analyzer = AudioAnalyzer()
        self.setWindowModality(Qt.NonModal)
        self.setWindowFlags(Qt.Window | Qt.WindowSystemMenuHint | Qt.WindowCloseButtonHint)

    def loadFiles(self, file1_path, file2_path=None):
        self.file1_path = file1_path
        self.file2_path = file2_path
        self.initUI()
        
        # Start analysis threads
        self.thread1 = AnalysisThread(file1_path, 1)
        self.thread1.analysis_complete.connect(self.handle_analysis_complete)
        self.thread1.error_occurred.connect(self.handle_error)
        self.thread1.start()
        
        if file2_path:
            self.thread2 = AnalysisThread(file2_path, 2)
            self.thread2.analysis_complete.connect(self.handle_analysis_complete)
            self.thread2.error_occurred.connect(self.handle_error)
            self.thread2.start()
        
        self.show()

    def initUI(self):
        if not self.file1_path:
            return

        layout = QVBoxLayout(self)
        self.setWindowTitle('Audio Comparison')
        self.setMinimumSize(1000, 800)

        # Add file names at the top
        files_layout = QHBoxLayout()
        files_layout.addWidget(QLabel(f"Track to Master: {os.path.basename(self.file1_path)}"))
        if self.file2_path:
            files_layout.addWidget(QLabel(f"Reference Track: {os.path.basename(self.file2_path)}"))
        layout.addLayout(files_layout)

        tab_widget = QTabWidget()

        # Waveform tab
        waveform_tab = QWidget()
        self.waveform_layout = QVBoxLayout(waveform_tab)
        
        # Track 1 loading section
        self.loading_label1 = QLabel("Analyzing Track to Master...")
        self.loading_label1.setStyleSheet("color: #4299E1;")
        self.waveform_viz1 = WaveformVisualizer()
        self.waveform_layout.addWidget(QLabel("Track to Master"))
        self.waveform_layout.addWidget(self.loading_label1)
        self.waveform_layout.addWidget(self.waveform_viz1)
        self.waveform_viz1.hide()  # Hide until analysis complete
        
        if self.file2_path:
            self.loading_label2 = QLabel("Analyzing Reference Track...")
            self.loading_label2.setStyleSheet("color: #4299E1;")
            self.waveform_viz2 = WaveformVisualizer()
            self.waveform_layout.addWidget(QLabel("Reference Track"))
            self.waveform_layout.addWidget(self.loading_label2)
            self.waveform_layout.addWidget(self.waveform_viz2)
            self.waveform_viz2.hide()  # Hide until analysis complete
        
        tab_widget.addTab(waveform_tab, "Waveforms")

        # Spectrum tab
        spectrum_tab = QWidget()
        self.spectrum_layout = QVBoxLayout(spectrum_tab)
        
        self.spectrum_viz1 = SpectrogramVisualizer()
        self.spectrum_layout.addWidget(QLabel("Track to Master"))
        self.spectrum_layout.addWidget(self.spectrum_viz1)
        self.spectrum_viz1.hide()  # Hide until analysis complete
        
        if self.file2_path:
            self.spectrum_viz2 = SpectrogramVisualizer()
            self.spectrum_layout.addWidget(QLabel("Reference Track"))
            self.spectrum_layout.addWidget(self.spectrum_viz2)
            self.spectrum_viz2.hide()  # Hide until analysis complete
        
        tab_widget.addTab(spectrum_tab, "Spectrums")

        # Info tab with artwork and detailed info
        info_tab = QWidget()
        info_layout = QHBoxLayout(info_tab)

        # Track to master info
        track_info_layout = QVBoxLayout()
        track_info_layout.addWidget(QLabel("<h3>Track to Master</h3>"))
        
        # Artwork for track to master
        self.track_artwork_label = QLabel()
        self.track_artwork_label.setFixedSize(200, 200)
        self.track_artwork_label.setAlignment(Qt.AlignCenter)
        self.track_artwork_label.setStyleSheet("""
            QLabel {
                border: 1px solid #4299E1;
                background-color: #2D3748;
                border-radius: 4px;
            }
        """)
        track_info_layout.addWidget(self.track_artwork_label)

        # Info for track to master
        self.track_info = QLabel("Loading...")
        self.track_info.setWordWrap(True)
        self.track_info.setTextFormat(Qt.RichText)
        track_info_layout.addWidget(self.track_info)
        
        info_layout.addLayout(track_info_layout)

        # Reference track info
        if self.file2_path:
            ref_info_layout = QVBoxLayout()
            ref_info_layout.addWidget(QLabel("<h3>Reference Track</h3>"))
            
            # Artwork for reference track
            self.ref_artwork_label = QLabel()
            self.ref_artwork_label.setFixedSize(200, 200)
            self.ref_artwork_label.setAlignment(Qt.AlignCenter)
            self.ref_artwork_label.setStyleSheet("""
                QLabel {
                    border: 1px solid #4299E1;
                    background-color: #2D3748;
                    border-radius: 4px;
                }
            """)
            ref_info_layout.addWidget(self.ref_artwork_label)

            # Info for reference track
            self.ref_info = QLabel("Loading...")
            self.ref_info.setWordWrap(True)
            self.ref_info.setTextFormat(Qt.RichText)
            ref_info_layout.addWidget(self.ref_info)
            
            info_layout.addLayout(ref_info_layout)

        tab_widget.addTab(info_tab, "Audio Info")
        layout.addWidget(tab_widget)

        # Load artwork immediately (no need to wait for analysis)
        self.load_artwork()

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

    def handle_analysis_complete(self, analysis, file_num):
        if file_num == 1:
            self.loading_label1.hide()
            self.waveform_viz1.show()
            self.spectrum_viz1.show()
            self.waveform_viz1.plot_waveform(analysis['waveform'], analysis['sample_rate'])
            self.spectrum_viz1.plot_spectrogram(analysis['spectrogram'], analysis['sample_rate'])
            self.update_info(1, analysis)
        else:
            self.loading_label2.hide()
            self.waveform_viz2.show()
            self.spectrum_viz2.show()
            self.waveform_viz2.plot_waveform(analysis['waveform'], analysis['sample_rate'])
            self.spectrum_viz2.plot_spectrogram(analysis['spectrogram'], analysis['sample_rate'])
            self.update_info(2, analysis)

    def handle_error(self, error_msg):
        print(f"Analysis error: {error_msg}")

    def load_artwork(self):
        """Load artwork immediately without waiting for analysis"""
        try:
            import mutagen
            # Load track to master artwork
            audio = mutagen.File(self.file1_path)
            if audio is not None:
                pixmap = self._extract_artwork(audio)
                if pixmap is not None:
                    scaled_pixmap = pixmap.scaled(200, 200, Qt.KeepAspectRatio, Qt.SmoothTransformation)
                    self.track_artwork_label.setPixmap(scaled_pixmap)
                else:
                    self.track_artwork_label.setText("No\nArtwork")
            
            # Load reference track artwork
            if self.file2_path:
                audio = mutagen.File(self.file2_path)
                if audio is not None:
                    pixmap = self._extract_artwork(audio)
                    if pixmap is not None:
                        scaled_pixmap = pixmap.scaled(200, 200, Qt.KeepAspectRatio, Qt.SmoothTransformation)
                        self.ref_artwork_label.setPixmap(scaled_pixmap)
                    else:
                        self.ref_artwork_label.setText("No\nArtwork")
        except Exception as e:
            print(f"Error loading artwork: {e}")

    def _extract_artwork(self, audio):
        """Extract artwork from audio file"""
        try:
            if hasattr(audio, 'tags'):
                # ID3 tags (MP3)
                if hasattr(audio.tags, 'getall'):
                    apic_frames = audio.tags.getall('APIC')
                    if apic_frames:
                        artwork_data = apic_frames[0].data
                        pixmap = QPixmap()
                        pixmap.loadFromData(artwork_data)
                        return pixmap

                # MP4/M4A files
                elif hasattr(audio.tags, 'get'):
                    artwork = audio.tags.get('covr')
                    if artwork:
                        artwork_data = artwork[0]
                        pixmap = QPixmap()
                        pixmap.loadFromData(artwork_data)
                        return pixmap

                # FLAC files
                elif hasattr(audio, 'pictures'):
                    pictures = audio.pictures
                    if pictures:
                        artwork_data = pictures[0].data
                        pixmap = QPixmap()
                        pixmap.loadFromData(artwork_data)
                        return pixmap
            return None
        except Exception as e:
            print(f"Error extracting artwork: {e}")
            return None
        
    def update_info(self, file_num, analysis):
        """Update audio information in the info tab"""
        try:
            import mutagen
            file_path = self.file1_path if file_num == 1 else self.file2_path
            audio = mutagen.File(file_path)
            
            stats = os.stat(file_path)
            
            info_text = f"""
            <b>File Size:</b> {stats.st_size / (1024*1024):.2f} MB<br>
            <b>Last Modified:</b> {datetime.fromtimestamp(stats.st_mtime).strftime('%Y-%m-%d %H:%M:%S')}<br>
            """
            
            if audio is not None:
                if hasattr(audio.info, 'sample_rate'):
                    info_text += f"<b>Sample Rate:</b> {audio.info.sample_rate} Hz<br>"
                if hasattr(audio.info, 'bitrate'):
                    info_text += f"<b>Bit Rate:</b> {audio.info.bitrate // 1000} kbps<br>"
                if hasattr(audio.info, 'channels'):
                    info_text += f"<b>Channels:</b> {audio.info.channels}<br>"

            info_text += f"""
            <b>Duration:</b> {analysis['duration']:.2f} seconds<br>
            <b>BPM:</b> {analysis['bpm']:.1f}<br>
            <b>Loudness:</b><br>
            • Average: {analysis['loudness']['mean']:.2f} dB<br>
            • Peak: {analysis['loudness']['max']:.2f} dB<br>
            • Dynamic Range: {analysis['loudness']['dynamic_range']:.2f} dB<br>
            """

            if audio is not None and hasattr(audio, 'tags') and audio.tags:
                info_text += "<br><b>Metadata Tags:</b><br>"
                for key, value in audio.tags.items():
                    if key.lower() not in ['apic', 'covr', 'cover art', 'picture', 'apic:cover']:
                        if not isinstance(value, bytes) and not (isinstance(value, list) and any(isinstance(v, bytes) for v in value)):
                            tag_value = str(value)
                            if isinstance(value, list):
                                tag_value = ', '.join(str(v) for v in value)
                            info_text += f"{key}: {tag_value}<br>"

            if file_num == 1:
                self.track_info.setText(info_text)
            else:
                self.ref_info.setText(info_text)
                
        except Exception as e:
            print(f"Error updating info: {e}")
            info_text = "Error loading audio information"
            if file_num == 1:
                self.track_info.setText(info_text)
            else:
                self.ref_info.setText(info_text)