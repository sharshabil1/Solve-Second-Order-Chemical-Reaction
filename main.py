import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import math
import csv

# Bisection method function
def bisection_method(A0, Ad, k, a=0, b=20, tol=0.001, max_iter=50):
    def f(t):
        return (1 / A0) + k * t - (1 / Ad)

    data = []

    for i in range(max_iter):
        c = (a + b) / 2
        f_c = f(c)
        error = abs(b - a) / 2

        data.append((i + 1, a, b, c, f_c, error))

        if abs(f_c) < tol or error < tol:
            break

        if f(a) * f_c < 0:
            b = c
        else:
            a = c

    return data

# GUI setup
def run_bisection():
    global results, iterations, errors
    try:
        A0 = float(entry_A0.get())
        Ad = float(entry_Ad.get())
        k = float(entry_k.get())
    except ValueError:
        messagebox.showerror("Input Error", "Please enter valid numerical values.")
        return

    results = bisection_method(A0, Ad, k)

    for row in tree.get_children():
        tree.delete(row)

    iterations = []
    errors = []

    for row in results:
        tree.insert("", "end", values=[f"{v:.6f}" if isinstance(v, float) else v for v in row])
        iterations.append(row[0])
        errors.append(row[5])

    plot_iterations(iterations, errors)

def plot_iterations(iterations, errors):
    fig.clear()
    ax = fig.add_subplot(111)
    ax.plot(iterations, errors, marker='o')
    ax.set_title("Error vs Iteration")
    ax.set_xlabel("Iteration")
    ax.set_ylabel("Error")
    ax.grid(True)
    canvas.draw()

def export_table():
    if not results:
        messagebox.showwarning("No Data", "Run the bisection method first.")
        return
    filepath = filedialog.asksaveasfilename(defaultextension=".csv", filetypes=[("CSV files", "*.csv")])
    if filepath:
        with open(filepath, "w", newline='') as f:
            writer = csv.writer(f)
            writer.writerow(["Iteration", "a", "b", "c (midpoint)", "f(c)", "Error"])
            for row in results:
                writer.writerow(row)
        messagebox.showinfo("Success", f"Data exported to {filepath}")

def save_plot():
    if not errors:
        messagebox.showwarning("No Plot", "Run the bisection method first.")
        return
    filepath = filedialog.asksaveasfilename(defaultextension=".png", filetypes=[("PNG files", "*.png")])
    if filepath:
        fig.savefig(filepath)
        messagebox.showinfo("Success", f"Plot saved to {filepath}")

root = tk.Tk()
root.title("Bisection Method for Reaction Rate")

# Input Frame
frame_input = tk.Frame(root)
frame_input.pack(pady=10)

labels = ["Initial Concentration [A0]", "Desired Concentration [Ad]", "Rate Constant [k]"]

tk.Label(frame_input, text="Initial Concentration [A0]").grid(row=0, column=0, padx=5, pady=5)
entry_A0 = tk.Entry(frame_input)
entry_A0.grid(row=0, column=1, padx=5, pady=5)
entry_A0.insert(0, "0.1")

tk.Label(frame_input, text="Desired Concentration [Ad]").grid(row=1, column=0, padx=5, pady=5)
entry_Ad = tk.Entry(frame_input)
entry_Ad.grid(row=1, column=1, padx=5, pady=5)
entry_Ad.insert(0, "0.03")

tk.Label(frame_input, text="Rate Constant [k]").grid(row=2, column=0, padx=5, pady=5)
entry_k = tk.Entry(frame_input)
entry_k.grid(row=2, column=1, padx=5, pady=5)
entry_k.insert(0, "2.5")

# Buttons
button_frame = tk.Frame(root)
button_frame.pack(pady=5)

tk.Button(button_frame, text="Run Bisection", command=run_bisection).grid(row=0, column=0, padx=10)
tk.Button(button_frame, text="Export Table", command=export_table).grid(row=0, column=1, padx=10)
tk.Button(button_frame, text="Save Plot", command=save_plot).grid(row=0, column=2, padx=10)

# Table Frame
frame_table = tk.Frame(root)
frame_table.pack(pady=10)

cols = ["Iteration", "a", "b", "c (midpoint)", "f(c)", "Error"]
tree = ttk.Treeview(frame_table, columns=cols, show="headings")
for col in cols:
    tree.heading(col, text=col)
    tree.column(col, anchor="center")
tree.pack()

# Plot Frame
frame_plot = tk.Frame(root)
frame_plot.pack(pady=10)

fig = plt.Figure(figsize=(6, 4))
canvas = FigureCanvasTkAgg(fig, master=frame_plot)
canvas.get_tk_widget().pack()

# Initialize global variables
results = []
iterations = []
errors = []

root.mainloop()
