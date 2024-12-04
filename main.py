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
    app = QApplication(sys.argv)
    app.setStyle('Fusion')
    
    # Create and show splash screen
    splash = CustomSplashScreen()
    splash.show()
    app.processEvents()
    
    # Initialize main window
    window = MASTWindow()
    
    # Hide splash and show window
    window.show()
    splash.finish(window)
    
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()