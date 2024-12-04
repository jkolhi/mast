import os
from datetime import datetime
from PyQt5.QtWidgets import (
    QDialog, QVBoxLayout, QHBoxLayout, QLabel, 
    QPushButton, QDialogButtonBox, QScrollArea, 
    QWidget, QGroupBox
)
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPixmap
from ui.dialogs.analysis_dialog import AudioAnalysisDialog
from ui.widgets.audio_player import AudioPlayer

class SongDetailsDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.song_path = None
        self.setWindowModality(Qt.NonModal)
        self.setWindowFlags(Qt.Window | Qt.WindowSystemMenuHint | Qt.WindowCloseButtonHint)

    def loadSong(self, song_path):
        """Initialize dialog with a song path"""
        self.song_path = song_path
        self.initUI()
        self.show()

    def initUI(self):
        if not self.song_path:
            return

        self.setWindowTitle('Song Details')
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
                # Extract and display artwork
                pixmap = self._extract_artwork(audio)
                if pixmap is not None:
                    scaled_pixmap = pixmap.scaled(200, 200, Qt.KeepAspectRatio, Qt.SmoothTransformation)
                    artwork_label.setPixmap(scaled_pixmap)
                else:
                    artwork_label.setText("No\nArtwork")

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

        # Add audio player
        player_group = QGroupBox("Audio Player")
        player_layout = QVBoxLayout()
        self.audio_player = AudioPlayer()
        self.audio_player.loadFile(self.song_path)
        player_layout.addWidget(self.audio_player)
        player_group.setLayout(player_layout)
        layout.addWidget(player_group)

        # Add button layout
        button_layout = QHBoxLayout()

        analyze_button = QPushButton('Audio Analysis')
        analyze_button.clicked.connect(self.show_audio_analysis)
        button_layout.addWidget(analyze_button)

        layout.addLayout(button_layout)

        # Dialog buttons
        button_box = QDialogButtonBox(QDialogButtonBox.Close)
        button_box.rejected.connect(self.reject)
        layout.addWidget(button_box)

        self.setLayout(layout)
        
        # Apply dark theme
        self.setStyleSheet("""
            QDialog {
                background-color: #1A365D;
            }
            QLabel {
                color: #E2E8F0;
                font-size: 12px;
                margin: 2px;
            }
            QPushButton {
                background-color: #4299E1;
                color: white;
                padding: 6px 12px;
                border-radius: 4px;
                border: none;
                min-width: 80px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #2B6CB0;
            }
            QScrollArea {
                border: 1px solid #4299E1;
                border-radius: 4px;
                background-color: #2D3748;
            }
            QGroupBox {
                color: #E2E8F0;
                font-weight: bold;
                border: 1px solid #4299E1;
                border-radius: 4px;
                margin-top: 1em;
                padding: 10px;
            }
            QScrollBar:vertical {
                border: none;
                background-color: #2D3748;
                width: 12px;
                margin: 0px;
            }
            QScrollBar::handle:vertical {
                background-color: #4299E1;
                min-height: 20px;
                border-radius: 6px;
            }
            QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical {
                border: none;
                background: none;
            }
        """)

    def _extract_artwork(self, audio):
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

    def show_audio_analysis(self):
        dialog = AudioAnalysisDialog(self)
        dialog.setStyleSheet(self.styleSheet())
        dialog.loadFiles(self.song_path)  # Use loadFiles instead of passing in constructor