import tkinter as tk
from tkinter import messagebox
from decimal import Decimal, getcontext, InvalidOperation
import webbrowser

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

        # Кнопка SWAP (между полями)
        self.swap_btn = tk.Button(self.root, text="⇅ Swap Numbers", command=self.swap_inputs, 
                                  bg=self.styles["bg"], fg="#888888", font=("Arial", 9), 
                                  bd=0, activebackground=self.styles["bg"], activeforeground="white", cursor="hand2")
        self.swap_btn.pack(pady=0)
        self._setup_hover(self.swap_btn, self.styles["bg"], "#444444", "#888888", "white")

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
            self._setup_hover(btn, self.styles["btn_bg"], "#5A5A5A")

        # HEX Конвертация
        h1 = tk.Button(btn_frame, text="DEC ➡ HEX", command=self.to_hex, bg="#5A5A5A", fg="white", font=self.styles["font_bold"], width=14)
        h1.grid(row=1, column=0, columnspan=2, pady=5)
        self._setup_hover(h1, "#5A5A5A", "#6A6A6A")

        h2 = tk.Button(btn_frame, text="HEX ➡ DEC", command=self.to_dec, bg="#5A5A5A", fg="white", font=self.styles["font_bold"], width=14)
        h2.grid(row=1, column=2, columnspan=2, pady=5)
        self._setup_hover(h2, "#5A5A5A", "#6A6A6A")
        
        # HEX Арифметика
        hex_ops = [('HEX +', '+'), ('HEX -', '-'), ('HEX ×', '*'), ('HEX ÷', '//')] 
        for i, (text, op) in enumerate(hex_ops):
            btn = tk.Button(btn_frame, text=text, command=lambda o=op: self.hex_calc(o), 
                            bg="#3A4A3A", fg="white", font=("Arial", 9, "bold"), width=8)
            btn.grid(row=2, column=i, padx=2, pady=5)
            self._setup_hover(btn, "#3A4A3A", "#4A5A4A")

        # ОКОШКО РЕЗУЛЬТАТА
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
            readonlybackground=self.styles["res_bg"],
            borderwidth=2
        )
        self.result_entry.pack(pady=5)
        self.result_entry.bind("<Button-1>", lambda e: self.copy_to_clipboard()) # Копировать по клику на поле

        # Кнопки управления
        ctrl_frame = tk.Frame(self.root, bg=self.styles["bg"])
        ctrl_frame.pack(pady=10)
        
        c1 = tk.Button(ctrl_frame, text="Copy Result", command=self.copy_to_clipboard, bg="#007ACC", fg="white", font=self.styles["font_bold"], width=15)
        c1.pack(side=tk.LEFT, padx=5)
        self._setup_hover(c1, "#007ACC", "#008AE6")

        c2 = tk.Button(ctrl_frame, text="Clear All", command=self.clear_inputs, bg="#CC3300", fg="white", font=self.styles["font_bold"], width=15)
        c2.pack(side=tk.LEFT, padx=5)
        self._setup_hover(c2, "#CC3300", "#E63900")

        # Status Label (Toast-like)
        self.status_var = tk.StringVar()
        self.status_label = tk.Label(self.root, textvariable=self.status_var, bg=self.styles["bg"], fg="#00FF00", font=("Arial", 9))
        self.status_label.pack(side=tk.BOTTOM, pady=(5, 0))

        # Footer Help
        help_btn = tk.Button(self.root, text="Help & About System", command=self.show_help, 
                             bg=self.styles["bg"], fg="#666666", font=("Arial", 8, "underline"), 
                             bd=0, activebackground=self.styles["bg"], activeforeground="white", cursor="hand2")
        help_btn.pack(side=tk.BOTTOM, pady=(0, 5))
        self._setup_hover(help_btn, self.styles["bg"], self.styles["bg"], "#666666", "white")

        # Bindings
        self.root.bind('<Return>', lambda e: self.calculate('add'))
        self.root.bind('<Escape>', lambda e: self.clear_inputs())
        self.entry1.focus_set()

    def show_status(self, msg, is_error=False):
        self.status_var.set(msg)
        self.status_label.config(fg="#FF4444" if is_error else "#00FF00")
        # Скрыть через 3 секунды
        self.root.after(3000, lambda: self.status_var.set(""))

    def _setup_hover(self, btn, bg, hbg, fg=None, hfg=None):
        btn.bind("<Enter>", lambda e: btn.config(bg=hbg, fg=hfg if hfg else btn['fg']))
        btn.bind("<Leave>", lambda e: btn.config(bg=bg, fg=fg if fg else btn['fg']))

    def swap_inputs(self):
        v1, v2 = self.entry1.get(), self.entry2.get()
        self.entry1.delete(0, tk.END)
        self.entry1.insert(0, v2)
        self.entry2.delete(0, tk.END)
        self.entry2.insert(0, v1)

    def show_help(self):
        help_window = tk.Toplevel(self.root)
        help_window.title("About & Help")
        help_window.geometry("350x300")
        help_window.configure(bg="#2E2E2E")
        help_window.resizable(False, False)

        help_text = (
            "Large Numbers Calculator v1.1\n\n"
            "• Supports up to 50 decimal digits\n"
            "• HEX <-> DEC conversion & math\n"
            "• [Enter] - Quick Add\n"
            "• [Esc] - Clear All\n\n"
            "Created by:"
        )
        
        tk.Label(help_window, text=help_text, bg="#2E2E2E", fg="white", font=("Arial", 10), justify=tk.CENTER).pack(pady=(20, 0))
        
        link = tk.Label(help_window, text="franklin-sys.vercel.app", bg="#2E2E2E", fg="#00A2FF", font=("Arial", 10, "underline"), cursor="hand2")
        link.pack()
        link.bind("<Button-1>", lambda e: webbrowser.open_new("https://franklin-sys.vercel.app/"))
        
        tk.Button(help_window, text="Close", command=help_window.destroy, bg="#4A4A4A", fg="white", width=10).pack(pady=20)

    def get_decimals(self):
        try:
            val1 = self.entry1.get().replace(',', '.').strip()
            val2 = self.entry2.get().replace(',', '.').strip()
            if not val1 or not val2:
                return None, None
            return Decimal(val1), Decimal(val2)
        except (InvalidOperation, ValueError):
            return None, None

    def calculate(self, op='add'):
        a, b = self.get_decimals()
        if a is None:
            self.show_status("Invalid numbers!", True)
            return
        try:
            if op == 'add': res = a + b
            elif op == 'sub': res = a - b
            elif op == 'mul': res = a * b
            elif op == 'div':
                if b == 0:
                    self.show_status("Division by zero!", True)
                    return
                res = a / b
            self.result_var.set(f"{res.normalize():f}") 
        except Exception as e:
            self.show_status(f"Calc error: {e}", True)

    def hex_calc(self, op):
        try:
            a = int(self.entry1.get(), 16)
            b = int(self.entry2.get(), 16)
            if op == '+': res = a + b
            elif op == '-': res = a - b
            elif op == '*': res = a * b
            elif op == '//':
                if b == 0:
                    self.show_status("Division by zero!", True)
                    return
                res = a // b
            self.result_var.set(hex(res)[2:].upper())
        except ValueError:
            self.show_status("Invalid HEX input!", True)

    def to_hex(self):
        try:
            val = int(Decimal(self.entry1.get().replace(',', '.').strip()))
            self.result_var.set(hex(val)[2:].upper())
        except:
             self.show_status("Invalid integer for HEX", True)

    def to_dec(self):
        try:
            val = int(self.entry1.get().strip(), 16)
            self.result_var.set(str(val))
        except:
            self.show_status("Invalid HEX string", True)

    def copy_to_clipboard(self):
        res = self.result_var.get()
        if res:
            self.root.clipboard_clear()
            self.root.clipboard_append(res)
            self.show_status("Result copied to clipboard!")
        else:
            self.show_status("Nothing to copy", True)

    def clear_inputs(self):
        self.entry1.delete(0, tk.END)
        self.entry2.delete(0, tk.END)
        self.result_var.set("")

if __name__ == "__main__":
    root = tk.Tk()
    app = CalculatorApp(root)
    root.mainloop()
