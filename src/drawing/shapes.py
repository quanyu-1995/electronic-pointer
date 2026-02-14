from PyQt6.QtCore import QPoint, QPointF, Qt, QRect
from PyQt6.QtGui import QPainter, QPen, QColor, QPainterPath, QFont, QFontMetrics

class DrawingElement:
    def draw(self, painter: QPainter):
        pass

class FreePath(DrawingElement):
    def __init__(self, points, color, width):
        self.points = points
        self.color = color
        self.width = width
        
    def draw(self, painter: QPainter):
        if len(self.points) < 2:
            return
            
        pen = QPen(QColor(self.color))
        pen.setWidth(self.width)
        pen.setCapStyle(Qt.PenCapStyle.RoundCap)
        pen.setJoinStyle(Qt.PenJoinStyle.RoundJoin)
        painter.setPen(pen)
        
        path = QPainterPath()
        path.moveTo(QPointF(self.points[0]))
        for point in self.points[1:]:
            path.lineTo(QPointF(point))
        painter.drawPath(path)

class Line(DrawingElement):
    def __init__(self, start, end, color, width):
        self.start = start
        self.end = end
        self.color = color
        self.width = width
        
    def draw(self, painter: QPainter):
        pen = QPen(QColor(self.color))
        pen.setWidth(self.width)
        pen.setCapStyle(Qt.PenCapStyle.RoundCap)
        painter.setPen(pen)
        painter.drawLine(self.start, self.end)

class Rectangle(DrawingElement):
    def __init__(self, start, end, color, width, fill_color=""):
        self.start = start
        self.end = end
        self.color = color
        self.width = width
        self.fill_color = fill_color
        
    def draw(self, painter: QPainter):
        pen = QPen(QColor(self.color))
        pen.setWidth(self.width)
        painter.setPen(pen)
        
        if self.fill_color:
            painter.setBrush(QColor(self.fill_color))
        else:
            painter.setBrush(Qt.BrushStyle.NoBrush)
            
        x, y, w, h = self._get_rect()
        painter.drawRect(x, y, w, h)
        
    def _get_rect(self):
        x = min(self.start.x(), self.end.x())
        y = min(self.start.y(), self.end.y())
        w = abs(self.end.x() - self.start.x())
        h = abs(self.end.y() - self.start.y())
        return x, y, w, h

class Circle(DrawingElement):
    def __init__(self, center, radius, color, width, fill_color=""):
        self.center = center
        self.radius = radius
        self.color = color
        self.width = width
        self.fill_color = fill_color
        
    def draw(self, painter: QPainter):
        pen = QPen(QColor(self.color))
        pen.setWidth(self.width)
        painter.setPen(pen)
        
        if self.fill_color:
            painter.setBrush(QColor(self.fill_color))
        else:
            painter.setBrush(Qt.BrushStyle.NoBrush)
            
        painter.drawEllipse(self.center, self.radius, self.radius)

class EraserStroke(DrawingElement):
    def __init__(self, points, size):
        self.points = points
        self.size = size
        
    def draw(self, painter: QPainter):
        pass

class TextElement(DrawingElement):
    def __init__(self, pos, text, color, font_size=16, bold=False, italic=False):
        self.pos = pos
        self.text = text
        self.color = color
        self.font_size = font_size
        self.bold = bold
        self.italic = italic
        
    def draw(self, painter: QPainter):
        font = painter.font()
        font.setPointSize(self.font_size)
        font.setBold(self.bold)
        font.setItalic(self.italic)
        painter.setFont(font)
        
        pen = QPen(QColor(self.color))
        painter.setPen(pen)
        painter.drawText(self.pos, self.text)
        
    def contains(self, pos: QPoint) -> bool:
        font = QFont()
        font.setPointSize(self.font_size)
        font.setBold(self.bold)
        font.setItalic(self.italic)
        
        fm = QFontMetrics(font)
        rect = fm.boundingRect(self.text)
        text_rect = QRect(self.pos.x(), self.pos.y() - rect.height(), rect.width(), rect.height())
        return text_rect.contains(pos)
        
    def update_text(self, text):
        self.text = text
