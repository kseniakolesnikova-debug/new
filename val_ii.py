from tkinter import *
from tkinter import messagebox as mb
from tkinter import ttk
import requests

def update_base1_label(event):
    code = base1_combobox.get()
    if code in currencies:
        base1_label.config(text=currencies[code])

def update_base2_label(event):
    code = base2_combobox.get()
    if code in currencies:
        base2_label.config(text=currencies[code])

def update_target_label(event):
    code = target_combobox.get()
    if code in currencies:
        target_label.config(text=currencies[code])

def exchange():
    base1_code = base1_combobox.get().strip()
    base2_code = base2_combobox.get().strip()
    target_code = target_combobox.get().strip()

    if not base1_code or not base2_code or not target_code:
        mb.showwarning('Внимание', 'Выберите обе базовые и целевую валюту')
        return

    result_messages = []

    # Запрос для первой базовой валюты
    try:

        res1 = requests.get(f'https://open.er-api.com/v6/latest/{base1_code}')

        res1.raise_for_status()
        data1 = res1.json()
        rates1 = data1.get('rates', {})

        if target_code in rates1:
            rate1 = rates1[target_code]
            result_messages.append(f'1 {currencies[base1_code]} = {rate1:.2f} {currencies[target_code]}')
        else:
            result_messages.append(f'Валюта {target_code} не найдена для базовой {base1_code}')
    except Exception as er:
        result_messages.append(f'Ошибка запроса для {base1_code}: {er}')

    # Запрос для второй базовой валюты
    try:
        res2 = requests.get(f'https://open.er-api.com/v6/latest/{base2_code}')
        res2.raise_for_status()
        data2 = res2.json()
        rates2 = data2.get('rates', {})

        if target_code in rates2:
            rate2 = rates2[target_code]
            result_messages.append(f'1 {currencies[base2_code]} = {rate2:.2f} {currencies[target_code]}')
        else:
            result_messages.append(f'Валюта {target_code} не найдена для базовой {base2_code}')
    except Exception as er:
        result_messages.append(f'Ошибка запроса для {base2_code}: {er}')

    # Вывод результатов
    mb.showinfo('Курсы обмена', '\n'.join(result_messages))

currencies = {
    'EUR': 'Евро',
    'USD': 'Доллар США',
    'JPY': 'Японская йена',
    'GBP': 'Фунт стерлингов',
    'AUD': 'Австралийский доллар',
    'CAD': 'Канадский доллар',
    'CHF': 'Швейцарский франк',
    'CNY': 'Китайский юань',
    'RUB': 'Российский рубль',
    'KZT': 'Казахстанский тенге',
    'UZS': 'Узбекский сум'
}

root = Tk()
root.title('Конвертация валют (Две базовые)')
root.geometry('360x320')

Label(root, text='Первая базовая валюта').pack(pady=(10, 0))
base1_combobox = ttk.Combobox(root, values=list(currencies.keys()), state="readonly")
base1_combobox.pack(pady=3, padx=10)
base1_combobox.bind('<<ComboboxSelected>>', update_base1_label)

base1_label = ttk.Label(root, text="")
base1_label.pack()

Label(root, text='Вторая базовая валюта').pack(pady=(10, 0))
base2_combobox = ttk.Combobox(root, values=list(currencies.keys()), state="readonly")
base2_combobox.pack(pady=3, padx=10)
base2_combobox.bind('<<ComboboxSelected>>', update_base2_label)

base2_label = ttk.Label(root, text="")
base2_label.pack()

Label(root, text='Целевая валюта').pack(pady=(10, 0))
target_combobox = ttk.Combobox(root, values=list(currencies.keys()), state="readonly")
target_combobox.pack(pady=3, padx=10)
target_combobox.bind('<<ComboboxSelected>>', update_target_label)

target_label = ttk.Label(root, text="")
target_label.pack()

exchange_button = Button(root, text='Получить курсы обмена', command=exchange, bg='#4CAF50', fg='white',
                         font=('Arial', 10, 'bold'))
exchange_button.pack(pady=20)

root.mainloop()
