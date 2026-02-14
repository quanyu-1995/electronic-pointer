from typing import List
import copy

class HistoryManager:
    def __init__(self, max_history=50):
        self.undo_stack: List[List] = []
        self.redo_stack: List[List] = []
        self.max_history = max_history
        self.current_state: List = []
        
    def save_state(self, elements: List):
        self.undo_stack.append(copy.deepcopy(elements))
        self.redo_stack.clear()
        
        if len(self.undo_stack) > self.max_history:
            self.undo_stack.pop(0)
            
    def undo(self) -> List:
        if not self.undo_stack:
            return []
            
        current = self.undo_stack.pop()
        self.redo_stack.append(current)
        
        if self.undo_stack:
            return copy.deepcopy(self.undo_stack[-1])
        return []
        
    def redo(self) -> List:
        if not self.redo_stack:
            return []
            
        state = self.redo_stack.pop()
        self.undo_stack.append(state)
        return copy.deepcopy(state)
        
    def can_undo(self) -> bool:
        return len(self.undo_stack) > 1
        
    def can_redo(self) -> bool:
        return len(self.redo_stack) > 0
