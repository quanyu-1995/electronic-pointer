import sys
import os
from PyQt6.QtWidgets import QWidget
from PyQt6.QtCore import Qt, QPoint, QRect
from PyQt6.QtGui import QPainter, QColor, QBrush

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from src.tools.brush_tool import BrushTool
from src.managers.history_manager import HistoryManager

class Canvas(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setMouseTracking(True)
        self.setAttribute(Qt.WidgetAttribute.WA_TransparentForMouseEvents, False)
        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground, True)
        self.setAttribute(Qt.WidgetAttribute.WA_OpaquePaintEvent, False)
        self.setAttribute(Qt.WidgetAttribute.WA_NoSystemBackground, True)
        self.setAutoFillBackground(False)
        self.current_tool = BrushTool(self)
        self.drawing_elements = []
        self.history_manager = HistoryManager()
        self.history_manager.save_state(self.drawing_elements)
        self.drawing_mode = True
        self.width_changed_callback = None
        self.toolbar_geometry = None
        self.after_show_callback = None
        
    def set_toolbar_geometry(self, geometry):
        self.toolbar_geometry = geometry
        
    def _is_in_toolbar(self, pos):
        if self.toolbar_geometry:
            return self.toolbar_geometry.contains(pos)
        return False
        
    def toggle_drawing_mode(self):
        self.drawing_mode = not self.drawing_mode
        self._update_window_state()
        
    def set_drawing_mode(self, enabled):
        self.drawing_mode = enabled
        self._update_window_state()
        
    def _update_window_state(self):
        if self.drawing_mode:
            self.setAttribute(Qt.WidgetAttribute.WA_TransparentForMouseEvents, False)
            self.setWindowFlags(
                Qt.WindowType.FramelessWindowHint |
                Qt.WindowType.WindowStaysOnTopHint |
                Qt.WindowType.Tool
            )
        else:
            self.setWindowFlags(
                Qt.WindowType.FramelessWindowHint |
                Qt.WindowType.WindowStaysOnTopHint |
                Qt.WindowType.Tool |
                Qt.WindowType.WindowTransparentForInput
            )
            self.setAttribute(Qt.WidgetAttribute.WA_TransparentForMouseEvents, True)
        from PyQt6.QtCore import QTimer
        QTimer.singleShot(10, self._delayed_show)
        
    def _delayed_show(self):
        self.showFullScreen()
        if self.after_show_callback:
            self.after_show_callback()
        
    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)
        painter.setRenderHint(QPainter.RenderHint.SmoothPixmapTransform)
        
        painter.fillRect(self.rect(), QColor(255, 255, 255, 1))
        
        for element in self.drawing_elements:
            element.draw(painter)
            
        if self.current_tool and self.drawing_mode:
            self.current_tool.draw_preview(painter)
            
        painter.end()
            
    def mousePressEvent(self, event):
        if not self.drawing_mode:
            return
        if self._is_in_toolbar(event.globalPosition().toPoint()):
            return
        if self.current_tool:
            self.current_tool.mouse_press(event.pos())
            
    def mouseMoveEvent(self, event):
        if not self.drawing_mode:
            return
        if self._is_in_toolbar(event.globalPosition().toPoint()):
            return
        if self.current_tool:
            self.current_tool.mouse_move(event.pos())
            
    def mouseReleaseEvent(self, event):
        if not self.drawing_mode:
            return
        if self._is_in_toolbar(event.globalPosition().toPoint()):
            return
        if self.current_tool:
            self.current_tool.mouse_release(event.pos())
            self.save_state()
            
    def mouseDoubleClickEvent(self, event):
        if not self.drawing_mode:
            return
        if self._is_in_toolbar(event.globalPosition().toPoint()):
            return
        if self.current_tool:
            self.current_tool.mouse_press(event.pos())
            
    def keyPressEvent(self, event):
        if event.key() == Qt.Key.Key_Z and event.modifiers() & Qt.KeyboardModifier.ControlModifier:
            self.undo()
        elif event.key() == Qt.Key.Key_Y and event.modifiers() & Qt.KeyboardModifier.ControlModifier:
            self.redo()
            
    def save_state(self):
        self.history_manager.save_state(self.drawing_elements)
        
    def undo(self):
        self.drawing_elements = self.history_manager.undo()
        self.update()
        
    def redo(self):
        self.drawing_elements = self.history_manager.redo()
        self.update()
            
    def clear_canvas(self):
        self.drawing_elements.clear()
        self.save_state()
        self.update()
        
    def wheelEvent(self, event):
        if not self.drawing_mode:
            return
        if hasattr(self.current_tool, 'width'):
            delta = event.angleDelta().y()
            if delta > 0:
                self.current_tool.increase_width()
            else:
                self.current_tool.decrease_width()
            if self.width_changed_callback:
                self.width_changed_callback(self.current_tool.width)
            self.update()
