from PyQt6.QtWidgets import QWidget
from PyQt6.QtCore import Qt, QPoint, QRect, QTimer
from PyQt6.QtGui import QPainter, QColor, QPen, QBrush, QRadialGradient, QPainterPath, QScreen
from PyQt6.QtWidgets import QApplication


class MagnifierWindow(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.zoom_factor = 2.0
        self.window_size = 200
        self.border_width = 4
        self.offset_x = 20
        self.offset_y = 20
        
        self.setWindowFlags(
            Qt.WindowType.FramelessWindowHint |
            Qt.WindowType.WindowStaysOnTopHint |
            Qt.WindowType.Tool
        )
        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)
        self.setAttribute(Qt.WidgetAttribute.WA_ShowWithoutActivating)
        self.setFixedSize(self.window_size + self.border_width * 2, 
                         self.window_size + self.border_width * 2)
        
        self.current_pos = QPoint(0, 0)
        self.update_timer = QTimer(self)
        self.update_timer.timeout.connect(self._update_content)
        self.update_interval = 33
        
    def show_at(self, pos: QPoint):
        self.current_pos = pos
        self._update_position()
        self.show()
        self.update_timer.start(self.update_interval)
        
    def move_to(self, pos: QPoint):
        self.current_pos = pos
        self._update_position()
        
    def _update_position(self):
        x = self.current_pos.x() + self.offset_x
        y = self.current_pos.y() + self.offset_y
        
        screen = QApplication.primaryScreen()
        if screen:
            screen_geometry = screen.geometry()
            if x + self.width() > screen_geometry.right():
                x = self.current_pos.x() - self.width() - self.offset_x
            if y + self.height() > screen_geometry.bottom():
                y = self.current_pos.y() - self.height() - self.offset_y
                
        self.move(x, y)
        
    def _update_content(self):
        self.update()
        
    def set_zoom_factor(self, factor: float):
        self.zoom_factor = factor
        self.update()
        
    def set_window_size(self, size: int):
        self.window_size = size
        self.setFixedSize(size + self.border_width * 2, 
                         size + self.border_width * 2)
        self.update()
        
    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)
        painter.setRenderHint(QPainter.RenderHint.SmoothPixmapTransform)
        
        center_x = self.width() // 2
        center_y = self.height() // 2
        radius = self.window_size // 2
        
        self._draw_magnified_content(painter, center_x, center_y, radius)
        self._draw_border(painter, center_x, center_y, radius)
        self._draw_crosshair(painter, center_x, center_y, radius)
        self._draw_zoom_indicator(painter)
        
    def _draw_magnified_content(self, painter: QPainter, cx: int, cy: int, radius: int):
        screen = QApplication.primaryScreen()
        if not screen:
            return
            
        capture_size = int(self.window_size / self.zoom_factor)
        half_size = capture_size // 2
        
        capture_x = self.current_pos.x() - half_size
        capture_y = self.current_pos.y() - half_size
        
        pixmap = screen.grabWindow(0, capture_x, capture_y, capture_size, capture_size)
        
        clip_path = QPainterPath()
        clip_path.addEllipse(cx - radius, cy - radius, radius * 2, radius * 2)
        painter.setClipPath(clip_path)
        
        target_rect = QRect(cx - radius, cy - radius, radius * 2, radius * 2)
        painter.drawPixmap(target_rect, pixmap)
        
        painter.setClipping(False)
        
    def _draw_border(self, painter: QPainter, cx: int, cy: int, radius: int):
        gradient = QRadialGradient(cx, cy, radius + self.border_width)
        gradient.setColorAt(0.7, QColor("#667eea"))
        gradient.setColorAt(1.0, QColor("#764ba2"))
        
        painter.setPen(QPen(QBrush(gradient), self.border_width))
        painter.setBrush(Qt.BrushStyle.NoBrush)
        painter.drawEllipse(cx, cy, radius * 2, radius * 2)
        
        painter.setPen(QPen(QColor(255, 255, 255, 100), 1))
        painter.drawEllipse(cx + 2, cy + 2, (radius - 2) * 2, (radius - 2) * 2)
        
    def _draw_crosshair(self, painter: QPainter, cx: int, cy: int, radius: int):
        painter.setPen(QPen(QColor(255, 0, 0, 150), 1))
        
        painter.drawLine(cx - 10, cy, cx - 3, cy)
        painter.drawLine(cx + 3, cy, cx + 10, cy)
        painter.drawLine(cx, cy - 10, cx, cy - 3)
        painter.drawLine(cx, cy + 3, cx, cy + 10)
        
    def _draw_zoom_indicator(self, painter: QPainter):
        painter.setPen(QPen(QColor(255, 255, 255), 1))
        painter.setBrush(QBrush(QColor(0, 0, 0, 150)))
        
        text = f"{int(self.zoom_factor)}x"
        from PyQt6.QtGui import QFont
        font = QFont("Microsoft YaHei", 10, QFont.Weight.Bold)
        painter.setFont(font)
        
        from PyQt6.QtCore import QRectF
        text_rect = QRectF(self.width() - 35, self.height() - 25, 30, 20)
        painter.drawRoundedRect(text_rect, 5, 5)
        painter.drawText(text_rect, Qt.AlignmentFlag.AlignCenter, text)
        
    def hideEvent(self, event):
        self.update_timer.stop()
        super().hideEvent(event)
