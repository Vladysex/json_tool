"""
Status Observer
Відстежує статус документа та надає інформацію для UI
"""

from observers.observer import Observer
from typing import TYPE_CHECKING, Optional
import time

if TYPE_CHECKING:
    from core.document import Document


class StatusObserver(Observer):
    """
    Спостерігач для відстеження статусу документа
    Зберігає інформацію про поточний стан для відображення в UI
    """
    
    def __init__(self, name: str = "StatusObserver"):
        """
        Ініціалізація спостерігача статусу
        
        Args:
            name: Ім'я спостерігача
        """
        super().__init__(name)
        self._status_message = "Готовий"
        self._last_event = None
        self._last_event_time = None
        self._event_history = []
        self._max_history = 20
    
    def update(self, document: 'Document', event_type: str, data: dict = None):
        """
        Обробити подію зміни документа
        
        Args:
            document: Документ, який змінився
            event_type: Тип події
            data: Додаткові дані
        """
        current_time = time.time()
        
        if event_type == 'content_changed':
            operation = data.get('operation', 'зміна') if data else 'зміна'
            if operation == 'insert':
                length = data.get('length', 0)
                self._status_message = f"Вставлено {length} символів"
            elif operation == 'delete':
                length = data.get('length', 0)
                self._status_message = f"Видалено {length} символів"
            else:
                self._status_message = "Документ змінено"
        
        elif event_type == 'saved':
            filepath = data.get('filepath', 'файл') if data else 'файл'
            self._status_message = f"Збережено: {filepath}"
        
        elif event_type == 'loaded':
            filepath = data.get('filepath', 'файл') if data else 'файл'
            size = data.get('size', 0) if data else 0
            self._status_message = f"Завантажено: {filepath} ({size} символів)"
        
        elif event_type == 'reset':
            self._status_message = "Документ скинуто"
        
        else:
            self._status_message = f"Подія: {event_type}"
        
        self._last_event = event_type
        self._last_event_time = current_time
        
        self._add_to_history({
            'event_type': event_type,
            'timestamp': current_time,
            'message': self._status_message,
            'data': data
        })
    
    def _add_to_history(self, event: dict):
        """
        Додати подію в історію
        
        Args:
            event: Інформація про подію
        """
        self._event_history.append(event)
        
        if len(self._event_history) > self._max_history:
            self._event_history = self._event_history[-self._max_history:]
    
    def get_status_message(self) -> str:
        """Отримати поточне статусне повідомлення"""
        return self._status_message
    
    def get_last_event(self) -> Optional[str]:
        """Отримати тип останньої події"""
        return self._last_event
    
    def get_last_event_time(self) -> Optional[float]:
        """Отримати час останньої події"""
        return self._last_event_time
    
    def get_time_since_last_event(self) -> Optional[float]:
        """Отримати час з останньої події в секундах"""
        if self._last_event_time is None:
            return None
        return time.time() - self._last_event_time
    
    def get_event_history(self) -> list:
        """
        Отримати історію подій
        
        Returns:
            Список подій
        """
        return self._event_history.copy()
    
    def get_recent_events(self, count: int = 5) -> list:
        """
        Отримати останні N подій
        
        Args:
            count: Кількість подій
            
        Returns:
            Список останніх подій
        """
        return self._event_history[-count:] if self._event_history else []
    
    def clear_history(self):
        """Очистити історію подій"""
        self._event_history.clear()
    
    def get_statistics(self) -> dict:
        """
        Отримати статистику
        
        Returns:
            Словник зі статистикою
        """
        event_counts = {}
        for event in self._event_history:
            event_type = event['event_type']
            event_counts[event_type] = event_counts.get(event_type, 0) + 1
        
        return {
            'current_status': self._status_message,
            'last_event': self._last_event,
            'events_count': len(self._event_history),
            'event_types': event_counts,
            'time_since_last_event': self.get_time_since_last_event()
        }