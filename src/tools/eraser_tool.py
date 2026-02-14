import sys
import os
from PyQt6.QtCore import QPoint, QRectF
from PyQt6.QtGui import QPainter, QColor, QPen

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from src.tools.base_tool import BaseTool
from src.drawing.shapes import EraserStroke, FreePath, Line, Rectangle, Circle

class EraserTool(BaseTool):
    def __init__(self, canvas, size=20):
        super().__init__(canvas)
        self.size = size
        self.current_points = []
        
    def mouse_press(self, pos: QPoint):
        self.start_pos = pos
        self.current_pos = pos
        self.current_points = [pos]
        self._erase_at(pos)
        
    def mouse_move(self, pos: QPoint):
        if self.start_pos:
            self.current_pos = pos
            self.current_points.append(pos)
            self._erase_at(pos)
            
    def mouse_release(self, pos: QPoint):
        if self.current_points:
            stroke = EraserStroke(self.current_points.copy(), self.size)
            self.canvas.drawing_elements.append(stroke)
        self.current_points = []
        self.start_pos = None
        
    def _erase_at(self, pos: QPoint):
        half_size = self.size // 2
        eraser_rect = (pos.x() - half_size, pos.y() - half_size, 
                      self.size, self.size)
        
        elements_to_remove = []
        for element in self.canvas.drawing_elements:
            if self._intersects(element, eraser_rect):
                elements_to_remove.append(element)
        
        for element in elements_to_remove:
            self.canvas.drawing_elements.remove(element)
            
        self.canvas.update()
        
    def _intersects(self, element, eraser_rect):
        eraser = QRectF(eraser_rect[0], eraser_rect[1], eraser_rect[2], eraser_rect[3])
        
        if isinstance(element, FreePath):
            for i in range(len(element.points) - 1):
                p1 = element.points[i]
                p2 = element.points[i + 1]
                if self._line_intersects_rect(p1, p2, eraser):
                    return True
            return False
        elif isinstance(element, Line):
            return self._line_intersects_rect(element.start, element.end, eraser)
        elif isinstance(element, Rectangle):
            x, y, w, h = element._get_rect()
            rect = QRectF(x, y, w, h)
            return eraser.intersects(rect)
        elif isinstance(element, Circle):
            return self._circle_intersects_rect(element.center, element.radius, eraser)
        return False
        
    def _line_intersects_rect(self, p1, p2, rect):
        return rect.intersects(QRectF(min(p1.x(), p2.x()), min(p1.y(), p2.y()),
                                    abs(p2.x() - p1.x()), abs(p2.y() - p1.y())))
        
    def _circle_intersects_rect(self, center, radius, rect):
        closest_x = max(rect.left(), min(center.x(), rect.right()))
        closest_y = max(rect.top(), min(center.y(), rect.bottom()))
        distance_x = center.x() - closest_x
        distance_y = center.y() - closest_y
        return (distance_x * distance_x + distance_y * distance_y) <= (radius * radius)
        
    def increase_width(self, delta=1):
        self.size = min(self.size + delta, 100)
        
    def decrease_width(self, delta=1):
        self.size = max(self.size - delta, 5)
