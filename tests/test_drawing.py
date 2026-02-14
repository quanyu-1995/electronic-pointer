import unittest
import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from PyQt6.QtCore import QPoint
from src.drawing.shapes import FreePath, Line, Rectangle, Circle, TextElement, EraserStroke


class TestFreePath(unittest.TestCase):
    def test_creation(self):
        points = [QPoint(0, 0), QPoint(10, 10), QPoint(20, 20)]
        path = FreePath(points, "#FF0000", 3)
        self.assertEqual(len(path.points), 3)
        self.assertEqual(path.color, "#FF0000")
        self.assertEqual(path.width, 3)
        
    def test_empty_points(self):
        path = FreePath([], "#FF0000", 3)
        self.assertEqual(len(path.points), 0)
        
    def test_single_point(self):
        points = [QPoint(0, 0)]
        path = FreePath(points, "#00FF00", 5)
        self.assertEqual(len(path.points), 1)
        self.assertEqual(path.color, "#00FF00")
        self.assertEqual(path.width, 5)


class TestLine(unittest.TestCase):
    def test_creation(self):
        line = Line(QPoint(0, 0), QPoint(100, 100), "#FF0000", 3)
        self.assertEqual(line.start, QPoint(0, 0))
        self.assertEqual(line.end, QPoint(100, 100))
        self.assertEqual(line.color, "#FF0000")
        self.assertEqual(line.width, 3)
        
    def test_horizontal_line(self):
        line = Line(QPoint(0, 50), QPoint(100, 50), "#0000FF", 2)
        self.assertEqual(line.start.y(), line.end.y())
        
    def test_vertical_line(self):
        line = Line(QPoint(50, 0), QPoint(50, 100), "#00FF00", 4)
        self.assertEqual(line.start.x(), line.end.x())


class TestRectangle(unittest.TestCase):
    def test_creation(self):
        rect = Rectangle(QPoint(0, 0), QPoint(100, 100), "#FF0000", 3)
        self.assertEqual(rect.start, QPoint(0, 0))
        self.assertEqual(rect.end, QPoint(100, 100))
        self.assertEqual(rect.color, "#FF0000")
        self.assertEqual(rect.width, 3)
        self.assertEqual(rect.fill_color, "")
        
    def test_with_fill_color(self):
        rect = Rectangle(QPoint(0, 0), QPoint(100, 100), "#FF0000", 3, "#00FF00")
        self.assertEqual(rect.fill_color, "#00FF00")
        
    def test_get_rect_normal(self):
        rect = Rectangle(QPoint(0, 0), QPoint(100, 50), "#FF0000", 3)
        x, y, w, h = rect._get_rect()
        self.assertEqual(x, 0)
        self.assertEqual(y, 0)
        self.assertEqual(w, 100)
        self.assertEqual(h, 50)
        
    def test_get_rect_reversed(self):
        rect = Rectangle(QPoint(100, 50), QPoint(0, 0), "#FF0000", 3)
        x, y, w, h = rect._get_rect()
        self.assertEqual(x, 0)
        self.assertEqual(y, 0)
        self.assertEqual(w, 100)
        self.assertEqual(h, 50)


class TestCircle(unittest.TestCase):
    def test_creation(self):
        circle = Circle(QPoint(50, 50), 50, "#FF0000", 3)
        self.assertEqual(circle.center, QPoint(50, 50))
        self.assertEqual(circle.radius, 50)
        self.assertEqual(circle.color, "#FF0000")
        self.assertEqual(circle.width, 3)
        self.assertEqual(circle.fill_color, "")
        
    def test_with_fill_color(self):
        circle = Circle(QPoint(50, 50), 50, "#FF0000", 3, "#00FF00")
        self.assertEqual(circle.fill_color, "#00FF00")
        
    def test_zero_radius(self):
        circle = Circle(QPoint(50, 50), 0, "#FF0000", 3)
        self.assertEqual(circle.radius, 0)


class TestTextElement(unittest.TestCase):
    def test_creation(self):
        text = TextElement(QPoint(50, 50), "Hello", "#FF0000", 16)
        self.assertEqual(text.pos, QPoint(50, 50))
        self.assertEqual(text.text, "Hello")
        self.assertEqual(text.color, "#FF0000")
        self.assertEqual(text.font_size, 16)
        self.assertFalse(text.bold)
        self.assertFalse(text.italic)
        
    def test_bold_italic(self):
        text = TextElement(QPoint(50, 50), "Hello", "#FF0000", 16, True, True)
        self.assertTrue(text.bold)
        self.assertTrue(text.italic)
        
    def test_update_text(self):
        text = TextElement(QPoint(50, 50), "Hello", "#FF0000", 16)
        text.update_text("World")
        self.assertEqual(text.text, "World")
        
    def test_empty_text(self):
        text = TextElement(QPoint(50, 50), "", "#FF0000", 16)
        self.assertEqual(text.text, "")


class TestEraserStroke(unittest.TestCase):
    def test_creation(self):
        points = [QPoint(0, 0), QPoint(10, 10)]
        eraser = EraserStroke(points, 20)
        self.assertEqual(len(eraser.points), 2)
        self.assertEqual(eraser.size, 20)


if __name__ == "__main__":
    unittest.main()
