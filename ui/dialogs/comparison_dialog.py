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
import librosa
import numpy as np

class AudioComparisonDialog(QDialog):
    # Add these signals
    file1_changed = pyqtSignal(str)  # Signal for song to master
    file2_changed = pyqtSignal(str)  # Signal for reference song

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
        self.analyze_files()
        self.show()

    def update_info(self, file_num, analysis):
        """Update audio information in the info tab"""
        info_text = f"""
        <h3 style='color: #63B3ED;'>{'Track to Master' if file_num == 1 else 'Reference Track'}</h3>
        <p><b>Duration:</b> {analysis['duration']:.2f} seconds</p>
        <p><b>BPM:</b> {analysis['bpm']:.1f}</p>
        <p><b>Loudness:</b><br>
        • Average: {analysis['loudness']['mean']:.2f} dB<br>
        • Peak: {analysis['loudness']['max']:.2f} dB<br>
        • Dynamic Range: {analysis['loudness']['dynamic_range']:.2f} dB</p>
        """
        
        if file_num == 1:
            if not hasattr(self, 'track_info'):
                self.track_info = QLabel()
            self.track_info.setText(info_text)
            self.track_info.setTextFormat(Qt.RichText)
        else:
            if not hasattr(self, 'reference_info'):
                self.reference_info = QLabel()
            self.reference_info.setText(info_text)
            self.reference_info.setTextFormat(Qt.RichText)

        # Update info tab if it exists
        if hasattr(self, 'info_layout'):
            if file_num == 1 and hasattr(self, 'track_info'):
                self.info_layout.addWidget(self.track_info)
            elif file_num == 2 and hasattr(self, 'reference_info'):
                self.info_layout.addWidget(self.reference_info)

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
        waveform_layout = QVBoxLayout(waveform_tab)
        self.waveform_viz1 = WaveformVisualizer()
        waveform_layout.addWidget(QLabel("Track to Master"))
        waveform_layout.addWidget(self.waveform_viz1)
        
        if self.file2_path:
            self.waveform_viz2 = WaveformVisualizer()
            waveform_layout.addWidget(QLabel("Reference Track"))
            waveform_layout.addWidget(self.waveform_viz2)
        
        tab_widget.addTab(waveform_tab, "Waveforms")

        # Spectrum tab
        spectrum_tab = QWidget()
        spectrum_layout = QVBoxLayout(spectrum_tab)
        self.spectrum_viz1 = SpectrogramVisualizer()
        spectrum_layout.addWidget(QLabel("Track to Master"))
        spectrum_layout.addWidget(self.spectrum_viz1)
        
        if self.file2_path:
            self.spectrum_viz2 = SpectrogramVisualizer()
            spectrum_layout.addWidget(QLabel("Reference Track"))
            spectrum_layout.addWidget(self.spectrum_viz2)
        
        tab_widget.addTab(spectrum_tab, "Spectrums")

        # Info tab with artwork and detailed info
        info_tab = QWidget()
        info_layout = QHBoxLayout(info_tab)

        # Track to master info
        track_info_layout = QVBoxLayout()
        track_info_layout.addWidget(QLabel("<h3>Track to Master</h3>"))
        
        # Artwork for track to master
        track_artwork_label = QLabel()
        track_artwork_label.setFixedSize(200, 200)
        track_artwork_label.setAlignment(Qt.AlignCenter)
        track_artwork_label.setStyleSheet("""
            QLabel {
                border: 1px solid #4299E1;
                background-color: #2D3748;
                border-radius: 4px;
            }
        """)
        track_info_layout.addWidget(track_artwork_label)

        # Info for track to master
        self.track_info = QLabel()
        self.track_info.setWordWrap(True)
        self.track_info.setTextFormat(Qt.RichText)
        track_info_layout.addWidget(self.track_info)
        
        info_layout.addLayout(track_info_layout)

        # Reference track info
        if self.file2_path:
            ref_info_layout = QVBoxLayout()
            ref_info_layout.addWidget(QLabel("<h3>Reference Track</h3>"))
            
            # Artwork for reference track
            ref_artwork_label = QLabel()
            ref_artwork_label.setFixedSize(200, 200)
            ref_artwork_label.setAlignment(Qt.AlignCenter)
            ref_artwork_label.setStyleSheet("""
                QLabel {
                    border: 1px solid #4299E1;
                    background-color: #2D3748;
                    border-radius: 4px;
                }
            """)
            ref_info_layout.addWidget(ref_artwork_label)

            # Info for reference track
            self.ref_info = QLabel()
            self.ref_info.setWordWrap(True)
            self.ref_info.setTextFormat(Qt.RichText)
            ref_info_layout.addWidget(self.ref_info)
            
            info_layout.addLayout(ref_info_layout)

            # Extract and show artwork for reference track
            try:
                import mutagen
                audio = mutagen.File(self.file2_path)
                if audio is not None:
                    pixmap = self._extract_artwork(audio)
                    if pixmap is not None:
                        scaled_pixmap = pixmap.scaled(200, 200, Qt.KeepAspectRatio, Qt.SmoothTransformation)
                        ref_artwork_label.setPixmap(scaled_pixmap)
                    else:
                        ref_artwork_label.setText("No\nArtwork")
            except:
                ref_artwork_label.setText("No\nArtwork")

        # Extract and show artwork for track to master
        try:
            import mutagen
            audio = mutagen.File(self.file1_path)
            if audio is not None:
                pixmap = self._extract_artwork(audio)
                if pixmap is not None:
                    scaled_pixmap = pixmap.scaled(200, 200, Qt.KeepAspectRatio, Qt.SmoothTransformation)
                    track_artwork_label.setPixmap(scaled_pixmap)
                else:
                    track_artwork_label.setText("No\nArtwork")
        except:
            track_artwork_label.setText("No\nArtwork")

        tab_widget.addTab(info_tab, "Audio Info")
        layout.addWidget(tab_widget)

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
        """Analyze the loaded audio files"""
        try:
            # Analyze first file (track to master)
            if self.file1_path:
                y1, sr1 = librosa.load(self.file1_path)
                if len(y1) > 0:
                    # Calculate spectrogram for first file
                    spec1 = np.abs(librosa.stft(y1))
                    spec_db1 = librosa.amplitude_to_db(spec1, ref=np.max)
                    
                    # Update visualizations for first file
                    self.waveform_viz1.plot_waveform(y1, sr1)
                    self.spectrum_viz1.plot_spectrogram(spec_db1, sr1)

                    # Calculate and update info for first file
                    tempo1, beats1 = librosa.beat.beat_track(y=y1, sr=sr1)
                    rms1 = librosa.feature.rms(y=y1)[0]
                    
                    analysis1 = {
                        'duration': len(y1) / sr1,
                        'bpm': float(tempo1),
                        'loudness': {
                            'mean': float(np.mean(rms1)),
                            'max': float(np.max(rms1)),
                            'min': float(np.min(rms1)),
                            'dynamic_range': float(np.max(rms1) - np.min(rms1))
                        }
                    }
                    self.update_info(1, analysis1)

            # Analyze second file (reference track)
            if self.file2_path:
                y2, sr2 = librosa.load(self.file2_path)
                if len(y2) > 0:
                    # Calculate spectrogram for second file
                    spec2 = np.abs(librosa.stft(y2))
                    spec_db2 = librosa.amplitude_to_db(spec2, ref=np.max)
                    
                    # Update visualizations for second file
                    self.waveform_viz2.plot_waveform(y2, sr2)
                    self.spectrum_viz2.plot_spectrogram(spec_db2, sr2)

                    # Calculate and update info for second file
                    tempo2, beats2 = librosa.beat.beat_track(y=y2, sr=sr2)
                    rms2 = librosa.feature.rms(y=y2)[0]
                    
                    analysis2 = {
                        'duration': len(y2) / sr2,
                        'bpm': float(tempo2),
                        'loudness': {
                            'mean': float(np.mean(rms2)),
                            'max': float(np.max(rms2)),
                            'min': float(np.min(rms2)),
                            'dynamic_range': float(np.max(rms2) - np.min(rms2))
                        }
                    }
                    self.update_info(2, analysis2)

        except Exception as e:
            print(f"Error analyzing files: {str(e)}")
            import traceback
            traceback.print_exc()

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