import tkinter as tk
from tkinter import ttk, colorchooser
import re


class Calculator:
    def __init__(self, root):
        self.root = root
        self.root.title("계산기")
        self.root.geometry("300x500")

        self.expression = "0"
        self.reset_next = False
        self.locked = False

        self.theme_colors = {
            "bg": "#ffffff",
            "btn_bg": "#e0e0e0",
            "btn_fg": "#000000",
            "entry_bg": "#ffffff",
            "entry_fg": "#000000"
        }

        self.notebook = ttk.Notebook(root)
        self.calc_frame = tk.Frame(self.notebook)
        self.theme_frame = tk.Frame(self.notebook)
        self.notebook.add(self.calc_frame, text="계산기")
        self.notebook.add(self.theme_frame, text="테마 설정")
        self.notebook.pack(fill="both", expand=True)

        self.create_calculator_ui()
        self.create_theme_ui()
        self.apply_theme()

    def create_calculator_ui(self):
        self.entry = tk.Entry(self.calc_frame, font=("Arial", 24), justify="right")
        self.entry.pack(fill="both", ipadx=8, ipady=15, padx=10, pady=10)

        self.button_frames = []
        buttons = [
            ['7', '8', '9', '/'],
            ['4', '5', '6', '*'],
            ['1', '2', '3', '-'],
            ['0', '.', 'C', '+'],
            ['=']
        ]

        for row in buttons:
            frame = tk.Frame(self.calc_frame)
            frame.pack(expand=True, fill="both")
            self.button_frames.append(frame)
            for char in row:
                btn = tk.Button(
                    frame,
                    text=char,
                    font=("Arial", 18),
                    command=lambda ch=char: self.on_click(ch)
                )
                btn.pack(side="left", expand=True, fill="both")

        self.root.bind("<Key>", self.on_keypress)
        self.update_entry()

    def create_theme_ui(self):
        keys = ["bg", "btn_bg", "btn_fg", "entry_bg", "entry_fg"]
        labels = {
            "bg": "배경색",
            "btn_bg": "버튼 배경",
            "btn_fg": "버튼 글자",
            "entry_bg": "입력창 배경",
            "entry_fg": "입력창 글자"
        }

        for key in keys:
            frame = tk.Frame(self.theme_frame)
            frame.pack(fill="x", padx=10, pady=5)
            lbl = tk.Label(frame, text=labels[key])
            lbl.pack(side="left")
            btn = tk.Button(frame, text="색상 선택", command=lambda k=key: self.choose_color(k))
            btn.pack(side="right")

        apply_btn = tk.Button(self.theme_frame, text="테마 적용", command=self.apply_theme)
        apply_btn.pack(pady=15)

    def choose_color(self, key):
        color = colorchooser.askcolor(title=f"{key} 색상 선택")[1]
        if color:
            self.theme_colors[key] = color

    def apply_theme(self):
        c = self.theme_colors
        self.root.config(bg=c["bg"])
        self.calc_frame.config(bg=c["bg"])
        self.entry.config(bg=c["entry_bg"], fg=c["entry_fg"], insertbackground=c["entry_fg"])

        for frame in self.button_frames:
            frame.config(bg=c["bg"])
            for btn in frame.winfo_children():
                btn.config(bg=c["btn_bg"], fg=c["btn_fg"])

        self.theme_frame.config(bg=c["bg"])
        for child in self.theme_frame.winfo_children():
            if isinstance(child, tk.Frame):
                child.config(bg=c["bg"])
                for sub in child.winfo_children():
                    sub.config(bg=c["bg"], fg=c["btn_fg"])

    def on_click(self, char):
        self.process_input(char)

    def on_keypress(self, event):
        if self.locked:
            return

        key = event.keysym
        if key in ('Return', 'equal'):
            self.process_input('=')
        elif key == 'BackSpace':
            self.process_input('BACK')
        elif key in ('Escape', 'Delete'):
            self.process_input('C')
        elif key in ('plus', 'minus', 'asterisk', 'slash', 'period'):
            self.process_input(event.char)
        elif key.isdigit():
            self.process_input(event.char)

        self.update_entry()

    def process_input(self, char):
        if self.locked:
            return

        if char == 'BACK':
            self.expression = self.expression[:-1] or "0"
            return

        if char == 'C':
            self.expression = "0"
        elif char == '=':
            try:
                if self.expression[-1] in '+-*/':
                    last_num_match = re.search(r'(\d+\.?\d*)$', self.expression[:-1])
                    if last_num_match:
                        last_num = last_num_match.group(1)
                        self.expression += last_num
                self.expression = str(eval(self.expression))
            except Exception:
                self.display_error()
                return
            self.reset_next = True
        else:
            if self.reset_next:
                if char.isdigit() or char == '.':
                    self.expression = char
                elif char in '+-*/':
                    if self.expression and self.expression[-1].isdigit():
                        self.expression += char
                self.reset_next = False
            else:
                if self.expression == "0" and char not in ['.', '+', '-', '*', '/']:
                    self.expression = ""

                if not self.expression:
                    if char == '-':
                        self.expression = '-'
                    elif char in '+*/.':
                        return
                    elif char.isdigit():
                        self.expression = char
                    return

                if char in '+-*/':
                    if self.expression[-1] in '+-*/':
                        self.expression = self.expression[:-1] + char
                        self.update_entry()
                        return

                if char == '.':
                    if self.expression[-1] in '+-*/':
                        return
                    tokens = re.split(r'[+\-*/]', self.expression)
                    if '.' in tokens[-1]:
                        return

                self.expression += char

        self.update_entry()

    def update_entry(self):
        self.entry.delete(0, tk.END)
        self.entry.insert(tk.END, self.expression)

    def display_error(self):
        self.expression = "에러"
        self.locked = True
        self.update_entry()
        self.root.after(1000, self.reset_after_error)
            
    def reset_after_error(self):
        self.expression = "0"
        self.locked = False
        self.update_entry()