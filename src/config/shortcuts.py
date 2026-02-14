from dataclasses import dataclass

@dataclass
class ShortcutConfig:
    brush: str = "B"
    eraser: str = "E"
    line: str = "L"
    rectangle: str = "R"
    circle: str = "C"
    text: str = "T"
    magnifier: str = "M"
    undo: str = "Ctrl+Z"
    redo: str = "Ctrl+Y"
    clear: str = "Delete"
    save: str = "Ctrl+S"
    exit: str = "Escape"
    penetrate: str = "F9"
