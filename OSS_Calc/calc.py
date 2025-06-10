import tkinter as tk
import re


class Calculator:
    def __init__(self, root):
        self.root = root
        self.root.title("계산기")
        self.root.geometry("300x400")

        self.expression = "0"
        self.reset_next = False
        self.locked = False

        self.entry = tk.Entry(root, font=("Arial", 24), justify="right")
        self.entry.pack(fill="both", ipadx=8, ipady=15, padx=10, pady=10)

        buttons = [
            ['7', '8', '9', '/'],
            ['4', '5', '6', '*'],
            ['1', '2', '3', '-'],
            ['0', '.', 'C', '+'],
            ['=']
        ]

        for row in buttons:
            frame = tk.Frame(root)
            frame.pack(expand=True, fill="both")
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
