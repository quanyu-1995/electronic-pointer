import os
from datetime import datetime
from PyQt6.QtWidgets import QApplication
from PyQt6.QtCore import QRect
from PyQt6.QtGui import QPixmap, QScreen

class ScreenshotManager:
    def __init__(self, save_path=None):
        if save_path is None:
            save_path = os.path.expanduser("~/Desktop/Screenshots")
        self.save_path = save_path
        self._ensure_directory()
        
    def _ensure_directory(self):
        if not os.path.exists(self.save_path):
            os.makedirs(self.save_path)
            
    def save_screenshot(self, canvas, filename=None):
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        if filename is None:
            filename = f"screenshot_{timestamp}.png"
            
        filepath = os.path.join(self.save_path, filename)
        
        pixmap = canvas.grab()
        pixmap.save(filepath)
        
        return filepath
