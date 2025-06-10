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
            self.process_input(event.char)import tkinter as tk
import re
import winsound

NOTE_MAP = {
    '1': 261, '2': 293, '3': 329, '4': 349,
    '5': 392, '6': 440, '7': 493, '8': 523,
    '9': 587, '0': 659,
    '+': 392, '-': 349, '*': 329, '/': 293,
    '=': 523, '.': 261, 'C': 220
}

def play_note_for(char):
    freq = NOTE_MAP.get(char)
    if freq:
        winsound.Beep(freq, 100)

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

        self.buttons = []
        self.button_refs = {}

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
                    bg="white",
                    relief="raised",
                    activebackground="lightblue",
                    command=lambda ch=char: self.on_click(ch)
                )
                btn.pack(side="left", expand=True, fill="both")
                self.button_refs[char] = btn

        self.root.bind("<Key>", self.on_keypress)
        self.update_entry()

    def on_click(self, char):
        self.animate_button(char)
        play_note_for(char)
        self.process_input(char)

    def animate_button(self, char):
        btn = self.button_refs.get(char)
        if not btn:
            return
        original_color = btn.cget("bg")
        btn.configure(bg="lightblue")
        self.root.after(150, lambda: btn.configure(bg=original_color))

    def on_keypress(self, event):
        if self.locked:
            return

        key = event.keysym

        if key in ('Return', 'equal'):
            char = '='
        elif key == 'BackSpace':
            char = 'BACK'
        elif key in ('Escape', 'Delete'):
            char = 'C'
        elif key in ('plus', 'minus', 'asterisk', 'slash', 'period'):
            char = event.char
        elif key.isdigit():
            char = event.char
        else:
            return

        self.animate_button(char)
        play_note_for(char)

        self.process_input(char)
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
