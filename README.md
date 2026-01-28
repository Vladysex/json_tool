# JSON Tool

Локальний інструмент для редагування, форматування та валідації JSON-файлів. Показує практичне застосування патернів проектування (Strategy, Command, Observer, Template Method, Flyweight) та має чисту багатошарову архітектуру.

## Можливості
- Редагування JSON з підсвічуванням синтаксису
- Форматування JSON з відступами
- Мінімізація JSON (видалення пробілів)
- Автоматична та ручна валідація синтаксису
- Валідація за JSON Schema (через `jsonschema`)
- Undo/Redo, автозбереження, статистика документа
- Кросплатформений: Windows, macOS, Linux

---

## Вимоги
- Python 3.11+
- Tkinter (стандартна бібліотека; на Linux може вимагати окремого пакета)
- pip (менеджер пакетів)
- Залежності з `requirements.txt` (наприклад, `jsonschema`)

---

## Швидкий старт

### 1) Клонувати репозиторій
```bash
git clone https://github.com/Vladysex/json_tool.git
cd json_tool
```

### 2) Створити та активувати віртуальне середовище
Linux/macOS:
```bash
python3 -m venv .venv
source .venv/bin/activate
```

Windows (PowerShell):
```powershell
python -m venv .venv
.venv\Scripts\Activate.ps1
```

### 3) Встановити залежності
```bash
pip install -r requirements.txt
```

Якщо на Linux відсутній Tkinter:
- Ubuntu/Debian:
  ```bash
  sudo apt update
  sudo apt install python3-tk
  ```
- Fedora:
  ```bash
  sudo dnf install python3-tkinter
  ```

macOS зазвичай має Tkinter у складі Python; за потреби:
```bash
brew install python-tk
```

### 4) Запустити застосунок
```bash
python main.py
```

---

## Використання

- Файл → Новий / Відкрити / Зберегти / Зберегти як…
- Інструменти → Форматувати JSON / Мінімізувати JSON / Валідувати JSON
- Вигляд → Статистика… / Підсвічування синтаксису

Клавіатурні скорочення:
- Новий: Ctrl+N (⌘+N)
- Відкрити: Ctrl+O (⌘+O)
- Зберегти: Ctrl+S (⌘+S)
- Форматувати: Ctrl+Shift+F (⌘+⇧+F)
- Валідувати: F5
- Undo/Redo: Ctrl+Z / Ctrl+Y (⌘+Z / ⌘+Y)
