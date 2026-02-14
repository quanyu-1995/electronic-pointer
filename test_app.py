import sys
import os
from PyQt6.QtWidgets import QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QLabel
from PyQt6.QtCore import Qt, QPoint
from PyQt6.QtGui import QPainter

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from src.drawing.canvas import Canvas
from src.tools.brush_tool import BrushTool
from src.tools.shape_tool import LineTool, RectangleTool, CircleTool
from src.tools.eraser_tool import EraserTool

class TestWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("电子教鞭工具 - 测试窗口")
        self.setGeometry(100, 100, 1200, 800)
        
        self.init_ui()
        
    def init_ui(self):
        central_widget = QWidget()
        layout = QVBoxLayout()
        
        toolbar = QHBoxLayout()
        
        self.brush_btn = QPushButton("画笔 (B)")
        self.brush_btn.clicked.connect(lambda: self.set_tool("brush"))
        toolbar.addWidget(self.brush_btn)
        
        self.line_btn = QPushButton("直线 (L)")
        self.line_btn.clicked.connect(lambda: self.set_tool("line"))
        toolbar.addWidget(self.line_btn)
        
        self.rect_btn = QPushButton("矩形 (R)")
        self.rect_btn.clicked.connect(lambda: self.set_tool("rectangle"))
        toolbar.addWidget(self.rect_btn)
        
        self.circle_btn = QPushButton("圆形 (C)")
        self.circle_btn.clicked.connect(lambda: self.set_tool("circle"))
        toolbar.addWidget(self.circle_btn)
        
        self.eraser_btn = QPushButton("橡皮擦 (E)")
        self.eraser_btn.clicked.connect(lambda: self.set_tool("eraser"))
        toolbar.addWidget(self.eraser_btn)
        
        self.clear_btn = QPushButton("清空画布")
        self.clear_btn.clicked.connect(self.clear_canvas)
        toolbar.addWidget(self.clear_btn)
        
        self.info_label = QLabel("当前工具: 画笔")
        toolbar.addWidget(self.info_label)
        
        layout.addLayout(toolbar)
        
        self.canvas = Canvas(self)
        layout.addWidget(self.canvas)
        
        central_widget.setLayout(layout)
        self.setCentralWidget(central_widget)
        
        self.brush_btn.setStyleSheet("background-color: #a0d8ef;")
        
    def set_tool(self, tool_name):
        if tool_name == "brush":
            self.canvas.current_tool = BrushTool(self.canvas)
            self.info_label.setText("当前工具: 画笔")
            self.brush_btn.setStyleSheet("background-color: #a0d8ef;")
            self.line_btn.setStyleSheet("")
            self.rect_btn.setStyleSheet("")
            self.circle_btn.setStyleSheet("")
            self.eraser_btn.setStyleSheet("")
        elif tool_name == "line":
            self.canvas.current_tool = LineTool(self.canvas)
            self.info_label.setText("当前工具: 直线")
            self.brush_btn.setStyleSheet("")
            self.line_btn.setStyleSheet("background-color: #a0d8ef;")
            self.rect_btn.setStyleSheet("")
            self.circle_btn.setStyleSheet("")
            self.eraser_btn.setStyleSheet("")
        elif tool_name == "rectangle":
            self.canvas.current_tool = RectangleTool(self.canvas)
            self.info_label.setText("当前工具: 矩形")
            self.brush_btn.setStyleSheet("")
            self.line_btn.setStyleSheet("")
            self.rect_btn.setStyleSheet("background-color: #a0d8ef;")
            self.circle_btn.setStyleSheet("")
            self.eraser_btn.setStyleSheet("")
        elif tool_name == "circle":
            self.canvas.current_tool = CircleTool(self.canvas)
            self.info_label.setText("当前工具: 圆形")
            self.brush_btn.setStyleSheet("")
            self.line_btn.setStyleSheet("")
            self.rect_btn.setStyleSheet("")
            self.circle_btn.setStyleSheet("background-color: #a0d8ef;")
            self.eraser_btn.setStyleSheet("")
        elif tool_name == "eraser":
            self.canvas.current_tool = EraserTool(self.canvas)
            self.info_label.setText("当前工具: 橡皮擦")
            self.brush_btn.setStyleSheet("")
            self.line_btn.setStyleSheet("")
            self.rect_btn.setStyleSheet("")
            self.circle_btn.setStyleSheet("")
            self.eraser_btn.setStyleSheet("background-color: #a0d8ef;")
            
    def clear_canvas(self):
        self.canvas.clear_canvas()
        
    def keyPressEvent(self, event):
        if event.key() == Qt.Key.Key_B:
            self.set_tool("brush")
        elif event.key() == Qt.Key.Key_L:
            self.set_tool("line")
        elif event.key() == Qt.Key.Key_R:
            self.set_tool("rectangle")
        elif event.key() == Qt.Key.Key_C:
            self.set_tool("circle")
        elif event.key() == Qt.Key.Key_E:
            self.set_tool("eraser")
        elif event.key() == Qt.Key.Key_Delete:
            self.clear_canvas()

def main():
    app = QApplication(sys.argv)
    window = TestWindow()
    window.show()
    sys.exit(app.exec())

if __name__ == "__main__":
    main()
