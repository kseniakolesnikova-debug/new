
from tkinter import *
from tkinter import filedialog as fd
from PIL import Image
import stepic
from tkinter import messagebox as mb


def encode_text():
    # Кодирование текста в изображение
    image_path = file_path.get()
    text = text_to_encode.get()
    output_path = "encoded_image.png"

    try:
        image = Image.open(image_path)
        encoded_image = stepic.encode(image, text.encode())
        encoded_image.save(output_path)
        mb.showinfo("Успешно", "Текст успешно зашифрован в изображение!")
    except Exception as e:
        mb.showerror("Ошибка", str(e))


def decode_text():
    # Декодирование текста из изображения
    image_path = file_path.get()

    try:
        image = Image.open(image_path)
        decoded_text = stepic.decode(image)  # если результат уже является строкой
        print(decoded_text)
        mb.showinfo("Декодированный текст", decoded_text)
    except Exception as e:
        mb.showerror("Ошибка", str(e))


def open_file():
    # Открытие диалога выбора файла
    file = fd.askopenfilename(filetypes=[("Image files", "*.png;*.jpg;*.jpeg;*.bmp;*.gif")])
    file_path.set(file)


window = Tk()
window.title("Шифровка/Дешифровка в изображении")

# Путь к файлу
file_path = StringVar()
Label(window, text="Путь к изображению:").pack()
Entry(window, textvariable=file_path, width=50).pack()
Button(window, text="Выбрать файл", command=open_file).pack()

# Текст для шифрования
text_to_encode = StringVar()
Label(window, text="Текст для шифрования:").pack()
Entry(window, textvariable=text_to_encode, width=50).pack()

# Кнопки для шифрования и дешифрования
Button(window, text="Зашифровать текст", command=encode_text).pack()
Button(window, text="Расшифровать текст", command=decode_text).pack()

window.mainloop()
