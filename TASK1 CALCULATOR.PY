import tkinter as tk
import math

# -------------------- WINDOW --------------------
root = tk.Tk()
root.title("✧ NeoCalc ✧")
root.geometry("520x650")
root.resizable(False, False)

# -------------------- GRADIENT BACKGROUND --------------------
bg_canvas = tk.Canvas(root, width=520, height=650, highlightthickness=0)
bg_canvas.pack(fill="both", expand=True)

# Create vertical gradient
for i in range(0, 650):
    color = f'#{15+i//8:02x}{23+i//10:02x}{42+i//12:02x}'
    bg_canvas.create_line(0, i, 520, i, fill=color)

# -------------------- DISPLAY --------------------
display = tk.Entry(
    root,
    font=("Segoe UI", 28, "bold"),
    bg="#020617",
    fg="#22d3ee",
    bd=0,
    justify="right",
    insertbackground="#22d3ee"
)
display.place(x=25, y=35, width=470, height=70)
display.insert(0, "0")

# -------------------- CALCULATOR LOGIC --------------------
class Calculator:
    def __init__(self):
        self.reset = True

    def write(self, value):
        if self.reset or display.get() == "0":
            display.delete(0, "end")
            self.reset = False
        display.insert("end", value)

    def clear(self):
        display.delete(0, "end")
        display.insert(0, "0")
        self.reset = True

    def eval(self):
        try:
            result = eval(display.get())
            display.delete(0, "end")
            display.insert(0, result)
            self.reset = True
        except:
            display.delete(0, "end")
            display.insert(0, "Error")
            self.reset = True

    def sci(self, func):
        try:
            value = float(display.get())
            display.delete(0, "end")
            display.insert(0, func(value))
            self.reset = True
        except:
            display.delete(0, "end")
            display.insert(0, "Error")
            self.reset = True

calc = Calculator()

# -------------------- BUTTON PANEL --------------------
panel = tk.Frame(root, bg="#0f172a")
panel.place(x=25, y=130, width=470, height=480)

# -------------------- GLOW BUTTON --------------------
def glow_button(text, r, c, cmd, bg):
    btn = tk.Button(
        panel,
        text=text,
        command=cmd,
        font=("Segoe UI", 14, "bold"),
        bg=bg,
        fg="white",
        bd=0,
        relief="flat",
        activebackground=bg,
        width=5,
        height=2
    )

    # Hover glow
    def on_enter(e):
        btn.config(bg="#38bdf8")

    def on_leave(e):
        btn.config(bg=bg)

    btn.bind("<Enter>", on_enter)
    btn.bind("<Leave>", on_leave)

    btn.grid(row=r, column=c, padx=10, pady=10, sticky="nsew")

# Grid config
for i in range(6):
    panel.columnconfigure(i, weight=1)
    panel.rowconfigure(i, weight=1)

# -------------------- BUTTONS --------------------
# Top row
glow_button("CE", 0, 0, calc.clear, "#ef4444")
glow_button("√", 0, 1, lambda: calc.sci(math.sqrt), "#8b5cf6")
glow_button("sin", 0, 2, lambda: calc.sci(lambda x: math.sin(math.radians(x))), "#06b6d4")
glow_button("cos", 0, 3, lambda: calc.sci(lambda x: math.cos(math.radians(x))), "#06b6d4")
glow_button("tan", 0, 4, lambda: calc.sci(lambda x: math.tan(math.radians(x))), "#06b6d4")
glow_button("log", 0, 5, lambda: calc.sci(math.log10), "#06b6d4")

# Numbers & operators
buttons = [
    ("7",1,0),("8",1,1),("9",1,2),("+",1,3),
    ("4",2,0),("5",2,1),("6",2,2),("-",2,3),
    ("1",3,0),("2",3,1),("3",3,2),("*",3,3),
    ("0",4,0),(".",4,1),("/",4,2),("=",4,3)
]

for txt, r, c in buttons:
    if txt.isdigit() or txt == ".":
        color = "#2563eb"
        cmd = lambda x=txt: calc.write(x)
    elif txt == "=":
        color = "#22c55e"
        cmd = calc.eval
    else:
        color = "#f97316"
        cmd = lambda x=txt: calc.write(x)

    glow_button(txt, r, c, cmd, color)

# Extra scientific
glow_button("ln", 1, 4, lambda: calc.sci(math.log), "#06b6d4")
glow_button("x²", 2, 4, lambda: calc.sci(lambda x: x*x), "#06b6d4")
glow_button("π", 3, 4, lambda: calc.write(str(math.pi)), "#06b6d4")
glow_button("e", 4, 4, lambda: calc.write(str(math.e)), "#06b6d4")

root.mainloop()