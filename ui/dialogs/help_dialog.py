from PyQt5.QtWidgets import (
    QDialog, QVBoxLayout, QTextBrowser,
    QDialogButtonBox
)

class HelpDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.initUI()

    def initUI(self):
        self.setWindowTitle('MAST - Help')
        self.setMinimumWidth(600)
        self.setMinimumHeight(400)

        # Apply dark theme
        self.setStyleSheet("""
            QDialog, QWidget {
                background-color: #1A365D;
            }
            QLabel {
                color: #E2E8F0;
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
            QScrollArea {
                border: 1px solid #4299E1;
                border-radius: 4px;
            }
            QTextBrowser {
                background-color: #2D3748;
                color: #E2E8F0;
                border: none;
                font-size: 13px;
            }
        """)

        layout = QVBoxLayout(self)

        # Create a QTextBrowser for the help content
        help_text = QTextBrowser()
        help_text.setOpenExternalLinks(True)
        help_text.setHtml("""
            <h2 style='color: #63B3ED;'>MAST - Master Audio Similarity Tool</h2>
            
            <h3 style='color: #63B3ED;'>Overview</h3>
            <p>MAST helps you find similar songs in your music collection and master your audio files to match the sound of reference tracks.</p>
            
            <h3 style='color: #63B3ED;'>Main Features</h3>
            <ul>
                <li><b>Song Similarity Search:</b> Find songs that sound similar to your selected track using audio analysis</li>
                <li><b>Audio Mastering:</b> Match the sound characteristics of one song to another using the Matchering engine</li>
                <li><b>Metadata Viewing:</b> View detailed song information including embedded artwork</li>
            </ul>
            
            <h3 style='color: #63B3ED;'>How to Use</h3>
            <ol>
                <li><b>Finding Similar Songs:</b>
                    <ul>
                        <li>Click "Select Song to Master" to choose your reference track</li>
                        <li>Set your music directory (or use the default from settings)</li>
                        <li>Click "Find Similar Songs" to start the search</li>
                        <li>Results will be shown in the list, sorted by similarity</li>
                    </ul>
                </li>
                <br>
                <li><b>Mastering a Song:</b>
                    <ul>
                        <li>Select your target song using "Select Song to Master"</li>
                        <li>Choose a reference song either by:
                            <ul>
                                <li>Using "Select Reference Song" button</li>
                                <li>Selecting a song from the similarity results and clicking "Use Selected as Reference"</li>
                            </ul>
                        </li>
                        <li>Click "Master Song" to start the mastering process</li>
                        <li>Choose your desired output format and settings</li>
                    </ul>
                </li>
            </ol>
            
            <h3 style='color: #63B3ED;'>Audio Formats</h3>
            <p>Supported formats:</p>
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

            <h3 style='color: #63B3ED;'>Tips</h3>
            <ul>
                <li>Use the Settings dialog to set your default preferences</li>
                <li>You can play any song in the results list by selecting it and clicking "Play Selected"</li>
                <li>Export your similarity search results using the "Export Results" button</li>
                <li>Double-click any song in the list to see detailed information and artwork</li>
                <li>The mastered song will automatically open in the details viewer when complete</li>
            </ul>
        """)
        
        layout.addWidget(help_text)

        # Add OK button
        button_box = QDialogButtonBox(QDialogButtonBox.Ok)
        button_box.accepted.connect(self.accept)
        layout.addWidget(button_box)