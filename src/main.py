"""
Tolerance Chain Visualizer
Entry point for the application
"""

import sys
import os
from pathlib import Path

current_dir = Path(__file__).parent
src_dir = current_dir / "src"
sys.path.insert(0, str(src_dir))

# Import after path setup
from PySide6.QtWidgets import QApplication
from PySide6.QtCore import Qt
from ui.main_window import MainWindow

def main():
    """Main application entry point."""

    #Enable high DPI support
    """
    Initializes the main application entry point and enables high DPI (Dots Per Inch) support for better display scaling.
    Sets Qt application attributes to ensure proper rendering on high-resolution screens:
    - Qt.AA_EnableHighDpiScaling: Enables automatic scaling of UI elements for high DPI displays.
    - Qt.AA_UseHighDpiPixmaps: Ensures pixmaps are rendered at high resolution on high DPI screens.
    """
    QApplication.setAttribute(Qt.AA_EnableHighDpiScaling, True)
    QApplication.setAttribute(Qt.AA_UseHighDpiPixmaps, True)

    #Create application
    app = QApplication(sys.argv)
    app.setApplicationName("Tolerance Chain Visualizer")

    #Create main window
    window = MainWindow()
    window.show()

    #Start event loop
    sys.exit(app.exec())

if __name__ == "__main__":
    main()