from abc import ABC, abstractmethod
from PyQt6.QtCore import QPoint
from PyQt6.QtGui import QPainter

class BaseTool(ABC):
    def __init__(self, canvas):
        self.canvas = canvas
        self.start_pos = None
        self.current_pos = None
        
    @abstractmethod
    def mouse_press(self, pos: QPoint):
        pass
        
    @abstractmethod
    def mouse_move(self, pos: QPoint):
        pass
        
    @abstractmethod
    def mouse_release(self, pos: QPoint):
        pass
        
    def draw_preview(self, painter: QPainter):
        pass
