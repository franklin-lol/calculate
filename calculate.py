import tkinter as tk
from tkinter import messagebox
import pyperclip  # Для копирования в буфер обмена


# Функции калькулятора
def add():
    try:
        a = int(entry_num1.get())
        b = int(entry_num2.get())
        result = a + b
        set_result(f"{result}")
    except ValueError:
        messagebox.showerror("Ошибка", "Введите корректные числа!")

def subtract():
    try:
        a = int(entry_num1.get())
        b = int(entry_num2.get())
        result = a - b
        set_result(f"{result}")
    except ValueError:
        messagebox.showerror("Ошибка", "Введите корректные числа!")

def multiply():
    try:
        a = int(entry_num1.get())
        b = int(entry_num2.get())
        result = a * b
        set_result(f"{result}")
    except ValueError:
        messagebox.showerror("Ошибка", "Введите корректные числа!")

def divide():
    try:
        a = int(entry_num1.get())
        b = int(entry_num2.get())
        if b == 0:
            messagebox.showerror("Ошибка", "Деление на ноль невозможно!")
        else:
            result = a // b
            set_result(f"{result}")
    except ValueError:
        messagebox.showerror("Ошибка", "Введите корректные числа!")

def to_hex():
    try:
        a = int(entry_num1.get())
        result = hex(a).upper()
        set_result(f"{result}")
    except ValueError:
        messagebox.showerror("Ошибка", "Введите корректное число!")

def to_dec():
    try:
        a = entry_num1.get().strip()
        result = int(a, 16)
        set_result(f"{result}")
    except ValueError:
        messagebox.showerror("Ошибка", "Введите корректное HEX число!")

def set_result(value):
    """Обновляет результат и позволяет копировать его"""
    result_var.set(value)

def copy_to_clipboard():
    """Копирует результат в буфер обмена"""
    pyperclip.copy(result_var.get())
    messagebox.showinfo("Скопировано", "Результат скопирован в буфер обмена!")

# Основное окно
root = tk.Tk()
root.title("Калькулятор для больших чисел")
root.geometry("350x450")
root.resizable(False, False)
root.configure(bg="#2E2E2E")  # Фон окна

# Стиль элементов
button_style = {"padx": 10, "pady": 10, "bg": "#4A4A4A", "fg": "white", "font": ("Arial", 10, "bold"), "borderwidth": 0}
label_style = {"bg": "#2E2E2E", "fg": "white", "font": ("Arial", 10, "bold")}

# Поля ввода
tk.Label(root, text="Число 1:", **label_style).pack(pady=5)
entry_num1 = tk.Entry(root, width=30, bg="#3C3C3C", fg="white", font=("Arial", 12), insertbackground="white")
entry_num1.pack(pady=5)

tk.Label(root, text="Число 2:", **label_style).pack(pady=5)
entry_num2 = tk.Entry(root, width=30, bg="#3C3C3C", fg="white", font=("Arial", 12), insertbackground="white")
entry_num2.pack(pady=5)

# Кнопки для операций
button_frame = tk.Frame(root, bg="#2E2E2E")
button_frame.pack(pady=10)

tk.Button(button_frame, text="+", command=add, **button_style).grid(row=0, column=0, padx=5, pady=5)
tk.Button(button_frame, text="-", command=subtract, **button_style).grid(row=0, column=1, padx=5, pady=5)
tk.Button(button_frame, text="×", command=multiply, **button_style).grid(row=0, column=2, padx=5, pady=5)
tk.Button(button_frame, text="÷", command=divide, **button_style).grid(row=0, column=3, padx=5, pady=5)

tk.Button(button_frame, text="DEC ➡ HEX", command=to_hex, **button_style).grid(row=1, column=0, columnspan=2, pady=5)
tk.Button(button_frame, text="HEX ➡ DEC", command=to_dec, **button_style).grid(row=1, column=2, columnspan=2, pady=5)

# Поле для вывода результата
tk.Label(root, text="Результат:", **label_style).pack(pady=5)
result_var = tk.StringVar()
result_entry = tk.Entry(root, textvariable=result_var, state="readonly", font=("Arial", 10), width=35, bg="#3C3C3C", fg="black", borderwidth=0)
result_entry.pack(pady=5)

# Кнопка копирования
tk.Button(root, text="Скопировать результат", command=copy_to_clipboard, **button_style).pack(pady=10)

# Запуск программы
root.mainloop()
