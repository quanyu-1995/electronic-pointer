import sys
import os
from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QButtonGroup, 
    QSlider, QLabel, QSpinBox, QFrame, QGridLayout, QSizePolicy
)
from PyQt6.QtCore import Qt, QPoint, QTimer, QRectF
from PyQt6.QtGui import (
    QPainter, QColor, QPen, QBrush, QLinearGradient, 
    QFont, QPainterPath, QRadialGradient
)

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

PRESET_COLORS = [
    "#FF0000", "#FF4500", "#FF8C00", "#FFD700",
    "#00FF00", "#00FF7F", "#00CED1", "#00BFFF",
    "#0000FF", "#8A2BE2", "#FF00FF", "#FF1493",
    "#000000", "#404040", "#808080", "#FFFFFF"
]

TOOL_INFO = {
    "brush": ("画笔", "B"),
    "eraser": ("橡皮", "E"),
    "line": ("直线", "L"),
    "rectangle": ("矩形", "R"),
    "circle": ("圆形", "C"),
    "text": ("文字", "T"),
    "magnifier": ("放大镜", "M"),
}

class ModernToolButton(QPushButton):
    def __init__(self, tool_type, parent=None):
        super().__init__(parent)
        self.tool_type = tool_type
        self.tool_name, self.shortcut = TOOL_INFO.get(tool_type, ("", ""))
        self.setFixedSize(48, 48)
        self.setCheckable(True)
        self.setCursor(Qt.CursorShape.PointingHandCursor)
        self.hovered = False
        
    def enterEvent(self, event):
        self.hovered = True
        self.update()
        
    def leaveEvent(self, event):
        self.hovered = False
        self.update()
        
    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)
        painter.setRenderHint(QPainter.RenderHint.SmoothPixmapTransform)
        
        rect = QRectF(0, 0, self.width(), self.height())
        radius = 10.0
        
        if self.isChecked():
            gradient = QLinearGradient(0, 0, 0, self.height())
            gradient.setColorAt(0, QColor("#667eea"))
            gradient.setColorAt(1, QColor("#764ba2"))
            painter.setBrush(QBrush(gradient))
            painter.setPen(Qt.PenStyle.NoPen)
            painter.drawRoundedRect(rect.adjusted(2, 2, -2, -2), radius, radius)
            
            shadow_color = QColor("#667eea")
            shadow_color.setAlpha(80)
            painter.setBrush(QBrush(shadow_color))
            painter.drawRoundedRect(rect.adjusted(0, 4, 0, 0), radius, radius)
            
        elif self.hovered:
            gradient = QLinearGradient(0, 0, 0, self.height())
            gradient.setColorAt(0, QColor(255, 255, 255, 250))
            gradient.setColorAt(1, QColor(240, 240, 250, 250))
            painter.setBrush(QBrush(gradient))
            painter.setPen(QPen(QColor("#e0e0e0"), 1))
            painter.drawRoundedRect(rect.adjusted(2, 2, -2, -2), radius, radius)
        else:
            gradient = QLinearGradient(0, 0, 0, self.height())
            gradient.setColorAt(0, QColor(255, 255, 255, 230))
            gradient.setColorAt(1, QColor(248, 248, 252, 230))
            painter.setBrush(QBrush(gradient))
            painter.setPen(QPen(QColor("#d0d0d0"), 1))
            painter.drawRoundedRect(rect.adjusted(2, 2, -2, -2), radius, radius)
        
        self._draw_icon(painter)
        
    def _draw_icon(self, painter):
        w, h = self.width(), self.height()
        center_x, center_y = w // 2, h // 2 - 4
        
        icon_color = QColor("#ffffff") if self.isChecked() else QColor("#555555")
        pen = QPen(icon_color, 2, Qt.PenStyle.SolidLine, Qt.PenCapStyle.RoundCap, Qt.PenJoinStyle.RoundJoin)
        painter.setPen(pen)
        
        if self.tool_type == "brush":
            path = QPainterPath()
            path.moveTo(center_x - 8, center_y + 8)
            path.cubicTo(center_x - 4, center_y + 4, center_x + 4, center_y - 4, center_x + 8, center_y - 8)
            painter.drawPath(path)
            painter.setBrush(QBrush(icon_color))
            painter.drawEllipse(center_x + 6, center_y - 10, 5, 5)
            
        elif self.tool_type == "eraser":
            painter.setBrush(QBrush(icon_color))
            painter.drawRoundedRect(center_x - 8, center_y - 6, 16, 12, 2, 2)
            if not self.isChecked():
                painter.setPen(QPen(QColor("#ffffff"), 1.5))
                painter.drawLine(center_x - 4, center_y - 1, center_x + 4, center_y - 1)
            
        elif self.tool_type == "line":
            painter.drawLine(center_x - 8, center_y + 6, center_x + 8, center_y - 6)
            
        elif self.tool_type == "rectangle":
            painter.setBrush(Qt.BrushStyle.NoBrush)
            painter.drawRoundedRect(center_x - 8, center_y - 6, 16, 12, 2, 2)
            
        elif self.tool_type == "circle":
            painter.setBrush(Qt.BrushStyle.NoBrush)
            painter.drawEllipse(center_x, center_y, 10, 10)
            
        elif self.tool_type == "text":
            font = QFont("Arial", 14, QFont.Weight.Bold)
            painter.setFont(font)
            painter.drawText(center_x - 4, center_y + 4, "T")
            
        elif self.tool_type == "magnifier":
            painter.setBrush(Qt.BrushStyle.NoBrush)
            painter.drawEllipse(center_x - 4, center_y - 6, 12, 12)
            painter.drawLine(center_x + 4, center_y + 2, center_x + 10, center_y + 8)
        
        painter.setPen(QPen(QColor("#999999") if not self.isChecked() else QColor("#ffffff"), 1))
        font = QFont("Microsoft YaHei", 6)
        painter.setFont(font)
        painter.drawText(QRectF(0, h - 12, w, 10), Qt.AlignmentFlag.AlignCenter, self.tool_name)


class PenetrateButton(QPushButton):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setFixedSize(48, 48)
        self.setCheckable(True)
        self.hovered = False
        self.setCursor(Qt.CursorShape.PointingHandCursor)
        
    def enterEvent(self, event):
        self.hovered = True
        self.update()
        
    def leaveEvent(self, event):
        self.hovered = False
        self.update()
        
    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)
        
        rect = QRectF(0, 0, self.width(), self.height())
        radius = 10.0
        
        if self.isChecked():
            gradient = QLinearGradient(0, 0, 0, self.height())
            gradient.setColorAt(0, QColor("#f093fb"))
            gradient.setColorAt(1, QColor("#f5576c"))
            painter.setBrush(QBrush(gradient))
            painter.setPen(Qt.PenStyle.NoPen)
            painter.drawRoundedRect(rect.adjusted(2, 2, -2, -2), radius, radius)
        elif self.hovered:
            gradient = QLinearGradient(0, 0, 0, self.height())
            gradient.setColorAt(0, QColor(255, 255, 255, 250))
            gradient.setColorAt(1, QColor(240, 240, 250, 250))
            painter.setBrush(QBrush(gradient))
            painter.setPen(QPen(QColor("#e0e0e0"), 1))
            painter.drawRoundedRect(rect.adjusted(2, 2, -2, -2), radius, radius)
        else:
            gradient = QLinearGradient(0, 0, 0, self.height())
            gradient.setColorAt(0, QColor(255, 255, 255, 230))
            gradient.setColorAt(1, QColor(248, 248, 252, 230))
            painter.setBrush(QBrush(gradient))
            painter.setPen(QPen(QColor("#d0d0d0"), 1))
            painter.drawRoundedRect(rect.adjusted(2, 2, -2, -2), radius, radius)
        
        icon_color = QColor("#ffffff") if self.isChecked() else QColor("#555555")
        painter.setPen(QPen(icon_color, 2))
        
        center_x = self.width() // 2
        center_y = self.height() // 2 - 6
        
        painter.drawLine(center_x - 6, center_y - 3, center_x + 6, center_y - 3)
        painter.drawLine(center_x - 6, center_y + 1, center_x + 6, center_y + 1)
        painter.drawLine(center_x - 6, center_y + 5, center_x + 6, center_y + 5)
        
        painter.setPen(QPen(QColor("#999999") if not self.isChecked() else QColor("#ffffff"), 1))
        font = QFont("Microsoft YaHei", 6)
        painter.setFont(font)
        painter.drawText(QRectF(0, self.height() - 12, self.width(), 10), 
                        Qt.AlignmentFlag.AlignCenter, "穿透")


class ColorButton(QPushButton):
    def __init__(self, color, parent=None):
        super().__init__(parent)
        self.color = color
        self.setFixedSize(22, 22)
        self.hovered = False
        self.setCursor(Qt.CursorShape.PointingHandCursor)
        
    def enterEvent(self, event):
        self.hovered = True
        self.update()
        
    def leaveEvent(self, event):
        self.hovered = False
        self.update()
        
    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)
        
        rect = QRectF(0, 0, self.width(), self.height())
        
        if self.hovered:
            painter.setPen(QPen(QColor("#667eea"), 2))
            painter.setBrush(Qt.BrushStyle.NoBrush)
            painter.drawEllipse(rect.adjusted(1, 1, -1, -1))
        
        painter.setPen(Qt.PenStyle.NoPen)
        painter.setBrush(QBrush(QColor(self.color)))
        painter.drawEllipse(rect.adjusted(3, 3, -3, -3))
        
    def set_color(self, color):
        self.color = color
        self.update()


class ActionButton(QPushButton):
    def __init__(self, text, parent=None):
        super().__init__(text, parent)
        self.setFixedHeight(38)
        self.hovered = False
        self.setCursor(Qt.CursorShape.PointingHandCursor)
        
    def enterEvent(self, event):
        self.hovered = True
        self.update()
        
    def leaveEvent(self, event):
        self.hovered = False
        self.update()
        
    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)
        
        rect = QRectF(0, 0, self.width(), self.height())
        radius = 10.0
        
        if self.hovered:
            gradient = QLinearGradient(0, 0, 0, self.height())
            gradient.setColorAt(0, QColor("#667eea"))
            gradient.setColorAt(1, QColor("#764ba2"))
            painter.setBrush(QBrush(gradient))
            painter.setPen(Qt.PenStyle.NoPen)
        else:
            painter.setBrush(QBrush(QColor(255, 255, 255, 230)))
            painter.setPen(QPen(QColor("#d0d0d0"), 1))
        
        painter.drawRoundedRect(rect.adjusted(1, 1, -1, -1), radius, radius)
        
        text_color = QColor("#ffffff") if self.hovered else QColor("#555555")
        painter.setPen(QPen(text_color))
        font = QFont("Microsoft YaHei", 10, QFont.Weight.Medium)
        painter.setFont(font)
        painter.drawText(rect, Qt.AlignmentFlag.AlignCenter, self.text())


class Separator(QFrame):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setFixedHeight(1)
        self.setStyleSheet("background-color: rgba(200, 200, 200, 150);")


class Toolbar(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowFlags(
            Qt.WindowType.FramelessWindowHint |
            Qt.WindowType.WindowStaysOnTopHint |
            Qt.WindowType.Tool
        )
        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)
        self.setFixedSize(80, 930)
        self.setFocusPolicy(Qt.FocusPolicy.StrongFocus)
        self.init_ui()
        self.dragging = False
        self.drag_pos = QPoint()
        self.tool_changed_callback = None
        self.color_changed_callback = None
        self.width_changed_callback = None
        self.drawing_mode_changed_callback = None
        self.screenshot_callback = None
        self.clear_callback = None
        self.current_color = "#FF0000"
        self.current_width = 3
        self.current_font_size = 24
        self.font_size_changed_callback = None
        self.drawing_mode = True
        self.auto_hide = False
        self.hide_delay = 3000
        self.hide_timer = QTimer(self)
        self.hide_timer.timeout.connect(self.hide)
        self.geometry_changed_callback = None
        self.zoom_changed_callback = None
        self.mag_size_changed_callback = None
        self.close_callback = None
        
        self.raise_timer = QTimer(self)
        self.raise_timer.timeout.connect(self._on_raise_timer)
        self.raise_timer.start(100)
        
    def _on_raise_timer(self):
        self.raise_()
        
    def init_ui(self):
        main_layout = QVBoxLayout()
        main_layout.setContentsMargins(8, 8, 8, 8)
        main_layout.setSpacing(0)
        self.setLayout(main_layout)
        
        self.bg_widget = QWidget(self)
        self.bg_widget.setObjectName("bg_widget")
        self.bg_widget.setStyleSheet("""
            #bg_widget {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                    stop:0 rgba(255, 255, 255, 245),
                    stop:1 rgba(245, 247, 250, 245));
                border-radius: 16px;
                border: 1px solid rgba(200, 200, 210, 180);
            }
        """)
        self.bg_widget.setGeometry(0, 0, self.width(), self.height())
        
        content_widget = QWidget(self)
        content_widget.setGeometry(8, 8, self.width() - 16, self.height() - 16)
        layout = QVBoxLayout(content_widget)
        layout.setContentsMargins(2, 6, 2, 6)
        layout.setSpacing(6)
        
        self.drag_handle = QLabel("⋮⋮")
        self.drag_handle.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.drag_handle.setFixedHeight(28)
        self.drag_handle.setStyleSheet("""
            QLabel {
                background-color: rgba(180, 180, 190, 100);
                border-radius: 5px;
                font-size: 14px;
                color: #888;
            }
            QLabel:hover {
                background-color: rgba(150, 150, 160, 150);
                color: #666;
            }
        """)
        layout.addWidget(self.drag_handle)
        
        layout.addSpacing(4)
        
        self.penetrate_btn = PenetrateButton(self)
        self.penetrate_btn.clicked.connect(self._on_penetrate_clicked)
        layout.addWidget(self.penetrate_btn, 0, Qt.AlignmentFlag.AlignHCenter)
        
        layout.addSpacing(8)
        separator1 = Separator(self)
        layout.addWidget(separator1)
        layout.addSpacing(8)
        
        self.button_group = QButtonGroup(self)
        self.buttons = {}
        
        tools = ["brush", "eraser", "line", "rectangle", "circle", "text", "magnifier"]
        for tool in tools:
            btn = ModernToolButton(tool, self)
            self.button_group.addButton(btn)
            self.buttons[tool] = btn
            layout.addWidget(btn, 0, Qt.AlignmentFlag.AlignHCenter)
            layout.addSpacing(2)
            
        layout.addSpacing(8)
        separator2 = Separator(self)
        layout.addWidget(separator2)
        layout.addSpacing(8)
        
        color_label = QLabel("颜色")
        color_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        color_label.setStyleSheet("color: #666; font-size: 11px; font-weight: bold;")
        layout.addWidget(color_label)
        
        color_grid = QGridLayout()
        color_grid.setSpacing(4)
        color_grid.setContentsMargins(4, 4, 4, 4)
        
        self.color_buttons = []
        for i, color in enumerate(PRESET_COLORS):
            btn = ColorButton(color, self)
            btn.clicked.connect(lambda checked, c=color: self._on_color_clicked(c))
            self.color_buttons.append(btn)
            row = i // 4
            col = i % 4
            color_grid.addWidget(btn, row, col)
            
        color_container = QWidget()
        color_container.setLayout(color_grid)
        color_container.setFixedHeight(56)
        layout.addWidget(color_container)
        
        layout.addSpacing(8)
        separator3 = Separator(self)
        layout.addWidget(separator3)
        layout.addSpacing(8)
        
        font_label = QLabel("字号")
        font_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        font_label.setStyleSheet("color: #666; font-size: 11px; font-weight: bold;")
        layout.addWidget(font_label)
        
        self.font_size_spin = QSpinBox()
        self.font_size_spin.setRange(12, 72)
        self.font_size_spin.setValue(24)
        self.font_size_spin.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.font_size_spin.setFixedHeight(32)
        self.font_size_spin.valueChanged.connect(self._on_font_size_changed)
        self.font_size_spin.setStyleSheet("""
            QSpinBox {
                background: rgba(255, 255, 255, 220);
                border: 1px solid #ccc;
                border-radius: 6px;
                padding: 4px;
                font-size: 12px;
                font-weight: bold;
            }
            QSpinBox:hover {
                border-color: #999;
            }
            QSpinBox::up-button, QSpinBox::down-button {
                width: 20px;
                background: rgba(200, 200, 210, 100);
                border-radius: 3px;
            }
        """)
        layout.addWidget(self.font_size_spin)
        
        layout.addSpacing(8)
        
        width_label = QLabel("粗细")
        width_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        width_label.setStyleSheet("color: #666; font-size: 11px; font-weight: bold;")
        layout.addWidget(width_label)
        
        self.width_slider = QSlider(Qt.Orientation.Horizontal)
        self.width_slider.setRange(1, 20)
        self.width_slider.setValue(3)
        self.width_slider.valueChanged.connect(self._on_width_changed)
        self.width_slider.setFixedHeight(24)
        self.width_slider.setStyleSheet("""
            QSlider::groove:horizontal {
                background: rgba(200, 200, 210, 150);
                height: 6px;
                border-radius: 3px;
            }
            QSlider::handle:horizontal {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                    stop:0 #667eea, stop:1 #764ba2);
                width: 18px;
                height: 18px;
                margin: -6px 0;
                border-radius: 9px;
            }
            QSlider::handle:horizontal:hover {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                    stop:0 #5a6fd6, stop:1 #6a4190);
            }
        """)
        layout.addWidget(self.width_slider)
        
        layout.addSpacing(8)
        
        zoom_label = QLabel("放大倍数")
        zoom_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        zoom_label.setStyleSheet("color: #666; font-size: 11px; font-weight: bold;")
        layout.addWidget(zoom_label)
        
        self.zoom_spin = QSpinBox()
        self.zoom_spin.setRange(2, 8)
        self.zoom_spin.setValue(2)
        self.zoom_spin.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.zoom_spin.setFixedHeight(32)
        self.zoom_spin.setSuffix("x")
        self.zoom_spin.valueChanged.connect(self._on_zoom_changed)
        self.zoom_spin.setStyleSheet("""
            QSpinBox {
                background: rgba(255, 255, 255, 220);
                border: 1px solid #ccc;
                border-radius: 6px;
                padding: 4px;
                font-size: 12px;
                font-weight: bold;
            }
            QSpinBox:hover {
                border-color: #999;
            }
            QSpinBox::up-button, QSpinBox::down-button {
                width: 20px;
                background: rgba(200, 200, 210, 100);
                border-radius: 3px;
            }
        """)
        layout.addWidget(self.zoom_spin)
        
        layout.addSpacing(8)
        
        mag_size_label = QLabel("镜片大小")
        mag_size_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        mag_size_label.setStyleSheet("color: #666; font-size: 11px; font-weight: bold;")
        layout.addWidget(mag_size_label)
        
        self.mag_size_slider = QSlider(Qt.Orientation.Horizontal)
        self.mag_size_slider.setRange(100, 400)
        self.mag_size_slider.setValue(200)
        self.mag_size_slider.valueChanged.connect(self._on_mag_size_changed)
        self.mag_size_slider.setFixedHeight(24)
        self.mag_size_slider.setStyleSheet("""
            QSlider::groove:horizontal {
                background: rgba(200, 200, 210, 150);
                height: 6px;
                border-radius: 3px;
            }
            QSlider::handle:horizontal {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                    stop:0 #667eea, stop:1 #764ba2);
                width: 18px;
                height: 18px;
                margin: -6px 0;
                border-radius: 9px;
            }
            QSlider::handle:horizontal:hover {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                    stop:0 #5a6fd6, stop:1 #6a4190);
            }
        """)
        layout.addWidget(self.mag_size_slider)
        
        layout.addSpacing(8)
        separator4 = Separator(self)
        layout.addWidget(separator4)
        layout.addSpacing(8)
        
        save_btn = ActionButton("保存截图", self)
        save_btn.clicked.connect(self._on_save_clicked)
        layout.addWidget(save_btn)
        
        clear_btn = ActionButton("清空画布", self)
        clear_btn.clicked.connect(self._on_clear_clicked)
        layout.addWidget(clear_btn)
        
        layout.addSpacing(8)
        
        close_btn = ActionButton("退出程序", self)
        close_btn.clicked.connect(self._on_close_clicked)
        layout.addWidget(close_btn)
        
        layout.addStretch()
        
        self.button_group.buttonClicked.connect(self._on_tool_changed)
        
    def _on_penetrate_clicked(self):
        self.drawing_mode = not self.drawing_mode
        self.penetrate_btn.setChecked(not self.drawing_mode)
        if self.drawing_mode_changed_callback:
            self.drawing_mode_changed_callback(self.drawing_mode)
            
    def set_drawing_mode_changed_callback(self, callback):
        self.drawing_mode_changed_callback = callback
        
    def _on_tool_changed(self, button):
        if self.tool_changed_callback:
            self.tool_changed_callback(button.tool_type)
            
    def _on_color_clicked(self, color):
        self.current_color = color
        if self.color_changed_callback:
            self.color_changed_callback(color)
            
    def _on_width_changed(self, value):
        self.current_width = value
        if self.width_changed_callback:
            self.width_changed_callback(value)
            
    def _on_font_size_changed(self, value):
        self.current_font_size = value
        if self.font_size_changed_callback:
            self.font_size_changed_callback(value)
            
    def set_font_size_changed_callback(self, callback):
        self.font_size_changed_callback = callback
        
    def update_font_size(self, size):
        self.font_size_spin.blockSignals(True)
        self.font_size_spin.setValue(size)
        self.font_size_spin.blockSignals(False)
            
    def set_tool(self, tool_type):
        if tool_type in self.buttons:
            self.buttons[tool_type].setChecked(True)
            if self.tool_changed_callback:
                self.tool_changed_callback(tool_type)
            
    def set_tool_changed_callback(self, callback):
        self.tool_changed_callback = callback
        
    def set_color_changed_callback(self, callback):
        self.color_changed_callback = callback
        
    def set_width_changed_callback(self, callback):
        self.width_changed_callback = callback
        
    def _on_save_clicked(self):
        if self.screenshot_callback:
            self.screenshot_callback()
            
    def _on_clear_clicked(self):
        if self.clear_callback:
            self.clear_callback()
            
    def _on_close_clicked(self):
        if self.close_callback:
            self.close_callback()
            
    def set_screenshot_callback(self, callback):
        self.screenshot_callback = callback
        
    def set_clear_callback(self, callback):
        self.clear_callback = callback
        
    def set_close_callback(self, callback):
        self.close_callback = callback
        
    def update_current_color(self, color):
        self.current_color = color
        
    def mousePressEvent(self, event):
        if event.button() == Qt.MouseButton.LeftButton:
            handle_rect = self.drag_handle.geometry()
            handle_rect.moveTo(handle_rect.x() + 8, handle_rect.y() + 8)
            if handle_rect.contains(event.pos()):
                self.dragging = True
                self.drag_pos = event.globalPosition().toPoint() - self.frameGeometry().topLeft()
                self.setCursor(Qt.CursorShape.ClosedHandCursor)
                event.accept()
                return
        super().mousePressEvent(event)
            
    def mouseMoveEvent(self, event):
        if self.dragging:
            self.move(event.globalPosition().toPoint() - self.drag_pos)
            if self.geometry_changed_callback:
                self.geometry_changed_callback()
            event.accept()
            return
        super().mouseMoveEvent(event)
            
    def mouseReleaseEvent(self, event):
        if event.button() == Qt.MouseButton.LeftButton:
            if self.dragging:
                self.dragging = False
                self.setCursor(Qt.CursorShape.ArrowCursor)
                event.accept()
                return
        super().mouseReleaseEvent(event)
            
    def enterEvent(self, event):
        if self.auto_hide:
            self.hide_timer.stop()
            self.show()
            
    def leaveEvent(self, event):
        if self.auto_hide:
            self.hide_timer.start(self.hide_delay)
            
    def set_auto_hide(self, enabled, delay=3000):
        self.auto_hide = enabled
        self.hide_delay = delay
        
    def update_penetrate_button(self, drawing_mode):
        self.drawing_mode = drawing_mode
        self.penetrate_btn.setChecked(not drawing_mode)
        
    def update_width_slider(self, width):
        self.width_slider.blockSignals(True)
        self.width_slider.setValue(width)
        self.width_slider.blockSignals(False)
        self.current_width = width
        
    def _on_zoom_changed(self, value):
        if self.zoom_changed_callback:
            self.zoom_changed_callback(value)
            
    def _on_mag_size_changed(self, value):
        if self.mag_size_changed_callback:
            self.mag_size_changed_callback(value)
            
    def set_zoom_changed_callback(self, callback):
        self.zoom_changed_callback = callback
        
    def set_mag_size_changed_callback(self, callback):
        self.mag_size_changed_callback = callback
