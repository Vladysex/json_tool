"""
Document - Core class
Представляє JSON документ та керує його вмістом
Реалізує Subject для Observer Pattern
"""

from observers.observer import Subject
from typing import Optional
import time


class Document(Subject):
    """
    Клас документа
    Зберігає та керує вмістом JSON документа
    Сповіщає спостерігачів про зміни
    """
    
    def __init__(self, filepath: Optional[str] = None, content: str = ""):
        """
        Ініціалізація документа
        
        Args:
            filepath: Шлях до файлу (може бути None для нового документа)
            content: Початковий вміст
        """
        super().__init__()
        
        self._filepath = filepath
        self._content = content
        self._modified = False
        self._created_time = time.time()
        self._modified_time = self._created_time
        self._read_only = False
        
        self._edit_count = 0
        self._last_validation_result = None
        
    def get_content(self) -> str:
        """Отримати весь вміст документа"""
        return self._content
    
    def set_content(self, content: str, notify: bool = True):
        """
        Встановити новий вміст документа
        
        Args:
            content: Новий вміст
            notify: Чи сповіщати спостерігачів
        """
        if self._read_only:
            raise RuntimeError("Документ доступний тільки для читання")
        
        old_content = self._content
        self._content = content
        self._modified = True
        self._modified_time = time.time()
        self._edit_count += 1
        
        if notify:
            self.notify('content_changed', {
                'old_content': old_content,
                'new_content': content,
                'full_replace': True
            })
    
    def insert(self, position: int, text: str, notify: bool = True):
        """
        Вставити текст на певну позицію
        
        Args:
            position: Позиція вставки
            text: Текст для вставки
            notify: Чи сповіщати спостерігачів
        """
        if self._read_only:
            raise RuntimeError("Документ доступний тільки для читання")
        
        if position < 0 or position > len(self._content):
            raise ValueError(f"Невалідна позиція: {position}")
        
        self._content = self._content[:position] + text + self._content[position:]
        self._modified = True
        self._modified_time = time.time()
        self._edit_count += 1
        
        if notify:
            self.notify('content_changed', {
                'operation': 'insert',
                'position': position,
                'text': text,
                'length': len(text)
            })
    
    def delete(self, start: int, end: int, notify: bool = True):
        """
        Видалити текст з діапазону
        
        Args:
            start: Початкова позиція
            end: Кінцева позиція
            notify: Чи сповіщати спостерігачів
        """
        if self._read_only:
            raise RuntimeError("Документ дост��пний тільки для читання")
        
        if start < 0 or end > len(self._content) or start > end:
            raise ValueError(f"Невалідний діапазон: {start}-{end}")
        
        deleted_text = self._content[start:end]
        self._content = self._content[:start] + self._content[end:]
        self._modified = True
        self._modified_time = time.time()
        self._edit_count += 1
        
        if notify:
            self.notify('content_changed', {
                'operation': 'delete',
                'start': start,
                'end': end,
                'deleted_text': deleted_text,
                'length': len(deleted_text)
            })
    
    def get_text(self, start: int, end: int) -> str:
        """
        Отримати текст з діапазону
        
        Args:
            start: Початкова позиція
            end: Кінцева позиція
            
        Returns:
            Текст з вказаного діапазону
        """
        if start < 0 or end > len(self._content) or start > end:
            raise ValueError(f"Невалідний діапазон: {start}-{end}")
        
        return self._content[start:end]
        
    def load_from_file(self, filepath: str, content: str):
        """
        Завантажити вміст з файлу
        
        Args:
            filepath: Шлях до файлу
            content: Вміст файлу
        """
        self._filepath = filepath
        self._content = content
        self._modified = False
        self._modified_time = time.time()
        
        self.notify('loaded', {
            'filepath': filepath,
            'size': len(content)
        })
    
    def mark_as_saved(self, filepath: Optional[str] = None):
        """
        Позначити документ як збережений
        
        Args:
            filepath: Новий шлях до файлу (якщо змінився)
        """
        if filepath:
            self._filepath = filepath
        
        self._modified = False
        
        self.notify('saved', {
            'filepath': self._filepath,
            'size': len(self._content)
        })
        
    @property
    def filepath(self) -> Optional[str]:
        """Отримати шлях до файлу"""
        return self._filepath
    
    @property
    def is_modified(self) -> bool:
        """Перевірити, чи змінено документ"""
        return self._modified
    
    @property
    def is_new(self) -> bool:
        """Перевірити, чи це новий документ (без файлу)"""
        return self._filepath is None
    
    @property
    def is_empty(self) -> bool:
        """Перевірити, чи порожній документ"""
        return len(self._content) == 0
    
    @property
    def size(self) -> int:
        """Отримати розмір документа в символах"""
        return len(self._content)
    
    @property
    def read_only(self) -> bool:
        """Перевірити, чи документ тільки для читання"""
        return self._read_only
    
    @read_only.setter
    def read_only(self, value: bool):
        """Встановити режим тільки для читання"""
        self._read_only = value
    
    @property
    def edit_count(self) -> int:
        """Отримати кількість редагувань"""
        return self._edit_count
        
    def get_info(self) -> dict:
        """
        Отримати інформацію про документ
        
        Returns:
            Словник з інформацією
        """
        return {
            'filepath': self._filepath,
            'is_new': self.is_new,
            'is_modified': self._modified,
            'is_empty': self.is_empty,
            'is_read_only': self._read_only,
            'size': self.size,
            'lines': self._content.count('\n') + 1,
            'edit_count': self._edit_count,
            'observers_count': self.get_observers_count(),
            'created_time': self._created_time,
            'modified_time': self._modified_time
        }
    
    def set_validation_result(self, result: dict):
        """
        Зберегти результат останньої валідації
        
        Args:
            result: Результат валідації
        """
        self._last_validation_result = result
    
    def get_validation_result(self) -> Optional[dict]:
        """Отримати результат останньої валідації"""
        return self._last_validation_result
        
    def clear(self, notify: bool = True):
        """
        Очистити документ
        
        Args:
            notify: Чи сповіщати спостерігачів
        """
        self.set_content("", notify=notify)
    
    def reset(self):
        """Скинути всі зміни (для нових документів)"""
        if not self.is_new:
            raise RuntimeError("Не можна скинути документ з файлом")
        
        self._content = ""
        self._modified = False
        self._edit_count = 0
        self._last_validation_result = None
        
        self.notify('reset', {})
    
    def __str__(self) -> str:
        """Строкове представлення документа"""
        name = self._filepath or "Новий документ"
        status = "змінено" if self._modified else "збережено"
        return f"Document('{name}', {self.size} символів, {status})"
    
    def __len__(self) -> int:
        """Отримати розмір документа"""
        return self.size