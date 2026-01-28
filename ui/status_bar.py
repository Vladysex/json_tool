"""
Status Bar - Application Status Bar
Рядок статусу для відображення інформації
"""

import tkinter as tk
from tkinter import ttk


class StatusBar(tk.Frame):
    """
    Рядок статусу застосунку
    Відображає різну інформацію про стан редактора
    """
    
    def __init__(self, parent):
        """
        Ініціалізація рядка статусу
        
        Args:
            parent: Батьківський віджет
        """
        super().__init__(parent, relief=tk.SUNKEN, bd=1)
        
        self._create_widgets()
    
    def _create_widgets(self):
        """Створити віджети статусного рядка"""
        self._message_label = tk.Label(
            self,
            text="Готовий",
            anchor=tk.W,
            padx=5
        )
        self._message_label.pack(side=tk.LEFT, fill=tk.X, expand=True)
        
        ttk.Separator(self, orient=tk.VERTICAL).pack(side=tk.LEFT, fill=tk.Y, padx=2)
        
        self._validation_label = tk.Label(
            self,
            text="",
            anchor=tk.CENTER,
            width=15,
            padx=5
        )
        self._validation_label.pack(side=tk.LEFT)
        
        ttk.Separator(self, orient=tk.VERTICAL).pack(side=tk.LEFT, fill=tk.Y, padx=2)
        
        self._position_label = tk.Label(
            self,
            text="Рядок: 1, Стовпець: 1",
            anchor=tk.CENTER,
            width=20,
            padx=5
        )
        self._position_label.pack(side=tk.LEFT)
        
        ttk.Separator(self, orient=tk.VERTICAL).pack(side=tk.LEFT, fill=tk.Y, padx=2)
        
        self._size_label = tk.Label(
            self,
            text="0 символів",
            anchor=tk.CENTER,
            width=15,
            padx=5
        )
        self._size_label.pack(side=tk.LEFT)
        
    def set_message(self, message: str):
        """
        Встановити головне повідомлення
        
        Args:
            message: Текст повідомлення
        """
        self._message_label.config(text=message)
    
    def set_validation_status(self, is_valid: bool, message: str = ""):
        """
        Встановити статус валідації
        
        Args:
            is_valid: Чи валідний документ
            message: Додаткове повідомлення
        """
        if is_valid:
            text = "✓ Валідний"
            fg = "green"
        else:
            text = "✗ Невалідний"
            fg = "red"
        
        if message:
            text = f"{text}: {message}"
        
        self._validation_label.config(text=text, fg=fg)
    
    def set_position(self, line: int, column: int):
        """
        Встановити позицію курсора
        
        Args:
            line: Номер рядка
            column: Номер стовпця
        """
        self._position_label.config(text=f"Рядок: {line}, Стовпець: {column}")
    
    def set_document_size(self, size: int, lines: int = None):
        """
        Встановити розмір документа
        
        Args:
            size: Кількість символів
            lines: Кількість рядків (опціонально)
        """
        text = f"{size} символів"
        if lines is not None:
            text += f", {lines} рядків"
        
        self._size_label.config(text=text)
    
    def clear_validation(self):
        """Очистити статус валідації"""
        self._validation_label.config(text="", fg="black")