from PyQt5.QtWidgets import QWidget, QVBoxLayout
from PyQt5.QtCore import Qt
import matplotlib.pyplot as plt
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
import numpy as np

class WaveformViewer(QWidget):
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
        self.ax.spines['bottom'].set_color('#4299E1')
        self.ax.spines['top'].set_color('#4299E1') 
        self.ax.spines['right'].set_color('#4299E1')
        self.ax.spines['left'].set_color('#4299E1')
        
        # Set labels
        self.ax.set_xlabel('Time (s)', color='#E2E8F0')
        self.ax.set_ylabel('Amplitude', color='#E2E8F0')

    def plot_waveform(self, audio_data, sample_rate):
        self.ax.clear()
        time = np.arange(len(audio_data)) / sample_rate
        self.ax.plot(time, audio_data, color='#4299E1', linewidth=0.5)
        self.ax.set_xlabel('Time (s)', color='#E2E8F0')
        self.ax.set_ylabel('Amplitude', color='#E2E8F0')
        self.ax.grid(True, color='#4A5568', alpha=0.3)
        self.canvas.draw()

    def clear(self):
        self.ax.clear()
        self.canvas.draw()