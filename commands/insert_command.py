"""
Command Pattern - Insert Command
Команда для вставки тексту в документ
"""

from .command import Command
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from core.document import Document


class InsertCommand(Command):
    """
    Команда вставки тексту
    Інкапсулює операцію вставки тексту на певну позицію
    """
    
    def __init__(self, document: 'Document', position: int, text: str):
        """
        Ініціалізація команди вставки
        
        Args:
            document: Документ, в який вставляється текст
            position: Позиція вставки (індекс символа)
            text: Текст для вставки
        """
        super().__init__(f"Вставка {len(text)} символів на позицію {position}")
        self._document = document
        self._position = position
        self._text = text
    
    def execute(self) -> bool:
        """
        Виконати вставку тексту
        
        Returns:
            True якщо вставка успішна
        """
        try:
            self._document.insert(self._position, self._text)
            self._executed = True
            return True
        except Exception as e:
            print(f"Помилка виконання InsertCommand: {e}")
            return False
    
    def undo(self) -> bool:
        """
        Скасувати вставку (видалити вставлений текст)
        
        Returns:
            True якщо скасування успішне
        """
        try:
            end_position = self._position + len(self._text)
            self._document.delete(self._position, end_position)
            self._executed = False
            return True
        except Exception as e:
            print(f"Помилка скасування InsertCommand: {e}")
            return False
    
    @property
    def position(self) -> int:
        """Отримати позицію вставки"""
        return self._position
    
    @property
    def text(self) -> str:
        """Отримати текст для вставки"""
        return self._text
    
    @property
    def length(self) -> int:
        """Отримати довжину вставленого тексту"""
        return len(self._text)