"""
Main Window - Application Main Window
Головне вікно застосунку JSON Tool
"""

import tkinter as tk
from tkinter import ttk, filedialog, messagebox
from typing import Optional
import os

from core.editor import Editor
from ui.editor_view import EditorView
from ui.status_bar import StatusBar
from utils.config import Config
from utils.file_manager import FileManager


class MainWindow:
    """
    Головне вікно застосунку
    Інтегрує всі компоненти UI та логіку
    """
    
    def __init__(self, root: tk.Tk):
        """
        Ініціалізація головного вікна
        
        Args:
            root: Кореневий Tk віджет
        """
        self.root = root
        self.editor = Editor()
        
        self._syncing = False
        
        self._setup_window()
        
        self._create_menu()
        self._create_toolbar()
        self._create_editor_area()
        self._create_status_bar()
        
        self._bind_events()
        
        self._update_title()
        self._update_ui_state()
        
        self._schedule_updates()
    
    def _setup_window(self):
        """Налаштувати параметри вікна"""
        self.root.title(Config.APP_NAME)
        self.root.geometry(f"{Config.WINDOW_WIDTH}x{Config.WINDOW_HEIGHT}")
        self.root.minsize(Config.WINDOW_MIN_WIDTH, Config.WINDOW_MIN_HEIGHT)
        
        self.root.protocol("WM_DELETE_WINDOW", self._on_closing)
        
    def _create_menu(self):
        """Створити меню"""
        menubar = tk.Menu(self.root)
        self.root.config(menu=menubar)
        
        file_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Файл", menu=file_menu)
        file_menu.add_command(label="Новий", command=self._new_file, accelerator="Ctrl+N")
        file_menu.add_command(label="Відкрити...", command=self._open_file, accelerator="Ctrl+O")
        file_menu.add_separator()
        file_menu.add_command(label="Зберегти", command=self._save_file, accelerator="Ctrl+S")
        file_menu.add_command(label="Зберегти як...", command=self._save_as_file, accelerator="Ctrl+Shift+S")
        file_menu.add_separator()
        file_menu.add_command(label="Вийти", command=self._on_closing, accelerator="Ctrl+Q")
        
        edit_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Редагування", menu=edit_menu)
        edit_menu.add_command(label="Скасувати", command=self._undo, accelerator="Ctrl+Z")
        edit_menu.add_command(label="Повторити", command=self._redo, accelerator="Ctrl+Y")
        edit_menu.add_separator()
        edit_menu.add_command(label="Вирізати", command=self._cut, accelerator="Ctrl+X")
        edit_menu.add_command(label="Копіювати", command=self._copy, accelerator="Ctrl+C")
        edit_menu.add_command(label="Вставити", command=self._paste, accelerator="Ctrl+V")
        edit_menu.add_separator()
        edit_menu.add_command(label="Виділити все", command=self._select_all, accelerator="Ctrl+A")
        
        tools_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Інструменти", menu=tools_menu)
        tools_menu.add_command(label="Валідувати JSON", command=self._validate_json, accelerator="F5")
        tools_menu.add_command(label="Форматувати JSON", command=self._format_json, accelerator="Ctrl+Shift+F")
        tools_menu.add_separator()
        tools_menu.add_checkbutton(label="Автозбереження", command=self._toggle_autosave)
        tools_menu.add_checkbutton(label="Автоматична валідація", command=self._toggle_auto_validation)
        
        view_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Вигляд", menu=view_menu)
        view_menu.add_checkbutton(label="Підсвічування синтаксису", command=self._toggle_syntax_highlighting)
        view_menu.add_separator()
        view_menu.add_command(label="Статистика", command=self._show_statistics)
        
        help_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Довідка", menu=help_menu)
        help_menu.add_command(label="Про програму", command=self._show_about)
        help_menu.add_command(label="Як працює форматування", command=self._show_format_help)
        
        self.menubar = menubar
    
    def _create_toolbar(self):
        """Створити панель інструментів"""
        toolbar = ttk.Frame(self.root)
        toolbar.pack(side=tk.TOP, fill=tk.X, padx=2, pady=2)
        
        ttk.Button(toolbar, text="📄 Новий", command=self._new_file, width=10).pack(side=tk.LEFT, padx=2)
        ttk.Button(toolbar, text="📂 Відкрити", command=self._open_file, width=10).pack(side=tk.LEFT, padx=2)
        ttk.Button(toolbar, text="💾 Зберегти", command=self._save_file, width=10).pack(side=tk.LEFT, padx=2)
        
        ttk.Separator(toolbar, orient=tk.VERTICAL).pack(side=tk.LEFT, fill=tk.Y, padx=5)
        
        ttk.Button(toolbar, text="↶ Скасувати", command=self._undo, width=12).pack(side=tk.LEFT, padx=2)
        ttk.Button(toolbar, text="↷ Повторити", command=self._redo, width=12).pack(side=tk.LEFT, padx=2)
        
        ttk.Separator(toolbar, orient=tk.VERTICAL).pack(side=tk.LEFT, fill=tk.Y, padx=5)
        
        ttk.Button(toolbar, text="✓ Валідувати", command=self._validate_json, width=12).pack(side=tk.LEFT, padx=2)
        ttk.Button(toolbar, text="⚡ Форматувати", command=self._format_json, width=12).pack(side=tk.LEFT, padx=2)
        
        self.toolbar = toolbar
    
    def _create_editor_area(self):
        """Створити область редактора"""
        self.editor_view = EditorView(self.root, on_change=self._on_editor_change)
        self.editor_view.pack(side=tk.TOP, fill=tk.BOTH, expand=True)
        
        initial_content = '''{
  "name": "Json Redactor",
  "course": "ІА-з31",
  "description": "Редактор JSON файлів",
  "features": [
    "Валідація JSON",
    "Форматування з відступами",
    "Undo/Redo підтримка",
    "Автозбереження"
  ],
  "author": "Присяжнюк Владислав"
}'''
        self.editor_view.set_content(initial_content)
        self.editor.set_content(initial_content)
    
    def _create_status_bar(self):
        """Створити рядок статусу"""
        self.status_bar = StatusBar(self.root)
        self.status_bar.pack(side=tk.BOTTOM, fill=tk.X)
    
    def _bind_events(self):
        """Прив'язати клавіатурні скорочення"""
        self.root.bind('<Control-n>', lambda e: self._new_file())
        self.root.bind('<Control-o>', lambda e: self._open_file())
        self.root.bind('<Control-s>', lambda e: self._save_file())
        self.root.bind('<Control-Shift-S>', lambda e: self._save_as_file())
        self.root.bind('<Control-q>', lambda e: self._on_closing())
        
        text_widget = self.editor_view.get_text_widget()
        text_widget.bind('<Control-z>', lambda e: self._undo())
        text_widget.bind('<Control-y>', lambda e: self._redo())
        text_widget.bind('<Control-a>', lambda e: self._select_all())
        
        self.root.bind('<F5>', lambda e: self._validate_json())
        self.root.bind('<Control-Shift-F>', lambda e: self._format_json())
        
        text_widget.bind('<KeyRelease>', self._on_cursor_move)
        text_widget.bind('<ButtonRelease-1>', self._on_cursor_move)
    
    
    def _new_file(self):
        """Створити новий файл"""
        if self.editor.is_modified:
            if not self._ask_save_changes():
                return
        
        self.editor.new_document()
        self.editor_view.clear()
        self._update_title()
        self._update_ui_state()
        self.status_bar.set_message("Створено новий документ")
    
    def _open_file(self):
        """Відкрити файл"""
        if self.editor.is_modified:
            if not self._ask_save_changes():
                return
        
        filepath = filedialog.askopenfilename(
            title="Відкрити JSON файл",
            filetypes=[("JSON Files", "*.json"), ("All Files", "*.*")],
            defaultextension=".json"
        )
        
        if not filepath:
            return
        
        success, error = self.editor.open_file(filepath)
        
        if success:
            content = self.editor.get_content()
            self._syncing = True
            self.editor_view.set_content(content)
            self._syncing = False
            self._update_title()
            self._update_ui_state()
            self.status_bar.set_message(f"Файл відкрито: {os.path.basename(filepath)}")
        else:
            messagebox.showerror("Помилка", f"Не вдалося відкрити файл:\n{error}")
    
    def _save_file(self):
        """Зберегти файл"""
        if self.editor.filepath:
            self._perform_save(self.editor.filepath)
        else:
            self._save_as_file()
    
    def _save_as_file(self):
        """Зберегти як новий файл"""
        filepath = filedialog.asksaveasfilename(
            title="Зберегти JSON файл",
            filetypes=[("JSON Files", "*.json"), ("All Files", "*.*")],
            defaultextension=".json"
        )
        
        if filepath:
            self._perform_save(filepath)
    
    def _perform_save(self, filepath: str):
        """
        Виконати збереження файлу
        
        Args:
            filepath: Шлях для збереження
        """
        content = self.editor_view.get_content()
        self.editor.set_content(content)
        
        success, error = self.editor.save_file(filepath)
        
        if success:
            self._update_title()
            self._update_ui_state()
            self.status_bar.set_message(f"Файл збережено: {os.path.basename(filepath)}")
        else:
            messagebox.showerror("Помилка", f"Не вдалося зберегти файл:\n{error}")
    
    def _ask_save_changes(self) -> bool:
        """
        Запитати користувача про збереження змін
        
        Returns:
            True якщо можна продовжити, False якщо скасовано
        """
        result = messagebox.askyesnocancel(
            "Незбережені зміни",
            "Документ містить незбережені зміни. Зберегти?"
        )
        
        if result is None:
            return False
        elif result:  
            self._save_file()
            return True
        else:
            return True
    
    
    def _undo(self):
        """Скасувати - використовуємо вбудований undo Text widget"""
        text_widget = self.editor_view.get_text_widget()
        try:
            text_widget.edit_undo()
            self.status_bar.set_message("Скасовано")
            self._on_editor_change()
        except tk.TclError:
            self.status_bar.set_message("Нічого скасовувати")
        return 'break' 
    
    def _redo(self):
        """Повторити - використовуємо вбудований redo Text widget"""
        text_widget = self.editor_view.get_text_widget()
        try:
            text_widget.edit_redo()
            self.status_bar.set_message("Повторено")
            self._on_editor_change()
        except tk.TclError:
            self.status_bar.set_message("Нічого повторювати")
        return 'break' 
    
    def _cut(self):
        """Вирізати"""
        text_widget = self.editor_view.get_text_widget()
        text_widget.event_generate("<<Cut>>")
    
    def _copy(self):
        """Копіювати"""
        text_widget = self.editor_view.get_text_widget()
        text_widget.event_generate("<<Copy>>")
    
    def _paste(self):
        """Вставити"""
        text_widget = self.editor_view.get_text_widget()
        text_widget.event_generate("<<Paste>>")
    
    def _select_all(self):
        """Виділити все"""
        text_widget = self.editor_view.get_text_widget()
        text_widget.tag_add(tk.SEL, "1.0", tk.END)
        text_widget.mark_set(tk.INSERT, "1.0")
        text_widget.see(tk.INSERT)
        return 'break'
        
    def _validate_json(self):
        """Валідувати JSON"""
        content = self.editor_view.get_content()
        self.editor.set_content(content)
        
        result = self.editor.validate()
        
        if result:
            if result.is_valid:
                self.status_bar.set_validation_status(True, result.message)
                messagebox.showinfo("Валідація", f"✓ {result.message}")
            else:
                self.status_bar.set_validation_status(False, result.message)
                error_text = "\n".join(str(e) for e in result.errors[:5])
                messagebox.showerror("Помилка валідації", f"✗ {result.message}\n\n{error_text}")
    
    def _format_json(self):
        """Форматувати JSON"""
        content = self.editor_view.get_content()
        self.editor.set_content(content)
        
        success, error = self.editor.format_json(indent=2)
        
        if success:
            formatted_content = self.editor.get_content()
            
            self._syncing = True
            self.editor_view.set_content(formatted_content)
            self._syncing = False
            
            self.editor_view.force_highlight()
            
            self.status_bar.set_message("JSON відформатовано (2 пробіли відступу)")
            messagebox.showinfo("Форматування", "✓ JSON відформатовано успішно!\n\nДодано правильні відступи та структуру.")
        else:
            messagebox.showerror("Помилка форматування", f"Не вдалося відформатувати JSON:\n{error}\n\nСпочатку виправте синтаксичні помилки.")
    
    def _toggle_autosave(self):
        """Перемкнути автозбереження"""
        if self.editor.autosave_observer.get_statistics()['enabled']:
            self.editor.disable_autosave()
            self.status_bar.set_message("Автозбереження вимкнено")
        else:
            self.editor.enable_autosave()
            self.status_bar.set_message("Автозбереження увімкнено")
    
    def _toggle_auto_validation(self):
        """Перемкнути автоматичну валідацію"""
        if self.editor.validator_observer.enabled:
            self.editor.disable_auto_validation()
            self.status_bar.set_message("Автоматична валідація вимкнена")
        else:
            self.editor.enable_auto_validation()
            self.status_bar.set_message("Автоматична валідація увімкнена")
    
    def _toggle_syntax_highlighting(self):
        """Перемкнути підсвічування синтаксису"""
        messagebox.showinfo("Підсвічування", "Підсвічування синтаксису завжди активне")
    
    def _show_statistics(self):
        """Показати статистику"""
        stats = self.editor.get_statistics()
        
        stats_window = tk.Toplevel(self.root)
        stats_window.title("Статистика")
        stats_window.geometry("500x400")
        
        text = tk.Text(stats_window, wrap=tk.WORD, padx=10, pady=10)
        text.pack(fill=tk.BOTH, expand=True)
        
        text.insert(tk.END, "=== СТАТИСТИКА ДОКУМЕНТА ===\n\n")
        
        doc_stats = stats['document']
        text.insert(tk.END, "Документ:\n")
        text.insert(tk.END, f"  Розмір: {doc_stats['size']} символів\n")
        text.insert(tk.END, f"  Рядків: {doc_stats['lines']}\n")
        text.insert(tk.END, f"  Редагувань: {doc_stats['edit_count']}\n")
        text.insert(tk.END, f"  Спостерігачів: {doc_stats['observers_count']}\n\n")
        
        cmd_stats = stats['commands']
        text.insert(tk.END, "Команди (для програмних операцій):\n")
        text.insert(tk.END, f"  Всього команд: {cmd_stats['total_commands']}\n")
        text.insert(tk.END, f"  Можна скасувати: {cmd_stats['undo_count']}\n")
        text.insert(tk.END, f"  Можна повторити: {cmd_stats['redo_count']}\n\n")
        
        if stats['validation']:
            text.insert(tk.END, "Валідація:\n")
            text.insert(tk.END, f"  Валідний: {stats['validation']['is_valid']}\n")
            text.insert(tk.END, f"  Повідомлення: {stats['validation']['message']}\n\n")
        
        text.config(state=tk.DISABLED)
    
    def _show_about(self):
        """Показати інформацію про програму"""
        about_text = f"""{Config.APP_NAME} v{Config.APP_VERSION}

Локальний інструмент для редагування та валідації JSON файлів.

Реалізовані патерни проєктування:
• Strategy Pattern - стратегії валідації
• Command Pattern - програмні операції
• Observer Pattern - автоматичні оновлення
• Template Method - обробка файлів
• Flyweight - оптимізація пам'яті


© 2026 Prysiazhniuk Vladyslav Project"""
        
        messagebox.showinfo("Про програму", about_text)
    
    def _show_format_help(self):
        """Показати довідку про форматування"""
        help_text = """ЩО РОБИТЬ ФОРМАТУВАННЯ JSON?

Кнопка "⚡ Форматувати" (Ctrl+Shift+F) автоматично:

1. Перевіряє синтаксис JSON
2. Додає правильні відступи (2 пробіли)
3. Розставляє переноси рядків
4. Вирівнює структуру

ПРИКЛАД:

До форматування:
{"name":"test","value":123,"nested":{"key":"value"}}

Після форматування:
{
  "name": "test",
  "value": 123,
  "nested": {
    "key": "value"
  }
}

ВАЖЛИВО:
• JSON має бути синтаксично коректним
• Якщо є помилки - спочатку виправте їх
• Використовуйте F5 для валідації перед форматуванням"""
        
        messagebox.showinfo("Довідка: Форматування JSON", help_text)
    
    
    def _on_editor_change(self):
        """Обробник зміни вмісту редактора"""
        if self._syncing:
            return
        
        content = self.editor_view.get_content()
        self.editor.set_content(content)
        
        self._update_title()
        self._update_ui_state()
    
    def _on_cursor_move(self, event=None):
        """Обробник переміщення курсора"""
        position = self.editor_view.get_cursor_position()
        line, column = position.split('.')
        self.status_bar.set_position(int(line), int(column))
    
    def _on_closing(self):
        """Обробник закриття вікна"""
        if self.editor.is_modified:
            if not self._ask_save_changes():
                return
        
        self.root.quit()
        
    def _update_title(self):
        """Оновити заголовок вікна"""
        filename = "Новий документ"
        if self.editor.filepath:
            filename = os.path.basename(self.editor.filepath)
        
        modified = "*" if self.editor.is_modified else ""
        self.root.title(f"{filename}{modified} - {Config.APP_NAME}")
    
    def _update_ui_state(self):
        """Оновити стан UI елементів"""
        size = self.editor.document.size
        lines = self.editor.document.get_content().count('\n') + 1
        self.status_bar.set_document_size(size, lines)
        
        status_msg = self.editor.get_status_message()
        if status_msg and status_msg != "Готовий":
            self.status_bar.set_message(status_msg)
    
    def _schedule_updates(self):
        """Запланувати періодичні оновлення"""
        self._update_validation_status()
        self.root.after(1000, self._schedule_updates)  
    
    def _update_validation_status(self):
        """Оновити статус валідації в статус барі"""
        result = self.editor.validator_observer.last_result
        if result:
            self.status_bar.set_validation_status(result.is_valid, "")
        
    def run(self):
        """Запустити головний цикл застосунку"""
        self.root.mainloop()