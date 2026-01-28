"""
Schema Validator - JSON Schema Validation
Валідація JSON за допомогою JSON Schema
"""

import json
import time
from typing import Optional
from .strategy import ValidationStrategy, ValidationResult, ValidationError

try:
    import jsonschema
    from jsonschema import validate, ValidationError as JsonSchemaValidationError
    JSONSCHEMA_AVAILABLE = True
except ImportError:
    JSONSCHEMA_AVAILABLE = False
    jsonschema = None


class SchemaValidator(ValidationStrategy):
    """
    Валідатор JSON Schema
    Перевіряє відповідність JSON певній схемі
    """
    
    def __init__(self, schema: Optional[dict] = None, schema_path: Optional[str] = None, 
                 name: str = "SchemaValidator"):
        """
        Ініціалізація валідатора схеми
        
        Args:
            schema: JSON Schema як словник
            schema_path: Шлях до файлу зі схемою
            name: Назва валідатора
        """
        super().__init__(name)
        
        if not JSONSCHEMA_AVAILABLE:
            raise ImportError(
                "Модуль jsonschema не встановлено. "
                "Встановіть його за допомогою: pip install jsonschema"
            )
        
        self._schema = None
        self._schema_path = schema_path
        
        if schema:
            self._schema = schema
        elif schema_path:
            self._load_schema_from_file(schema_path)
    
    def _load_schema_from_file(self, filepath: str):
        """
        Завантажити схему з файлу
        
        Args:
            filepath: Шлях до файлу схеми
        """
        try:
            with open(filepath, 'r', encoding='utf-8') as f:
                self._schema = json.load(f)
        except FileNotFoundError:
            raise FileNotFoundError(f"Файл схеми не знайдено: {filepath}")
        except json.JSONDecodeError as e:
            raise ValueError(f"Невалідний JSON в файлі схеми: {e}")
    
    def set_schema(self, schema: dict):
        """
        Встановити нову схему
        
        Args:
            schema: JSON Schema як словник
        """
        self._schema = schema
    
    def load_schema_from_file(self, filepath: str):
        """
        Завантажити схему з файлу
        
        Args:
            filepath: Шлях до файлу схеми
        """
        self._load_schema_from_file(filepath)
        self._schema_path = filepath
    
    def validate(self, json_text: str) -> ValidationResult:
        """
        Валідувати JSON за схемою
        
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
        
        if not self._schema:
            result.is_valid = False
            result.message = "Схема не встановлена"
            result.add_error(ValidationError(
                message="JSON Schema не встановлена для валідації",
                error_type="no_schema"
            ))
            result.duration = time.time() - start_time
            return result
        
        json_text = json_text.strip()
        if not json_text:
            result.is_valid = False
            result.message = "Документ порожній"
            result.add_error(ValidationError(
                message="Неможливо валідувати порожній документ за схемою",
                error_type="empty_document"
            ))
            result.duration = time.time() - start_time
            return result
        
        try:
            data = json.loads(json_text)
        except json.JSONDecodeError as e:
            result.is_valid = False
            result.message = "Невалідний JSON синтаксис"
            result.add_error(ValidationError(
                message=f"Спочатку виправте синтаксис JSON: {e.msg}",
                line=e.lineno,
                column=e.colno,
                error_type="syntax_error"
            ))
            result.duration = time.time() - start_time
            return result
        
        try:
            jsonschema.validate(instance=data, schema=self._schema)
            result.is_valid = True
            result.message = "JSON відповідає схемі"
            
        except JsonSchemaValidationError as e:
            result.is_valid = False
            result.message = "JSON не відповідає схемі"
            
            path = " → ".join(str(p) for p in e.path) if e.path else "root"
            
            result.add_error(ValidationError(
                message=e.message,
                path=path,
                error_type="schema_validation_error"
            ))
            
        except jsonschema.SchemaError as e:
            result.is_valid = False
            result.message = "Помилка в самій схемі"
            result.add_error(ValidationError(
                message=f"JSON Schema невалідна: {e.message}",
                error_type="schema_error"
            ))
        
        except Exception as e:
            result.is_valid = False
            result.message = "Неочікувана помилка"
            result.add_error(ValidationError(
                message=str(e),
                error_type="unexpected_error"
            ))
        
        result.duration = time.time() - start_time
        return result
    
    @property
    def has_schema(self) -> bool:
        """Перевірити, чи встановлена схема"""
        return self._schema is not None
    
    @property
    def schema(self) -> Optional[dict]:
        """Отримати поточну схему"""
        return self._schema
    
    @property
    def schema_path(self) -> Optional[str]:
        """Отримати шлях до файлу схеми"""
        return self._schema_path