"""
Concrete JSON Processor
Ко��кретна реалізація процесора JSON
"""

from .template import JSONProcessor
from typing import Tuple


class BasicJSONProcessor(JSONProcessor):
    """
    Базовий процесор JSON
    Виконує просту обробку та аналіз JSON файлів
    """
    
    def __init__(self):
        """Ініціалізація базового процесора"""
        super().__init__("BasicJSONProcessor")
    
    def validate_data(self, data: dict) -> Tuple[bool, dict]:
        """
        Валідувати дані (базова валідація структури)
        
        Args:
            data: Розпарсені JSON дані
            
        Returns:
            Tuple[success, validation_details]
        """
        validation_details = {
            'type': type(data).__name__,
            'is_dict': isinstance(data, dict),
            'is_list': isinstance(data, list),
            'is_empty': len(data) == 0 if isinstance(data, (dict, list)) else False
        }
        
        return True, validation_details
    
    def process_data(self, data: dict) -> Tuple[bool, dict]:
        """
        Обробити дані (базовий аналіз)
        
        Args:
            data: Валідовані дані
            
        Returns:
            Tuple[success, processed_data]
        """
        processed = {
            'statistics': self._calculate_statistics(data),
            'structure': self._analyze_structure(data)
        }
        
        return True, processed
    
    def generate_report(self, original_data: dict, processed_data: dict) -> dict:
        """
        Згенерувати звіт
        
        Args:
            original_data: Оригінальні дані
            processed_data: Оброблені дані
            
        Returns:
            Словник зі звітом
        """
        stats = processed_data.get('statistics', {})
        structure = processed_data.get('structure', {})
        
        return {
            'summary': f"Оброблено JSON з {stats.get('total_keys', 0)} ключами",
            'statistics': stats,
            'structure': structure
        }
    
    def _calculate_statistics(self, data) -> dict:
        """
        Розрахувати статистику JSON
        
        Args:
            data: JSON дані
            
        Returns:
            Словник зі статистикою
        """
        stats = {
            'total_keys': 0,
            'total_values': 0,
            'max_depth': 0,
            'types': {}
        }
        
        def count_recursive(obj, depth=0):
            stats['max_depth'] = max(stats['max_depth'], depth)
            
            if isinstance(obj, dict):
                stats['total_keys'] += len(obj)
                for value in obj.values():
                    stats['total_values'] += 1
                    type_name = type(value).__name__
                    stats['types'][type_name] = stats['types'].get(type_name, 0) + 1
                    count_recursive(value, depth + 1)
            
            elif isinstance(obj, list):
                for item in obj:
                    stats['total_values'] += 1
                    type_name = type(item).__name__
                    stats['types'][type_name] = stats['types'].get(type_name, 0) + 1
                    count_recursive(item, depth + 1)
        
        count_recursive(data)
        return stats
    
    def _analyze_structure(self, data) -> dict:
        """
        Аналізувати структуру JSON
        
        Args:
            data: JSON дані
            
        Returns:
            Словник з аналізом структури
        """
        structure = {
            'root_type': type(data).__name__,
            'root_keys': list(data.keys()) if isinstance(data, dict) else None,
            'root_length': len(data) if isinstance(data, (dict, list)) else 0
        }
        
        return structure


class StatisticsJSONProcessor(JSONProcessor):
    """
    Процесор JSON для детальної статистики
    Розширює базовий процесор додатковими можливостями аналізу
    """
    
    def __init__(self):
        """Ініціалізація статистичного процесора"""
        super().__init__("StatisticsJSONProcessor")
    
    def validate_data(self, data: dict) -> Tuple[bool, dict]:
        """Валідувати дані"""
        return True, {'validated': True}
    
    def process_data(self, data: dict) -> Tuple[bool, dict]:
        """Обробити дані з детальною статистикою"""
        processed = {
            'string_analysis': self._analyze_strings(data),
            'number_analysis': self._analyze_numbers(data),
            'array_analysis': self._analyze_arrays(data)
        }
        
        return True, processed
    
    def generate_report(self, original_data: dict, processed_data: dict) -> dict:
        """Згенерувати детальний звіт"""
        return {
            'summary': 'Детальний статистичний аналіз JSON',
            'details': processed_data
        }
    
    def _analyze_strings(self, data) -> dict:
        """Аналіз рядків у JSON"""
        strings = []
        
        def find_strings(obj):
            if isinstance(obj, str):
                strings.append(obj)
            elif isinstance(obj, dict):
                for value in obj.values():
                    find_strings(value)
            elif isinstance(obj, list):
                for item in obj:
                    find_strings(item)
        
        find_strings(data)
        
        return {
            'count': len(strings),
            'total_length': sum(len(s) for s in strings),
            'avg_length': sum(len(s) for s in strings) / len(strings) if strings else 0
        }
    
    def _analyze_numbers(self, data) -> dict:
        """Аналіз чисел у JSON"""
        numbers = []
        
        def find_numbers(obj):
            if isinstance(obj, (int, float)) and not isinstance(obj, bool):
                numbers.append(obj)
            elif isinstance(obj, dict):
                for value in obj.values():
                    find_numbers(value)
            elif isinstance(obj, list):
                for item in obj:
                    find_numbers(item)
        
        find_numbers(data)
        
        return {
            'count': len(numbers),
            'min': min(numbers) if numbers else None,
            'max': max(numbers) if numbers else None,
            'avg': sum(numbers) / len(numbers) if numbers else None
        }
    
    def _analyze_arrays(self, data) -> dict:
        """Аналіз масивів у JSON"""
        arrays = []
        
        def find_arrays(obj):
            if isinstance(obj, list):
                arrays.append(obj)
                for item in obj:
                    find_arrays(item)
            elif isinstance(obj, dict):
                for value in obj.values():
                    find_arrays(value)
        
        find_arrays(data)
        
        return {
            'count': len(arrays),
            'total_elements': sum(len(arr) for arr in arrays),
            'avg_size': sum(len(arr) for arr in arrays) / len(arrays) if arrays else 0
        }