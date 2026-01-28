"""
Observer Pattern - Base Observer
Базовий абстрактний клас для всіх спостерігачів
"""

from abc import ABC, abstractmethod
from typing import TYPE_CHECKING, Any

if TYPE_CHECKING:
    from core.document import Document


class Observer(ABC):
    """
    Абстрактний базовий клас для спостерігачів
    Спостерігачі отримують сповіщення про зміни в документі
    """
    
    def __init__(self, name: str = "Observer"):
        """
        Ініціалізація спостерігача
        
        Args:
            name: Ім'я спостерігача для ідентифікації
        """
        self._name = name
        self._enabled = True
    
    @abstractmethod
    def update(self, document: 'Document', event_type: str, data: dict = None):
        """
        Метод, який викликається при зміні документа
        
        Args:
            document: Документ, який змінився
            event_type: Тип події ('content_changed', 'saved', 'loaded' тощо)
            data: Додаткові дані про подію
        """
        pass
    
    @property
    def name(self) -> str:
        """Отримати ім'я спостерігача"""
        return self._name
    
    @property
    def enabled(self) -> bool:
        """Перевірити, чи увімкнений спостерігач"""
        return self._enabled
    
    def enable(self):
        """Увімкнути спостерігача"""
        self._enabled = True
    
    def disable(self):
        """Вимкнути спостерігача"""
        self._enabled = False
    
    def __str__(self) -> str:
        """Строкове представлення спостерігача"""
        status = "увімкнено" if self._enabled else "вимкнено"
        return f"{self.__class__.__name__}('{self._name}', {status})"


class Subject(ABC):
    """
    Абстрактний клас для об'єктів, які можуть мати спостерігачів
    Subject (Суб'єкт) — об'єкт, за яким спостерігають
    """
    
    def __init__(self):
        """Ініціалізація суб'єкта"""
        self._observers: list[Observer] = []
    
    def attach(self, observer: Observer):
        """
        Приєднати спостерігача
        
        Args:
            observer: Спостерігач для приєднання
        """
        if observer not in self._observers:
            self._observers.append(observer)
    
    def detach(self, observer: Observer):
        """
        Відключити спостерігача
        
        Args:
            observer: Спостерігач для відключення
        """
        if observer in self._observers:
            self._observers.remove(observer)
    
    def notify(self, event_type: str, data: dict = None):
        """
        Сповістити всіх спостерігачів про зміну
        
        Args:
            event_type: Тип події
            data: Додаткові дані про подію
        """
        for observer in self._observers:
            if observer.enabled:
                try:
                    observer.update(self, event_type, data or {})
                except Exception as e:
                    print(f"Помилка в observer {observer.name}: {e}")
    
    def get_observers_count(self) -> int:
        """Отримати кількість приєднаних спостерігачів"""
        return len(self._observers)
    
    def get_observers(self) -> list[Observer]:
        """Отримати список всіх спостерігачів"""
        return self._observers.copy()
    
    def clear_observers(self):
        """Видалити всіх спостерігачів"""
        self._observers.clear()