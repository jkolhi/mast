import librosa
import numpy as np
import scipy.spatial.distance as distance
from PyQt5.QtCore import QThread, pyqtSignal
import os

def extract_audio_embedding(file_path, max_length=128):
    try:
        y, sr = librosa.load(file_path, duration=30)
        mel_spec = librosa.feature.melspectrogram(y=y, sr=sr)
        mel_spec = librosa.power_to_db(mel_spec)
        
        if mel_spec.shape[1] > max_length:
            mel_spec = mel_spec[:, :max_length]
        else:
            pad_width = max_length - mel_spec.shape[1]
            mel_spec = np.pad(mel_spec, ((0,0),(0,pad_width)), mode='constant')
        
        embedding = mel_spec.flatten()
        return embedding / np.linalg.norm(embedding)
    except Exception as e:
        print(f"Error processing {file_path}: {e}")
        return None

def calculate_song_similarity(embedding1, embedding2, method='cosine'):
    if embedding1 is None or embedding2 is None:
        return None
    
    if method == 'cosine':
        return distance.cosine(embedding1, embedding2)
    elif method == 'euclidean':
        return distance.euclidean(embedding1, embedding2)

class AudioAnalyzer:
    """Advanced audio analysis features"""
    def __init__(self):
        self._audio = None
        self._sr = None

    def load_audio(self, file_path):
        try:
            self._audio, self._sr = librosa.load(file_path)
            return True
        except Exception as e:
            print(f"Error loading audio: {str(e)}")
            return False

    def analyze_audio(self, file_path):
        """Perform complete audio analysis"""
        if not self.load_audio(file_path):
            return None

        try:
            analysis = {}
            
            # Basic properties
            analysis['duration'] = librosa.get_duration(y=self._audio, sr=self._sr)

            # BPM Detection
            tempo, beats = librosa.beat.beat_track(y=self._audio, sr=self._sr)
            analysis['bpm'] = float(tempo)
            analysis['beats'] = beats

            # Key Detection
            key, scale = self._detect_key()
            analysis['key'] = key
            analysis['scale'] = scale

            # Loudness Analysis
            rms = librosa.feature.rms(y=self._audio)[0]
            analysis['loudness'] = {
                'mean': float(np.mean(rms)),
                'max': float(np.max(rms)),
                'min': float(np.min(rms)),
                'dynamic_range': float(np.max(rms) - np.min(rms))
            }

            # Spectral Analysis
            spec = np.abs(librosa.stft(self._audio))
            analysis['spectrogram'] = librosa.amplitude_to_db(spec, ref=np.max)

            # Waveform
            analysis['waveform'] = self._audio
            analysis['sample_rate'] = self._sr

            return analysis

        except Exception as e:
            print(f"Error during analysis: {str(e)}")
            return None

    def _detect_key(self):
        """Detect musical key and scale"""
        chroma = librosa.feature.chroma_cqt(y=self._audio, sr=self._sr)
        chroma_avg = np.mean(chroma, axis=1)
        keys = ['C', 'C#', 'D', 'D#', 'E', 'F', 'F#', 'G', 'G#', 'A', 'A#', 'B']
        key_index = np.argmax(chroma_avg)
        
        # Simple major/minor detection
        major_profile = np.array([1, 0, 1, 0, 1, 1, 0, 1, 0, 1, 0, 1])
        minor_profile = np.array([1, 0, 1, 1, 0, 1, 0, 1, 1, 0, 1, 0])
        
        # Rotate profiles to match detected key
        major_profile = np.roll(major_profile, key_index)
        minor_profile = np.roll(minor_profile, key_index)
        
        # Compare correlations
        major_corr = np.corrcoef(chroma_avg, major_profile)[0,1]
        minor_corr = np.corrcoef(chroma_avg, minor_profile)[0,1]
        
        scale = 'major' if major_corr > minor_corr else 'minor'
        return keys[key_index], scale

    def get_waveform_data(self):
        return self._audio, self._sr if self._audio is not None else (None, None)

    def get_spectrum_data(self):
        if self._audio is None:
            return None
        spec = np.abs(librosa.stft(self._audio))
        return librosa.amplitude_to_db(spec, ref=np.max)

class SimilarityThread(QThread):
    update_progress = pyqtSignal(int)
    comparison_complete = pyqtSignal(dict)
    error_occurred = pyqtSignal(str)

    def __init__(self, reference_song, directory, threshold=0.5, max_results=50):
        super().__init__()
        self.reference_song = reference_song
        self.directory = directory
        self.threshold = threshold
        self.max_results = max_results

    def run(self):
        try:
            reference_embedding = extract_audio_embedding(self.reference_song)
            if reference_embedding is None:
                self.error_occurred.emit(f"Could not extract embedding for {self.reference_song}")
                return

            song_files = self._find_audio_files(self.directory)
            song_files = [f for f in song_files if os.path.abspath(f) != os.path.abspath(self.reference_song)]

            similarities = {}
            total_files = len(song_files)

            for i, other_song_path in enumerate(song_files):
                try:
                    other_embedding = extract_audio_embedding(other_song_path)
                    if other_embedding is not None:
                        similarity = calculate_song_similarity(reference_embedding, other_embedding)
                        if similarity <= self.threshold:
                            similarities[other_song_path] = similarity
                    
                    progress = int(((i + 1) / total_files) * 100)
                    self.update_progress.emit(progress)

                except Exception as e:
                    print(f"Error processing {other_song_path}: {e}")

            sorted_similarities = dict(
                sorted(similarities.items(), key=lambda x: x[1])[:self.max_results]
            )
            self.comparison_complete.emit(sorted_similarities)

        except Exception as e:
            self.error_occurred.emit(str(e))

    def _find_audio_files(self, directory):
        supported_formats = ['.mp3', '.wav', '.aif', '.flac', '.m4a', '.ogg']
        audio_files = []
        
        for root, dirs, files in os.walk(directory):
            for file in files:
                if os.path.splitext(file)[1].lower() in supported_formats:
                    audio_files.append(os.path.join(root, file))
        
        return audio_files