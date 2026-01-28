"""
Command Pattern - Delete Command
Команда для видалення тексту з документа
"""

from .command import Command
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from core.document import Document


class DeleteCommand(Command):
    """
    Команда видалення тексту
    Інкапсулює операцію видалення тексту з певної позиції
    """
    
    def __init__(self, document: 'Document', start_position: int, end_position: int):
        """
        Ініціалізація команди видалення
        
        Args:
            document: Документ, з якого видаляється текст
            start_position: Початкова позиція видалення
            end_position: Кінцева позиція видалення
        """
        length = end_position - start_position
        super().__init__(f"Видалення {length} символів з позиції {start_position}")
        self._document = document
        self._start_position = start_position
        self._end_position = end_position
        self._deleted_text = ""  # Зберігається при виконанні для можливості undo
    
    def execute(self) -> bool:
        """
        Виконати видалення тексту
        
        Returns:
            True якщо видалення успішне
        """
        try:
            self._deleted_text = self._document.get_text(
                self._start_position, 
                self._end_position
            )
            
            self._document.delete(self._start_position, self._end_position)
            self._executed = True
            return True
        except Exception as e:
            print(f"Помилка виконання DeleteCommand: {e}")
            return False
    
    def undo(self) -> bool:
        """
        Скасувати видалення (вставити видалений текст назад)
        
        Returns:
            True якщо скасування успішне
        """
        try:
            self._document.insert(self._start_position, self._deleted_text)
            self._executed = False
            return True
        except Exception as e:
            print(f"Помилка скасування DeleteCommand: {e}")
            return False
    
    @property
    def start_position(self) -> int:
        """Отримати початкову позицію видалення"""
        return self._start_position
    
    @property
    def end_position(self) -> int:
        """Отримати кінцову позицію видалення"""
        return self._end_position
    
    @property
    def deleted_text(self) -> str:
        """Отримати видалений текст"""
        return self._deleted_text
    
    @property
    def length(self) -> int:
        """Отримати довжину видаленого тексту"""
        return len(self._deleted_text)