from PyQt6.QtCore import QPoint, QRect
from PyQt6.QtGui import QPainter, QScreen
from PyQt6.QtWidgets import QApplication
from .base_tool import BaseTool


class MagnifierTool(BaseTool):
    def __init__(self, canvas, zoom_factor: float = 2.0, window_size: int = 200):
        super().__init__(canvas)
        self.zoom_factor = zoom_factor
        self.window_size = window_size
        self._active = False
        self.magnifier_window = None
        
    def mouse_press(self, pos: QPoint):
        self._active = True
        self.current_pos = pos
        self._show_magnifier(pos)
        
    def mouse_move(self, pos: QPoint):
        if self._active:
            self.current_pos = pos
            self._update_magnifier(pos)
            
    def mouse_release(self, pos: QPoint):
        self._active = False
        self._hide_magnifier()
        
    def _show_magnifier(self, pos: QPoint):
        if self.magnifier_window:
            self.magnifier_window.show_at(pos)
            
    def _update_magnifier(self, pos: QPoint):
        if self.magnifier_window:
            self.magnifier_window.move_to(pos)
            
    def _hide_magnifier(self):
        if self.magnifier_window:
            self.magnifier_window.hide()
            
    def set_zoom_factor(self, factor: float):
        self.zoom_factor = factor
        if self.magnifier_window:
            self.magnifier_window.set_zoom_factor(factor)
            
    def set_window_size(self, size: int):
        self.window_size = size
        if self.magnifier_window:
            self.magnifier_window.set_window_size(size)
            
    def set_magnifier_window(self, window):
        self.magnifier_window = window
        
    def is_active(self) -> bool:
        return self._active
        
    def get_capture_rect(self, pos: QPoint) -> QRect:
        capture_size = int(self.window_size / self.zoom_factor)
        half_size = capture_size // 2
        return QRect(
            pos.x() - half_size,
            pos.y() - half_size,
            capture_size,
            capture_size
        )
