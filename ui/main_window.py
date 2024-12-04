from PyQt5.QtWidgets import (
    QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, 
    QPushButton, QLabel, QListWidget, QFileDialog, 
    QProgressBar, QMessageBox, QStyle, QListWidgetItem,
    QMenuBar, QDialog, QGroupBox
)
from PyQt5.QtCore import Qt, QSettings
from PyQt5.QtGui import QIcon, QPixmap
import os
import sys
import csv
from datetime import datetime
from pathlib import Path
import tempfile
import subprocess

from ui.dialogs.settings_dialog import SettingsDialog
from ui.dialogs.help_dialog import HelpDialog
from ui.dialogs.details_dialog import SongDetailsDialog
from ui.dialogs.mastering_dialog import MasteringOptionsDialog
from ui.dialogs.comparison_dialog import AudioComparisonDialog
from ui.widgets.audio_player import AudioPlayer
from core.analyzer import SimilarityThread
from core.mastering import MasteringThread
from config.theme import COMBINED_STYLE

class MASTWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        # Initialize settings
        self.settings = QSettings('JK', 'MAST')
        
        # Initialize file paths
        self.song_to_master = None
        self.reference_song = None
        self.music_directory = self.settings.value('default_directory', None)
        
        # Initialize state variables
        self.current_similarities = {}
        self.open_dialogs = []
        
        # Initialize similarity options
        self.similarity_options = {
            'threshold': float(self.settings.value('similarity_threshold', 0.5)),
            'max_results': int(self.settings.value('max_results', 50))
        }
        
        # Initialize UI
        self.initUI()
        
        # Update directory label if default directory exists
        if self.music_directory:
            self.directory_label.setText(f'Selected: {self.music_directory}')

    def show_comparison_dialog(self):
        if not self.song_to_master:
            QMessageBox.warning(
                self,
                "Error",
                "Please select a song to master first"
            )
            return

        dialog = AudioComparisonDialog(
            file1_path=self.song_to_master,
            file2_path=self.reference_song if self.reference_song else None,
            parent=self
        )
        dialog.setAttribute(Qt.WA_DeleteOnClose)
        self.open_dialogs.append(dialog)
        dialog.show()

    def initUI(self):
        self.setWindowTitle('MAST - Master Audio Similarity Tool')
        self.setGeometry(100, 100, 800, 600)

        # Create central widget and main layout
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        layout = QVBoxLayout(central_widget)

        # Create menu bar
        menubar = self.menuBar()
        file_menu = menubar.addMenu('File')
        settings_action = file_menu.addAction('Settings')
        settings_action.triggered.connect(self.show_settings)

        # Top section with icon and buttons
        top_section = QHBoxLayout()
        
        # Create icon label
        icon_label = QLabel()
        svg_data = '''<?xml version="1.0" encoding="UTF-8"?>
        <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 100 100">
            <circle cx="50" cy="50" r="45" fill="#1A365D"/>
            <path d="M30 50 Q40 20, 50 50 T70 50" 
                  fill="none" 
                  stroke="#4299E1" 
                  stroke-width="4"
                  stroke-linecap="round"/>
            <path d="M25 50 Q40 10, 50 50 T75 50" 
                  fill="none" 
                  stroke="#63B3ED" 
                  stroke-width="3"
                  stroke-linecap="round"/>
            <path d="M20 50 Q40 0, 50 50 T80 50" 
                  fill="none" 
                  stroke="#90CDF4" 
                  stroke-width="2"
                  stroke-linecap="round"/>
        </svg>'''
        
        # Create temporary file for the SVG
        with tempfile.NamedTemporaryFile(suffix='.svg', delete=False) as tmp_file:
            tmp_file.write(svg_data.encode())
            icon_path = tmp_file.name

        # Create QPixmap from the SVG and scale it
        pixmap = QIcon(icon_path).pixmap(50, 50)  # 50x50 pixels
        icon_label.setPixmap(pixmap)
        
        # Clean up temporary file
        os.unlink(icon_path)

        # Add icon to the left side
        top_section.addWidget(icon_label)
        
        # Add title next to icon
        title_label = QLabel('MAST - Master Audio Similarity Tool')
        title_label.setStyleSheet("""
            QLabel {
                font-size: 16px;
                font-weight: bold;
            }
        """)
        top_section.addWidget(title_label)
        
        # Add stretch to push buttons to the right
        top_section.addStretch()

        # Add Settings and Help buttons
        settings_btn = QPushButton('⚙ Settings')
        settings_btn.clicked.connect(self.show_settings)
        
        help_btn = QPushButton('❓ Help')
        help_btn.clicked.connect(self.show_help)
        
        top_section.addWidget(settings_btn)
        top_section.addWidget(help_btn)
        
        layout.addLayout(top_section)
        layout.addSpacing(10)

        # Song to master section with player
        master_group = QGroupBox("Song to Master")
        master_layout = QVBoxLayout()
        
        # File selection
        song_layout = QHBoxLayout()
        self.song_to_master_label = QLabel('No song selected')
        select_song_btn = QPushButton('Select Song')
        select_song_btn.clicked.connect(self.select_song_to_master)
        song_layout.addWidget(self.song_to_master_label)
        song_layout.addWidget(select_song_btn)
        master_layout.addLayout(song_layout)
        
        # Add player
        self.master_player = AudioPlayer()
        master_layout.addWidget(self.master_player)
        
        master_group.setLayout(master_layout)
        layout.addWidget(master_group)

        # Reference song section with player
        reference_group = QGroupBox("Reference Song")
        reference_layout = QVBoxLayout()
        
        # File selection
        ref_song_layout = QHBoxLayout()
        self.reference_song_label = QLabel('No reference song selected')
        select_ref_btn = QPushButton('Select Song')
        select_ref_btn.clicked.connect(self.select_reference_song)
        ref_song_layout.addWidget(self.reference_song_label)
        ref_song_layout.addWidget(select_ref_btn)
        reference_layout.addLayout(ref_song_layout)
        
        # Add player
        self.reference_player = AudioPlayer()
        reference_layout.addWidget(self.reference_player)
        
        reference_group.setLayout(reference_layout)
        layout.addWidget(reference_group)

        # Directory selection
        dir_layout = QHBoxLayout()
        self.directory_label = QLabel('No directory selected')
        select_dir_btn = QPushButton('Select Music Directory')
        select_dir_btn.clicked.connect(self.select_music_directory)
        dir_layout.addWidget(self.directory_label)
        dir_layout.addWidget(select_dir_btn)
        layout.addLayout(dir_layout)

        # Search controls
        button_layout = QHBoxLayout()
        compare_btn = QPushButton('Find Similar Songs')
        compare_btn.clicked.connect(self.start_comparison)
        button_layout.addWidget(compare_btn)
        layout.addLayout(button_layout)

        # Progress bar
        self.progress_bar = QProgressBar()
        layout.addWidget(self.progress_bar)

        # Results list
        self.similar_songs_list = QListWidget()
        layout.addWidget(self.similar_songs_list)

        # Control buttons
        controls_layout = QHBoxLayout()
        
        self.use_as_reference_button = QPushButton('Use Selected as Reference')
        self.use_as_reference_button.clicked.connect(self.use_selected_as_reference)
        self.use_as_reference_button.setEnabled(False)
        controls_layout.addWidget(self.use_as_reference_button)

        self.master_button = QPushButton('Master Song')
        self.master_button.clicked.connect(self.master_with_reference)
        self.master_button.setEnabled(False)
        controls_layout.addWidget(self.master_button)

        compare_button = QPushButton('Compare Songs')
        compare_button.clicked.connect(self.show_comparison_dialog)
        controls_layout.addWidget(compare_button)

        layout.addLayout(controls_layout)

        # Mastering progress
        self.mastering_progress = QProgressBar()
        self.mastering_progress.hide()
        layout.addWidget(self.mastering_progress)

        # Export button
        export_btn = QPushButton('Export Results')
        export_btn.clicked.connect(self.export_results)
        layout.addWidget(export_btn)

        # Apply style
        self.setStyleSheet(COMBINED_STYLE)

    def select_song_to_master(self):
        file_path, _ = QFileDialog.getOpenFileName(
            self, 'Select Song to Master', '',
            'Audio Files (*.mp3 *.wav *.aif *.flac *.m4a *.ogg)'
        )
        if file_path:
            self.song_to_master = file_path
            self.song_to_master_label.setText(f'Selected: {os.path.basename(file_path)}')
            self.master_player.loadFile(file_path)
            self.update_master_button()

    def select_reference_song(self):
        file_path, _ = QFileDialog.getOpenFileName(
            self, 'Select Reference Song', '',
            'Audio Files (*.mp3 *.wav *.aif *.flac *.m4a *.ogg)'
        )
        if file_path:
            self.reference_song = file_path
            self.reference_song_label.setText(f'Selected: {os.path.basename(file_path)}')
            self.reference_player.loadFile(file_path)
            self.update_master_button()

    def use_selected_as_reference(self):
        current_item = self.similar_songs_list.currentItem()
        if not current_item:
            return
            
        song_name = current_item.text().split(' (Similarity:')[0]
        for song_path in self.current_similarities.keys():
            if os.path.basename(song_path) == song_name:
                self.reference_song = song_path
                self.reference_song_label.setText(f'Selected: {os.path.basename(song_path)}')
                self.reference_player.loadFile(song_path)
                self.update_master_button()
                break
    def select_music_directory(self):
        directory = QFileDialog.getExistingDirectory(
            self, 'Select Music Directory',
            self.music_directory or ''
        )
        if directory:
            self.music_directory = directory
            self.directory_label.setText(f'Selected: {directory}')

    def show_audio_analysis(self):
        if not self.song_to_master:
            QMessageBox.warning(self, "Error", "Please select a song to analyze")
            return
            
        # Create analysis dialog with both songs if reference is selected
        if self.reference_song:
            dialog = AudioAnalysisDialog(
                file_path=self.song_to_master,
                reference_path=self.reference_song,
                parent=self
            )
        else:
            dialog = AudioAnalysisDialog(
                file_path=self.song_to_master,
                parent=self
            )
        
        dialog.setStyleSheet(self.styleSheet())
        dialog.exec_()    

    def update_song_to_master(self, file_path):
        self.song_to_master = file_path
        self.song_to_master_label.setText(f'Selected: {os.path.basename(file_path)}')
        self.update_master_button()

    def update_reference_song(self, file_path):
        self.reference_song = file_path
        self.reference_song_label.setText(f'Selected: {os.path.basename(file_path)}')
        self.update_master_button()

    def show_settings(self):
        dialog = SettingsDialog(self)  # Only pass parent parameter
        dialog.loadSettings(self.settings)  # Set settings separately
        dialog.setStyleSheet(self.styleSheet())
        if dialog.exec_() == QDialog.Accepted:
            dialog.save_settings()
            self.music_directory = self.settings.value('default_directory', None)
            if self.music_directory:
                self.directory_label.setText(f'Selected: {self.music_directory}')
            
            self.similarity_options = {
                'threshold': float(self.settings.value('similarity_threshold', 0.5)),
                'max_results': int(self.settings.value('max_results', 50))
            }     

    def show_help(self):
        dialog = HelpDialog(self)
        dialog.exec_()

    def show_similarity_options(self):
        dialog = SimilarityOptionsDialog(self)
        dialog.setStyleSheet(self.styleSheet())  # Apply the same dark theme
        
        # Set current values
        dialog.threshold_slider.setValue(int(self.similarity_options['threshold'] * 100))
        dialog.max_results_input.setText(str(self.similarity_options['max_results']))
        
        if dialog.exec_():
            self.similarity_options = dialog.get_options()

    def update_master_button(self):
        self.master_button.setEnabled(bool(self.song_to_master and self.reference_song))

    def update_play_button(self):
        has_selection = bool(self.similar_songs_list.currentItem())
        self.use_as_reference_button.setEnabled(has_selection)

    def start_comparison(self):
        if not self.song_to_master or not self.music_directory:
            QMessageBox.warning(self, "Error", "Please select both a song to master and a music directory")
            return

        self.similar_songs_list.clear()
        self.progress_bar.setValue(0)

        self.comparison_thread = SimilarityThread(
            self.song_to_master,
            self.music_directory,
            self.similarity_options['threshold'],
            self.similarity_options['max_results']
        )
        self.comparison_thread.update_progress.connect(self.progress_bar.setValue)
        self.comparison_thread.comparison_complete.connect(self.show_similar_songs)
        self.comparison_thread.error_occurred.connect(
            lambda msg: QMessageBox.critical(self, "Error", msg)
        )
        self.comparison_thread.start()

    def show_similar_songs(self, similarities):
        self.current_similarities = similarities
        self.similar_songs_list.clear()
        
        for song_path, similarity in similarities.items():
            item = QListWidgetItem(
                f"{os.path.basename(song_path)} (Similarity: {similarity:.4f})"
            )
            self.similar_songs_list.addItem(item)
        
        try:
            self.similar_songs_list.itemSelectionChanged.disconnect()
            self.similar_songs_list.itemDoubleClicked.disconnect()
        except:
            pass
            
        self.similar_songs_list.itemSelectionChanged.connect(self.update_play_button)
        self.similar_songs_list.itemDoubleClicked.connect(self.show_song_details)
      
    def use_selected_as_reference(self):
        current_item = self.similar_songs_list.currentItem()
        if not current_item:
            return
            
        song_name = current_item.text().split(' (Similarity:')[0]
        for song_path in self.current_similarities.keys():
            if os.path.basename(song_path) == song_name:
                self.reference_song = song_path
                self.reference_song_label.setText(f'Selected: {os.path.basename(song_path)}')
                self.update_master_button()
                break

    def play_selected_song(self):
        current_item = self.similar_songs_list.currentItem()
        if not current_item:
            return
            
        song_name = current_item.text().split(' (Similarity:')[0]
        for song_path in self.current_similarities.keys():
            if os.path.basename(song_path) == song_name:
                try:
                    if sys.platform.startswith('darwin'):  # macOS
                        subprocess.call(('open', song_path))
                    elif sys.platform.startswith('win'):   # Windows
                        os.startfile(song_path)
                    else:                                  # Linux
                        subprocess.call(('xdg-open', song_path))
                except Exception as e:
                    QMessageBox.warning(
                        self,
                        "Playback Error",
                        f"Could not play file: {str(e)}"
                    )
                break

    def show_song_details(self, item):
        song_name = item.text().split(' (Similarity:')[0]
        for song_path in self.current_similarities.keys():
            if os.path.basename(song_path) == song_name:
                dialog = SongDetailsDialog(self)  # Pass only parent
                dialog.setStyleSheet(self.styleSheet())
                dialog.loadSong(song_path)  # Load song path separately
                break

    def update_mastering_progress(self, value):
        self.mastering_progress.setValue(value)

    def show_mastering_error(self, error_message):
        QMessageBox.critical(
            self,
            "Mastering Error",
            f"An error occurred during mastering:\n{error_message}"
        )
        self.mastering_progress.hide()
        self.update_play_button()

    def mastering_finished(self):
        self.update_play_button()
        self.mastering_progress.hide()
        
        output_path = str(Path(self.song_to_master).parent)
        
        # Show completion message
        QMessageBox.information(
            self,
            "Mastering Complete",
            f"The mastered track has been saved in:\n{output_path}"
        )
        
        # Show song details dialog for the mastered file
        if hasattr(self, 'mastering_thread') and hasattr(self.mastering_thread, 'output_path'):
            dialog = SongDetailsDialog(self)
            dialog.setStyleSheet(self.styleSheet())
            dialog.loadSong(str(self.mastering_thread.output_path))

    def master_with_reference(self):
        if not self.song_to_master or not self.reference_song:
            QMessageBox.warning(
                self,
                "Selection Required",
                "Please select both a song to master and a reference song."
            )
            return

        # Show mastering options dialog with filenames
        target_name = Path(self.song_to_master).stem
        reference_name = Path(self.reference_song).stem
        options_dialog = MasteringOptionsDialog(target_name, reference_name, self)
        options_dialog.setStyleSheet(self.styleSheet())

        # Set default values from settings
        options_dialog.format_combo.setCurrentText(self.settings.value('default_format', 'WAV'))
        options_dialog.bitdepth_combo.setCurrentText(self.settings.value('default_bitdepth', '24-bit PCM'))
        options_dialog.mp3_bitrate_combo.setCurrentText(self.settings.value('default_bitrate', '320k'))

        if not options_dialog.exec_():
            return
        
        mastering_options = options_dialog.get_options()
        
        # Create output path
        target_path = Path(self.song_to_master)
        reference_path = Path(self.reference_song)
        
        # Format filename using pattern
        filename_vars = {
            'target': target_path.stem,
            'reference': reference_path.stem,
            'date': datetime.now().strftime('%Y%m%d'),
            'time': datetime.now().strftime('%H%M%S')
        }
        
        output_filename = mastering_options['naming_pattern'].format(**filename_vars)
        output_filename = f"{output_filename}.{mastering_options['format']}"
        
        if mastering_options['output_dir']:
            output_path = Path(mastering_options['output_dir']) / output_filename
        else:
            output_path = target_path.parent / output_filename

        msg = QMessageBox()
        msg.setIcon(QMessageBox.Question)
        msg.setText("Start Mastering Process")
        msg.setInformativeText(
            f"Target: {target_path.name}\n"
            f"Reference: {reference_path.name}\n"
            f"Output: {output_filename}\n"
            f"Format: {mastering_options['format'].upper()}\n"
            f"{'Bitrate: ' + mastering_options['mp3_bitrate'] if mastering_options['format'] == 'mp3' else 'Subtype: ' + (mastering_options['subtype'] or 'Default')}\n\n"
            "Do you want to continue?"
        )
        msg.setStandardButtons(QMessageBox.Yes | QMessageBox.No)
        msg.setDefaultButton(QMessageBox.Yes)
        msg.setStyleSheet(self.styleSheet())
        
        if msg.exec_() != QMessageBox.Yes:
            return

        # Show mastering progress
        self.mastering_progress.show()
        self.mastering_progress.setValue(0)
        
        # Disable buttons during processing
        self.master_button.setEnabled(False)
        self.use_as_reference_button.setEnabled(False)

        # Create and start mastering thread
        self.mastering_thread = MasteringThread(
            target_path=str(target_path),
            reference_path=str(reference_path),
            output_path=str(output_path),
            options=mastering_options
        )
        self.mastering_thread.progress_updated.connect(self.update_mastering_progress)
        self.mastering_thread.finished.connect(self.mastering_finished)
        self.mastering_thread.error_occurred.connect(self.show_mastering_error)
        self.mastering_thread.start()    
        
    def export_results(self):
        if not self.current_similarities:
            QMessageBox.warning(self, "Export Failed", "No results to export")
            return

        file_path, _ = QFileDialog.getSaveFileName(
            self,
            'Export Results',
            f'mast_similarities_{datetime.now().strftime("%Y%m%d_%H%M%S")}.csv',
            'CSV Files (*.csv)'
        )

        if file_path:
            try:
                with open(file_path, 'w', newline='', encoding='utf-8') as f:
                    writer = csv.writer(f)
                    writer.writerow([
                        'Reference Song', 
                        'Reference Full Path', 
                        'Compared Song', 
                        'Compared Full Path', 
                        'Similarity Score'
                    ])
                    ref_name = os.path.basename(self.song_to_master)
                    for song_path, similarity in self.current_similarities.items():
                        writer.writerow([
                            ref_name,
                            self.song_to_master,
                            os.path.basename(song_path),
                            song_path,
                            f"{similarity:.4f}"
                        ])
                QMessageBox.information(
                    self,
                    "Success",
                    f"Results exported to {file_path}"
                )
            except Exception as e:
                QMessageBox.critical(
                    self,
                    "Export Failed",
                    f"Error exporting results: {str(e)}"
                )
