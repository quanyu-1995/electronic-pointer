import sys
import os
from PyQt6.QtCore import QPoint, Qt
from PyQt6.QtGui import QPainter, QPen, QColor

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from src.tools.base_tool import BaseTool
from src.drawing.shapes import FreePath

class BrushTool(BaseTool):
    def __init__(self, canvas, color="#FF0000", width=3):
        super().__init__(canvas)
        self.color = color
        self.width = width
        self.current_points = []
        
    def mouse_press(self, pos: QPoint):
        self.start_pos = pos
        self.current_pos = pos
        self.current_points = [pos]
        
    def mouse_move(self, pos: QPoint):
        if self.start_pos:
            self.current_pos = pos
            self.current_points.append(pos)
            self.canvas.update()
            
    def mouse_release(self, pos: QPoint):
        if self.current_points:
            path = FreePath(self.current_points.copy(), self.color, self.width)
            self.canvas.drawing_elements.append(path)
        self.current_points = []
        self.start_pos = None
        self.canvas.update()
        
    def draw_preview(self, painter):
        if len(self.current_points) < 2:
            return
            
        pen = painter.pen()
        pen.setColor(QColor(self.color))
        pen.setWidth(self.width)
        pen.setCapStyle(Qt.PenCapStyle.RoundCap)
        painter.setPen(pen)
        
        for i in range(len(self.current_points) - 1):
            painter.drawLine(self.current_points[i], self.current_points[i + 1])
            
    def increase_width(self, delta=1):
        self.width = min(self.width + delta, 50)
        
    def decrease_width(self, delta=1):
        self.width = max(self.width - delta, 1)
