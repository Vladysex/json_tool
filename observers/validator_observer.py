"""
Validator Observer
Автоматично валідує JSON при зміні документа
"""

from observers.observer import Observer
from typing import TYPE_CHECKING
import json
import time

if TYPE_CHECKING:
    from core.document import Document


class ValidationResult:
    """Клас для зберігання результату валідації"""
    
    def __init__(self, is_valid: bool, message: str = "", errors: list = None):
        self.is_valid = is_valid
        self.message = message
        self.errors = errors or []
        self.timestamp = time.time()
    
    def __str__(self) -> str:
        status = "✓ Валідний" if self.is_valid else "✗ Невалідний"
        return f"{status}: {self.message}"


class ValidatorObserver(Observer):
    """
    Спостерігач для автоматичної валідації JSON
    Перевіряє синтаксис JSON при кожній зміні документа
    """
    
    def __init__(self, name: str = "ValidatorObserver", auto_validate: bool = True):
        """
        Ініціалізація спостерігача валідації
        
        Args:
            name: Ім'я спостерігача
            auto_validate: Чи автом��тично валідувати при змінах
        """
        super().__init__(name)
        self._auto_validate = auto_validate
        self._last_result: ValidationResult = None
        self._validation_count = 0
    
    def update(self, document: 'Document', event_type: str, data: dict = None):
        """
        Обробити подію зміни документа
        
        Args:
            document: Документ, який змінився
            event_type: Тип події
            data: Додаткові дані
        """
        if event_type == 'content_changed' and self._auto_validate:
            self.validate(document)
    
    def validate(self, document: 'Document') -> ValidationResult:
        """
        Валідувати JSON документ
        
        Args:
            document: Документ для валідації
            
        Returns:
            ValidationResult з результатом валідації
        """
        content = document.get_content().strip()
        
        if not content:
            result = ValidationResult(
                is_valid=True,
                message="Документ порожній"
            )
            self._last_result = result
            self._validation_count += 1
            document.set_validation_result(result.__dict__)
            return result
        
        # Спроба парсити JSON
        try:
            json.loads(content)
            result = ValidationResult(
                is_valid=True,
                message="JSON синтаксис коректний"
            )
        except json.JSONDecodeError as e:
            result = ValidationResult(
                is_valid=False,
                message=f"Помилка JSON на рядку {e.lineno}, позиція {e.colno}",
                errors=[{
                    'line': e.lineno,
                    'column': e.colno,
                    'message': e.msg,
                    'position': e.pos
                }]
            )
        except Exception as e:
            result = ValidationResult(
                is_valid=False,
                message=f"Помилка валідації: {str(e)}",
                errors=[{'message': str(e)}]
            )
        
        self._last_result = result
        self._validation_count += 1
        
        document.set_validation_result({
            'is_valid': result.is_valid,
            'message': result.message,
            'errors': result.errors,
            'timestamp': result.timestamp
        })
        
        return result
    
    @property
    def last_result(self) -> ValidationResult:
        """Отримати результат останньої валідації"""
        return self._last_result
    
    @property
    def validation_count(self) -> int:
        """Отримати кількість виконаних валідацій"""
        return self._validation_count
    
    def enable_auto_validate(self):
        """Увімкнути автоматичну валідацію"""
        self._auto_validate = True
    
    def disable_auto_validate(self):
        """Вимкнути автоматичну валідацію"""
        self._auto_validate = False