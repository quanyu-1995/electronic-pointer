from dataclasses import dataclass
from typing import Tuple
import json
import os

@dataclass
class DrawingStyle:
    line_width: int = 3
    color: str = "#FF0000"
    fill_color: str = ""
    opacity: int = 255

@dataclass
class AppSettings:
    default_style: DrawingStyle = DrawingStyle()
    screenshot_path: str = os.path.expanduser("~/Desktop/Screenshots")
    auto_hide_toolbar: bool = False
    toolbar_hide_delay: int = 3000
    
    def save(self, path: str):
        with open(path, 'w', encoding='utf-8') as f:
            json.dump(self.__dict__, f, indent=2, ensure_ascii=False)
    
    @classmethod
    def load(cls, path: str) -> 'AppSettings':
        if not os.path.exists(path):
            return cls()
        with open(path, 'r', encoding='utf-8') as f:
            data = json.load(f)
            return cls(**data)
