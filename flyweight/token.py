"""
Flyweight Pattern - Token
Представляє токен JSON (дужки, коми, лапки тощо)
Використовується для економії пам'яті при роботі з великими документами
"""


class Token:
    """
    Flyweight клас для представлення токенів JSON
    Об'єкти цього класу будуть спільними для однакових токенів
    """
    
    def __init__(self, value: str, token_type: str = 'symbol'):
        """
        Ініціалізація токена
        
        Args:
            value: Значення токена (наприклад, '{', '}', '[', ']', ':', ',')
            token_type: Тип токена ('symbol', 'string', 'number', 'boolean', 'null')
        """
        self._value = value
        self._token_type = token_type
    
    @property
    def value(self) -> str:
        """Отримати значення токена"""
        return self._value
    
    @property
    def token_type(self) -> str:
        """Отримати тип токена"""
        return self._token_type
    
    def __str__(self) -> str:
        """Строкове представлення токена"""
        return f"Token(value='{self._value}', type='{self._token_type}')"
    
    def __repr__(self) -> str:
        """Представлення для debugging"""
        return self.__str__()
    
    def __eq__(self, other) -> bool:
        """Порівняння токенів"""
        if not isinstance(other, Token):
            return False
        return self._value == other._value and self._token_type == other._token_type
    
    def __hash__(self) -> int:
        """Хеш для використання в словниках"""
        return hash((self._value, self._token_type))
    
    def get_color(self, color_scheme: dict) -> str:
        """
        Отримати колір токена згідно зі схемою
        
        Args:
            color_scheme: Словник з кольорами для різних типів токенів
            
        Returns:
            Колір у форматі hex
        """
        type_to_color_key = {
            'symbol': 'brace',
            'string': 'string',
            'number': 'number',
            'boolean': 'boolean',
            'null': 'null',
            'key': 'key'
        }
        
        color_key = type_to_color_key.get(self._token_type, 'brace')
        return color_scheme.get(color_key, '#000000')