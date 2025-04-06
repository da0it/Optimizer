import tkinter as tk
from tkinter import *
from tkinter import messagebox
from tkinter.ttk import Combobox
import numpy as np
import optimizer
import sympy as sp
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

window = tk.Tk()
window.title("Функциональный оптимизатор")
window.geometry("1000x600")

# Основные фреймы
main_frame = tk.Frame(window)
main_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

left_frame = tk.Frame(main_frame)
left_frame.grid(row=0, column=0, sticky="nsew", padx=10, pady=10)

right_frame = tk.Frame(main_frame)
right_frame.grid(row=0, column=1, sticky="nsew", padx=10, pady=10)

main_frame.grid_columnconfigure(0, weight=1)
main_frame.grid_columnconfigure(1, weight=3)
main_frame.grid_rowconfigure(0, weight=1)

# Элементы управления
var = tk.StringVar()
var_minmax = tk.StringVar()
var_minmax.set("min")

# Поля ввода
tk.Label(left_frame, text="Enter your function:").grid(row=3, column=1)
function_entry = Entry(left_frame)
function_entry.grid(row=4, column=1)

tk.Label(left_frame, text="Left limit:").grid(row=5, column=1)
left_lim_entry = Entry(left_frame)
left_lim_entry.grid(row=6, column=1)

tk.Label(left_frame, text="Right limit:").grid(row=7, column=1)
right_lim_entry = Entry(left_frame)
right_lim_entry.grid(row=8, column=1)

epsilon_label = tk.Label(left_frame, text="Epsilon:")
epsilon_label.grid(row=9, column=1)
epsilon_entry = Entry(left_frame)
epsilon_entry.grid(row=10, column=1)

tk.Label(left_frame, text="Finite uncertainty interval (l):").grid(row=11, column=1)
minimal_interval_entry = Entry(left_frame)
minimal_interval_entry.grid(row=12, column=1)

tk.Label(left_frame, text="Choose algorithm:").grid(row=13, column=1)

def update_visibility(event=None):
    selected_method = combo_method.get()
    if selected_method in ["Dyhotomy method", "Fibonacci method"]:
        epsilon_label.grid(row=9, column=1)
        epsilon_entry.grid(row=10, column=1)
    else:
        epsilon_label.grid_remove()
        epsilon_entry.grid_remove()

combo_method = Combobox(left_frame, textvariable=var, 
                       values=('Dyhotomy method', 'Golden ratio method', 'Fibonacci method'))
combo_method.current(0)
combo_method.grid(row=14, column=1)
combo_method.bind("<<ComboboxSelected>>", update_visibility)

tk.Label(left_frame, text="Min or max:").grid(row=15, column=1)
combo_minmax = Combobox(left_frame, textvariable=var_minmax, values=('min', 'max'))
combo_minmax.current(0)
combo_minmax.grid(row=16, column=1)

solve = Button(left_frame, text='Solve')
solve.grid(row=17, column=1)

# Таблица результатов
class CustomTable:
    def __init__(self, parent):
        self.parent = parent
        self.table_frame = tk.Frame(parent)
        self.table_frame.pack(fill="both", expand=True)
        self.rows = []
        self.columns = ['k', 'a', 'b', 'L_k', 'M_k', 'F_L', 'F_M']
        self.create_header()

    def create_header(self):
        header_frame = tk.Frame(self.table_frame)
        header_frame.pack(fill="x")
        for col in self.columns:
            tk.Label(header_frame, text=col, borderwidth=1, relief="solid", width=10).pack(side="left")

    def add_row(self, data):
        row_frame = tk.Frame(self.table_frame)
        row_frame.pack(fill="x")
        for value in data:
            tk.Label(row_frame, text=str(value), borderwidth=1, relief="solid", width=10).pack(side="left")
        self.rows.append(row_frame)

    def clear_table(self):
        for row in self.rows:
            row.destroy()
        self.rows = []

table_header = tk.Label(right_frame, text="", font=("Arial", 14, "bold"))
table_header.grid(row=17, columnspan=2)

table_frame = Frame(right_frame)
table_frame.grid(row=18, columnspan=2)

custom_table = CustomTable(table_frame)

opt_x_label = tk.Label(table_frame, text="Optimal x: ")
opt_x_label.pack(fill="x")

opt_f_label = tk.Label(table_frame, text="Optimal F(x): ")
opt_f_label.pack(fill="x")

func_eval_label = tk.Label(table_frame, text="Function evaluation count: ")
func_eval_label.pack(fill="x")

def update_table(k, a, b, L_k, M_k, F_L, F_M):
    custom_table.add_row([k, a, b, L_k, M_k, F_L, F_M])

# График
graph_frame = tk.Frame(right_frame)
graph_frame.grid(row=20, columnspan=2, sticky="nsew")
right_frame.grid_rowconfigure(20, weight=1)

def plot_graph(a_initial, b_initial, a, b, opt_x, opt_f, func, func_type, min_max):
    for widget in graph_frame.winfo_children():
        widget.destroy()

    x = sp.symbols('x')
    formula_expr = sp.sympify(func)
    func = sp.lambdify(x, formula_expr)

    fig = Figure(figsize=(6, 4), dpi=100)
    ax = fig.add_subplot(111)
    
    # Автоматические отступы
    fig.subplots_adjust(left=0.1, right=0.95, bottom=0.15, top=0.85)

    x_min = min(a_initial, a, -10)
    x_max = max(b_initial, b, 10)
    x_vals = np.linspace(x_min, x_max, 400)
    y_vals = func(x_vals)

    ax.plot(x_vals, y_vals, label='f(x)', color='blue')
    ax.axvspan(a_initial, b_initial, alpha=0.2, color='gray', label='Начальный интервал')
    ax.axvspan(a, b, alpha=0.2, color='red', label='Конечный интервал')
    ax.axvline(x=opt_x, color='red', linestyle='--', label=f'x = {opt_x}')
    ax.scatter(opt_x, opt_f, color='green', s=33)

    ax.set_xlabel('x', labelpad=10)
    ax.set_ylabel('f(x)', labelpad=10)
    ax.set_title(f'График функции и интервалы неопределенности\nМетод: {func_type} ({min_max})', pad=20)
    ax.grid(True)
    ax.legend(loc='best', bbox_to_anchor=(1.02, 1), borderaxespad=0.5)
    
    fig.tight_layout()

    canvas = FigureCanvasTkAgg(fig, master=graph_frame)
    canvas.draw()
    canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=True)

def solve_function():
    try:
        custom_table.clear_table()
        func_type = combo_method.get()
        min_max = combo_minmax.get()
        a = float(left_lim_entry.get())
        b = float(right_lim_entry.get())
        l = float(minimal_interval_entry.get())
        f = function_entry.get()
        
        if not f:
            raise ValueError("Функция не введена")
            
    except ValueError as e:
        messagebox.showerror("Ошибка", f"Некорректные входные данные: {str(e)}")
        return

    table_header['text'] = f"Optimization result by method: {func_type} ({min_max})"

    def result_callback(opt_x, opt_f, a, b, func_eval):
        opt_x_label['text'] = f"Optimal x: {round(opt_x, 4)}"
        opt_f_label['text'] = f"Optimal F(x): {round(opt_f, 4)}"
        func_eval_label['text'] = f"Function evaluation count: {func_eval}"
        plot_graph(a, b, a, b, opt_x, opt_f, f, func_type, min_max)

    e = None
    if combo_method.get() != "Golden ratio method": 
        try:
            e = float(epsilon_entry.get())
        except ValueError:
            messagebox.showerror("Ошибка", "Некорректное значение epsilon")
            return

    if func_type == "Dyhotomy method":
        optimizer.dyhotomy(a, b, e, l, min_max, f, update_table, result_callback)
    elif func_type == "Golden ratio method":
        optimizer.golden_ratio(a, b, l, min_max, f, update_table, result_callback)
    elif func_type == "Fibonacci method":
        optimizer.fibonacci_search(f, a, b, l, e, min_max, update_table, result_callback)

update_visibility()
solve.config(command=solve_function)

window.mainloop()