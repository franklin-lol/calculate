import tkinter as tk
from tkinter import messagebox
from decimal import Decimal, getcontext, InvalidOperation

# Установка точности (можно увеличить до 100-1000 для гигантских чисел)
getcontext().prec = 50 

class CalculatorApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Large Numbers Calc")
        self.root.geometry("400x550")
        self.root.configure(bg="#2E2E2E")
        self.root.resizable(False, False)

        self.styles = {
            "bg": "#2E2E2E",
            "fg": "white",
            "btn_bg": "#4A4A4A",
            "entry_bg": "#3C3C3C",
            "res_bg": "#CCCCCC", # Светлое окошко для результата
            "res_fg": "#333333", # ТЕМНО-СЕРЫЙ шрифт
            "font_main": ("Arial", 12),
            "font_bold": ("Arial", 10, "bold")
        }

        self._create_widgets()

    def _create_widgets(self):
        # Ввод Число 1
        tk.Label(self.root, text="Number 1:", bg=self.styles["bg"], fg=self.styles["fg"], font=self.styles["font_bold"]).pack(pady=(10, 0))
        self.entry1 = tk.Entry(self.root, width=35, bg=self.styles["entry_bg"], fg="white", font=self.styles["font_main"], insertbackground="white")
        self.entry1.pack(pady=5)

        # Ввод Число 2
        tk.Label(self.root, text="Number 2:", bg=self.styles["bg"], fg=self.styles["fg"], font=self.styles["font_bold"]).pack(pady=5)
        self.entry2 = tk.Entry(self.root, width=35, bg=self.styles["entry_bg"], fg="white", font=self.styles["font_main"], insertbackground="white")
        self.entry2.pack(pady=5)

        # Кнопки операций
        btn_frame = tk.Frame(self.root, bg=self.styles["bg"])
        btn_frame.pack(pady=15)

        ops = [('+', 'add'), ('-', 'sub'), ('×', 'mul'), ('÷', 'div')]
        for i, (symbol, op) in enumerate(ops):
            btn = tk.Button(btn_frame, text=symbol, command=lambda o=op: self.calculate(o), 
                            bg=self.styles["btn_bg"], fg="white", font=("Arial", 14, "bold"), width=4)
            btn.grid(row=0, column=i, padx=5, pady=5)

        # HEX Конвертация
        tk.Button(btn_frame, text="DEC ➡ HEX", command=self.to_hex, bg="#5A5A5A", fg="white", font=self.styles["font_bold"], width=14).grid(row=1, column=0, columnspan=2, pady=5)
        tk.Button(btn_frame, text="HEX ➡ DEC", command=self.to_dec, bg="#5A5A5A", fg="white", font=self.styles["font_bold"], width=14).grid(row=1, column=2, columnspan=2, pady=5)
        
        # HEX Арифметика
        hex_ops = [('HEX +', '+'), ('HEX -', '-'), ('HEX ×', '*'), ('HEX ÷', '//')] 
        for i, (text, op) in enumerate(hex_ops):
            btn = tk.Button(btn_frame, text=text, command=lambda o=op: self.hex_calc(o), 
                            bg="#3A4A3A", fg="white", font=("Arial", 9, "bold"), width=8)
            btn.grid(row=2, column=i, padx=2, pady=5)

        # ОКОШКО РЕЗУЛЬТАТА (Светлое с серым шрифтом)
        tk.Label(self.root, text="Result:", bg=self.styles["bg"], fg=self.styles["fg"], font=self.styles["font_bold"]).pack(pady=5)
        
        self.result_var = tk.StringVar()
        self.result_entry = tk.Entry(
            self.root, 
            textvariable=self.result_var, 
            state="readonly", 
            font=("Arial", 12, "bold"), 
            width=35, 
            bg=self.styles["res_bg"], 
            fg=self.styles["res_fg"], 
            readonlybackground=self.styles["res_bg"], # Чтобы фон не менялся при readonly
            borderwidth=2
        )
        self.result_entry.pack(pady=5)

        # Кнопки управления
        ctrl_frame = tk.Frame(self.root, bg=self.styles["bg"])
        ctrl_frame.pack(pady=10)
        
        tk.Button(ctrl_frame, text="Copy Result", command=self.copy_to_clipboard, bg="#007ACC", fg="white", font=self.styles["font_bold"], width=15).pack(side=tk.LEFT, padx=5)
        tk.Button(ctrl_frame, text="Clear All", command=self.clear_inputs, bg="#CC3300", fg="white", font=self.styles["font_bold"], width=15).pack(side=tk.LEFT, padx=5)

    def get_decimals(self):
        try:
            val1 = self.entry1.get().replace(',', '.').strip()
            val2 = self.entry2.get().replace(',', '.').strip()
            return Decimal(val1), Decimal(val2)
        except (InvalidOperation, ValueError):
            return None, None

    def calculate(self, op):
        a, b = self.get_decimals()
        if a is None:
            messagebox.showerror("Error", "Invalid numbers!")
            return
        try:
            if op == 'add': res = a + b
            elif op == 'sub': res = a - b
            elif op == 'mul': res = a * b
            elif op == 'div':
                if b == 0:
                    messagebox.showerror("Error", "Division by zero!")
                    return
                res = a / b
            self.result_var.set(f"{res.normalize():f}") 
        except Exception as e:
            messagebox.showerror("Error", f"Calc error: {e}")

    def hex_calc(self, op):
        try:
            a = int(self.entry1.get(), 16)
            b = int(self.entry2.get(), 16)
            if op == '+': res = a + b
            elif op == '-': res = a - b
            elif op == '*': res = a * b
            elif op == '//':
                if b == 0:
                    messagebox.showerror("Error", "Division by zero!")
                    return
                res = a // b
            self.result_var.set(hex(res)[2:].upper())
        except ValueError:
            messagebox.showerror("Error", "Invalid HEX input!")

    def to_hex(self):
        try:
            val = int(Decimal(self.entry1.get().replace(',', '.').strip()))
            self.result_var.set(hex(val)[2:].upper())
        except:
             messagebox.showerror("Error", "Invalid integer for HEX")

    def to_dec(self):
        try:
            val = int(self.entry1.get().strip(), 16)
            self.result_var.set(str(val))
        except:
            messagebox.showerror("Error", "Invalid HEX string")

    def copy_to_clipboard(self):
        self.root.clipboard_clear()
        self.root.clipboard_append(self.result_var.get())
        messagebox.showinfo("Copied", "Result in clipboard!")

    def clear_inputs(self):
        self.entry1.delete(0, tk.END)
        self.entry2.delete(0, tk.END)
        self.result_var.set("")

if __name__ == "__main__":
    root = tk.Tk()
    app = CalculatorApp(root)
    root.mainloop()
