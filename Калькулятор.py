# Задание
#Доработайте проект калькулятора. Добавьте кнопку для умножения трех чисел.
from tkinter import *
from tkinter import messagebox as mb


def multi():
    s1 = e1.get()
    if not s1.lstrip('-').isdigit():
        mb.showerror("Ошибка", "В первое поле должно быть введено число")
        return  # Возвращаемся из функции, если ввод некорректен
    s2 = e2.get()
    if not s2.lstrip('-').isdigit():
        mb.showerror("Ошибка", "Во второе поле должно быть введено число")
        return  # Возвращаемся из функции, если ввод некорректен
    s3 = e3.get()
    if not s3.lstrip('-').isdigit():
        mb.showerror("Ошибка", "В третье поле должно быть введено число")
        return  # Возвращаемся из функции, если ввод некорректен

    slag1 = int(s1)
    slag2 = int(s2)
    slag3 = int(s3)
    mult = slag1 * slag2 * slag3
    # Исправлен знак "+" на " * " для корректного отображения операции умножения
    m1['text'] = f"{s1} * {s2} * {s3} = {str(mult)}"

    answer = mb.askretrycancel(title="Вопрос", message="Умножить еще три числа?")
    if answer:
        e1.delete(0, END)
        e2.delete(0, END)
        e3.delete(0, END)
        m1['text'] = ""
    else:
        window.destroy()


def summ():
    s1 = e1.get()
    if not s1.lstrip('-').isdigit():
        mb.showerror("Ошибка", "В первое поле должно быть введено число")
        return  # Возвращаемся из функции, если ввод некорректен
    s2 = e2.get()
    if not s2.lstrip('-').isdigit():
        mb.showerror("Ошибка", "Во второе поле должно быть введено число")
        return  # Возвращаемся из функции, если ввод некорректен
    s3 = e3.get()
    if not s3.lstrip('-').isdigit():
        mb.showerror("Ошибка", "В третье поле должно быть введено число")
        return  # Возвращаемся из функции, если ввод некорректен

    slag1 = int(s1)
    slag2 = int(s2)
    slag3 = int(s3)
    summa = slag1 + slag2 + slag3
    m1['text'] = f"{s1} + {s2} + {s3} = {str(summa)}"

    answer = mb.askretrycancel(title="Вопрос", message="Сложить еще три числа?")
    if answer:
        e1.delete(0, END)
        e2.delete(0, END)
        e3.delete(0, END)
        m1['text'] = ""
    else:
        window.destroy()


window = Tk()
window.title("Калькулятор")

# Изменен текст приветствия, так как теперь калькулятор умеет и умножать
m = Label(height=3, text="Введите три числа и нажмите на кнопку для вычисления")
m.pack()

e1 = Entry()
e1.pack()
e2 = Entry()
e2.pack()
e3 = Entry()
e3.pack()

# Кнопка для сложения
b_sum = Button(text="Сложить три числа", command=summ)
b_sum.pack()

# Новая кнопка для умножения, которая вызывает функцию multi
b_multi = Button(text="Умножить три числа", command=multi)
b_multi.pack()

m1 = Label(height=3)
m1.pack()

window.mainloop()

