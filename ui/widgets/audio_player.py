from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QPushButton,
    QLabel, QSlider, QStyle
)
from PyQt5.QtCore import Qt, QTimer, QUrl
from PyQt5.QtMultimedia import QMediaPlayer, QMediaContent
import os

class AudioPlayer(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.player = QMediaPlayer()
        self.initUI()
        self.setupConnections()

    def initUI(self):
        layout = QVBoxLayout()
        
        # Time and slider layout
        time_layout = QHBoxLayout()
        
        self.time_label = QLabel('0:00 / 0:00')
        self.time_label.setStyleSheet("color: #E2E8F0; min-width: 80px;")
        
        self.position_slider = QSlider(Qt.Horizontal)
        self.position_slider.setRange(0, 0)
        
        time_layout.addWidget(self.time_label)
        time_layout.addWidget(self.position_slider)
        
        layout.addLayout(time_layout)

        # Controls layout
        controls_layout = QHBoxLayout()
        
        self.play_button = QPushButton()
        self.play_button.setIcon(self.style().standardIcon(QStyle.SP_MediaPlay))
        self.play_button.setFixedSize(32, 32)
        
        self.stop_button = QPushButton()
        self.stop_button.setIcon(self.style().standardIcon(QStyle.SP_MediaStop))
        self.stop_button.setFixedSize(32, 32)
        
        self.volume_slider = QSlider(Qt.Horizontal)
        self.volume_slider.setRange(0, 100)
        self.volume_slider.setValue(70)
        self.volume_slider.setFixedWidth(100)
        
        controls_layout.addWidget(self.play_button)
        controls_layout.addWidget(self.stop_button)
        controls_layout.addWidget(QLabel("Volume:"))
        controls_layout.addWidget(self.volume_slider)
        controls_layout.addStretch()
        
        layout.addLayout(controls_layout)
        
        self.setLayout(layout)
        
        # Apply styles
        self.setStyleSheet("""
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
            QPushButton {
                background-color: #4299E1;
                border-radius: 16px;
                padding: 4px;
            }
            QPushButton:hover {
                background-color: #2B6CB0;
            }
            QLabel {
                color: #E2E8F0;
            }
        """)

    def setupConnections(self):
        self.play_button.clicked.connect(self.togglePlayback)
        self.stop_button.clicked.connect(self.stop)
        self.position_slider.sliderMoved.connect(self.setPosition)
        self.volume_slider.valueChanged.connect(self.player.setVolume)
        
        self.player.stateChanged.connect(self.updatePlayButton)
        self.player.positionChanged.connect(self.updatePosition)
        self.player.durationChanged.connect(self.updateDuration)

    def loadFile(self, file_path):
        self.player.setMedia(QMediaContent(QUrl.fromLocalFile(file_path)))
        self.play_button.setEnabled(True)
        self.stop_button.setEnabled(True)

    def togglePlayback(self):
        if self.player.state() == QMediaPlayer.PlayingState:
            self.player.pause()
        else:
            self.player.play()

    def stop(self):
        self.player.stop()

    def setPosition(self, position):
        self.player.setPosition(position)

    def updatePlayButton(self):
        if self.player.state() == QMediaPlayer.PlayingState:
            self.play_button.setIcon(self.style().standardIcon(QStyle.SP_MediaPause))
        else:
            self.play_button.setIcon(self.style().standardIcon(QStyle.SP_MediaPlay))

    def updatePosition(self, position):
        self.position_slider.setValue(position)
        self.updateTimeLabel(position, self.player.duration())

    def updateDuration(self, duration):
        self.position_slider.setRange(0, duration)
        self.updateTimeLabel(self.player.position(), duration)

    def updateTimeLabel(self, position, duration):
        position_str = self.formatTime(position)
        duration_str = self.formatTime(duration)
        self.time_label.setText(f'{position_str} / {duration_str}')

    def formatTime(self, ms):
        s = ms // 1000
        m = s // 60
        s = s % 60
        return f'{m}:{s:02d}'