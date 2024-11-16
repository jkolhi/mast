from PyQt5.QtCore import QThread, pyqtSignal
import matchering as mg
from pathlib import Path

class MasteringThread(QThread):
    progress_updated = pyqtSignal(int)
    error_occurred = pyqtSignal(str)
    
    def __init__(self, target_path, reference_path, output_path, options):
        super().__init__()
        self.target_path = target_path
        self.reference_path = reference_path
        self.output_path = output_path
        self.options = options

    def run(self):
        try:
            self.progress_updated.emit(10)
            
            from matchering import Result
            
            # Configure Result based on format options
            format_ext = self.options['format']
            subtype = self.options['subtype']
            
            if format_ext == 'mp3':
                # Handle MP3 format (no subtype needed)
                result = Result(self.output_path)
            else:
                # Handle WAV/FLAC with subtype
                result = Result(self.output_path, subtype=subtype)
            
            mg.process(
                target=self.target_path,
                reference=self.reference_path,
                results=[result]
            )
            
            self.progress_updated.emit(100)

        except Exception as e:
            print(f"Matchering error details: {str(e)}")
            import traceback
            traceback.print_exc()
            self.error_occurred.emit(str(e))