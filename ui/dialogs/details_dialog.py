import os
import sys
import subprocess
from datetime import datetime
from PyQt5.QtWidgets import (
    QDialog, QVBoxLayout, QHBoxLayout, QLabel, 
    QPushButton, QDialogButtonBox, QScrollArea, 
    QWidget, QMessageBox
)
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPixmap
from .analysis_dialog import AudioAnalysisDialog

class SongDetailsDialog(QDialog):
    def __init__(self, song_path, parent=None):
        super().__init__(parent)
        self.song_path = song_path
        self.initUI()

    def initUI(self):
        self.setWindowTitle('Song Details')
        self.setMinimumWidth(500)
        layout = QVBoxLayout()

        # Create a horizontal layout for artwork and details
        content_layout = QHBoxLayout()

        # Create artwork section
        artwork_layout = QVBoxLayout()
        artwork_label = QLabel()
        artwork_label.setFixedSize(200, 200)
        artwork_label.setAlignment(Qt.AlignCenter)
        artwork_label.setStyleSheet("""
            QLabel {
                border: 1px solid #4299E1;
                background-color: #2D3748;
                border-radius: 4px;
            }
        """)

        # Basic file information
        stats = os.stat(self.song_path)
        details = [
            f"Filename: {os.path.basename(self.song_path)}",
            f"Full Path: {self.song_path}",
            f"File Size: {stats.st_size / (1024*1024):.2f} MB",
            f"Last Modified: {datetime.fromtimestamp(stats.st_mtime).strftime('%Y-%m-%d %H:%M:%S')}"
        ]

        try:
            import mutagen
            audio = mutagen.File(self.song_path)
            if audio is not None:
                # Duration
                if hasattr(audio.info, 'length'):
                    minutes = int(audio.info.length // 60)
                    seconds = int(audio.info.length % 60)
                    details.append(f"Duration: {minutes}:{seconds:02d}")
                
                # Sample rate
                if hasattr(audio.info, 'sample_rate'):
                    details.append(f"Sample Rate: {audio.info.sample_rate} Hz")
                
                # Bit rate
                if hasattr(audio.info, 'bitrate'):
                    details.append(f"Bit Rate: {audio.info.bitrate // 1000} kbps")
                
                # Channels
                if hasattr(audio.info, 'channels'):
                    details.append(f"Channels: {audio.info.channels}")
                
                # Format
                format_type = os.path.splitext(self.song_path)[1][1:].upper()
                details.append(f"Format: {format_type}")
                
                # Extract and display artwork
                pixmap = self._extract_artwork(audio)
                if pixmap is not None:
                    artwork_label.setPixmap(pixmap.scaled(200, 200, Qt.KeepAspectRatio, Qt.SmoothTransformation))
                else:
                    artwork_label.setText("No\nArtwork")
                
                # Tags
                if hasattr(audio, 'tags') and audio.tags:
                    details.append("\nMetadata Tags:")
                    for key, value in audio.tags.items():
                        # Skip cover art related tags
                        if key.lower() in ['apic', 'covr', 'cover art', 'picture', 'apic:cover']:
                            continue
                        
                        # Skip binary data
                        if isinstance(value, bytes) or (isinstance(value, list) and any(isinstance(v, bytes) for v in value)):
                            continue
                            
                        # Clean up the tag representation
                        tag_value = str(value)
                        if isinstance(value, list):
                            tag_value = ', '.join(str(v) for v in value)
                        details.append(f"{key}: {tag_value}")

        except ImportError:
            details.append("\nInstall 'mutagen' package for detailed audio information")
            artwork_label.setText("No\nArtwork")
        except Exception as e:
            details.append(f"\nError reading audio metadata: {str(e)}")
            artwork_label.setText("No\nArtwork")

        artwork_layout.addWidget(artwork_label)
        artwork_layout.addStretch()
        content_layout.addLayout(artwork_layout)

        # Create scrollable area for details
        scroll_area = QScrollArea()
        scroll_area.setWidgetResizable(True)
        scroll_widget = QWidget()
        scroll_layout = QVBoxLayout(scroll_widget)

        # Add details to scroll area
        for detail in details:
            label = QLabel(detail)
            label.setWordWrap(True)
            scroll_layout.addWidget(label)

        scroll_area.setWidget(scroll_widget)
        content_layout.addWidget(scroll_area)

        # Add the content layout to the main layout
        layout.addLayout(content_layout)

        # Buttons
        button_box = QDialogButtonBox(
            QDialogButtonBox.Ok | QDialogButtonBox.Cancel
        )
        button_box.accepted.connect(self.accept)
        button_box.rejected.connect(self.reject)
        layout.addWidget(button_box)

        play_button = QPushButton('Play')
        play_button.clicked.connect(self.play_song)
        layout.addWidget(play_button)

        # Add button layout
        button_layout = QHBoxLayout()
        
        play_button = QPushButton('Play')
        play_button.clicked.connect(self.play_song)
        button_layout.addWidget(play_button)

        analyze_button = QPushButton('Audio Analysis')
        analyze_button.clicked.connect(self.show_audio_analysis)
        button_layout.addWidget(analyze_button)

        layout.addLayout(button_layout)

        button_box = QDialogButtonBox(
            QDialogButtonBox.Close
        )
        button_box.rejected.connect(self.reject)
        layout.addWidget(button_box)

        self.setLayout(layout)

    def _extract_artwork(self, audio):
        try:
            # Try different methods to extract artwork
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
        
    def show_audio_analysis(self):
        dialog = AudioAnalysisDialog(
            file_path=self.song_path,
            parent=self
        )
        dialog.setStyleSheet(self.styleSheet())
        dialog.exec_()

    def play_song(self):
        try:
            if sys.platform.startswith('darwin'):
                subprocess.call(('open', self.song_path))
            elif sys.platform.startswith('win'):
                os.startfile(self.song_path)
            else:
                subprocess.call(('xdg-open', self.song_path))
        except Exception as e:
            QMessageBox.warning(self, "Error", f"Could not play file: {str(e)}")