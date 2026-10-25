from tkinter import *
from opencage.geocoder import OpenCageGeocode
import webbrowser
import requests

lat = None
lon = None
map_url = None


def get_weather(lat, lon):
    try:
        response = requests.get(
            f"https://api.open-meteo.com/v1/forecast?latitude={lat}&longitude={lon}&current_weather=true")
        weather_data = response.json()
        current_weather = weather_data['current_weather']
        return current_weather
    except Exception as e:
        return f"Ошибка при получении погоды: {e}"


def show_weather():
    if lat is None or lon is None:
        mb_warning = Toplevel(window)
        mb_warning.title("Внимание")
        Label(mb_warning, text="Сначала введите город и нажмите 'Поиск'!", padx=20, pady=20).pack()
        return

    city_name = entry.get().strip().capitalize()
    current_weather = get_weather(lat, lon)

    weather_window = Toplevel(window)
    weather_window.title(f"Текущая погода — {city_name}")

    weather_window.resizable(False, False)

    if isinstance(current_weather, str):
        label_weather = Label(weather_window, text=current_weather)
    else:
        temperature = current_weather['temperature']
        windspeed = current_weather['windspeed']
        weather_text = f"Город: {city_name}\nТемпература: {temperature}°C\nСкорость ветра: {windspeed} км/ч"

        label_weather = Label(weather_window, text=weather_text, font=("Arial", 12), justify=CENTER)

    label_weather.pack(expand=True, padx=50, pady=20)


def get_coordinates(city, key):
    global lat, lon
    try:
        geocoder = OpenCageGeocode(key)
        results = geocoder.geocode(city, language='ru')

        if results:
            lat = round(results[0]['geometry']['lat'], 2)
            lon = round(results[0]['geometry']['lng'], 2)
            country = results[0]['components'].get('country', 'Страна не определена')
            region = results[0]['components'].get('state', 'Регион не определен')

            # Находим название местной валюты по указанному пути в JSON
            currency_info = results[0].get('annotations', {}).get('currency', {})
            currency_name = currency_info.get('name', 'Валюта не найдена')

            osm_url = f"https://www.openstreetmap.org/?mlat={lat}&mlon={lon}"

            return {
                "coordinates": f"Широта: {lat}, Долгота: {lon}\nСтрана: {country}\nРегион: {region}\nВалюта: {currency_name}",
                "map_url": osm_url
            }
        else:
            return {"coordinates": "Город не найден", "map_url": None}
    except Exception as e:
        return {"coordinates": f"Ошибка: {e}", "map_url": None}


def show_coordinates(event=None):
    city = entry.get()
    result = get_coordinates(city, key)
    label.config(text=result["coordinates"])
    global map_url
    map_url = result["map_url"]


def show_map():
    if map_url:
        webbrowser.open(map_url)


# Новая функция для очистки полей ввода и сброса результатов
def clear_all():
    global lat, lon, map_url
    lat = None
    lon = None
    map_url = None
    entry.delete(0, END)
    label.config(text="Введите город и нажмите Поиск")


window = Tk()
window.title("Поиск координат и погоды")
window.geometry("350x290")  # Немного увеличили высоту, чтобы уместить кнопку очистки

key = 'f7018087af3446f89e94b420f4fa49a7'

entry = Entry(window, width=30)
entry.pack(pady=10)
entry.bind("<Return>", show_coordinates)

button = Button(window, text="Поиск", command=show_coordinates)
button.pack(pady=3)

label = Label(window, text="Введите город и нажмите Поиск", justify=CENTER)
label.pack(pady=10)

map_button = Button(window, text="Показать карту", command=show_map)
map_button.pack(pady=3)

weather_button = Button(window, text="Показать погоду", command=show_weather, bg='#008CBA', fg='white')
weather_button.pack(pady=3)

# Добавлена кнопка очистки
clear_button = Button(window, text="Очистить", command=clear_all, bg='#f44336', fg='white')
clear_button.pack(pady=10)

root = window
window.mainloop()
