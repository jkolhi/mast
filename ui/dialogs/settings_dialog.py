from PyQt5.QtWidgets import (
    QDialog, QVBoxLayout, QHBoxLayout, QLabel, 
    QPushButton, QComboBox, QLineEdit, QGroupBox,
    QDialogButtonBox, QSlider, QFileDialog
)
from PyQt5.QtCore import Qt

class SettingsDialog(QDialog):
    def __init__(self, settings, parent=None):
        super().__init__(parent)
        self.settings = settings
        self.initUI()

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
        self.default_threshold = QSlider(Qt.Horizontal)
        self.default_threshold.setMinimum(0)
        self.default_threshold.setMaximum(100)
        self.default_threshold.setValue(int(float(self.settings.value('default_threshold', '50')) * 100))
        self.threshold_label = QLabel(f"{self.default_threshold.value()}%")
        self.default_threshold.valueChanged.connect(
            lambda: self.threshold_label.setText(f"{self.default_threshold.value()}%")
        )
        threshold_layout.addWidget(self.default_threshold)
        threshold_layout.addWidget(self.threshold_label)
        similarity_layout.addLayout(threshold_layout)

        # Default max results
        results_layout = QHBoxLayout()
        results_layout.addWidget(QLabel("Default Max Results:"))
        self.default_max_results = QLineEdit()
        self.default_max_results.setText(self.settings.value('default_max_results', '50'))
        results_layout.addWidget(self.default_max_results)
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
                padding-top: 10px;
            }
            QGroupBox::title {
                subcontrol-origin: margin;
                left: 10px;
                padding: 0 3px 0 3px;
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
        self.settings.setValue('default_threshold', self.default_threshold.value() / 100.0)
        self.settings.setValue('default_max_results', self.default_max_results.text())
        self.settings.sync()