import librosa
import numpy as np
import librosa.display
import matplotlib.pyplot as plt
from PyQt5.QtCore import QObject, pyqtSignal

class AudioAnalyzer(QObject):
    """
    Core class for audio analysis functionality
    """
    analysis_complete = pyqtSignal(dict)
    error_occurred = pyqtSignal(str)
    progress_updated = pyqtSignal(int)

    def __init__(self):
        super().__init__()
        self.current_audio = None
        self.sr = None

    def load_audio(self, file_path):
        """Load audio file and prepare for analysis"""
        try:
            self.current_audio, self.sr = librosa.load(file_path)
            return True
        except Exception as e:
            self.error_occurred.emit(f"Error loading audio: {str(e)}")
            return False

    def analyze_audio(self, file_path):
        """Perform complete audio analysis"""
        if not self.load_audio(file_path):
            return

        try:
            analysis_results = {}
            
            # Basic audio properties
            analysis_results['duration'] = librosa.get_duration(y=self.current_audio, sr=self.sr)
            self.progress_updated.emit(20)

            # BPM detection
            tempo, _ = librosa.beat.beat_track(y=self.current_audio, sr=self.sr)
            analysis_results['bpm'] = float(tempo)
            self.progress_updated.emit(40)

            # Key detection
            chroma = librosa.feature.chroma_cqt(y=self.current_audio, sr=self.sr)
            key = self._estimate_key(chroma)
            analysis_results['key'] = key
            self.progress_updated.emit(60)

            # Loudness analysis
            rms = librosa.feature.rms(y=self.current_audio)
            analysis_results['average_loudness'] = float(np.mean(rms))
            analysis_results['peak_loudness'] = float(np.max(rms))
            self.progress_updated.emit(80)

            # Spectral analysis
            spectral_centroids = librosa.feature.spectral_centroid(y=self.current_audio, sr=self.sr)
            analysis_results['spectral_centroid'] = float(np.mean(spectral_centroids))

            self.progress_updated.emit(100)
            self.analysis_complete.emit(analysis_results)
            return analysis_results

        except Exception as e:
            self.error_occurred.emit(f"Error during analysis: {str(e)}")
            return None

    def get_waveform_data(self):
        """Generate waveform data for visualization"""
        if self.current_audio is None:
            return None
        return self.current_audio

    def get_spectrum_data(self):
        """Generate spectrum data for visualization"""
        if self.current_audio is None:
            return None
        D = librosa.stft(self.current_audio)
        S_db = librosa.amplitude_to_db(np.abs(D), ref=np.max)
        return S_db

    def _estimate_key(self, chroma):
        """Estimate musical key from chroma features"""
        keys = ['C', 'C#', 'D', 'D#', 'E', 'F', 'F#', 'G', 'G#', 'A', 'A#', 'B']
        chroma_avg = np.mean(chroma, axis=1)
        key_index = np.argmax(chroma_avg)
        return keys[key_index]

    def detect_clipping(self, threshold=0.99):
        """Check for potential clipping in the audio"""
        if self.current_audio is None:
            return False
        return np.any(np.abs(self.current_audio) > threshold)

    def get_stereo_info(self):
        """Analyze stereo field information"""
        if self.current_audio is None:
            return None
        
        if len(self.current_audio.shape) == 1:
            return {"type": "mono"}
        
        # For stereo audio
        left = self.current_audio[0]
        right = self.current_audio[1]
        correlation = np.corrcoef(left, right)[0,1]
        
        return {
            "type": "stereo",
            "correlation": correlation,
            "balance": np.mean(np.abs(left)) / np.mean(np.abs(right))
        }