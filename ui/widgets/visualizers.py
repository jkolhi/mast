from PyQt5.QtWidgets import QWidget, QVBoxLayout
import matplotlib.pyplot as plt
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg
import numpy as np
import librosa
import librosa.display

class WaveformVisualizer(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.figure, self.ax = plt.subplots()
        self.canvas = FigureCanvasQTAgg(self.figure)
        layout = QVBoxLayout()
        layout.addWidget(self.canvas)
        self.setLayout(layout)
        self._style_plot()

    def _style_plot(self):
        self.figure.patch.set_facecolor('#1A365D')
        self.ax.set_facecolor('#2D3748')
        self.ax.tick_params(colors='#E2E8F0', labelsize=8)
        self.ax.set_xlabel('Time (s)', color='#E2E8F0')
        self.ax.set_ylabel('Amplitude', color='#E2E8F0')
        for spine in self.ax.spines.values():
            spine.set_color('#4299E1')
        self.figure.tight_layout()

    def plot_waveform(self, audio_data, sr):
        self.ax.clear()
        times = np.linspace(0, len(audio_data)/sr, len(audio_data))
        self.ax.plot(times, audio_data, color='#4299E1', linewidth=0.5)
        self._style_plot()
        self.canvas.draw()
        
    def clear(self):
        self.ax.clear()
        self._style_plot()
        self.canvas.draw()

class SpectrogramVisualizer(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.figure, self.ax = plt.subplots()
        self.canvas = FigureCanvasQTAgg(self.figure)
        layout = QVBoxLayout()
        layout.addWidget(self.canvas)
        self.setLayout(layout)
        self._style_plot()

    def _style_plot(self):
        self.figure.patch.set_facecolor('#1A365D')
        self.ax.set_facecolor('#2D3748')
        self.ax.tick_params(colors='#E2E8F0', labelsize=8)
        self.ax.set_xlabel('Time', color='#E2E8F0')
        self.ax.set_ylabel('Frequency (Hz)', color='#E2E8F0')
        for spine in self.ax.spines.values():
            spine.set_color('#4299E1')
        self.figure.tight_layout()

    def plot_spectrogram(self, spec_data, sr):
        self.ax.clear()
        img = librosa.display.specshow(
            spec_data,
            sr=sr,
            x_axis='time',
            y_axis='hz',
            ax=self.ax,
            cmap='coolwarm'
        )
        # Remove previous colorbars if they exist
        if hasattr(self, 'colorbar'):
            self.colorbar.remove()
        self.colorbar = self.figure.colorbar(img, ax=self.ax, format='%+2.0f dB')
        self._style_plot()
        self.canvas.draw()
                
    def clear(self):
        self.ax.clear()
        self._style_plot()
        self.canvas.draw()

class ComparisonVisualizer(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.figure, (self.ax1, self.ax2) = plt.subplots(2, 1, figsize=(8, 6))
        self.canvas = FigureCanvasQTAgg(self.figure)
        layout = QVBoxLayout()
        layout.addWidget(self.canvas)
        self.setLayout(layout)
        self._style_plot()

    def _style_plot(self):
        self.figure.patch.set_facecolor('#1A365D')
        for ax in [self.ax1, self.ax2]:
            ax.set_facecolor('#2D3748')
            ax.tick_params(colors='#E2E8F0', labelsize=8)
            ax.set_xlabel('Time', color='#E2E8F0')
            ax.set_ylabel('Hz', color='#E2E8F0')
            for spine in ax.spines.values():
                spine.set_color('#4299E1')
        self.figure.tight_layout()

    def plot_comparison(self, spec1, spec2, sr, labels=('Target', 'Reference')):
        self.ax1.clear()
        self.ax2.clear()
        
        img1 = librosa.display.specshow(
            spec1,
            sr=sr,
            x_axis='time',
            y_axis='hz',
            ax=self.ax1,
            cmap='coolwarm'
        )
        self.figure.colorbar(img1, ax=self.ax1, format='%+2.0f dB')
        self.ax1.set_title(labels[0], color='#E2E8F0')
        
        img2 = librosa.display.specshow(
            spec2,
            sr=sr,
            x_axis='time',
            y_axis='hz',
            ax=self.ax2,
            cmap='coolwarm'
        )
        self.figure.colorbar(img2, ax=self.ax2, format='%+2.0f dB')
        self.ax2.set_title(labels[1], color='#E2E8F0')
        
        self._style_plot()
        self.canvas.draw()
        
    def clear(self):
        self.ax1.clear()
        self.ax2.clear()
        self._style_plot()
        self.canvas.draw()