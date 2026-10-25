import json
#
# d = {'black': 'черный',
#      'white': 'белый'
#      }

with open('dict.json','r', encoding='utf-8') as file:

    d = json.load(file)
while True:
        
    word = input('ВВедите слово для перевода: ')

    if word in d:
        print(f'{word} - {d[word]}')
    else:
        translate = input(f'Введите перевод слова {word}')
#
# with open('dict.json','w', encoding='utf-8') as file:
#     json.dump(d, file, indent=4)