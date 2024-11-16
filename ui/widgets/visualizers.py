from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel
import matplotlib.pyplot as plt
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
import numpy as np
import librosa

class WaveformVisualizer(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setup_ui()

    def setup_ui(self):
        layout = QVBoxLayout(self)
        
        # Create matplotlib figure
        self.figure, self.ax = plt.subplots(figsize=(8, 3))
        self.canvas = FigureCanvas(self.figure)
        layout.addWidget(self.canvas)

        # Set dark theme for plot
        self.figure.patch.set_facecolor('#1A365D')
        self.ax.set_facecolor('#2D3748')
        self.ax.tick_params(colors='#E2E8F0')
        for spine in self.ax.spines.values():
            spine.set_color('#4299E1')
        
        self.ax.set_xlabel('Time (s)', color='#E2E8F0')
        self.ax.set_ylabel('Amplitude', color='#E2E8F0')

    def plot_waveform(self, audio_data, sr):
        self.ax.clear()
        time = np.arange(len(audio_data)) / sr
        self.ax.plot(time, audio_data, color='#4299E1', linewidth=0.5)
        self.ax.set_xlabel('Time (s)', color='#E2E8F0')
        self.ax.set_ylabel('Amplitude', color='#E2E8F0')
        self.ax.grid(True, color='#4A5568', alpha=0.3)
        self.canvas.draw()

class SpectrogramVisualizer(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setup_ui()

    def setup_ui(self):
        layout = QVBoxLayout(self)
        
        self.figure, self.ax = plt.subplots(figsize=(8, 4))
        self.canvas = FigureCanvas(self.figure)
        layout.addWidget(self.canvas)

        # Set dark theme
        self.figure.patch.set_facecolor('#1A365D')
        self.ax.set_facecolor('#2D3748')
        self.ax.tick_params(colors='#E2E8F0')
        for spine in self.ax.spines.values():
            spine.set_color('#4299E1')

    def plot_spectrogram(self, spec_data, sr):
        self.ax.clear()
        librosa.display.specshow(
            spec_data,
            sr=sr,
            x_axis='time',
            y_axis='hz',
            ax=self.ax,
            cmap='coolwarm'
        )
        self.ax.set_xlabel('Time', color='#E2E8F0')
        self.ax.set_ylabel('Frequency', color='#E2E8F0')
        self.canvas.draw()

class ComparisonVisualizer(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setup_ui()

    def setup_ui(self):
        layout = QVBoxLayout(self)
        
        self.figure, (self.ax1, self.ax2) = plt.subplots(2, 1, figsize=(8, 6))
        self.canvas = FigureCanvas(self.figure)
        layout.addWidget(self.canvas)

        # Set dark theme
        self.figure.patch.set_facecolor('#1A365D')
        for ax in [self.ax1, self.ax2]:
            ax.set_facecolor('#2D3748')
            ax.tick_params(colors='#E2E8F0')
            for spine in ax.spines.values():
                spine.set_color('#4299E1')

    def plot_comparison(self, spec1, spec2, sr, labels=('Target', 'Reference')):
        self.ax1.clear()
        self.ax2.clear()
        
        librosa.display.specshow(
            spec1,
            sr=sr,
            x_axis='time',
            y_axis='hz',
            ax=self.ax1,
            cmap='coolwarm'
        )
        self.ax1.set_title(labels[0], color='#E2E8F0')
        
        librosa.display.specshow(
            spec2,
            sr=sr,
            x_axis='time',
            y_axis='hz',
            ax=self.ax2,
            cmap='coolwarm'
        )
        self.ax2.set_title(labels[1], color='#E2E8F0')
        
        self.figure.tight_layout()
        self.canvas.draw()