import sys
from tkinter import *
from tkinter import filedialog as fd
from tkinter import messagebox as mb
from PIL import Image, ImageTk, ImageGrab

# Глобальные переменные для настроек кисти
pen_color = "red"
pen_size = 5  # Начальная толщина пера по умолчанию


# Функция для рисования на холсте
def draw(event):
    x, y = event.x, event.y
    # Используем глобальную переменную pen_size для расчета радиуса точки
    canvas.create_oval(
        x - pen_size // 2, y - pen_size // 2,
        x + pen_size // 2, y + pen_size // 2,
        fill=pen_color, outline=pen_color
    )


# Функция изменения цвета кисти через палитру
def change_color(color):
    global pen_color
    pen_color = color


# Функция для обновления толщины пера с обработкой исключения ValueError
def set_pen_size():
    global pen_size
    try:
        # Пытаемся получить значение из поля ввода и преобразовать в целое число
        size = int(size_entry.get())
        if size > 0:
            pen_size = size
        else:
            mb.showwarning("Предупреждение", "Толщина должна быть больше 0!")
    except ValueError:
        # Если введено не целое число (буквы, пустая строка, дроби)
        mb.showerror("Ошибка ввода", "Пожалуйста, введите корректное целое число!")


# Метод для полной очистки холста
def delete():
    canvas.delete("all")


# Загрузка изображения с обработкой исключений
def load_image():
    try:
        file_path = fd.askopenfilename(filetypes=[('Image files', '*.png;*.jpg;*.jpeg;*.bmp;*.gif')])
        if file_path:
            image = Image.open(file_path)
            image = image.resize((600, 400))
            image_tk = ImageTk.PhotoImage(image)
            canvas.create_image(0, 0, anchor=NW, image=image_tk)
            canvas.image = image_tk
    except Exception as e:
        mb.showerror("Ошибка", f"Не удалось загрузить: {e}")


# Сохранение холста с обработкой исключений
def save_canvas():
    try:
        file_path = fd.asksaveasfilename(defaultextension='.png', filetypes=[('PNG files', '*.png')])
        if file_path:
            x = window.winfo_rootx() + canvas.winfo_x()
            y = window.winfo_rooty() + canvas.winfo_y()
            x1 = x + canvas.winfo_width()
            y1 = y + canvas.winfo_height()

            ImageGrab.grab().crop((x, y, x1, y1)).save(file_path)
            mb.showinfo("Сохранено!", "Изображение успешно сохранено в PNG файл!")
    except Exception as e:
        mb.showerror("Ошибка", f"Не удалось сохранить: {e}")


# Закрытие приложения
def quit_app():
    window.destroy()


# Настройка главного окна
window = Tk()
window.title("Графический редактор")
window.geometry("600x470")
window.resizable(False, False)

menu_bar = Menu(window)
window.config(menu=menu_bar)

file_menu = Menu(menu_bar, tearoff=0)
menu_bar.add_cascade(label="Файл", menu=file_menu)
file_menu.add_command(label="Загрузить изображение", command=load_image)
file_menu.add_command(label="Сохранить холст", command=save_canvas)
file_menu.add_command(label="Очистить", command=delete)
file_menu.add_separator()
file_menu.add_command(label="Выход", command=quit_app)

canvas = Canvas(window, width=600, height=400, bg="white")
canvas.pack()
canvas.bind("<B1-Motion>", draw)

controls_frame = Frame(window)
controls_frame.pack(side=BOTTOM, fill=X, padx=5, pady=5)

colors = ["red", "green", "blue", "black", "yellow", "orange", "purple"]
for color in colors:
    lbl = Label(controls_frame, text="", bg=color, width=4, height=2, relief=RAISED, cursor="hand2")
    lbl.pack(side=LEFT, padx=2)
    lbl.bind("<Button-1>", lambda event, c=color: change_color(c))

# Элементы изменения толщины кисти (размещаются справа внутри панели управления)
size_label = Label(controls_frame, text="Толщина:")
size_label.pack(side=LEFT, padx=(20, 5))

size_entry = Entry(controls_frame, width=5)
size_entry.insert(0, str(pen_size))  # Устанавливаем начальное значение в поле
size_entry.pack(side=LEFT, padx=5)

size_button = Button(controls_frame, text="Применить", command=set_pen_size)
size_button.pack(side=LEFT, padx=5)

window.mainloop()
