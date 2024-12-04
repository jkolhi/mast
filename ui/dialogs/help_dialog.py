from PyQt5.QtWidgets import (
    QDialog, QVBoxLayout, QTextBrowser,
    QDialogButtonBox
)
from PyQt5.QtCore import Qt  # Add this import

class HelpDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowModality(Qt.NonModal)
        self.setWindowFlags(Qt.Window | Qt.WindowSystemMenuHint | Qt.WindowCloseButtonHint)
        self.initUI()
        
    def initUI(self):
        self.setWindowTitle('MAST - Help')
        self.setMinimumWidth(800)
        self.setMinimumHeight(600)

        layout = QVBoxLayout(self)

        help_text = QTextBrowser()
        help_text.setOpenExternalLinks(True)
        help_text.setHtml("""
            <h2 style='color: #63B3ED;'>MAST - Master Audio Similarity Tool</h2>
            
            <h3 style='color: #63B3ED;'>Overview</h3>
            <p>MAST is a professional audio tool that combines two powerful features:
            finding similar songs in your music collection and mastering your audio files to match the sound of reference tracks.</p>
            
            <h3 style='color: #63B3ED;'>Getting Started</h3>
            <p>First-time setup:</p>
            <ol>
                <li>Open Settings (⚙) and set your default music directory</li>
                <li>Configure your preferred audio output settings (format, bit depth, MP3 bitrate)</li>
                <li>Adjust similarity search settings to your needs</li>
            </ol>
            
            <h3 style='color: #63B3ED;'>Main Features</h3>
            
            <h4 style='color: #63B3ED;'>1. Audio Players</h4>
            <ul>
                <li>Two built-in audio players for easy comparison</li>
                <li>Independent volume controls for each track</li>
                <li>Instant playback of selected files</li>
                <li>Time display and seeking capability</li>
            </ul>
            
            <h4 style='color: #63B3ED;'>2. Finding Similar Songs</h4>
            <ol>
                <li>Select your reference track using "Select Song to Master"</li>
                <li>Ensure your music directory is set</li>
                <li>Click "Find Similar Songs"</li>
                <li>The results will show:
                    <ul>
                        <li>Songs sorted by similarity</li>
                        <li>Similarity score for each track</li>
                        <li>Double-click any song to view detailed metadata</li>
                    </ul>
                </li>
            </ol>
            
            <h4 style='color: #63B3ED;'>3. Audio Mastering</h4>
            <p>Two ways to master your audio:</p>
            <ol>
                <li>Direct Selection:
                    <ul>
                        <li>Select your song to master</li>
                        <li>Use "Select Reference Song" to choose your reference track</li>
                        <li>Click "Master Song"</li>
                    </ul>
                </li>
                <li>From Similarity Results:
                    <ul>
                        <li>Find similar songs first</li>
                        <li>Select a song from the results</li>
                        <li>Click "Use Selected as Reference"</li>
                        <li>Click "Master Song"</li>
                    </ul>
                </li>
            </ol>
            
            <h4 style='color: #63B3ED;'>4. Audio Analysis and Comparison</h4>
            <ul>
                <li>Click "Compare Songs" to see:
                    <ul>
                        <li>Waveform visualization</li>
                        <li>Spectrum analysis</li>
                        <li>Side-by-side comparison</li>
                        <li>Key and BPM information</li>
                    </ul>
                </li>
                <li>Double-click any song to view:
                    <ul>
                        <li>Detailed metadata</li>
                        <li>Technical information</li>
                        <li>Embedded artwork</li>
                    </ul>
                </li>
            </ul>

            <h3 style='color: #63B3ED;'>Tips for Best Results</h3>
            <ul>
                <li><b>Similarity Search:</b>
                    <ul>
                        <li>Use a high-quality reference track</li>
                        <li>Adjust similarity threshold in settings for broader or narrower results</li>
                        <li>Export results for later reference</li>
                    </ul>
                </li>
                <li><b>Mastering:</b>
                    <ul>
                        <li>Use reference tracks with similar genre/style</li>
                        <li>Compare before mastering using the analysis tools</li>
                        <li>Choose appropriate output formats for your needs</li>
                    </ul>
                </li>
                <li><b>File Management:</b>
                    <ul>
                        <li>Organize your music directory for faster searches</li>
                        <li>Use the comparison tool to verify results</li>
                        <li>Save your preferred settings for consistency</li>
                    </ul>
                </li>
            </ul>

            <h3 style='color: #63B3ED;'>Supported Audio Formats</h3>
            <ul>
                <li>WAV (16/24/32-bit)</li>
                <li>FLAC</li>
                <li>MP3</li>
                <li>AIFF</li>
                <li>OGG</li>
                <li>M4A</li>
            </ul>

            <h3 style='color: #63B3ED;'>Credits and Acknowledgments</h3>
            <p><b>Application:</b></p>
            <ul>
                <li><b>Created by:</b> JK</li>
                <li>UI implementation and program development</li>
                <li>Integration of audio processing libraries</li>
                <li>Original concept and design</li>
            </ul>

            <p><b>Built with:</b></p>
            <ul>
                <li><b>Matchering:</b> An open-source audio matching and mastering tool
                    <ul>
                        <li>Created by Sergree (<a href="https://github.com/sergree/matchering" style="color: #63B3ED;">https://github.com/sergree/matchering</a>)</li>
                        <li>License: GPL-3.0</li>
                        <li>A powerful library that enables reference audio matching and mastering</li>
                    </ul>
                </li>
                <li><b>Librosa:</b> Audio and music processing library</li>
                <li><b>PyQt5:</b> GUI framework</li>
            </ul>

            <p><b>Development Assistance:</b></p>
            <ul>
                <li>Interface design and programming assistance by Claude (Anthropic)</li>
                <li>Built to provide an intuitive interface for audio similarity analysis and mastering</li>
            </ul>
        """)
        
        layout.addWidget(help_text)

        button_box = QDialogButtonBox(QDialogButtonBox.Ok)
        button_box.accepted.connect(self.accept)
        layout.addWidget(button_box)
        
        # Apply dark theme
        self.setStyleSheet("""
            QDialog {
                background-color: #1A365D;
            }
            QTextBrowser {
                background-color: #2D3748;
                color: #E2E8F0;
                border: none;
                font-size: 13px;
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
        """)