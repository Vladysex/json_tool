"""
Конфігураційний модуль для JSON Tool
Містить налаштування застосунку
"""

import os

class Config:
    """Клас конфігурації застосунку"""
    
    APP_NAME = "JSON Tool"
    APP_VERSION = "1.0.0"
    
    WINDOW_WIDTH = 1000
    WINDOW_HEIGHT = 700
    WINDOW_MIN_WIDTH = 800
    WINDOW_MIN_HEIGHT = 600
    
    EDITOR_FONT_FAMILY = "Courier New"
    EDITOR_FONT_SIZE = 12
    EDITOR_TAB_WIDTH = 4
    
    SYNTAX_COLORS = {
        'brace': '#383A42',     
        'string': '#E45649',     
        'number': '#50A14F',     
        'boolean': '#986801',    
        'null': '#A626A4',       
        'key': '#A626A4',     
    }
    
    AUTOSAVE_ENABLED = True
    AUTOSAVE_INTERVAL = 5000 
    
    BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    DATA_DIR = os.path.join(BASE_DIR, 'data')
    
    
    VALIDATION_ON_TYPE = True
    VALIDATION_DELAY = 500
    
    MAX_UNDO_HISTORY = 100
    
    @classmethod
    def get_data_path(cls, filename):
        """Отримати повний шлях до файлу в папці data"""
        return os.path.join(cls.DATA_DIR, filename)
    
    @classmethod
    def ensure_data_dir(cls):
        """Переконатися, що папка data існує"""
        if not os.path.exists(cls.DATA_DIR):
            os.makedirs(cls.DATA_DIR)