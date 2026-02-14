import sys
import os
from PyQt6.QtCore import QPoint
from PyQt6.QtWidgets import QInputDialog

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from src.tools.base_tool import BaseTool
from src.drawing.shapes import TextElement

class TextTool(BaseTool):
    def __init__(self, canvas, color="#FF0000", font_size=24):
        super().__init__(canvas)
        self.color = color
        self.font_size = font_size
        self.bold = False
        self.italic = False
        
    def mouse_press(self, pos: QPoint):
        for element in reversed(self.canvas.drawing_elements):
            if isinstance(element, TextElement) and element.contains(pos):
                text, ok = QInputDialog.getText(self.canvas, "编辑文字", "编辑文字:", text=element.text)
                if ok:
                    element.update_text(text)
                    self.canvas.update()
                return
                
        text, ok = QInputDialog.getText(self.canvas, "输入文字", "请输入文字:")
        if ok and text:
            text_element = TextElement(pos, text, self.color, self.font_size, self.bold, self.italic)
            self.canvas.drawing_elements.append(text_element)
            self.canvas.update()
            
    def mouse_move(self, pos: QPoint):
        pass
        
    def mouse_release(self, pos: QPoint):
        pass
