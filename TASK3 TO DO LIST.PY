import tkinter as tk
from tkinter import ttk
from tkinter import simpledialog
import json
from datetime import datetime

# ---------------- WINDOW ----------------
root = tk.Tk()
root.title("📝 Neo To-Do List - Final Boss Edition")
root.geometry("600x680")
root.resizable(False, False)
root.configure(bg="#0b1220")

ACCENT = "#38bdf8"
TASK_FILE = "tasks.json"
theme = "dark"

# ---------------- CARD ----------------
card = tk.Frame(root, bg="#020617")
card.place(x=30, y=20, width=540, height=620)

# ---------------- TITLE ----------------
title = tk.Label(
    card,
    text="📝 To-Do List Manager",
    font=("Segoe UI", 20, "bold"),
    fg=ACCENT,
    bg="#020617"
)
title.pack(pady=(15, 5))

subtitle = tk.Label(
    card,
    text="Organize your tasks efficiently",
    font=("Segoe UI", 10),
    fg="#94a3b8",
    bg="#020617"
)
subtitle.pack()

# ---------------- INPUT ----------------
task_entry = tk.Entry(
    card,
    font=("Segoe UI", 14),
    bg="#0b1220",
    fg="#e5e7eb",
    insertbackground=ACCENT,
    bd=0
)
task_entry.pack(fill="x", padx=30, pady=10, ipady=8)
task_entry.focus()

# ---------------- TASK LIST ----------------
task_list = tk.Listbox(
    card,
    font=("Segoe UI", 12),
    bg="#0b1220",
    fg="#e5e7eb",
    selectbackground=ACCENT,
    bd=0,
    height=15
)
task_list.pack(fill="both", padx=30)

# ---------------- STATUS ----------------
status = tk.Label(
    card,
    text="No tasks yet",
    font=("Segoe UI", 10, "bold"),
    fg="#94a3b8",
    bg="#020617"
)
status.pack(pady=5)

# ---------------- PROGRESS BAR ----------------
progress = ttk.Progressbar(card, length=460, mode='determinate')
progress.pack(pady=5)

# ---------------- FUNCTIONS ----------------
def save_tasks():
    tasks = list(task_list.get(0, "end"))
    with open(TASK_FILE, "w") as f:
        json.dump(tasks, f)

def load_tasks():
    try:
        with open(TASK_FILE, "r") as f:
            tasks = json.load(f)
            for t in tasks:
                task_list.insert("end", t)
            update_status()
    except FileNotFoundError:
        pass

def update_status():
    total = task_list.size()
    done = sum(1 for i in range(total) if task_list.get(i).startswith("✅"))
    status.config(text=f"Total: {total}   Completed: {done}", fg="#94a3b8")
    progress['value'] = (done / total * 100) if total > 0 else 0
    save_tasks()

def add_task(event=None):
    task_name = task_entry.get().strip()
    if not task_name:
        status.config(text="⚠ Enter a task", fg="#f59e0b")
        return
    
    # Ask for priority
    priority = simpledialog.askstring("Priority", "Enter priority (Low/Medium/High):", parent=root)
    if not priority:
        priority = "Medium"

    # Ask for due date
    due_date = simpledialog.askstring("Due Date", "Enter due date (YYYY-MM-DD):", parent=root)
    try:
        if due_date:
            datetime.strptime(due_date, "%Y-%m-%d")
    except:
        due_date = "No date"

    task_text = f"⬜ [{priority}] {due_date}: {task_name}"
    task_list.insert("end", task_text)
    task_entry.delete(0, "end")
    update_status()

def mark_done():
    try:
        i = task_list.curselection()[0]
        task = task_list.get(i)
        if not task.startswith("✅"):
            task_list.delete(i)
            task_list.insert(i, task.replace("⬜", "✅"))
        update_status()
    except IndexError:
        status.config(text="⚠ Select a task", fg="#f59e0b")

def delete_task():
    try:
        task_list.delete(task_list.curselection()[0])
        update_status()
    except IndexError:
        status.config(text="⚠ Select a task", fg="#f59e0b")

def clear_completed():
    tasks = list(task_list.get(0, "end"))
    task_list.delete(0, "end")
    for t in tasks:
        if not t.startswith("✅"):
            task_list.insert("end", t)
    update_status()

def switch_theme():
    global theme
    if theme == "dark":
        theme = "light"
        card.config(bg="#f3f4f6")
        task_list.config(bg="white", fg="black", selectbackground=ACCENT)
        status.config(bg="#f3f4f6", fg="black")
        title.config(bg="#f3f4f6", fg="#2563eb")
        subtitle.config(bg="#f3f4f6", fg="#334155")
    else:
        theme = "dark"
        card.config(bg="#020617")
        task_list.config(bg="#0b1220", fg="#e5e7eb", selectbackground=ACCENT)
        status.config(bg="#020617", fg="#94a3b8")
        title.config(bg="#020617", fg=ACCENT)
        subtitle.config(bg="#020617", fg="#94a3b8")

# ---------------- BUTTONS ----------------
btn_frame = tk.Frame(card, bg=card.cget("bg"))
btn_frame.pack(pady=10)

tk.Button(
    btn_frame,
    text="➕ Add",
    font=("Segoe UI", 12, "bold"),
    bg="#2563eb",
    fg="white",
    bd=0,
    width=10,
    command=add_task
).grid(row=0, column=0, padx=6)

tk.Button(
    btn_frame,
    text="✅ Done",
    font=("Segoe UI", 12, "bold"),
    bg="#22c55e",
    fg="white",
    bd=0,
    width=10,
    command=mark_done
).grid(row=0, column=1, padx=6)

tk.Button(
    btn_frame,
    text="🗑 Delete",
    font=("Segoe UI", 12, "bold"),
    bg="#ef4444",
    fg="white",
    bd=0,
    width=10,
    command=delete_task
).grid(row=0, column=2, padx=6)

tk.Button(
    card,
    text="🧹 Clear Completed Tasks",
    font=("Segoe UI", 11, "bold"),
    bg="#334155",
    fg="white",
    bd=0,
    command=clear_completed
).pack(pady=5)

tk.Button(
    card,
    text="🌓 Switch Theme",
    font=("Segoe UI", 11, "bold"),
    bg="#64748b",
    fg="white",
    bd=0,
    command=switch_theme
).pack(pady=5)

# Keyboard support
root.bind("<Return>", add_task)

# Load saved tasks on startup
load_tasks()

root.mainloop()
