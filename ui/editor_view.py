"""
Editor View - Text Editor with Syntax Highlighting
Текстовий редактор з підсвічуванням синтаксису JSON
"""

import tkinter as tk
from tkinter import font as tkfont
import re
from typing import Optional, Callable
from utils.config import Config


class EditorView(tk.Frame):
    """
    Віджет текстового редактора з підсвічуванням синтаксису JSON
    """
    
    def __init__(self, parent, on_change: Optional[Callable] = None):
        """
        Ініціалізація редактора
        
        Args:
            parent: Батьківський віджет
            on_change: Callback функція при зміні тексту
        """
        super().__init__(parent)
        
        self._on_change = on_change
        self._highlighting_enabled = True
        self._last_content = ""
        
        self._create_widgets()
        self._setup_syntax_highlighting()
        self._bind_events()
    
    def _create_widgets(self):
        """Створити віджети"""
        scrollbar = tk.Scrollbar(self)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        self._text = tk.Text(
            self,
            wrap=tk.NONE,
            undo=True,
            font=(Config.EDITOR_FONT_FAMILY, Config.EDITOR_FONT_SIZE),
            tabs=tkfont.Font(font=(Config.EDITOR_FONT_FAMILY, Config.EDITOR_FONT_SIZE)).measure(' ' * Config.EDITOR_TAB_WIDTH),
            yscrollcommand=scrollbar.set
        )
        self._text.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        
        scrollbar.config(command=self._text.yview)
    
    def _setup_syntax_highlighting(self):
        """Налаштувати підсвічування синтаксису"""
        colors = Config.SYNTAX_COLORS
        
        self._text.tag_configure("brace", foreground=colors['brace'])
        self._text.tag_configure("string", foreground=colors['string'])
        self._text.tag_configure("number", foreground=colors['number'])
        self._text.tag_configure("boolean", foreground=colors['boolean'])
        self._text.tag_configure("null", foreground=colors['null'])
        self._text.tag_configure("key", foreground=colors['key'])
    
    def _bind_events(self):
        """Прив'язати події"""
        self._text.bind('<<Modified>>', self._on_text_modified)
        
        self._text.bind('<KeyRelease>', self._schedule_highlight)
    
    def _on_text_modified(self, event=None):
        """Обробник події зміни тексту"""
        if self._text.edit_modified():
            if self._on_change:
                self._on_change()
            
            self._text.edit_modified(False)
    
    def _schedule_highlight(self, event=None):
        """Запланувати підсвічування"""
        if hasattr(self, '_highlight_job'):
            self.after_cancel(self._highlight_job)
        
        self._highlight_job = self.after(100, self._highlight_syntax)
    
    def _highlight_syntax(self):
        """Підсвітити синтаксис JSON"""
        if not self._highlighting_enabled:
            return
        
        content = self.get_content()
        
        for tag in ["brace", "string", "number", "boolean", "null", "key"]:
            self._text.tag_remove(tag, "1.0", tk.END)
        
        if not content.strip():
            self._last_content = content
            return
        
        self._highlight_strings(content)
        self._highlight_numbers(content)
        self._highlight_keywords(content)
        self._highlight_braces(content)
        
        self._last_content = content
    
    def _highlight_strings(self, content: str):
        """Підсвітити рядки"""
        pattern = r'"(?:[^"\\]|\\.)*"'
        
        for match in re.finditer(pattern, content):
            start_idx = self._get_text_index(content, match.start())
            end_idx = self._get_text_index(content, match.end())
            
            after_text = content[match.end():match.end()+10]
            if after_text.strip().startswith(':'):
                self._text.tag_add("key", start_idx, end_idx)
            else:
                self._text.tag_add("string", start_idx, end_idx)
    
    def _highlight_numbers(self, content: str):
        """Підсвітити числа"""
        pattern = r'\b-?\d+\.?\d*([eE][+-]?\d+)?\b'
        
        for match in re.finditer(pattern, content):
            start_idx = self._get_text_index(content, match.start())
            end_idx = self._get_text_index(content, match.end())
            self._text.tag_add("number", start_idx, end_idx)
    
    def _highlight_keywords(self, content: str):
        """Підсвітити ключові слова (true, false, null)"""
        for match in re.finditer(r'\b(true|false)\b', content):
            start_idx = self._get_text_index(content, match.start())
            end_idx = self._get_text_index(content, match.end())
            self._text.tag_add("boolean", start_idx, end_idx)
        
        for match in re.finditer(r'\bnull\b', content):
            start_idx = self._get_text_index(content, match.start())
            end_idx = self._get_text_index(content, match.end())
            self._text.tag_add("null", start_idx, end_idx)
    
    def _highlight_braces(self, content: str):
        """Підсвітити дужки"""
        braces = ['{', '}', '[', ']', ':', ',']
        
        for i, char in enumerate(content):
            if char in braces:
                idx = self._get_text_index(content, i)
                self._text.tag_add("brace", idx, f"{idx}+1c")
    
    def _get_text_index(self, content: str, offset: int) -> str:
        """
        Конвертувати offset в текстовий індекс Tkinter
        
        Args:
            content: Вміст тексту
            offset: Offset в символах
            
        Returns:
            Індекс у форматі "row.col"
        """
        lines = content[:offset].split('\n')
        row = len(lines)
        col = len(lines[-1]) if lines else 0
        return f"{row}.{col}"
        
    def get_content(self) -> str:
        """Отримати вміст редактора"""
        return self._text.get("1.0", tk.END)[:-1] 
    
    def set_content(self, content: str):
        """
        Встановити вміст редактора
        
        Args:
            content: Новий вміст
        """
        try:
            cursor_pos = self._text.index(tk.INSERT)
        except:
            cursor_pos = "1.0"
        
        self._text.delete("1.0", tk.END)
        
        self._text.insert("1.0", content)
        
        self._text.update_idletasks()
        
        self._last_content = ""
        
        self._highlight_syntax()
        
        try:
            self._text.mark_set(tk.INSERT, cursor_pos)
            self._text.see(tk.INSERT)
        except:
            pass
    
    def clear(self):
        """Очистити редактор"""
        self._text.delete("1.0", tk.END)
        self._last_content = ""
    
    def insert(self, position: str, text: str):
        """
        Вставити текст
        
        Args:
            position: Позиція у форматі Tkinter
            text: Текст для вставки
        """
        self._text.insert(position, text)
    
    def delete(self, start: str, end: str):
        """
        Видалити текст
        
        Args:
            start: Початкова позиція
            end: Кінцева позиція
        """
        self._text.delete(start, end)
    
    def get_cursor_position(self) -> str:
        """Отримати позицію курсора"""
        return self._text.index(tk.INSERT)
    
    def set_cursor_position(self, position: str):
        """
        Встановити позицію курсора
        
        Args:
            position: Позиція у форматі Tkinter
        """
        self._text.mark_set(tk.INSERT, position)
    
    def enable_highlighting(self):
        """Увімкнути підсвічування"""
        self._highlighting_enabled = True
        self._highlight_syntax()
    
    def disable_highlighting(self):
        """Вимкнути підсвічування"""
        self._highlighting_enabled = False
    
    def set_readonly(self, readonly: bool):
        """
        Встановити режим тільки для читання
        
        Args:
            readonly: True - тільки читання, False - редагування
        """
        if readonly:
            self._text.config(state=tk.DISABLED)
        else:
            self._text.config(state=tk.NORMAL)
    
    def focus(self):
        """Встановити фокус на редактор"""
        self._text.focus_set()
    
    def get_text_widget(self) -> tk.Text:
        """Отримати внутрішній Text віджет"""
        return self._text
    
    def force_highlight(self):
        """
        Примусово перезапустити підсвічування синтаксису
        Викликати після програмної зміни вмісту
        """
        self._last_content = ""
        
        self._text.update_idletasks()
        
        self._highlight_syntax()