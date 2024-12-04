from PyQt5.QtWidgets import (
    QDialog, QVBoxLayout, QHBoxLayout, QLabel, 
    QPushButton, QComboBox, QLineEdit, QGroupBox,
    QDialogButtonBox, QFileDialog
)
from PyQt5.QtWidgets import QDialog, QVBoxLayout  # Add other widgets as needed
from PyQt5.QtCore import Qt

from datetime import datetime
from pathlib import Path

class MasteringOptionsDialog(QDialog):
    def __init__(self, target_name, reference_name, parent=None):
        super().__init__(parent)
        self.target_name = target_name
        self.reference_name = reference_name
        # Make dialog non-modal
        self.setWindowModality(Qt.NonModal)
        # Set window flags to make it independent
        self.setWindowFlags(Qt.Window | Qt.WindowSystemMenuHint | Qt.WindowCloseButtonHint)
        self.initUI()

    def initUI(self):
        self.setWindowTitle('Mastering Options')
        layout = QVBoxLayout()

        # Output Format Selection
        format_group = QGroupBox("Output Format")
        format_layout = QVBoxLayout()
        
        self.format_combo = QComboBox()
        self.format_combo.addItems(['WAV', 'FLAC', 'MP3', 'AIFF'])
        self.format_combo.currentTextChanged.connect(self.on_format_changed)
        format_layout.addWidget(QLabel("Format:"))
        format_layout.addWidget(self.format_combo)
        
        # Bit Depth Selection (for WAV/FLAC)
        self.bitdepth_combo = QComboBox()
        self.bitdepth_combo.addItems(['16-bit PCM', '24-bit PCM', '32-bit Float'])
        format_layout.addWidget(QLabel("Bit Depth:"))
        format_layout.addWidget(self.bitdepth_combo)
        
        # MP3 Bitrate Selection
        self.mp3_bitrate_combo = QComboBox()
        self.mp3_bitrate_combo.addItems(['320k', '256k', '192k', '128k'])
        self.mp3_bitrate_combo.hide()  # Initially hidden
        format_layout.addWidget(QLabel("MP3 Bitrate:"))
        format_layout.addWidget(self.mp3_bitrate_combo)
        
        format_group.setLayout(format_layout)
        layout.addWidget(format_group)

        # File Naming Options
        naming_group = QGroupBox("File Naming")
        naming_layout = QVBoxLayout()
        
        self.naming_pattern = QLineEdit()
        # Create default pattern using actual filenames
        default_pattern = f"{self.target_name}_mastered_to_{self.reference_name}"
        self.naming_pattern.setText(default_pattern)
        self.naming_pattern.setPlaceholderText("e.g., {target}_mastered_to_{reference}")
        naming_layout.addWidget(QLabel("Naming Pattern:"))
        naming_layout.addWidget(self.naming_pattern)
        
        # Add naming pattern help
        help_text = QLabel(
            "Available variables:\n"
            "{target} - Target filename\n"
            "{reference} - Reference filename\n"
            "{date} - Current date\n"
            "{time} - Current time"
        )
        help_text.setStyleSheet("color: #A0AEC0;")  # Slightly dimmed text for help
        naming_layout.addWidget(help_text)
        
        naming_group.setLayout(naming_layout)
        layout.addWidget(naming_group)

        # Output Directory
        dir_group = QGroupBox("Output Location")
        dir_layout = QVBoxLayout()
        
        dir_select_layout = QHBoxLayout()
        self.output_dir = QLineEdit()
        self.output_dir.setPlaceholderText("Same as target file")
        dir_select_layout.addWidget(self.output_dir)
        
        browse_btn = QPushButton("Browse...")
        browse_btn.clicked.connect(self.browse_output_dir)
        dir_select_layout.addWidget(browse_btn)
        
        dir_layout.addLayout(dir_select_layout)
        dir_group.setLayout(dir_layout)
        layout.addWidget(dir_group)

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
            QPushButton:disabled {
                background-color: #718096;
            }
            QLineEdit, QComboBox {
                padding: 5px;
                border: 1px solid #4299E1;
                border-radius: 4px;
                background-color: #2D3748;
                color: #E2E8F0;
            }
            QComboBox::drop-down {
                border: none;
                padding-right: 10px;
            }
            QComboBox::down-arrow {
                image: none;
                border-left: 5px solid transparent;
                border-right: 5px solid transparent;
                border-top: 5px solid #E2E8F0;
                margin-right: 5px;
            }
        """)

    def on_format_changed(self, format_text):
        # Show/hide relevant options based on format
        if format_text == 'MP3':
            self.bitdepth_combo.hide()
            self.mp3_bitrate_combo.show()
        else:
            self.bitdepth_combo.show()
            self.mp3_bitrate_combo.hide()

    def browse_output_dir(self):
        directory = QFileDialog.getExistingDirectory(self, "Select Output Directory")
        if directory:
            self.output_dir.setText(directory)

    def get_options(self):
        format_map = {
            'WAV': {
                '16-bit PCM': 'PCM_16',
                '24-bit PCM': 'PCM_24',
                '32-bit Float': 'FLOAT'
            },
            'FLAC': {
                '16-bit PCM': 'PCM_16',
                '24-bit PCM': 'PCM_24'
            }
        }

        format_text = self.format_combo.currentText()
        subtype = None
        
        if format_text in ['WAV', 'FLAC']:
            bitdepth = self.bitdepth_combo.currentText()
            subtype = format_map[format_text][bitdepth]
        
        return {
            'format': format_text.lower(),
            'subtype': subtype,
            'mp3_bitrate': self.mp3_bitrate_combo.currentText() if format_text == 'MP3' else None,
            'naming_pattern': self.naming_pattern.text() or "{target}_mastered_to_{reference}",
            'output_dir': self.output_dir.text() or None
        }