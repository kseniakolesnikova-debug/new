def scrabble(letters, word):
    # Создаем список из доступных букв, чтобы их можно было удалять
    available_letters = list(letters)

    for c in word:
        if c in available_letters:
            # Убираем одну использованную букву из набора
            available_letters.remove(c)
        else:
            # Если буквы нет или её лимит исчерпан
            return False

    return True
