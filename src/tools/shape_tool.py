import sys
import os
from PyQt6.QtCore import QPoint, Qt
from PyQt6.QtGui import QPainter, QPen, QColor

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from src.tools.base_tool import BaseTool
from src.drawing.shapes import Line, Rectangle, Circle

class LineTool(BaseTool):
    def __init__(self, canvas, color="#FF0000", width=3):
        super().__init__(canvas)
        self.color = color
        self.width = width
        
    def mouse_press(self, pos: QPoint):
        self.start_pos = pos
        self.current_pos = pos
        
    def mouse_move(self, pos: QPoint):
        if self.start_pos:
            self.current_pos = pos
            self.canvas.update()
            
    def mouse_release(self, pos: QPoint):
        if self.start_pos:
            line = Line(self.start_pos, pos, self.color, self.width)
            self.canvas.drawing_elements.append(line)
        self.start_pos = None
        self.canvas.update()
        
    def draw_preview(self, painter):
        if self.start_pos and self.current_pos:
            pen = painter.pen()
            pen.setColor(QColor(self.color))
            pen.setWidth(self.width)
            painter.setPen(pen)
            painter.drawLine(self.start_pos, self.current_pos)

class RectangleTool(BaseTool):
    def __init__(self, canvas, color="#FF0000", width=3, fill_color=""):
        super().__init__(canvas)
        self.color = color
        self.width = width
        self.fill_color = fill_color
        
    def mouse_press(self, pos: QPoint):
        self.start_pos = pos
        self.current_pos = pos
        
    def mouse_move(self, pos: QPoint):
        if self.start_pos:
            self.current_pos = pos
            self.canvas.update()
            
    def mouse_release(self, pos: QPoint):
        if self.start_pos:
            rect = Rectangle(self.start_pos, pos, self.color, self.width, self.fill_color)
            self.canvas.drawing_elements.append(rect)
        self.start_pos = None
        self.canvas.update()
        
    def draw_preview(self, painter):
        if self.start_pos and self.current_pos:
            pen = painter.pen()
            pen.setColor(QColor(self.color))
            pen.setWidth(self.width)
            painter.setPen(pen)
            
            if self.fill_color:
                painter.setBrush(QColor(self.fill_color))
            else:
                painter.setBrush(Qt.BrushStyle.NoBrush)
                
            x = min(self.start_pos.x(), self.current_pos.x())
            y = min(self.start_pos.y(), self.current_pos.y())
            w = abs(self.current_pos.x() - self.start_pos.x())
            h = abs(self.current_pos.y() - self.start_pos.y())
            painter.drawRect(x, y, w, h)

class CircleTool(BaseTool):
    def __init__(self, canvas, color="#FF0000", width=3, fill_color=""):
        super().__init__(canvas)
        self.color = color
        self.width = width
        self.fill_color = fill_color
        
    def mouse_press(self, pos: QPoint):
        self.start_pos = pos
        self.current_pos = pos
        
    def mouse_move(self, pos: QPoint):
        if self.start_pos:
            self.current_pos = pos
            self.canvas.update()
            
    def mouse_release(self, pos: QPoint):
        if self.start_pos:
            radius = int(((pos.x() - self.start_pos.x())**2 + 
                         (pos.y() - self.start_pos.y())**2)**0.5)
            circle = Circle(self.start_pos, radius, self.color, self.width, self.fill_color)
            self.canvas.drawing_elements.append(circle)
        self.start_pos = None
        self.canvas.update()
        
    def draw_preview(self, painter):
        if self.start_pos and self.current_pos:
            pen = painter.pen()
            pen.setColor(QColor(self.color))
            pen.setWidth(self.width)
            painter.setPen(pen)
            
            if self.fill_color:
                painter.setBrush(QColor(self.fill_color))
            else:
                painter.setBrush(Qt.BrushStyle.NoBrush)
                
            radius = int(((self.current_pos.x() - self.start_pos.x())**2 + 
                         (self.current_pos.y() - self.start_pos.y())**2)**0.5)
            painter.drawEllipse(self.start_pos, radius, radius)
