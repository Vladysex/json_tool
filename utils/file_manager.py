"""
Менеджер роботи з файлами
Відповідає за читання та запис JSON-файлів
"""

import json
import os
from typing import Optional, Tuple


class FileManager:
    """Клас для роботи з файловою системою"""
    
    @staticmethod
    def read_file(filepath: str) -> Tuple[bool, Optional[str], Optional[str]]:
        """
        Читання файлу
        
        Args:
            filepath: Шлях до файлу
            
        Returns:
            Tuple[success, content, error_message]
        """
        try:
            if not os.path.exists(filepath):
                return False, None, f"Файл не знайдено: {filepath}"
            
            with open(filepath, 'r', encoding='utf-8') as file:
                content = file.read()
            
            return True, content, None
            
        except PermissionError:
            return False, None, "Немає прав доступу до файлу"
        except Exception as e:
            return False, None, f"Помилка читання файлу: {str(e)}"
    
    @staticmethod
    def write_file(filepath: str, content: str) -> Tuple[bool, Optional[str]]:
        """
        Запис файлу
        
        Args:
            filepath: Шлях до файлу
            content: Вміст для запису
            
        Returns:
            Tuple[success, error_message]
        """
        try:
            directory = os.path.dirname(filepath)
            if directory and not os.path.exists(directory):
                os.makedirs(directory)
            
            with open(filepath, 'w', encoding='utf-8') as file:
                file.write(content)
            
            return True, None
            
        except PermissionError:
            return False, "Немає прав запису до файлу"
        except Exception as e:
            return False, f"Помилка запису файлу: {str(e)}"
    
    @staticmethod
    def validate_json_file(filepath: str) -> Tuple[bool, Optional[dict], Optional[str]]:
        """
        Прочитати та валідувати JSON-файл
        
        Args:
            filepath: Шлях до файлу
            
        Returns:
            Tuple[success, parsed_data, error_message]
        """
        success, content, error = FileManager.read_file(filepath)
        
        if not success:
            return False, None, error
        
        try:
            data = json.loads(content)
            return True, data, None
        except json.JSONDecodeError as e:
            return False, None, f"Невалідний JSON: {str(e)}"
    
    @staticmethod
    def format_json(content: str, indent: int = 2) -> Tuple[bool, Optional[str], Optional[str]]:
        """
        Форматування JSON-тексту
        
        Args:
            content: JSON-текст
            indent: Відступ для форматування
            
        Returns:
            Tuple[success, formatted_content, error_message]
        """
        try:
            data = json.loads(content)
            formatted = json.dumps(data, indent=indent, ensure_ascii=False)
            return True, formatted, None
        except json.JSONDecodeError as e:
            return False, None, f"Невалідний JSON: {str(e)}"
    
    @staticmethod
    def get_file_info(filepath: str) -> dict:
        """
        Отримати інформацію про файл
        
        Args:
            filepath: Шлях до файлу
            
        Returns:
            Словник з інформацією про файл
        """
        if not os.path.exists(filepath):
            return {
                'exists': False,
                'size': 0,
                'modified': None
            }
        
        stat = os.stat(filepath)
        return {
            'exists': True,
            'size': stat.st_size,
            'modified': stat.st_mtime,
            'path': os.path.abspath(filepath),
            'name': os.path.basename(filepath)
        }