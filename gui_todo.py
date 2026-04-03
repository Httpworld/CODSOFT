"""
To-Do List Application - GUI Version using Tkinter
Task 1 - Internship Project
"""

import json
import os
import tkinter as tk
from tkinter import ttk, messagebox, simpledialog
from datetime import datetime


# ─────────────────────────────────────────────
# FILE STORAGE
# ─────────────────────────────────────────────
TASKS_FILE = "tasks.json"

def load_tasks():
    if os.path.exists(TASKS_FILE):
        with open(TASKS_FILE, "r") as f:
            return json.load(f)
    return []

def save_tasks(tasks):
    with open(TASKS_FILE, "w") as f:
        json.dump(tasks, f, indent=4)


# ─────────────────────────────────────────────
# MAIN APPLICATION CLASS
# ─────────────────────────────────────────────
class ToDoApp:
    def __init__(self, root):
        self.root = root
        self.root.title("📝 To-Do List App")
        self.root.geometry("750x580")
        self.root.resizable(True, True)
        self.root.configure(bg="#1e1e2e")

        self.tasks = load_tasks()
        self.setup_styles()
        self.build_ui()
        self.refresh_task_list()

    # ── STYLES ─────────────────────────────────
    def setup_styles(self):
        style = ttk.Style()
        style.theme_use("clam")

        style.configure("Treeview",
                        background="#2a2a3e",
                        foreground="#cdd6f4",
                        fieldbackground="#2a2a3e",
                        rowheight=32,
                        font=("Consolas", 11))

        style.configure("Treeview.Heading",
                        background="#313244",
                        foreground="#cba6f7",
                        font=("Consolas", 11, "bold"))

        style.map("Treeview",
                  background=[("selected", "#45475a")],
                  foreground=[("selected", "#cdd6f4")])

        style.configure("TButton",
                        background="#89b4fa",
                        foreground="#1e1e2e",
                        font=("Consolas", 10, "bold"),
                        padding=(10, 6))

        style.map("TButton",
                  background=[("active", "#b4befe")],
                  foreground=[("active", "#1e1e2e")])

    # ── UI BUILDER ─────────────────────────────
    def build_ui(self):
        # ── Title Bar ──
        title_frame = tk.Frame(self.root, bg="#313244", pady=12)
        title_frame.pack(fill="x")

        tk.Label(title_frame, text="📝  TO-DO LIST",
                 font=("Consolas", 20, "bold"),
                 bg="#313244", fg="#cba6f7").pack()

        tk.Label(title_frame, text="Manage your tasks efficiently",
                 font=("Consolas", 10),
                 bg="#313244", fg="#6c7086").pack()

        # ── Input Area ──
        input_frame = tk.Frame(self.root, bg="#1e1e2e", pady=14, padx=20)
        input_frame.pack(fill="x")

        tk.Label(input_frame, text="Task Title:",
                 bg="#1e1e2e", fg="#a6e3a1",
                 font=("Consolas", 10, "bold")).grid(row=0, column=0, sticky="w")

        self.task_entry = tk.Entry(input_frame,
                                   font=("Consolas", 11),
                                   bg="#313244", fg="#cdd6f4",
                                   insertbackground="#cdd6f4",
                                   relief="flat", bd=6, width=35)
        self.task_entry.grid(row=0, column=1, padx=10, sticky="ew")
        self.task_entry.bind("<Return>", lambda e: self.add_task())

        tk.Label(input_frame, text="Due Date:",
                 bg="#1e1e2e", fg="#a6e3a1",
                 font=("Consolas", 10, "bold")).grid(row=0, column=2, padx=(10,0), sticky="w")

        self.date_entry = tk.Entry(input_frame,
                                   font=("Consolas", 11),
                                   bg="#313244", fg="#6c7086",
                                   insertbackground="#cdd6f4",
                                   relief="flat", bd=6, width=14)
        self.date_entry.insert(0, "DD-MM-YYYY")
        self.date_entry.grid(row=0, column=3, padx=10, sticky="ew")
        self.date_entry.bind("<FocusIn>",  self._on_date_click)
        self.date_entry.bind("<FocusOut>", self._on_date_leave)

        add_btn = tk.Button(input_frame, text="➕ Add Task",
                            bg="#a6e3a1", fg="#1e1e2e",
                            font=("Consolas", 10, "bold"),
                            relief="flat", padx=12, pady=6,
                            cursor="hand2",
                            command=self.add_task)
        add_btn.grid(row=0, column=4, padx=(4, 0))

        # ── Filter Buttons ──
        filter_frame = tk.Frame(self.root, bg="#1e1e2e", padx=20)
        filter_frame.pack(fill="x", pady=(0, 8))

        self.filter_var = tk.StringVar(value="All")
        for label, val in [("All", "All"), ("⏳ Pending", "Pending"), ("✅ Completed", "Completed")]:
            rb = tk.Radiobutton(filter_frame, text=label, variable=self.filter_var,
                                value=val, command=self.refresh_task_list,
                                bg="#1e1e2e", fg="#89b4fa", selectcolor="#313244",
                                font=("Consolas", 10), cursor="hand2",
                                activebackground="#1e1e2e", activeforeground="#cba6f7")
            rb.pack(side="left", padx=8)

        # ── Task List (Treeview) ──
        list_frame = tk.Frame(self.root, bg="#1e1e2e", padx=20)
        list_frame.pack(fill="both", expand=True)

        columns = ("ID", "Title", "Status", "Due Date", "Created")
        self.tree = ttk.Treeview(list_frame, columns=columns,
                                  show="headings", selectmode="browse")

        self.tree.heading("ID",      text="ID")
        self.tree.heading("Title",   text="TITLE")
        self.tree.heading("Status",  text="STATUS")
        self.tree.heading("Due Date",text="DUE DATE")
        self.tree.heading("Created", text="CREATED")

        self.tree.column("ID",       width=40,  anchor="center")
        self.tree.column("Title",    width=240, anchor="w")
        self.tree.column("Status",   width=110, anchor="center")
        self.tree.column("Due Date", width=110, anchor="center")
        self.tree.column("Created",  width=140, anchor="center")

        scrollbar = ttk.Scrollbar(list_frame, orient="vertical",
                                   command=self.tree.yview)
        self.tree.configure(yscrollcommand=scrollbar.set)

        self.tree.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

        # ── Tag Colors for status ──
        self.tree.tag_configure("completed", foreground="#a6e3a1")
        self.tree.tag_configure("pending",   foreground="#f38ba8")

        # ── Action Buttons ──
        btn_frame = tk.Frame(self.root, bg="#1e1e2e", pady=12, padx=20)
        btn_frame.pack(fill="x")

        buttons = [
            ("✅ Complete", "#a6e3a1", self.complete_task),
            ("✏️  Update",  "#89b4fa", self.update_task),
            ("🗑️  Delete",  "#f38ba8", self.delete_task),
            ("🧹 Clear Done","#fab387", self.clear_completed),
        ]

        for text, color, cmd in buttons:
            tk.Button(btn_frame, text=text, bg=color, fg="#1e1e2e",
                      font=("Consolas", 10, "bold"),
                      relief="flat", padx=14, pady=7,
                      cursor="hand2", command=cmd).pack(side="left", padx=6)

        # ── Status Bar ──
        self.status_var = tk.StringVar()
        tk.Label(self.root, textvariable=self.status_var,
                 bg="#313244", fg="#6c7086",
                 font=("Consolas", 9), anchor="w", padx=10).pack(
                 fill="x", side="bottom", ipady=4)

    # ── HELPERS ────────────────────────────────
    def _on_date_click(self, event):
        if self.date_entry.get() == "DD-MM-YYYY":
            self.date_entry.delete(0, "end")
            self.date_entry.config(fg="#cdd6f4")

    def _on_date_leave(self, event):
        if not self.date_entry.get():
            self.date_entry.insert(0, "DD-MM-YYYY")
            self.date_entry.config(fg="#6c7086")

    def get_selected_task(self):
        """Return the task dict for the selected row."""
        selected = self.tree.selection()
        if not selected:
            messagebox.showwarning("No Selection", "Please select a task first!")
            return None
        task_id = int(self.tree.item(selected[0])["values"][0])
        return next((t for t in self.tasks if t["id"] == task_id), None)

    def refresh_task_list(self):
        """Re-populate the treeview based on current filter."""
        for row in self.tree.get_children():
            self.tree.delete(row)

        filter_val = self.filter_var.get()
        filtered = [t for t in self.tasks
                    if filter_val == "All" or t["status"] == filter_val]

        for task in filtered:
            icon   = "✅" if task["status"] == "Completed" else "⏳"
            tag    = "completed" if task["status"] == "Completed" else "pending"
            self.tree.insert("", "end",
                             values=(task["id"], task["title"],
                                     f"{icon} {task['status']}",
                                     task["due_date"], task["created_at"]),
                             tags=(tag,))

        total     = len(self.tasks)
        done      = sum(1 for t in self.tasks if t["status"] == "Completed")
        pending   = total - done
        self.status_var.set(f"  Total: {total}  |  ✅ Completed: {done}  |  ⏳ Pending: {pending}")

    # ── TASK ACTIONS ───────────────────────────
    def add_task(self):
        title = self.task_entry.get().strip()
        if not title:
            messagebox.showerror("Error", "Task title cannot be empty!")
            return

        due = self.date_entry.get().strip()
        due = due if due not in ("", "DD-MM-YYYY") else "No due date"

        task = {
            "id":         len(self.tasks) + 1,
            "title":      title,
            "status":     "Pending",
            "due_date":   due,
            "created_at": datetime.now().strftime("%d-%m-%Y %H:%M")
        }

        self.tasks.append(task)
        save_tasks(self.tasks)
        self.task_entry.delete(0, "end")
        self.date_entry.delete(0, "end")
        self.date_entry.insert(0, "DD-MM-YYYY")
        self.date_entry.config(fg="#6c7086")
        self.refresh_task_list()
        self.status_var.set(f"  ✅ Task '{title}' added!")

    def complete_task(self):
        task = self.get_selected_task()
        if not task:
            return
        if task["status"] == "Completed":
            messagebox.showinfo("Info", "Task is already completed!")
            return
        task["status"] = "Completed"
        save_tasks(self.tasks)
        self.refresh_task_list()
        self.status_var.set(f"  ✅ '{task['title']}' marked as completed!")

    def update_task(self):
        task = self.get_selected_task()
        if not task:
            return
        new_title = simpledialog.askstring(
            "Update Task",
            "Enter new title:",
            initialvalue=task["title"],
            parent=self.root)
        if new_title and new_title.strip():
            task["title"] = new_title.strip()
            save_tasks(self.tasks)
            self.refresh_task_list()
            self.status_var.set(f"  ✏️  Task updated to '{new_title.strip()}'")

    def delete_task(self):
        task = self.get_selected_task()
        if not task:
            return
        if messagebox.askyesno("Confirm Delete",
                               f"Delete task:\n'{task['title']}'?"):
            self.tasks.remove(task)
            for i, t in enumerate(self.tasks, start=1):
                t["id"] = i
            save_tasks(self.tasks)
            self.refresh_task_list()
            self.status_var.set(f"  🗑️  Task deleted.")

    def clear_completed(self):
        done = [t for t in self.tasks if t["status"] == "Completed"]
        if not done:
            messagebox.showinfo("Info", "No completed tasks to clear!")
            return
        if messagebox.askyesno("Confirm",
                               f"Remove all {len(done)} completed task(s)?"):
            self.tasks = [t for t in self.tasks if t["status"] == "Pending"]
            for i, t in enumerate(self.tasks, start=1):
                t["id"] = i
            save_tasks(self.tasks)
            self.refresh_task_list()
            self.status_var.set(f"  🧹 {len(done)} completed task(s) cleared.")


# ─────────────────────────────────────────────
# ENTRY POINT
# ─────────────────────────────────────────────
if __name__ == "__main__":
    root = tk.Tk()
    app = ToDoApp(root)
    root.mainloop()
