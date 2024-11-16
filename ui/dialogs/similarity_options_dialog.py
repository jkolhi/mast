from PyQt5.QtWidgets import (
    QDialog, QVBoxLayout, QHBoxLayout, QLabel,
    QDialogButtonBox, QSlider, QLineEdit
)
from PyQt5.QtCore import Qt

class SimilarityOptionsDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.initUI()

    def initUI(self):
        self.setWindowTitle('Similarity Search Options')
        layout = QVBoxLayout()

        threshold_layout = QHBoxLayout()
        threshold_label = QLabel('Similarity Threshold:')
        self.threshold_slider = QSlider(Qt.Horizontal)
        self.threshold_slider.setMinimum(0)
        self.threshold_slider.setMaximum(100)
        self.threshold_slider.setValue(50)
        self.threshold_value_label = QLabel('50%')
        
        self.threshold_slider.valueChanged.connect(
            lambda: self.threshold_value_label.setText(f'{self.threshold_slider.value()}%')
        )

        threshold_layout.addWidget(threshold_label)
        threshold_layout.addWidget(self.threshold_slider)
        threshold_layout.addWidget(self.threshold_value_label)
        layout.addLayout(threshold_layout)

        results_layout = QHBoxLayout()
        results_label = QLabel('Max Results:')
        self.max_results_input = QLineEdit('50')
        results_layout.addWidget(results_label)
        results_layout.addWidget(self.max_results_input)
        layout.addLayout(results_layout)

        button_box = QDialogButtonBox(
            QDialogButtonBox.Ok | QDialogButtonBox.Cancel
        )
        button_box.accepted.connect(self.accept)
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
            QLineEdit {
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

    def get_options(self):
        return {
            'threshold': self.threshold_slider.value() / 100.0,
            'max_results': int(self.max_results_input.text())
        }