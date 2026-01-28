"""
Flyweight Pattern - TokenFactory
Фабрика для створення та кешування токенів
Гарантує, що для однакових значень використовується один об'єкт
"""

from .token import Token
from typing import Dict, Tuple


class TokenFactory:
    """
    Фабрика токенів (Flyweight Factory)
    Створює та кешує токени для економії пам'яті
    """
    
    def __init__(self):
        """Ініціалізація фабрики з порожнім кешем"""
        self._tokens: Dict[Tuple[str, str], Token] = {}
        self._statistics = {
            'created': 0,
            'reused': 0
        }
        
        self._initialize_common_tokens()
    
    def _initialize_common_tokens(self):
        """Попередньо створити найпоширеніші токени"""
        common_tokens = [
            ('{', 'symbol'),
            ('}', 'symbol'),
            ('[', 'symbol'),
            (']', 'symbol'),
            (':', 'symbol'),
            (',', 'symbol'),
            ('"', 'symbol'),
            ('true', 'boolean'),
            ('false', 'boolean'),
            ('null', 'null'),
        ]
        
        for value, token_type in common_tokens:
            self.get_token(value, token_type)
    
    def get_token(self, value: str, token_type: str = 'symbol') -> Token:
        """
        Отримати токен (створити новий або повернути існуючий)
        
        Args:
            value: Значення токена
            token_type: Тип токена
            
        Returns:
            Token об'єкт
        """
        key = (value, token_type)
        
        if key not in self._tokens:
            self._tokens[key] = Token(value, token_type)
            self._statistics['created'] += 1
        else:
            self._statistics['reused'] += 1
        
        return self._tokens[key]
    
    def get_token_count(self) -> int:
        """Отримати кількість унікальних токенів у кеші"""
        return len(self._tokens)
    
    def get_statistics(self) -> dict:
        """
        Отримати статистику використання фабрики
        
        Returns:
            Словник зі статистикою
        """
        total = self._statistics['created'] + self._statistics['reused']
        reuse_rate = (self._statistics['reused'] / total * 100) if total > 0 else 0
        
        return {
            'unique_tokens': len(self._tokens),
            'tokens_created': self._statistics['created'],
            'tokens_reused': self._statistics['reused'],
            'total_requests': total,
            'reuse_rate_percent': round(reuse_rate, 2),
            'memory_saved_estimate': self._estimate_memory_saved()
        }
    
    def _estimate_memory_saved(self) -> str:
        """
        Оцінити приблизну економію пам'яті
        
        Returns:
            Рядок з оцінкою економії
        """
        token_size_bytes = 64 
        
        saved_objects = self._statistics['reused']
        saved_bytes = saved_objects * token_size_bytes
        
        if saved_bytes < 1024:
            return f"{saved_bytes} bytes"
        elif saved_bytes < 1024 * 1024:
            return f"{saved_bytes / 1024:.2f} KB"
        else:
            return f"{saved_bytes / (1024 * 1024):.2f} MB"
    
    def clear_cache(self):
        """Очистити кеш токенів"""
        self._tokens.clear()
        self._statistics = {
            'created': 0,
            'reused': 0
        }
        self._initialize_common_tokens()
    
    def get_all_tokens(self) -> list:
        """
        Отримати список всіх закешованих токенів
        
        Returns:
            Список Token об'єктів
        """
        return list(self._tokens.values())


_global_token_factory = None


def get_token_factory() -> TokenFactory:
    """
    Отримати глобальний екземпляр фабрики токенів
    
    Returns:
        TokenFactory instance
    """
    global _global_token_factory
    if _global_token_factory is None:
        _global_token_factory = TokenFactory()
    return _global_token_factory