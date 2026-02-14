import sys
import os
from PyQt6.QtWidgets import QMainWindow
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QShortcut, QKeySequence
from PyQt6.QtWidgets import QApplication

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from src.drawing.canvas import Canvas
from src.ui.toolbar import Toolbar
from src.tools.brush_tool import BrushTool
from src.tools.eraser_tool import EraserTool
from src.tools.shape_tool import LineTool, RectangleTool, CircleTool
from src.tools.text_tool import TextTool
from src.tools.magnifier_tool import MagnifierTool
from src.managers.style_manager import StyleManager
from src.utils.screenshot import ScreenshotManager
from src.config.shortcuts import ShortcutConfig
from src.ui.magnifier_window import MagnifierWindow

try:
    from pynput import keyboard
    PYNPUT_AVAILABLE = True
except ImportError:
    PYNPUT_AVAILABLE = False

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.style_manager = StyleManager()
        self.screenshot_manager = ScreenshotManager()
        self.shortcuts = ShortcutConfig()
        self.init_window()
        self.init_canvas()
        self.init_toolbar()
        self.init_shortcuts()
        self.init_global_hotkey()
        
    def init_window(self):
        self.setWindowFlags(
            Qt.WindowType.FramelessWindowHint |
            Qt.WindowType.WindowStaysOnTopHint |
            Qt.WindowType.Tool
        )
        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)
        self.setFocusPolicy(Qt.FocusPolicy.StrongFocus)
        
    def init_canvas(self):
        self.canvas = Canvas(None)
        self.canvas.setWindowFlags(
            Qt.WindowType.FramelessWindowHint |
            Qt.WindowType.WindowStaysOnTopHint |
            Qt.WindowType.Tool
        )
        self.canvas.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground, True)
        self.canvas.after_show_callback = self._raise_toolbar
        
        self.magnifier_window = MagnifierWindow()
        self.magnifier_tool = MagnifierTool(self.canvas)
        self.magnifier_tool.set_magnifier_window(self.magnifier_window)
        
    def _raise_toolbar(self):
        self.toolbar.raise_()
        self.toolbar.show()
        
    def init_toolbar(self):
        self.toolbar = Toolbar(self)
        self.toolbar.move(100, 100)
        self.toolbar.show()
        
        self.toolbar.set_tool_changed_callback(self._on_tool_changed)
        self.toolbar.set_color_changed_callback(self._on_color_changed)
        self.toolbar.set_width_changed_callback(self._on_width_changed)
        self.toolbar.set_font_size_changed_callback(self._on_font_size_changed)
        self.toolbar.set_drawing_mode_changed_callback(self._on_drawing_mode_changed)
        self.toolbar.set_screenshot_callback(self._on_screenshot)
        self.toolbar.set_clear_callback(self._on_clear)
        self.toolbar.set_zoom_changed_callback(self._on_zoom_changed)
        self.toolbar.set_mag_size_changed_callback(self._on_mag_size_changed)
        self.toolbar.set_close_callback(self._on_close)
        
        self.toolbar.set_tool("brush")
        
        self.canvas.width_changed_callback = self.toolbar.update_width_slider
        
        self._update_toolbar_geometry()
        self.toolbar.geometry_changed_callback = self._on_toolbar_moved
        
    def _update_toolbar_geometry(self):
        self.canvas.set_toolbar_geometry(self.toolbar.geometry())
        
    def _on_toolbar_moved(self):
        self._update_toolbar_geometry()
        
    def _on_drawing_mode_changed(self, drawing_mode):
        self.canvas.set_drawing_mode(drawing_mode)
        self.toolbar.raise_()
        
    def _on_tool_changed(self, tool_type):
        style = self.style_manager.get_style()
        
        if tool_type == "brush":
            self.canvas.current_tool = BrushTool(self.canvas, style.color, style.line_width)
        elif tool_type == "eraser":
            self.canvas.current_tool = EraserTool(self.canvas, 20)
        elif tool_type == "line":
            self.canvas.current_tool = LineTool(self.canvas, style.color, style.line_width)
        elif tool_type == "rectangle":
            self.canvas.current_tool = RectangleTool(self.canvas, style.color, style.line_width)
        elif tool_type == "circle":
            self.canvas.current_tool = CircleTool(self.canvas, style.color, style.line_width)
        elif tool_type == "text":
            self.canvas.current_tool = TextTool(self.canvas, style.color, style.font_size)
        elif tool_type == "magnifier":
            self.canvas.current_tool = self.magnifier_tool
        
        self.toolbar.raise_()
            
    def _on_color_changed(self, color):
        self.style_manager.set_color(color)
        self._update_tool_style()
        self.toolbar.raise_()
        
    def _on_width_changed(self, width):
        self.style_manager.set_line_width(width)
        self._update_tool_style()
        self.toolbar.raise_()
        
    def _on_font_size_changed(self, size):
        self.style_manager.set_font_size(size)
        if isinstance(self.canvas.current_tool, TextTool):
            self.canvas.current_tool.font_size = size
        self.toolbar.raise_()
        
    def _update_tool_style(self):
        style = self.style_manager.get_style()
        if hasattr(self.canvas.current_tool, 'color'):
            self.canvas.current_tool.color = style.color
        if hasattr(self.canvas.current_tool, 'width'):
            self.canvas.current_tool.width = style.line_width
            
    def _on_screenshot(self):
        filepath = self.screenshot_manager.save_screenshot(self.canvas)
        print(f"截图已保存: {filepath}")
        self.toolbar.raise_()
        
    def _on_clear(self):
        self.canvas.clear_canvas()
        self.toolbar.raise_()
        
    def _on_close(self):
        self.canvas.close()
        self.toolbar.close()
        self.magnifier_window.close()
        QApplication.quit()
        
    def _on_zoom_changed(self, zoom):
        self.magnifier_tool.set_zoom_factor(float(zoom))
        self.magnifier_window.set_zoom_factor(float(zoom))
        self.toolbar.raise_()
        
    def _on_mag_size_changed(self, size):
        self.magnifier_tool.set_window_size(size)
        self.magnifier_window.set_window_size(size)
        self.toolbar.raise_()
        
    def init_shortcuts(self):
        self.shortcut_undo = QShortcut(QKeySequence(self.shortcuts.undo), self)
        self.shortcut_undo.activated.connect(self._on_undo)
        
        self.shortcut_redo = QShortcut(QKeySequence(self.shortcuts.redo), self)
        self.shortcut_redo.activated.connect(self._on_redo)
        
        self.shortcut_clear = QShortcut(QKeySequence(self.shortcuts.clear), self)
        self.shortcut_clear.activated.connect(self._on_clear)
        
        self.shortcut_save = QShortcut(QKeySequence(self.shortcuts.save), self)
        self.shortcut_save.activated.connect(self._on_screenshot)
        
        self.shortcut_exit = QShortcut(QKeySequence(self.shortcuts.exit), self)
        self.shortcut_exit.activated.connect(self.close)
        
        self.shortcut_brush = QShortcut(QKeySequence(self.shortcuts.brush), self)
        self.shortcut_brush.activated.connect(lambda: self.toolbar.set_tool("brush"))
        
        self.shortcut_eraser = QShortcut(QKeySequence(self.shortcuts.eraser), self)
        self.shortcut_eraser.activated.connect(lambda: self.toolbar.set_tool("eraser"))
        
        self.shortcut_line = QShortcut(QKeySequence(self.shortcuts.line), self)
        self.shortcut_line.activated.connect(lambda: self.toolbar.set_tool("line"))
        
        self.shortcut_rectangle = QShortcut(QKeySequence(self.shortcuts.rectangle), self)
        self.shortcut_rectangle.activated.connect(lambda: self.toolbar.set_tool("rectangle"))
        
        self.shortcut_circle = QShortcut(QKeySequence(self.shortcuts.circle), self)
        self.shortcut_circle.activated.connect(lambda: self.toolbar.set_tool("circle"))
        
        self.shortcut_text = QShortcut(QKeySequence(self.shortcuts.text), self)
        self.shortcut_text.activated.connect(lambda: self.toolbar.set_tool("text"))
        
        self.shortcut_magnifier = QShortcut(QKeySequence(self.shortcuts.magnifier), self)
        self.shortcut_magnifier.activated.connect(lambda: self.toolbar.set_tool("magnifier"))
        
    def _on_penetrate_toggle(self):
        self.canvas.toggle_drawing_mode()
        self.toolbar.update_penetrate_button(self.canvas.drawing_mode)
        
    def _on_undo(self):
        self.canvas.undo()
        
    def _on_redo(self):
        self.canvas.redo()
        
    def init_global_hotkey(self):
        self.hotkey_listener = None
        if PYNPUT_AVAILABLE:
            self.hotkey_listener = keyboard.GlobalHotKeys({
                '<f9>': self._on_penetrate_toggle
            })
            self.hotkey_listener.start()
            
    def showEvent(self, event):
        super().showEvent(event)
        self.showFullScreen()
        self.canvas.showFullScreen()
        self.toolbar.raise_()
        self.toolbar.show()
        
    def closeEvent(self, event):
        if self.hotkey_listener:
            self.hotkey_listener.stop()
        super().closeEvent(event)
