
import tkinter as tk
import random
import string

# ---------------- WINDOW ----------------
root = tk.Tk()
root.title("🔐 Neo Password Generator")
root.geometry("520x580")
root.resizable(False, False)
root.configure(bg="#0b1220")

ACCENT = "#38bdf8"

# ---------------- CARD ----------------
card = tk.Frame(root, bg="#020617")
card.place(x=30, y=20, width=460, height=540)

# ---------------- TITLE ----------------
title = tk.Label(
    card,
    text="Strong Password Generator",
    font=("Segoe UI", 18, "bold"),
    fg=ACCENT,
    bg="#020617"
)
title.pack(pady=15)

# ---------------- LENGTH ----------------
tk.Label(
    card, text="Password Length",
    font=("Segoe UI", 12),
    fg="#e5e7eb",
    bg="#020617"
).pack()

length_entry = tk.Entry(
    card,
    font=("Segoe UI", 15, "bold"),
    justify="center",
    bg="#0b1220",
    fg=ACCENT,
    bd=0,
    insertbackground=ACCENT
)
length_entry.pack(pady=8, ipadx=12, ipady=6)
length_entry.insert(0, "12")

# ---------------- OPTIONS ----------------
tk.Label(
    card, text="Select Characters",
    font=("Segoe UI", 12, "bold"),
    fg="#94a3b8",
    bg="#020617"
).pack(pady=(12, 4))

options = tk.Frame(card, bg="#020617")
options.pack()

upper = tk.BooleanVar(value=True)
lower = tk.BooleanVar(value=True)
digits = tk.BooleanVar(value=True)
symbols = tk.BooleanVar(value=True)

def option(text, var, r, c):
    tk.Checkbutton(
        options,
        text=text,
        variable=var,
        bg="#020617",
        fg="#e5e7eb",
        activebackground="#020617",
        selectcolor="#020617",
        font=("Segoe UI", 10)
    ).grid(row=r, column=c, padx=20, pady=4, sticky="w")

option("Uppercase (A-Z)", upper, 0, 0)
option("Lowercase (a-z)", lower, 1, 0)
option("Numbers (0-9)", digits, 0, 1)
option("Symbols (!@#$)", symbols, 1, 1)

# ---------------- OUTPUT ----------------
output = tk.Entry(
    card,
    font=("Segoe UI", 16, "bold"),
    justify="center",
    bg="#0b1220",
    fg="#22c55e",
    bd=0
)
output.pack(fill="x", padx=30, pady=15)

# ---------------- STRENGTH ----------------
strength = tk.Label(
    card,
    text="Strength:",
    font=("Segoe UI", 11, "bold"),
    fg="#e5e7eb",
    bg="#020617"
)
strength.pack()

def check_strength(pwd):
    score = sum([
        any(c.islower() for c in pwd),
        any(c.isupper() for c in pwd),
        any(c.isdigit() for c in pwd),
        any(c in "!@#$%^&*" for c in pwd)
    ])

    if score <= 1:
        strength.config(text="Strength: Weak ❌", fg="#ef4444")
    elif score == 2:
        strength.config(text="Strength: Medium ⚠", fg="#f59e0b")
    else:
        strength.config(text="Strength: Strong ✅", fg="#22c55e")

# ---------------- HISTORY ----------------
history_box = tk.Listbox(
    card,
    height=5,
    bg="#0b1220",
    fg=ACCENT,
    bd=0,
    font=("Segoe UI", 10)
)
history_box.pack(fill="x", padx=40, pady=10)

history = []

# ---------------- LOGIC ----------------
def generate_password(event=None):
    try:
        length = int(length_entry.get())
        chars = ""

        if upper.get(): chars += string.ascii_uppercase
        if lower.get(): chars += string.ascii_lowercase
        if digits.get(): chars += string.digits
        if symbols.get(): chars += "!@#$%^&*"

        if not chars:
            output.delete(0, "end")
            output.insert(0, "Select options!")
            return

        pwd = "".join(random.choice(chars) for _ in range(length))
        output.delete(0, "end")
        output.insert(0, pwd)
        check_strength(pwd)

        history.insert(0, pwd)
        history[:] = history[:5]
        history_box.delete(0, "end")
        for h in history:
            history_box.insert("end", h)

        root.after(10000, lambda: output.delete(0, "end"))

    except:
        output.delete(0, "end")
        output.insert(0, "Invalid Length")

# ---------------- COPY ----------------
def copy_password():
    if output.get():
        root.clipboard_clear()
        root.clipboard_append(output.get())
        strength.config(text="Copied to clipboard ✔", fg="#22c55e")

# ---------------- ACCENT SELECTOR ----------------
def set_accent(color):
    global ACCENT
    ACCENT = color
    title.config(fg=ACCENT)
    length_entry.config(fg=ACCENT, insertbackground=ACCENT)
    history_box.config(fg=ACCENT)

accent_frame = tk.Frame(card, bg="#020617")
accent_frame.pack(pady=8)

tk.Button(accent_frame, text="Blue", bg="#38bdf8", bd=0,
          command=lambda: set_accent("#38bdf8")).grid(row=0, column=0, padx=6)
tk.Button(accent_frame, text="Green", bg="#22c55e", bd=0,
          command=lambda: set_accent("#22c55e")).grid(row=0, column=1, padx=6)
tk.Button(accent_frame, text="Purple", bg="#a855f7", bd=0,
          command=lambda: set_accent("#a855f7")).grid(row=0, column=2, padx=6)

# ---------------- BUTTONS ----------------
tk.Button(
    card,
    text="Generate Password",
    font=("Segoe UI", 14, "bold"),
    bg="#2563eb",
    fg="white",
    bd=0,
    height=2,
    command=generate_password
).pack(pady=12)

tk.Button(
    card,
    text="Copy",
    font=("Segoe UI", 11, "bold"),
    bg="#22c55e",
    fg="white",
    bd=0,
    command=copy_password
).pack()

# Enter key binding
root.bind("<Return>", generate_password)

root.mainloop()
