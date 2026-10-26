import os
import shutil
from tkinter import *
from tkinter import ttk, filedialog as fd, messagebox as mb
import requests
from bottle import response
import pyperclip
import json
import os


def show_history():
    if  not os.path.exists(history_file):
        mb.showinfo('History', 'История загрузок пуста')
        return
    history_window = Toplevel(root)
    history_window.title('История загрузок')
    files_lisbox = Listbox(history_window, width=50, height=20)
    files_lisbox.grid(row=0, column=0, padx=(10, 0), pady=10)
    links_lisbox = Listbox(history_window, width=50, height=20)
    links_lisbox.grid(row=0, column=1, padx=(0, 10), pady=10)
    with open(history_file, 'r') as f:
        history = json.load(f)
        for item in history:
            files_lisbox.insert(END, item['file_path'])
            links_lisbox.insert(END, item['download_link'])


def save_history(file_path, download_link):
    history = []
    if os.path.exists(history_file):
        with open(history_file, 'r') as f:
            history = json.load(f)
    history.append({'file_path': os.path.basename(file_path),
                    'download_link': download_link})
    with open(history_file, 'w') as f:
        json.dump(history, f, indent=4)


def uploud():
    try:
        filepath = fd.askopenfilename()
        if filepath:
            with open(filepath, 'r') as f:
                files = {'file': open(filepath, 'rb')}
                response = requests.post('https://store1.gofile.io/uploudFile',
                                     files=files)
                response.raise_for_status()
                if response.status_code == 200:
                    data = response.json()
                    download_link = data['data']['downloadPage']
                    entry.insert(0,download_link)
                    pyperclip.copy(download_link)
                    save_history(filepath, download_link)
                    mb.showinfo('Ссыка скопирована', f'Ссылка {download_link} в буфере обмена')
                else:
                    raise ValueError('Не удалось получить ссыку для скачивания')
    except ValueError as err:
        mb.showerror('Ошибка:', f'Произошла ошибка  {err}')
    except Exception as err:
        mb.showerror('Ошибка:', f'Произошла ошибка  {err}')

history_file = 'uploud_history.json'
root = Tk()
root.title('Облачное хранилище файлов')
root.geometry('400x120')

uploud_button = ttk.Button(text='загрузить файл', command=uploud)
uploud_button.pack()
entry = ttk.Entry(width=40)
entry.pack(pady=5)
historu_btn=ttk.Button(root, text='Показать историю', command=show_history())
historu_btn.pack()

root.mainloop()
