# Application information
APP_NAME = "MAST"
ORGANIZATION_NAME = "JK"
VERSION = "1.0.0"

# Audio processing settings
SUPPORTED_FORMATS = ['.mp3', '.wav', '.aif', '.flac', '.m4a', '.ogg']
DEFAULT_SAMPLE_RATE = 44100
MAX_ANALYSIS_DURATION = 30  # seconds for similarity analysis

# UI Settings
DEFAULT_WINDOW_SIZE = (800, 600)
DEFAULT_WINDOW_POSITION = (100, 100)

# Analysis Settings
DEFAULT_SIMILARITY_THRESHOLD = 0.5
DEFAULT_MAX_RESULTS = 50

# Processing Settings
DEFAULT_OUTPUT_FORMAT = 'WAV'
DEFAULT_BIT_DEPTH = '24-bit PCM'
DEFAULT_MP3_BITRATE = '320k'

# File paths
import os
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_DIR = os.path.join(BASE_DIR, 'data')
PRESETS_DIR = os.path.join(DATA_DIR, 'presets')

# Create directories if they don't exist
for directory in [DATA_DIR, PRESETS_DIR]:
    if not os.path.exists(directory):
        os.makedirs(directory)