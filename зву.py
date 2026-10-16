
from tkinter import *
from tkinter import filedialog as fd
from tkinter import messagebox as mb
from tkinter.font import Font, families
from tkinter import simpledialog as sd
from transliterate import translit
from googletrans import Translator

def delete():
    text.delete(1.0, END)

def insert():
    file = fd.askopenfilename()
    if file:
        with open(file, 'r') as f:
            content = f.read()
        text.delete(1.0, END)
        text.insert(1.0, content)

def save():
    file = fd.asksaveasfilename(
        filetypes=(("TXT files", "*.txt"),
                   ("HTML files", "*.html;*.htm"),
                   ("All files", "*.*")))
    if file:
        with open(file, 'w') as f:
            content = text.get(1.0, END)
            f.write(content)

def transliterate_text():
    source_text = text.get(1.0, END)
    transliterated_text = translit(source_text, 'ru', reversed=True)
    text.delete(1.0, END)
    text.insert(1.0, transliterated_text)

def translate_text():
    source_text = text.get(1.0, END)
    translator = Translator()
    translated_text = translator.translate(source_text, src='ru', dest='en').text
    text.delete(1.0, END)
    text.insert(1.0, translated_text)

def change_font():
    font_family = sd.askstring("Шрифт", "Введите название шрифта:")
    font_size = sd.askstring("Размер шрифта", "Введите размер шрифта:")
    if font_family and font_size:
        try:
            new_font = Font(family=font_family, size=int(font_size))
            text.configure(font=new_font)
        except Exception as e:
            mb.showerror("Ошибка", f"Произошла ошибка: {e}")

window = Tk()
window.title("Текстовый редактор")

text = Text(window, width=50, height=15)
text.pack(side=LEFT, fill=BOTH, expand=True)
scroll = Scrollbar(window, command=text.yview)
scroll.pack(side=LEFT, fill=Y)
text.config(yscrollcommand=scroll.set)

menu_bar = Menu(window)
window.config(menu=menu_bar)

file_menu = Menu(menu_bar, tearoff=0)
menu_bar.add_cascade(label="Файл", menu=file_menu)
file_menu.add_command(label="Открыть", command=insert)
file_menu.add_command(label="Сохранить", command=save)
file_menu.add_separator()
file_menu.add_command(label="Выход", command=window.quit)

process_menu = Menu(menu_bar, tearoff=0)
menu_bar.add_cascade(label="Обработка", menu=process_menu)
process_menu.add_command(label="Транслитерация", command=transliterate_text)
process_menu.add_command(label="Перевод на английский", command=translate_text)
process_menu.add_separator()
process_menu.add_command(label="Изменить шрифт и размер", command=change_font)

window.mainloop()
