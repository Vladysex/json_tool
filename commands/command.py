"""
Command Pattern - Base Command
Базовий абстрактний клас для всіх команд редагування
"""

from abc import ABC, abstractmethod
from typing import Any


class Command(ABC):
    """
    Абстрактний базовий клас для команд
    Інкапсулює операцію разом з її параметрами
    """
    
    def __init__(self, description: str = ""):
        """
        Ініціалізація команди
        
        Args:
            description: Опис команди для відображення користувачу
        """
        self._description = description
        self._executed = False
    
    @abstractmethod
    def execute(self) -> bool:
        """
        Виконати команду
        
        Returns:
            True якщо команда виконана успішно, False інакше
        """
        pass
    
    @abstractmethod
    def undo(self) -> bool:
        """
        Скасувати команду (відкотити зміни)
        
        Returns:
            True якщо скасування успішне, False інакше
        """
        pass
    
    @property
    def description(self) -> str:
        """Отримати опис команди"""
        return self._description
    
    @property
    def executed(self) -> bool:
        """Перевірити, чи була команда виконана"""
        return self._executed
    
    def __str__(self) -> str:
        """Строкове представлення команди"""
        status = "виконано" if self._executed else "не виконано"
        return f"{self.__class__.__name__}: {self._description} ({status})"


class CompositeCommand(Command):
    """
    Складена команда (Composite Pattern)
    Дозволяє групувати декілька команд в одну
    """
    
    def __init__(self, description: str = "Група команд"):
        """Ініціалізація складеної команди"""
        super().__init__(description)
        self._commands: list[Command] = []
    
    def add_command(self, command: Command):
        """Додати команду до групи"""
        self._commands.append(command)
    
    def execute(self) -> bool:
        """Виконати всі команди в групі"""
        success = True
        for command in self._commands:
            if not command.execute():
                success = False
                break
        
        if success:
            self._executed = True
        
        return success
    
    def undo(self) -> bool:
        """Скасувати всі команди в зворотному порядку"""
        success = True
        for command in reversed(self._commands):
            if not command.undo():
                success = False
                break
        
        if success:
            self._executed = False
        
        return success
    
    def get_commands_count(self) -> int:
        """Отримати кількість команд у групі"""
        return len(self._commands)