import math
from tkinter import *


def add(n1, d1, n2, d2):
    n = n1 * d2 + n2 * d1
    d = d1 * d2
    return n, d


def sub(n1, d1, n2, d2):
    n = n1 * d2 - n2 * d1
    d = d1 * d2
    return n, d


def mult(n1, d1, n2, d2):
    n = n1 * n2
    d = d1 * d2
    return n, d


def div(n1, d1, n2, d2):

    n = n1 * d2
    d = n2 * d1
    return n, d


def handler():
    try:
        n1 = int(num1.get())
        d1 = int(den1.get())
        n2 = int(num2.get())
        d2 = int(den2.get())
        operator = oper.get().strip()

        if d1 == 0 or d2 == 0:
            raise ZeroDivisionError('Знаменатель не может быть равен нулю')

        if operator == "+":
            result = add(n1, d1, n2, d2)
        elif operator == "-":
            result = sub(n1, d1, n2, d2)
        elif operator == "*":
            result = mult(n1, d1, n2, d2)
        elif operator == "/":
            if n2 == 0:
                raise ZeroDivisionError('На ноль делить нельзя')
            result = div(n1, d1, n2, d2)
        else:
            return

        res_n, res_d = result[0], result[1]

        # Корректный перенос знака минус в числитель
        if res_d < 0:
            res_n = -res_n
            res_d = -res_d

        # Сокращение дроби с помощью НОД
        nod = math.gcd(res_n, res_d)
        n = res_n // nod
        d = res_d // nod

        # Выделение целой части (работаем с модулем числа)
        abs_n = abs(n)
        int_part_val = abs_n // d
        remainder = abs_n % d

        # Определение знака итогового ответа
        sign = "-" if n < 0 else ""

        # Формирование вывода
        if remainder == 0:  # Если делится нацело
            int_part = f"{sign}{int_part_val}" if int_part_val != 0 else "0"
            n_str, d_str = "", ""
        else:  # Если осталась дробная часть
            if int_part_val != 0:
                int_part = f"{sign}{int_part_val}"
            else:
                int_part = "-" if sign == "-" else ""  # Минус перед самой дробью
            n_str, d_str = str(remainder), str(d)

        # Вывод результатов на экран
        num3.config(text=n_str)
        den3.config(text=d_str)
        res_int.config(text=int_part)

    except Exception as err:
        print(err)
        num3.config(text="?")
        den3.config(text="?")
        res_int.config(text=" Error ")


root = Tk()
root.title("Калькулятор дробей")
root.geometry("300x140+600+150")

frame = Frame(root)
frame.pack(pady=10)

num1 = Entry(frame, width=2)
num1.config(font=("Arial", 15), justify="center")
num1.grid(row=0, column=0)
Label(frame, text=chr(8212) * 3).grid(row=1, column=0)
den1 = Entry(frame, width=2)
den1.config(font=("Arial", 15), justify="center")
den1.grid(row=2, column=0)

oper = Entry(frame, width=2)
oper.config(font=("Arial", 15), justify="center")
oper.grid(row=1, column=1, padx=5)

num2 = Entry(frame, width=2)
num2.config(font=("Arial", 15), justify="center")
num2.grid(row=0, column=2)
Label(frame, text=chr(8212) * 3).grid(row=1, column=2)
den2 = Entry(frame, width=2)
den2.config(font=("Arial", 15), justify="center")
den2.grid(row=2, column=2)

btn = Button(frame, text='=', command=handler)
btn.config(font=("Arial", 15), justify="center", width=3)
btn.grid(row=1, column=3, padx=5)

res_int = Label(frame, text='   ', bg="light gray", width=2)
res_int.config(font=("Arial", 20), justify="center")
res_int.grid(row=1, column=4)

num3 = Label(frame, width=2, bg="light gray")
num3.config(font=("Arial", 15), justify="center")
num3.grid(row=0, column=5)
Label(frame, text=chr(8212) * 3).grid(row=1, column=5)
den3 = Label(frame, width=2, bg="light gray")
den3.config(font=("Arial", 15), justify="center")
den3.grid(row=2, column=5)

root.mainloop()