import unittest
import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from src.managers.history_manager import HistoryManager
from src.managers.style_manager import StyleManager, Style


class TestHistoryManager(unittest.TestCase):
    def setUp(self):
        self.manager = HistoryManager()
        
    def test_initial_state(self):
        self.assertEqual(len(self.manager.undo_stack), 0)
        self.assertEqual(len(self.manager.redo_stack), 0)
        
    def test_save_state(self):
        self.manager.save_state([])
        self.assertEqual(len(self.manager.undo_stack), 1)
        
    def test_save_multiple_states(self):
        self.manager.save_state(['a'])
        self.manager.save_state(['b'])
        self.manager.save_state(['c'])
        self.assertEqual(len(self.manager.undo_stack), 3)
        
    def test_undo(self):
        self.manager.save_state(['a'])
        self.manager.save_state(['b'])
        state = self.manager.undo()
        self.assertEqual(len(self.manager.redo_stack), 1)
        self.assertEqual(state, ['a'])
        
    def test_undo_empty_stack(self):
        state = self.manager.undo()
        self.assertEqual(state, [])
        
    def test_redo(self):
        self.manager.save_state(['a'])
        self.manager.save_state(['b'])
        self.manager.undo()
        state = self.manager.redo()
        self.assertEqual(len(self.manager.undo_stack), 2)
        self.assertEqual(state, ['b'])
        
    def test_redo_empty_stack(self):
        state = self.manager.redo()
        self.assertEqual(state, [])
        
    def test_can_undo(self):
        self.assertFalse(self.manager.can_undo())
        self.manager.save_state(['a'])
        self.manager.save_state(['b'])
        self.assertTrue(self.manager.can_undo())
        
    def test_can_redo(self):
        self.assertFalse(self.manager.can_redo())
        self.manager.save_state(['a'])
        self.manager.save_state(['b'])
        self.manager.undo()
        self.assertTrue(self.manager.can_redo())
        
    def test_save_clears_redo_stack(self):
        self.manager.save_state(['a'])
        self.manager.save_state(['b'])
        self.manager.undo()
        self.assertEqual(len(self.manager.redo_stack), 1)
        self.manager.save_state(['c'])
        self.assertEqual(len(self.manager.redo_stack), 0)
        
    def test_max_history_limit(self):
        manager = HistoryManager(max_history=3)
        manager.save_state(['a'])
        manager.save_state(['b'])
        manager.save_state(['c'])
        manager.save_state(['d'])
        self.assertEqual(len(manager.undo_stack), 3)
        
    def test_deep_copy_on_save(self):
        original = [['a']]
        self.manager.save_state(original)
        self.manager.save_state(['b'])
        original[0] = ['modified']
        state = self.manager.undo()
        self.assertEqual(state, [['a']])


class TestStyle(unittest.TestCase):
    def test_default_values(self):
        style = Style()
        self.assertEqual(style.color, "#FF0000")
        self.assertEqual(style.line_width, 3)
        self.assertEqual(style.fill_color, "")
        self.assertEqual(style.opacity, 255)
        self.assertEqual(style.font_size, 24)
        
    def test_custom_values(self):
        style = Style(color="#00FF00", line_width=5, fill_color="#0000FF", opacity=128, font_size=32)
        self.assertEqual(style.color, "#00FF00")
        self.assertEqual(style.line_width, 5)
        self.assertEqual(style.fill_color, "#0000FF")
        self.assertEqual(style.opacity, 128)
        self.assertEqual(style.font_size, 32)


class TestStyleManager(unittest.TestCase):
    def setUp(self):
        self.manager = StyleManager()
        
    def test_initial_style(self):
        style = self.manager.get_style()
        self.assertEqual(style.color, "#FF0000")
        self.assertEqual(style.line_width, 3)
        
    def test_set_color(self):
        self.manager.set_color("#00FF00")
        style = self.manager.get_style()
        self.assertEqual(style.color, "#00FF00")
        
    def test_set_line_width(self):
        self.manager.set_line_width(5)
        style = self.manager.get_style()
        self.assertEqual(style.line_width, 5)
        
    def test_set_fill_color(self):
        self.manager.set_fill_color("#0000FF")
        style = self.manager.get_style()
        self.assertEqual(style.fill_color, "#0000FF")
        
    def test_set_opacity(self):
        self.manager.set_opacity(128)
        style = self.manager.get_style()
        self.assertEqual(style.opacity, 128)
        
    def test_set_font_size(self):
        self.manager.set_font_size(32)
        style = self.manager.get_style()
        self.assertEqual(style.font_size, 32)
        
    def test_recent_colors_added(self):
        initial_count = len(self.manager.recent_colors)
        self.manager.set_color("#123456")
        self.assertEqual(len(self.manager.recent_colors), initial_count + 1)
        self.assertEqual(self.manager.recent_colors[0], "#123456")
        
    def test_recent_colors_not_duplicated(self):
        initial_count = len(self.manager.recent_colors)
        self.manager.set_color("#FF0000")
        self.assertEqual(len(self.manager.recent_colors), initial_count)
        
    def test_recent_colors_limit(self):
        for i in range(15):
            self.manager.set_color(f"#{i:06x}")
        self.assertLessEqual(len(self.manager.recent_colors), 10)


if __name__ == "__main__":
    unittest.main()
