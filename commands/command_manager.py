"""
Command Manager
Управляє історією команд та забезпечує Undo/Redo функціональність
"""

from .command import Command
from typing import Optional, List
from utils.config import Config


class CommandManager:
    """
    Менеджер команд
    Відповідає за виконання команд та ведення історії для Undo/Redo
    """
    
    def __init__(self, max_history: int = None):
        """
        Ініціалізація менеджера команд
        
        Args:
            max_history: Максимальний розмір історії (None = необмежений)
        """
        self._history: List[Command] = []
        self._current_index = -1
        self._max_history = max_history or Config.MAX_UNDO_HISTORY
    
    def execute(self, command: Command) -> bool:
        """
        Виконати команду та додати її в історію
        
        Args:
            command: Команда для виконання
            
        Returns:
            True якщо команда виконана успішно
        """
        if not command.execute():
            return False
        
        if self._current_index < len(self._history) - 1:
            self._history = self._history[:self._current_index + 1]
        
        self._history.append(command)
        self._current_index += 1
        
        if len(self._history) > self._max_history:
            removed_count = len(self._history) - self._max_history
            self._history = self._history[removed_count:]
            self._current_index -= removed_count
        
        return True
    
    def undo(self) -> bool:
        """
        Скасувати останню команду
        
        Returns:
            True якщо скасування успішне, False якщо немає що скасовувати
        """
        if not self.can_undo():
            return False
        
        command = self._history[self._current_index]
        if command.undo():
            self._current_index -= 1
            return True
        
        return False
    
    def redo(self) -> bool:
        """
        Повторити скасовану команду
        
        Returns:
            True якщо повторення успішне, False якщо немає що повторювати
        """
        if not self.can_redo():
            return False
        
        command = self._history[self._current_index + 1]
        if command.execute():
            self._current_index += 1
            return True
        
        return False
    
    def can_undo(self) -> bool:
        """Перевірити, чи можна виконати undo"""
        return self._current_index >= 0
    
    def can_redo(self) -> bool:
        """Перевірити, чи можна виконати redo"""
        return self._current_index < len(self._history) - 1
    
    def get_undo_description(self) -> Optional[str]:
        """
        Отримати опис команди, яку можна скасувати
        
        Returns:
            Опис команди або None
        """
        if self.can_undo():
            return self._history[self._current_index].description
        return None
    
    def get_redo_description(self) -> Optional[str]:
        """
        Отримати опис команди, яку можна повторити
        
        Returns:
            Опис команди або None
        """
        if self.can_redo():
            return self._history[self._current_index + 1].description
        return None
    
    def clear_history(self):
        """Очистити всю історію команд"""
        self._history.clear()
        self._current_index = -1
    
    def get_history_info(self) -> dict:
        """
        Отримати інформацію про історію команд
        
        Returns:
            Словник з інформацією
        """
        return {
            'total_commands': len(self._history),
            'current_index': self._current_index,
            'can_undo': self.can_undo(),
            'can_redo': self.can_redo(),
            'undo_count': self._current_index + 1,
            'redo_count': len(self._history) - self._current_index - 1,
            'max_history': self._max_history
        }
    
    def get_history(self) -> List[str]:
        """
        Отримати список описів всіх команд в історії
        
        Returns:
            Список описів команд
        """
        history = []
        for i, command in enumerate(self._history):
            prefix = "→ " if i == self._current_index else "  "
            history.append(f"{prefix}{command.description}")
        return history
    
    def __str__(self) -> str:
        """Строкове представлення менеджера"""
        info = self.get_history_info()
        return (f"CommandManager(commands={info['total_commands']}, "
                f"position={info['current_index'] + 1}, "
                f"can_undo={info['can_undo']}, "
                f"can_redo={info['can_redo']})")