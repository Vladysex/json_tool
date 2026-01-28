"""
Strategy Pattern - Validation Strategy
Базовий інтерфейс для стратегій валідації JSON
"""

from abc import ABC, abstractmethod
from typing import Optional
from dataclasses import dataclass
from datetime import datetime


@dataclass
class ValidationError:
    """Клас для представлення помилки валідації"""
    message: str
    line: Optional[int] = None
    column: Optional[int] = None
    path: Optional[str] = None
    error_type: str = "validation_error"
    
    def __str__(self) -> str:
        if self.line and self.column:
            return f"[Рядок {self.line}, позиція {self.column}] {self.message}"
        elif self.path:
            return f"[{self.path}] {self.message}"
        return self.message


@dataclass
class ValidationResult:
    """Клас для представлення результату валідації"""
    is_valid: bool
    validator_name: str
    message: str = ""
    errors: list[ValidationError] = None
    warnings: list[str] = None
    timestamp: float = None
    duration: float = 0.0
    
    def __post_init__(self):
        if self.errors is None:
            self.errors = []
        if self.warnings is None:
            self.warnings = []
        if self.timestamp is None:
            self.timestamp = datetime.now().timestamp()
    
    def add_error(self, error: ValidationError):
        """Додати помилку"""
        self.errors.append(error)
        self.is_valid = False
    
    def add_warning(self, warning: str):
        """Додати попередження"""
        self.warnings.append(warning)
    
    def get_summary(self) -> str:
        """Отримати короткий підсумок"""
        status = "✓ Валідний" if self.is_valid else "✗ Невалідний"
        error_count = len(self.errors)
        warning_count = len(self.warnings)
        
        summary = f"{status} [{self.validator_name}]"
        if error_count > 0:
            summary += f" ({error_count} помилок)"
        if warning_count > 0:
            summary += f" ({warning_count} попереджень)"
        
        return summary
    
    def __str__(self) -> str:
        return self.get_summary()


class ValidationStrategy(ABC):
    """
    Абстрактна базова стратегія валідації
    Визначає інтерфейс для всіх валідаторів
    """
    
    def __init__(self, name: str = "Validator"):
        """
        Ініціалізація стратегії
        
        Args:
            name: Назва валідатора
        """
        self._name = name
        self._enabled = True
    
    @abstractmethod
    def validate(self, json_text: str) -> ValidationResult:
        """
        Валідувати JSON текст
        
        Args:
            json_text: JSON текст для валідації
            
        Returns:
            ValidationResult з результатом валідації
        """
        pass
    
    @property
    def name(self) -> str:
        """Отримати назву валідатора"""
        return self._name
    
    @property
    def enabled(self) -> bool:
        """Перевірити, чи увімкнений валідатор"""
        return self._enabled
    
    def enable(self):
        """Увімкнути валідатор"""
        self._enabled = True
    
    def disable(self):
        """Вимкнути валідатор"""
        self._enabled = False
    
    def __str__(self) -> str:
        status = "увімкнено" if self._enabled else "вимкнено"
        return f"{self.__class__.__name__}('{self._name}', {status})"


class CompositeValidator(ValidationStrategy):
    """
    Складений валідатор (Composite Pattern)
    Дозволяє комбінувати декілька валідаторів
    """
    
    def __init__(self, name: str = "CompositeValidator"):
        """Ініціалізація складеного валідатора"""
        super().__init__(name)
        self._validators: list[ValidationStrategy] = []
    
    def add_validator(self, validator: ValidationStrategy):
        """
        Додати валідатор
        
        Args:
            validator: Валідатор для додавання
        """
        if validator not in self._validators:
            self._validators.append(validator)
    
    def remove_validator(self, validator: ValidationStrategy):
        """
        Видалити валідатор
        
        Args:
            validator: Валідатор для видалення
        """
        if validator in self._validators:
            self._validators.remove(validator)
    
    def validate(self, json_text: str) -> ValidationResult:
        """
        Виконати валідацію всіма валідаторами
        
        Args:
            json_text: JSON текст для валідації
            
        Returns:
            ValidationResult з об'єднаними результатами
        """
        import time
        start_time = time.time()
        
        result = ValidationResult(
            is_valid=True,
            validator_name=self._name,
            message="Композитна валідація"
        )
        
        for validator in self._validators:
            if validator.enabled:
                validator_result = validator.validate(json_text)
                
                if not validator_result.is_valid:
                    result.is_valid = False
                
                result.errors.extend(validator_result.errors)
                result.warnings.extend(validator_result.warnings)
        
        result.duration = time.time() - start_time
        
        if result.is_valid:
            result.message = f"Всі валідатори ({len(self._validators)}) пройдено успішно"
        else:
            result.message = f"Виявлено помилки в {len(result.errors)} валідаторах"
        
        return result
    
    def get_validators_count(self) -> int:
        """Отримати кількість валідаторів"""
        return len(self._validators)