"""
Simple Validator - Basic JSON Syntax Validation
Базова валідація синтаксису JSON
"""

import json
import time
from .strategy import ValidationStrategy, ValidationResult, ValidationError


class SimpleValidator(ValidationStrategy):
    """
    Простий валідатор JSON
    Перевіряє тільки синтаксичну коректність JSON
    """
    
    def __init__(self, name: str = "SimpleValidator"):
        """Ініціалізація простого валідатора"""
        super().__init__(name)
        self._allow_empty = True
        self._check_structure = True
    
    def validate(self, json_text: str) -> ValidationResult:
        """
        Валідувати JSON синтаксис
        
        Args:
            json_text: JSON текст для валідації
            
        Returns:
            ValidationResult з результатом валідації
        """
        start_time = time.time()
        
        result = ValidationResult(
            is_valid=True,
            validator_name=self._name
        )
        
        json_text = json_text.strip()
        if not json_text:
            if self._allow_empty:
                result.message = "Документ порожній (дозволено)"
                result.duration = time.time() - start_time
                return result
            else:
                result.is_valid = False
                result.message = "Документ порожній"
                result.add_error(ValidationError(
                    message="JSON документ не може бути порожнім",
                    error_type="empty_document"
                ))
                result.duration = time.time() - start_time
                return result
        
        try:
            parsed_data = json.loads(json_text)
            
            result.is_valid = True
            result.message = "JSON синтаксис коректний"
            
            if self._check_structure:
                self._check_json_structure(parsed_data, result)
            
        except json.JSONDecodeError as e:
            result.is_valid = False
            result.message = "Помилка синтаксису JSON"
            result.add_error(ValidationError(
                message=e.msg,
                line=e.lineno,
                column=e.colno,
                error_type="syntax_error"
            ))
        
        except Exception as e:
            result.is_valid = False
            result.message = "Неочікувана помилка валідації"
            result.add_error(ValidationError(
                message=str(e),
                error_type="unexpected_error"
            ))
        
        result.duration = time.time() - start_time
        return result
    
    def _check_json_structure(self, data, result: ValidationResult):
        """
        Перевірити структуру JSON (додаткові перевірки)
        
        Args:
            data: Розпарсені дані JSON
            result: Результат валідації для додавання попереджень
        """
        
        if isinstance(data, dict):
            depth = self._get_depth(data)
            if depth > 10:
                result.add_warning(f"Велика глибина вкладеності: {depth} рівнів")
            
            # Перевірити кількість ключів
            if len(data) > 100:
                result.add_warning(f"Велика кількість ключів на верхньому рівні: {len(data)}")
        
        elif isinstance(data, list):
            if len(data) > 1000:
                result.add_warning(f"Великий масив: {len(data)} елементів")
    
    def _get_depth(self, obj, current_depth=1) -> int:
        """
        Отримати глибину вкладеності JSON
        
        Args:
            obj: Об'єкт для перевірки
            current_depth: Поточна глибина
            
        Returns:
            Максимальна глибина вкладеності
        """
        if isinstance(obj, dict):
            if not obj:
                return current_depth
            return max(self._get_depth(v, current_depth + 1) for v in obj.values())
        elif isinstance(obj, list):
            if not obj:
                return current_depth
            return max(self._get_depth(item, current_depth + 1) for item in obj)
        else:
            return current_depth
    
    def set_allow_empty(self, allow: bool):
        """
        Встановити, чи дозволяти порожні документи
        
        Args:
            allow: True - дозволити, False - заборонити
        """
        self._allow_empty = allow
    
    def set_check_structure(self, check: bool):
        """
        Встановити, чи перевіряти структуру
        
        Args:
            check: True - перевіряти, False - не перевіряти
        """
        self._check_structure = check