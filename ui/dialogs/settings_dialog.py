from PyQt5.QtWidgets import (
    QDialog, QVBoxLayout, QHBoxLayout, QLabel, 
    QPushButton, QComboBox, QLineEdit, QGroupBox,
    QDialogButtonBox, QSlider, QFileDialog
)
from PyQt5.QtCore import Qt

class SettingsDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.settings = None
        self.setWindowModality(Qt.NonModal)
        self.setWindowFlags(Qt.Window | Qt.WindowSystemMenuHint | Qt.WindowCloseButtonHint)

    def loadSettings(self, settings):
        """Initialize dialog with QSettings"""
        self.settings = settings
        self.initUI()
        self.show()
        
    def initUI(self):
        self.setWindowTitle('MAST Settings')
        self.setMinimumWidth(500)
        
        layout = QVBoxLayout()

        # Catalog Settings
        catalog_group = QGroupBox("Music Catalog")
        catalog_layout = QVBoxLayout()

        # Default music directory
        dir_layout = QHBoxLayout()
        self.default_dir = QLineEdit()
        self.default_dir.setText(self.settings.value('default_directory', ''))
        self.default_dir.setPlaceholderText("Default Music Directory")
        browse_btn = QPushButton("Browse...")
        browse_btn.clicked.connect(self.browse_directory)
        dir_layout.addWidget(self.default_dir)
        dir_layout.addWidget(browse_btn)
        catalog_layout.addWidget(QLabel("Default Music Directory:"))
        catalog_layout.addLayout(dir_layout)

        catalog_group.setLayout(catalog_layout)
        layout.addWidget(catalog_group)

        # Audio Settings
        audio_group = QGroupBox("Audio Settings")
        audio_layout = QVBoxLayout()

        # Default output format
        format_layout = QHBoxLayout()
        format_layout.addWidget(QLabel("Default Output Format:"))
        self.default_format = QComboBox()
        self.default_format.addItems(['WAV', 'FLAC', 'MP3', 'AIFF'])
        self.default_format.setCurrentText(self.settings.value('default_format', 'WAV'))
        format_layout.addWidget(self.default_format)
        audio_layout.addLayout(format_layout)

        # Default bit depth
        bitdepth_layout = QHBoxLayout()
        bitdepth_layout.addWidget(QLabel("Default Bit Depth:"))
        self.default_bitdepth = QComboBox()
        self.default_bitdepth.addItems(['16-bit PCM', '24-bit PCM', '32-bit Float'])
        self.default_bitdepth.setCurrentText(self.settings.value('default_bitdepth', '24-bit PCM'))
        bitdepth_layout.addWidget(self.default_bitdepth)
        audio_layout.addLayout(bitdepth_layout)

        # Default MP3 bitrate
        bitrate_layout = QHBoxLayout()
        bitrate_layout.addWidget(QLabel("Default MP3 Bitrate:"))
        self.default_bitrate = QComboBox()
        self.default_bitrate.addItems(['320k', '256k', '192k', '128k'])
        self.default_bitrate.setCurrentText(self.settings.value('default_bitrate', '320k'))
        bitrate_layout.addWidget(self.default_bitrate)
        audio_layout.addLayout(bitrate_layout)

        audio_group.setLayout(audio_layout)
        layout.addWidget(audio_group)

        # Similarity Settings
        similarity_group = QGroupBox("Similarity Search Settings")
        similarity_layout = QVBoxLayout()

        # Default threshold
        threshold_layout = QHBoxLayout()
        threshold_layout.addWidget(QLabel("Default Similarity Threshold:"))
        self.threshold_slider = QSlider(Qt.Horizontal)  # Fixed: Changed variable name
        self.threshold_slider.setMinimum(0)
        self.threshold_slider.setMaximum(100)
        current_threshold = int(float(self.settings.value('similarity_threshold', '0.5')) * 100)
        self.threshold_slider.setValue(current_threshold)
        self.threshold_value_label = QLabel(f"{current_threshold}%")
        self.threshold_slider.valueChanged.connect(
            lambda: self.threshold_value_label.setText(f"{self.threshold_slider.value()}%")
        )
        threshold_layout.addWidget(self.threshold_slider)
        threshold_layout.addWidget(self.threshold_value_label)
        similarity_layout.addLayout(threshold_layout)

        # Default max results
        results_layout = QHBoxLayout()
        results_layout.addWidget(QLabel("Maximum Results:"))
        self.max_results_input = QLineEdit()
        self.max_results_input.setText(self.settings.value('max_results', '50'))
        results_layout.addWidget(self.max_results_input)
        similarity_layout.addLayout(results_layout)

        similarity_group.setLayout(similarity_layout)
        layout.addWidget(similarity_group)

        # Buttons
        button_box = QDialogButtonBox(
            QDialogButtonBox.Ok | QDialogButtonBox.Cancel
        )
        button_box.accepted.connect(self.accept)
        button_box.rejected.connect(self.reject)
        layout.addWidget(button_box)

        self.setLayout(layout)

        # Apply dark theme style
        self.setStyleSheet("""
            QDialog {
                background-color: #1A365D;
            }
            QGroupBox {
                color: #E2E8F0;
                font-weight: bold;
                border: 1px solid #4299E1;
                border-radius: 4px;
                margin-top: 1em;
                padding: 10px;
            }
            QLabel {
                color: #E2E8F0;
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
            QLineEdit, QComboBox {
                padding: 5px;
                border: 1px solid #4299E1;
                border-radius: 4px;
                background-color: #2D3748;
                color: #E2E8F0;
            }
            QSlider::groove:horizontal {
                border: 1px solid #4299E1;
                height: 8px;
                background: #2D3748;
                margin: 2px 0;
                border-radius: 4px;
            }
            QSlider::handle:horizontal {
                background: #4299E1;
                border: 1px solid #4299E1;
                width: 18px;
                margin: -5px 0;
                border-radius: 9px;
            }
            QSlider::handle:horizontal:hover {
                background: #2B6CB0;
            }
        """)

    def browse_directory(self):
        directory = QFileDialog.getExistingDirectory(
            self, 
            "Select Default Music Directory",
            self.default_dir.text()
        )
        if directory:
            self.default_dir.setText(directory)

    def save_settings(self):
        self.settings.setValue('default_directory', self.default_dir.text())
        self.settings.setValue('default_format', self.default_format.currentText())
        self.settings.setValue('default_bitdepth', self.default_bitdepth.currentText())
        self.settings.setValue('default_bitrate', self.default_bitrate.currentText())
        self.settings.setValue('similarity_threshold', self.threshold_slider.value() / 100.0)
        self.settings.setValue('max_results', self.max_results_input.text())
        self.settings.sync()

    def show_settings(self):
        dialog = SettingsDialog(self)  # Only pass parent
        dialog.setStyleSheet(self.styleSheet())
        dialog.loadSettings(self.settings)  # Load settings separately
        if dialog.exec_() == QDialog.Accepted:
            dialog.save_settings()
            self.music_directory = self.settings.value('default_directory', None)
            if self.music_directory:
                self.directory_label.setText(f'Selected: {self.music_directory}')
            
            self.similarity_options = {
                'threshold': float(self.settings.value('similarity_threshold', 0.5)),
                'max_results': int(self.settings.value('max_results', 50))
            }
        dialog = SettingsDialog(self)
        dialog.setStyleSheet(self.styleSheet())
        dialog.loadSettings(self.settings)
        if dialog.exec_() == QDialog.Accepted:
            dialog.save_settings()
            self.music_directory = self.settings.value('default_directory', None)
            if self.music_directory:
                self.directory_label.setText(f'Selected: {self.music_directory}')
            
            self.similarity_options = {
                'threshold': float(self.settings.value('similarity_threshold', 0.5)),
                'max_results': int(self.settings.value('max_results', 50))
            }