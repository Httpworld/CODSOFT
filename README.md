# 📝 To-Do List Application
### Task 1 — Internship Project

A Python-based To-Do List application available in both **CLI** and **GUI** versions.

---

## 📁 Project Structure
```
todo_app/
├── cli_todo.py      ← Command Line Interface version
├── gui_todo.py      ← GUI version (Tkinter)
├── tasks.json       ← Auto-created when you add your first task
└── README.md        ← This file
```

---

## ⚙️ Requirements
- Python 3.7 or higher
- `tkinter` (built-in with Python — no install needed)
- No external libraries required

---

## 🚀 How to Run

### CLI Version
```bash
python cli_todo.py
```

### GUI Version
```bash
python gui_todo.py
```

---

## ✨ Features

| Feature              | CLI | GUI |
|----------------------|-----|-----|
| Add Task             | ✅  | ✅  |
| View All Tasks       | ✅  | ✅  |
| Mark as Complete     | ✅  | ✅  |
| Update Task Title    | ✅  | ✅  |
| Delete Task          | ✅  | ✅  |
| Clear Completed      | ✅  | ✅  |
| Filter by Status     | ❌  | ✅  |
| Due Date Support     | ✅  | ✅  |
| Persistent Storage   | ✅  | ✅  |

---

## 💾 Data Storage
Tasks are saved in `tasks.json` automatically.
Both versions share the **same data file**, so tasks added in CLI appear in GUI and vice versa.

---

## 👨‍💻 Author
Internship Project — Task 1
