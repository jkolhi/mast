import sys
from PyQt5.QtWidgets import QApplication, QSplashScreen, QLabel
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPixmap, QColor
from ui.main_window import MASTWindow

class CustomSplashScreen(QSplashScreen):
    def __init__(self):
        # Create blank pixmap
        pixmap = QPixmap(400, 200)
        pixmap.fill(QColor("#1A365D"))
        super().__init__(pixmap)

        # Add text label
        self.label = QLabel("MAST\nLoading...", self)
        self.label.setStyleSheet("""
            QLabel {
                color: #E2E8F0;
                font-size: 24px;
                font-weight: bold;
            }
        """)
        self.label.setAlignment(Qt.AlignCenter)
        self.label.resize(400, 200)

def main():
    try:
        print("Starting application...")
        app = QApplication(sys.argv)
        print("QApplication created")
        app.setStyle('Fusion')
        print("Style set")
        
        # Create and show splash screen
        splash = CustomSplashScreen()
        print("Splash screen created")
        splash.show()
        print("Splash screen shown")
        app.processEvents()
        
        print("Initializing main window...")
        # Initialize main window
        window = MASTWindow()
        print("Main window created")
        
        # Hide splash and show window
        window.show()
        print("Main window shown")
        splash.finish(window)
        
        print("Starting event loop...")
        # Start the event loop
        return app.exec_()
    except Exception as e:
        print(f"Error occurred: {str(e)}")
        import traceback
        traceback.print_exc()
        return 1

if __name__ == '__main__':
    sys.exit(main())