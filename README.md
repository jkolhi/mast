# MAST - Master Audio Similarity Tool

MAST is a powerful audio analysis and mastering application that helps you find similar songs in your music collection and master your audio files to match the sound of reference tracks.

## Features

- Audio similarity analysis
- Reference-based audio mastering
- Detailed audio analysis (BPM, key, spectrum)
- Batch processing capabilities
- Metadata viewing and editing
- Built-in audio visualization
- High-quality audio resampling
- Noise reduction and audio enhancement
- Customizable mastering presets

## Installation

```bash
# Clone the repository
git clone https://github.com/yourusername/mast.git
cd mast

# Create and activate a virtual environment (recommended)
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install the package
pip install -e .
```

## Usage

```bash
# Run the application
mast
```

## Building a macOS App

To build a standalone macOS application, run the provided `build_macos.sh` script:

```bash
./build_macos.sh
```

The built app will be located in the `dist` directory.

## Requirements

- Python 3.8 or higher
- PyQt5
- librosa
- matchering
- Additional dependencies are listed in requirements.txt

## Credits

- Created by JK
- Using Matchering by Sergree
- Interface assistance by Claude (Anthropic)

## License

Apache License 2.0
