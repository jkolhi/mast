import sys
from PyQt5.QtWidgets import QApplication
from PyQt5.QtCore import QSettings
from ui.main_window import MASTWindow

def main():
    app = QApplication(sys.argv)
    
    # Initialize application settings
    app.setApplicationName("MAST")
    app.setOrganizationName("JK")
    
    # Set application style
    app.setStyle('Fusion')
    
    # Create and show the main window
    window = MASTWindow()
    window.show()
    
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()