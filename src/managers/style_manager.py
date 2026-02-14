from dataclasses import dataclass
from typing import Optional

@dataclass
class Style:
    color: str = "#FF0000"
    line_width: int = 3
    fill_color: str = ""
    opacity: int = 255
    font_size: int = 24

class StyleManager:
    def __init__(self):
        self.current_style = Style()
        self.recent_colors = ["#FF0000", "#00FF00", "#0000FF", "#FFFF00", "#FF00FF", "#00FFFF"]
        
    def set_color(self, color: str):
        self.current_style.color = color
        if color not in self.recent_colors:
            self.recent_colors.insert(0, color)
            if len(self.recent_colors) > 10:
                self.recent_colors.pop()
                
    def set_line_width(self, width: int):
        self.current_style.line_width = width
        
    def set_fill_color(self, color: str):
        self.current_style.fill_color = color
        
    def set_opacity(self, opacity: int):
        self.current_style.opacity = opacity
        
    def set_font_size(self, size: int):
        self.current_style.font_size = size
        
    def get_style(self) -> Style:
        return self.current_style
