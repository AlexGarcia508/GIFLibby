import sys
from PySide6.QtWidgets import QApplication
from gui.main_window import MainWindow

# Start the PySide application
app = QApplication(sys.argv)

# Create and show the main window
window = MainWindow()
window.show()

# Keep the application running
sys.exit(app.exec())