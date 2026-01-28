"""
Autosave Observer
Автоматично зберігає документ при зміні
"""

from observers.observer import Observer
from typing import TYPE_CHECKING, Optional
import time
import os

if TYPE_CHECKING:
    from core.document import Document


class AutosaveObserver(Observer):
    """
    Спостерігач для автоматичного збереження документа
    Зберігає документ після певного часу неактивності
    """
    
    def __init__(self, 
                 name: str = "AutosaveObserver",
                 autosave_dir: str = None,
                 interval: float = 5.0):
        """
        Ініціалізація спостерігача автозбереження
        
        Args:
            name: Ім'я спостерігача
            autosave_dir: Директорія для автозбереження
            interval: Інтервал в секундах (мінімальний час між збереженнями)
        """
        super().__init__(name)
        self._autosave_dir = autosave_dir or os.path.join(os.getcwd(), 'autosave')
        self._interval = interval
        self._last_save_time = 0
        self._changes_since_save = 0
        self._total_autosaves = 0
        self._enabled_autosave = True
    
    def update(self, document: 'Document', event_type: str, data: dict = None):
        """
        Обробити подію зміни документа
        
        Args:
            document: Документ, який змінився
            event_type: Тип події
            data: Додаткові дані
        """
        if event_type == 'content_changed' and self._enabled_autosave:
            self._changes_since_save += 1
            
            current_time = time.time()
            if current_time - self._last_save_time >= self._interval:
                self._perform_autosave(document)
    
    def _perform_autosave(self, document: 'Document'):
        """
        Виконати автозбереження
        
        Args:
            document: Документ для збереження
        """
        try:
            if not os.path.exists(self._autosave_dir):
                os.makedirs(self._autosave_dir)
            
            if document.filepath:
                base_name = os.path.basename(document.filepath)
                autosave_path = os.path.join(self._autosave_dir, f".autosave_{base_name}")
            else:
                timestamp = int(time.time())
                autosave_path = os.path.join(self._autosave_dir, f".autosave_untitled_{timestamp}.json")
            
            with open(autosave_path, 'w', encoding='utf-8') as f:
                f.write(document.get_content())
            
            self._last_save_time = time.time()
            self._changes_since_save = 0
            self._total_autosaves += 1
            
            print(f"[Autosave] Документ автоматично збережено: {autosave_path}")
            
        except Exception as e:
            print(f"[Autosave] Помилка автозбереження: {e}")
    
    def get_statistics(self) -> dict:
        """
        Отримати статистику автозбереження
        
        Returns:
            Словник зі статистикою
        """
        time_since_save = time.time() - self._last_save_time if self._last_save_time > 0 else 0
        
        return {
            'enabled': self._enabled_autosave,
            'interval': self._interval,
            'total_autosaves': self._total_autosaves,
            'changes_since_save': self._changes_since_save,
            'time_since_last_save': round(time_since_save, 2),
            'autosave_dir': self._autosave_dir
        }
    
    def enable_autosave(self):
        """Увімкнути автозбереження"""
        self._enabled_autosave = True
    
    def disable_autosave(self):
        """Вимкнути автозбереження"""
        self._enabled_autosave = False
    
    def force_autosave(self, document: 'Document'):
        """
        Примусово виконати автозбереження
        
        Args:
            document: Документ для збереження
        """
        self._perform_autosave(document)