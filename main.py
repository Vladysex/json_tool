"""
JSON Tool - Main Entry Point
Точка входу застосунку
"""

import sys
import os
import tkinter as tk
from tkinter import messagebox

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from ui.main_window import MainWindow
from utils.config import Config


def main():
    """Головна функція застосунку"""
    try:
        root = tk.Tk()
        
        Config.ensure_data_dir()
        
        app = MainWindow(root)
        
        app.run()
        
    except Exception as e:
        messagebox.showerror(
            "Критична помилка",
            f"Не вдало��я запустити застосунок:\n{str(e)}"
        )
        sys.exit(1)


if __name__ == "__main__":
    main()