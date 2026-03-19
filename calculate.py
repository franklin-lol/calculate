import tkinter as tk
from tkinter import messagebox
from decimal import Decimal, getcontext, InvalidOperation
import pyperclip
import re

# Precision for large numbers
getcontext().prec = 64


# utility functions

def is_valid_hex(value: str) -> bool:
    return re.fullmatch(r"[0-9a-fA-F]+", value) is not None


def set_result(value: str):
    result_var.set(value)


def copy_to_clipboard():
    pyperclip.copy(result_var.get())
    messagebox.showinfo("Copied", "The result has been copied to the clipboard!")


# operation with decimal

def calculate(op: str):
    try:
        a = Decimal(entry_num1.get())
        b = Decimal(entry_num2.get())

        if op == "+":
            result = a + b
        elif op == "-":
            result = a - b
        elif op == "*":
            result = a * b
        elif op == "/":
            if b == 0:
                messagebox.showerror("Error", "Division by zero is not allowed!")
                return
            result = a / b
        else:
            return

        set_result(str(result))

    except (InvalidOperation, ValueError):
        messagebox.showerror("Error", "Please enter valid decimal numbers!")


# HEX op

def hex_calculate(op: str):
    a = entry_num1.get().strip()
    b = entry_num2.get().strip()

    if not is_valid_hex(a) or not is_valid_hex(b):
        messagebox.showerror("Error", "Please enter valid HEX numbers!")
        return

    a_dec = int(a, 16)
    b_dec = int(b, 16)

    if op == "+":
        result = a_dec + b_dec
    elif op == "-":
        result = a_dec - b_dec
    elif op == "*":
        result = a_dec * b_dec
    elif op == "/":
        if b_dec == 0:
            messagebox.showerror("Error", "Division by zero is not allowed!")
            return
        result = a_dec // b_dec
    else:
        return

    set_result(hex(result)[2:].upper())


def dec_to_hex():
    try:
        value = Decimal(entry_num1.get())
        set_result(hex(int(value))[2:].upper())
    except (InvalidOperation, ValueError):
        messagebox.showerror("Error", "Please enter a valid decimal number!")


def hex_to_dec():
    value = entry_num1.get().strip()

    if not is_valid_hex(value):
        messagebox.showerror("Error", "Please enter a valid HEX number!")
        return

    set_result(str(int(value, 16)))


# gui

root = tk.Tk()
root.title("Large Numbers Calculator")
root.geometry("400x500")
root.resizable(False, False)
root.configure(bg="#2E2E2E")

button_style = {
    "padx": 10,
    "pady": 10,
    "bg": "#4A4A4A",
    "fg": "white",
    "font": ("Arial", 10, "bold"),
    "borderwidth": 0
}

label_style = {
    "bg": "#2E2E2E",
    "fg": "white",
    "font": ("Arial", 10, "bold")
}

tk.Label(root, text="Number 1:", **label_style).pack(pady=5)
entry_num1 = tk.Entry(root, width=30, bg="#3C3C3C", fg="white",
                      font=("Arial", 12), insertbackground="white")
entry_num1.pack(pady=5)

tk.Label(root, text="Number 2:", **label_style).pack(pady=5)
entry_num2 = tk.Entry(root, width=30, bg="#3C3C3C", fg="white",
                      font=("Arial", 12), insertbackground="white")
entry_num2.pack(pady=5)

button_frame = tk.Frame(root, bg="#2E2E2E")
button_frame.pack(pady=10)

tk.Button(button_frame, text="+", command=lambda: calculate("+"), **button_style).grid(row=0, column=0, padx=5, pady=5)
tk.Button(button_frame, text="-", command=lambda: calculate("-"), **button_style).grid(row=0, column=1, padx=5, pady=5)
tk.Button(button_frame, text="×", command=lambda: calculate("*"), **button_style).grid(row=0, column=2, padx=5, pady=5)
tk.Button(button_frame, text="÷", command=lambda: calculate("/"), **button_style).grid(row=0, column=3, padx=5, pady=5)

tk.Button(button_frame, text="DEC ➡ HEX", command=dec_to_hex, **button_style).grid(row=1, column=0, columnspan=2, pady=5)
tk.Button(button_frame, text="HEX ➡ DEC", command=hex_to_dec, **button_style).grid(row=1, column=2, columnspan=2, pady=5)

tk.Button(button_frame, text="HEX +", command=lambda: hex_calculate("+"), **button_style).grid(row=2, column=0, padx=5)
tk.Button(button_frame, text="HEX -", command=lambda: hex_calculate("-"), **button_style).grid(row=2, column=1, padx=5)
tk.Button(button_frame, text="HEX ×", command=lambda: hex_calculate("*"), **button_style).grid(row=2, column=2, padx=5)
tk.Button(button_frame, text="HEX ÷", command=lambda: hex_calculate("/"), **button_style).grid(row=2, column=3, padx=5)

tk.Label(root, text="Result:", **label_style).pack(pady=5)
result_var = tk.StringVar()
tk.Entry(root, textvariable=result_var, state="readonly",
         width=35, bg="#3C3C3C", fg="black",
         font=("Arial", 10), borderwidth=0).pack(pady=5)

tk.Button(root, text="Copy Result", command=copy_to_clipboard, **button_style).pack(pady=10)

root.mainloop()
