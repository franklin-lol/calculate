import tkinter as tk
from tkinter import messagebox
import pyperclip  # For copying to clipboard


# Calculator functions
def add():
    try:
        a = int(entry_num1.get())
        b = int(entry_num2.get())
        result = a + b
        set_result(f"{result}")
    except ValueError:
        messagebox.showerror("Error", "Please enter valid numbers!")

def subtract():
    try:
        a = int(entry_num1.get())
        b = int(entry_num2.get())
        result = a - b
        set_result(f"{result}")
    except ValueError:
        messagebox.showerror("Error", "Please enter valid numbers!")

def multiply():
    try:
        a = int(entry_num1.get())
        b = int(entry_num2.get())
        result = round(a * b, 6)
        set_result(f"{result}")
    except ValueError:
        messagebox.showerror("Error", "Please enter valid numbers!")

def divide():
    try:
        a = int(entry_num1.get())
        b = int(entry_num2.get())
        if b == 0:
            messagebox.showerror("Error", "Division by zero is not allowed!")
        else:
            result = round(a / b, 6)
            set_result(f"{result}")
    except ValueError:
        messagebox.showerror("Error", "Please enter valid numbers!")

def to_hex():
    try:
        a = int(entry_num1.get())
        result = hex(a)[2:].upper()  # Convert to hex and remove '0x'
        set_result(f"{result}")
    except ValueError:
        messagebox.showerror("Error", "Please enter a valid decimal number!")

def to_dec():
    try:
        a = entry_num1.get().strip()
        result = int(a, 16)  # Convert from HEX to DEC
        set_result(f"{result}")
    except ValueError:
        messagebox.showerror("Error", "Please enter a valid HEX number!")

def hex_operations(op):
    try:
        a = int(entry_num1.get(), 16)
        b = int(entry_num2.get(), 16)
        if op == "+":
            result = a + b
        elif op == "-":
            result = a - b
        elif op == "*":
            result = round(a * b, 6)
        elif op == "/":
            if b == 0:
                messagebox.showerror("Error", "Division by zero is not allowed!")
                return
            result = round(a / b, 6)
        else:
            return
        set_result(hex(result)[2:].upper())  # Show result as HEX without '0x'
    except ValueError:
        messagebox.showerror("Error", "Please enter valid HEX numbers!")

def set_result(value):
    """Updates the result and allows copying it."""
    result_var.set(value)

def copy_to_clipboard():
    """Copies the result to the clipboard."""
    pyperclip.copy(result_var.get())
    messagebox.showinfo("Copied", "The result has been copied to the clipboard!")

# Main window
root = tk.Tk()
root.title("Large Numbers Calculator")
root.geometry("400x500")
root.resizable(False, False)
root.configure(bg="#2E2E2E")  # Window background

# Widget styles
button_style = {"padx": 10, "pady": 10, "bg": "#4A4A4A", "fg": "white", "font": ("Arial", 10, "bold"), "borderwidth": 0}
label_style = {"bg": "#2E2E2E", "fg": "white", "font": ("Arial", 10, "bold")}

# Input fields
tk.Label(root, text="Number 1:", **label_style).pack(pady=5)
entry_num1 = tk.Entry(root, width=30, bg="#3C3C3C", fg="white", font=("Arial", 12), insertbackground="white")
entry_num1.pack(pady=5)

tk.Label(root, text="Number 2:", **label_style).pack(pady=5)
entry_num2 = tk.Entry(root, width=30, bg="#3C3C3C", fg="white", font=("Arial", 12), insertbackground="white")
entry_num2.pack(pady=5)

# Operation buttons
button_frame = tk.Frame(root, bg="#2E2E2E")
button_frame.pack(pady=10)

tk.Button(button_frame, text="+", command=add, **button_style).grid(row=0, column=0, padx=5, pady=5)
tk.Button(button_frame, text="-", command=subtract, **button_style).grid(row=0, column=1, padx=5, pady=5)
tk.Button(button_frame, text="×", command=multiply, **button_style).grid(row=0, column=2, padx=5, pady=5)
tk.Button(button_frame, text="÷", command=divide, **button_style).grid(row=0, column=3, padx=5, pady=5)

tk.Button(button_frame, text="DEC ➡ HEX", command=to_hex, **button_style).grid(row=1, column=0, columnspan=2, pady=5)
tk.Button(button_frame, text="HEX ➡ DEC", command=to_dec, **button_style).grid(row=1, column=2, columnspan=2, pady=5)

tk.Button(button_frame, text="HEX +", command=lambda: hex_operations("+"), **button_style).grid(row=2, column=0, padx=5, pady=5)
tk.Button(button_frame, text="HEX -", command=lambda: hex_operations("-"), **button_style).grid(row=2, column=1, padx=5, pady=5)
tk.Button(button_frame, text="HEX ×", command=lambda: hex_operations("*"), **button_style).grid(row=2, column=2, padx=5, pady=5)
tk.Button(button_frame, text="HEX ÷", command=lambda: hex_operations("/"), **button_style).grid(row=2, column=3, padx=5, pady=5)

# Result display
tk.Label(root, text="Result:", **label_style).pack(pady=5)
result_var = tk.StringVar()
result_entry = tk.Entry(root, textvariable=result_var, state="readonly", font=("Arial", 10), width=35, bg="#3C3C3C", fg="black", borderwidth=0)
result_entry.pack(pady=5)

# Copy button
tk.Button(root, text="Copy Result", command=copy_to_clipboard, **button_style).pack(pady=10)

# Run the program
root.mainloop()
