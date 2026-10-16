import math

result = {}

# Открываем файл. Обратите внимание: метод .strip() убирает переносы строк
for line in open('ice-cream.csv', 'r', encoding='utf-8'):
    # Разбиваем строку по точке с запятой
    ls = line.strip().split(';')

    # Считаем уникальные топпинги в рамках одного заказа (строки)
    for topping in set(ls):
        # Пропускаем пустые строки или заголовок (если он начинается на 't')
        if not topping or topping.startswith('t'):
            continue

        # Увеличиваем счетчик для текущего топпинга
        result[topping] = result.get(topping, 0) + 1

# Инициализируем переменные для поиска максимума и минимума
mx = 0
name_max = ''
mn = math.inf
name_min = ''

# Перебираем пары (название_топпинга, количество)
for topping, count_value in result.items():
    # Ищем самый популярный топпинг
    if count_value > mx:
        mx = count_value
        name_max = topping

    # Ищем самый непопулярный топпинг
    if count_value < mn:
        mn = count_value
        name_min = topping
mx = max(result.items(), key = lambda x: x[1])[0]
mn = min(result.items(), key = lambda x: x[1])[0]
# Выводим названия самого популярного и самого редкого топпинга
print(f"Самый популярный: {name_max} (встречается {mx} раз)")
print(f"Самый редкий: {name_min} (встречается {mn} раз)")
