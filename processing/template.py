"""
Template Method Pattern - JSON Processor
Визначає загальний алгоритм обробки JSON файлів
"""

from abc import ABC, abstractmethod
from typing import Optional, Tuple
import json
import time


class JSONProcessor(ABC):
    """
    Абстрактний процесор JSON (Template Method Pattern)
    Визначає скелет алгоритму обробки JSON файлів
    """
    
    def __init__(self, name: str = "JSONProcessor"):
        """
        Ініціалізація процесора
        
        Args:
            name: Назва процесора
        """
        self._name = name
        self._last_result = None
    
    def process(self, filepath: str) -> dict:
        """
        Шаблонний метод для обробки JSON файлу
        Визначає послідовність кроків обробки
        
        Args:
            filepath: Шлях до JSON файлу
            
        Returns:
            Словник з результатами обробки
        """
        start_time = time.time()
        
        result = {
            'success': False,
            'processor': self._name,
            'filepath': filepath,
            'steps': {},
            'duration': 0.0
        }
        
        try:
            load_success, content = self.load_file(filepath)
            result['steps']['load'] = {'success': load_success}
            
            if not load_success:
                result['error'] = 'Помилка завантаження файлу'
                return result
            
            parse_success, data, parse_error = self.parse_json(content)
            result['steps']['parse'] = {
                'success': parse_success,
                'error': parse_error
            }
            
            if not parse_success:
                result['error'] = f'Помилка парсингу: {parse_error}'
                return result
            
            validate_success, validation_result = self.validate_data(data)
            result['steps']['validate'] = {
                'success': validate_success,
                'details': validation_result
            }
            
            if not validate_success:
                result['error'] = 'Валідація не пройдена'
                return result
            
            process_success, processed_data = self.process_data(data)
            result['steps']['process'] = {'success': process_success}
            result['processed_data'] = processed_data
            
            if not process_success:
                result['error'] = 'Помилка обробки даних'
                return result
            
            report = self.generate_report(data, processed_data)
            result['report'] = report
            
            # Успіх!
            result['success'] = True
            
        except Exception as e:
            result['error'] = f'Неочікувана помилка: {str(e)}'
        
        finally:
            result['duration'] = time.time() - start_time
            self._last_result = result
        
        return result
        
    def load_file(self, filepath: str) -> Tuple[bool, Optional[str]]:
        """
        Завантажити файл (конкретна реалізація)
        
        Args:
            filepath: Шлях до файлу
            
        Returns:
            Tuple[success, content]
        """
        try:
            with open(filepath, 'r', encoding='utf-8') as f:
                content = f.read()
            return True, content
        except Exception as e:
            print(f"Помилка завантаження файлу: {e}")
            return False, None
    
    def parse_json(self, content: str) -> Tuple[bool, Optional[dict], Optional[str]]:
        """
        Парсити JSON (конкретна реалізація)
        
        Args:
            content: JSON текст
            
        Returns:
            Tuple[success, data, error]
        """
        try:
            data = json.loads(content)
            return True, data, None
        except json.JSONDecodeError as e:
            return False, None, str(e)
        except Exception as e:
            return False, None, str(e)
    
    
    @abstractmethod
    def validate_data(self, data: dict) -> Tuple[bool, dict]:
        """
        Валідувати дані (має бути перевизначено в підкласах)
        
        Args:
            data: Розпарсені JSON дані
            
        Returns:
            Tuple[success, validation_details]
        """
        pass
    
    @abstractmethod
    def process_data(self, data: dict) -> Tuple[bool, dict]:
        """
        Обробити дані (має бути перевизначено в підкласах)
        
        Args:
            data: Валідовані дані
            
        Returns:
            Tuple[success, processed_data]
        """
        pass
    
    @abstractmethod
    def generate_report(self, original_data: dict, processed_data: dict) -> dict:
        """
        Згенерувати звіт (може бути перевизначено в підкласах)
        
        Args:
            original_data: Оригінальні дані
            processed_data: Оброблені дані
            
        Returns:
            Словник зі звітом
        """
        pass
        
    @property
    def name(self) -> str:
        """Отримати назву процесора"""
        return self._name
    
    @property
    def last_result(self) -> Optional[dict]:
        """Отримати результат останньої обробки"""
        return self._last_result