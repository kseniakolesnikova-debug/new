import tkinter as tk

# Глобальная переменная для хранения значения памяти
memory_value = None


def get_numbers():
    raw_a = entry_first.get().strip()
    raw_b = entry_second.get().strip()

    try:
        a = int(raw_a)
        b = int(raw_b)
        return a, b
    except ValueError:
        return None


def get_result_value():
    """Вспомогательная функция для получения текущего числового результата из метки out"""
    text = out.cget("text")
    if text.startswith("Результат: ") and text != "Результат: —":
        try:
            return int(text.replace("Результат: ", ""))
        except ValueError:
            return None
    return None


def add_numbers():
    nums = get_numbers()
    if nums is not None:
        a, b = nums
        out.config(text=f"Результат: {a + b}")
    else:
        out.config(text="Ошибка, введите целые числа")


def subtract_numbers():
    nums = get_numbers()
    if nums is not None:
        a, b = nums
        out.config(text=f"Результат: {a - b}")
    else:
        out.config(text="Ошибка, введите целые числа")


def swap_numbers():
    val1 = entry_first.get()
    val2 = entry_second.get()

    entry_first.delete(0, tk.END)
    entry_second.delete(0, tk.END)

    entry_first.insert(0, val2)
    entry_second.insert(0, val1)


def save_to_memory():
    """Записывает текущий результат вычислений в память"""
    global memory_value
    val = get_result_value()
    if val is not None:
        memory_value = val
        label_mem_status.config(text=f"В памяти: {memory_value}")
    else:
        out.config(text="Нечего сохранять: нет результата")


def read_from_memory():
    """Вставляет значение из памяти в первое поле ввода"""
    if memory_value is not None:
        entry_first.delete(0, tk.END)
        entry_first.insert(0, str(memory_value))
    else:
        out.config(text="Память пуста")


root = tk.Tk()
root.title("Мой калькулятор")
root.geometry("420x400")  # Увеличена высота для новых кнопок

label_first = tk.Label(root, text="Первое число")
label_first.pack(pady=2)

entry_first = tk.Entry(root)
entry_first.pack(pady=5)

label_second = tk.Label(root, text="Второе число")
label_second.pack(pady=2)

entry_second = tk.Entry(root)
entry_second.pack(pady=5)

btn_add = tk.Button(root, text="Сложить", command=add_numbers)
btn_add.pack(pady=3)

btn_subtract = tk.Button(root, text="Вычесть", command=subtract_numbers)
btn_subtract.pack(pady=3)

btn_swap = tk.Button(root, text="Поменять местами", command=swap_numbers)
btn_swap.pack(pady=3)

# Новые кнопки для работы с памятью
btn_ms = tk.Button(root, text="В память", command=save_to_memory)
btn_ms.pack(pady=3)

btn_mr = tk.Button(root, text="Из памяти", command=read_from_memory)
btn_mr.pack(pady=3)

# Индикатор текущего значения в памяти
label_mem_status = tk.Label(root, text="В памяти: пусто", fg="gray")
label_mem_status.pack(pady=2)

out = tk.Label(root, text="Результат: —")
out.pack(pady=10)

root.mainloop()
