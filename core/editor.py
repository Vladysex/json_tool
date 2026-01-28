"""
Editor - Core class
Головний клас редактора, що інтегрує всі компоненти
"""

from typing import Optional
from .document import Document
from commands.command_manager import CommandManager
from commands.insert_command import InsertCommand
from commands.delete_command import DeleteCommand
from validation.strategy import ValidationStrategy
from validation.simple_validator import SimpleValidator
from observers.validator_observer import ValidatorObserver
from observers.autosave_observer import AutosaveObserver
from observers.status_observer import StatusObserver
from utils.file_manager import FileManager


class Editor:
    """
    Головний клас редактора
    Координує роботу всіх компонентів системи
    """
    
    def __init__(self):
        """Ініціалізація редактора"""
        self._document = Document()
        
        self._command_manager = CommandManager()
        
        self._validator_observer = ValidatorObserver(auto_validate=True)
        self._autosave_observer = AutosaveObserver(interval=5.0)
        self._status_observer = StatusObserver()
        
        self._document.attach(self._validator_observer)
        self._document.attach(self._autosave_observer)
        self._document.attach(self._status_observer)
        
        self._validation_strategy: Optional[ValidationStrategy] = SimpleValidator()
        
        self._initialized = True
        
    def new_document(self):
        """Створити новий документ"""
        if self._document.is_modified:
            pass
        
        self._command_manager.clear_history()
        
        self._document = Document()
        
        self._document.attach(self._validator_observer)
        self._document.attach(self._autosave_observer)
        self._document.attach(self._status_observer)
    
    def open_file(self, filepath: str) -> tuple[bool, Optional[str]]:
        """
        Відкрити файл
        
        Args:
            filepath: Шлях до файлу
            
        Returns:
            Tuple[success, error_message]
        """
        success, content, error = FileManager.read_file(filepath)
        
        if not success:
            return False, error
        
        self._command_manager.clear_history()
        
        self._document = Document()
        self._document.attach(self._validator_observer)
        self._document.attach(self._autosave_observer)
        self._document.attach(self._status_observer)
        
        self._document.load_from_file(filepath, content)
        
        return True, None
    
    def save_file(self, filepath: Optional[str] = None) -> tuple[bool, Optional[str]]:
        """
        Зберегти файл
        
        Args:
            filepath: Шлях для збереження (якщо None, використовується поточний)
            
        Returns:
            Tuple[success, error_message]
        """
        save_path = filepath or self._document.filepath
        
        if not save_path:
            return False, "Не вказано шлях для збереження"
        
        content = self._document.get_content()
        success, error = FileManager.write_file(save_path, content)
        
        if success:
            self._document.mark_as_saved(save_path)
        
        return success, error
    
    def save_as(self, filepath: str) -> tuple[bool, Optional[str]]:
        """
        Зберегти як новий файл
        
        Args:
            filepath: Новий шлях для збереження
            
        Returns:
            Tuple[success, error_message]
        """
        return self.save_file(filepath)
        
    def insert_text(self, position: int, text: str) -> bool:
        """
        Вставити текст через Command Pattern
        
        Args:
            position: Позиція вставки
            text: Текст для вставки
            
        Returns:
            True якщо успішно
        """
        command = InsertCommand(self._document, position, text)
        return self._command_manager.execute(command)
    
    def delete_text(self, start: int, end: int) -> bool:
        """
        Видалити текст через Command Pattern
        
        Args:
            start: Початкова позиція
            end: Кінцева позиція
            
        Returns:
            True якщо успішно
        """
        command = DeleteCommand(self._document, start, end)
        return self._command_manager.execute(command)
    
    def replace_text(self, start: int, end: int, new_text: str) -> bool:
        """
        Замінити текст (комбінація delete + insert)
        
        Args:
            start: Початкова позиція
            end: Кінцева позиція
            new_text: Новий текст
            
        Returns:
            True якщо успішно
        """
        if not self.delete_text(start, end):
            return False
        
        return self.insert_text(start, new_text)
    
    def set_content(self, content: str):
        """
        Встановити весь вміст документа
        
        Args:
            content: Новий вміст
        """
        self._document.set_content(content)
    
    def get_content(self) -> str:
        """Отримати вміст документа"""
        return self._document.get_content()
        
    def undo(self) -> bool:
        """Скасувати останню команду"""
        return self._command_manager.undo()
    
    def redo(self) -> bool:
        """Повторити скасовану команду"""
        return self._command_manager.redo()
    
    def can_undo(self) -> bool:
        """Перевірити, чи можна скасувати"""
        return self._command_manager.can_undo()
    
    def can_redo(self) -> bool:
        """Перевірити, чи можна повторити"""
        return self._command_manager.can_redo()
    
    def get_undo_description(self) -> Optional[str]:
        """Отримати опис команди для скасування"""
        return self._command_manager.get_undo_description()
    
    def get_redo_description(self) -> Optional[str]:
        """Отримати опис команди для повторення"""
        return self._command_manager.get_redo_description()
        
    def set_validation_strategy(self, strategy: ValidationStrategy):
        """
        Встановити стратегію валідації
        
        Args:
            strategy: Нова стратегія валідації
        """
        self._validation_strategy = strategy
    
    def validate(self):
        """
        Виконати валідацію документа
        
        Returns:
            ValidationResult
        """
        if self._validation_strategy:
            return self._validation_strategy.validate(self._document.get_content())
        return None
    
    def get_validation_result(self):
        """Отримати результат останньої валідації"""
        return self._document.get_validation_result()
        
    def format_json(self, indent: int = 2) -> tuple[bool, Optional[str]]:
        """
        Форматувати JSON
        
        Args:
            indent: Розмір відступу
            
        Returns:
            Tuple[success, error_message]
        """
        content = self._document.get_content()
        success, formatted, error = FileManager.format_json(content, indent)
        
        if success:
            self._document.set_content(formatted)
            return True, None
        
        return False, error
        
    @property
    def document(self) -> Document:
        """Отримати документ"""
        return self._document
    
    @property
    def command_manager(self) -> CommandManager:
        """Отримати менеджер команд"""
        return self._command_manager
    
    @property
    def validator_observer(self) -> ValidatorObserver:
        """Отримати валідатор observer"""
        return self._validator_observer
    
    @property
    def status_observer(self) -> StatusObserver:
        """Отримати статус observer"""
        return self._status_observer
    
    @property
    def autosave_observer(self) -> AutosaveObserver:
        """Отримати autosave observer"""
        return self._autosave_observer
    
    @property
    def is_modified(self) -> bool:
        """Перевірити, чи змінено документ"""
        return self._document.is_modified
    
    @property
    def filepath(self) -> Optional[str]:
        """Отримати шлях до файлу"""
        return self._document.filepath
        
    def get_statistics(self) -> dict:
        """
        Отримати статистику редактора
        
        Returns:
            Словник зі статистикою
        """
        return {
            'document': self._document.get_info(),
            'commands': self._command_manager.get_history_info(),
            'validation': self._validator_observer.last_result.__dict__ if self._validator_observer.last_result else None,
            'status': self._status_observer.get_statistics(),
            'autosave': self._autosave_observer.get_statistics()
        }
    
    def get_status_message(self) -> str:
        """Отр��мати поточне статусне повідомлення"""
        return self._status_observer.get_status_message()
        
    def enable_autosave(self):
        """Увімкнути автозбереження"""
        self._autosave_observer.enable_autosave()
    
    def disable_autosave(self):
        """Вимкнути автозбереження"""
        self._autosave_observer.disable_autosave()
    
    def enable_auto_validation(self):
        """Увімкнути автоматичну валідацію"""
        self._validator_observer.enable_auto_validate()
    
    def disable_auto_validation(self):
        """Вимкнути автоматичну валідацію"""
        self._validator_observer.disable_auto_validate()
    
    def __str__(self) -> str:
        """Строкове представлення редактора"""
        filename = self._document.filepath or "Новий документ"
        status = "змінено" if self._document.is_modified else "збережено"
        return f"Editor('{filename}', {self._document.size} символів, {status})"