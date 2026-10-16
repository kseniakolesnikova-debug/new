with open('tetx.txt','r', encoding='utf-8') as f:
    s = f.read()
    key = input('Введите ключ шифрования: ')
    secret = ''
    for c in s:
        code = ord(c) + int(key)
        symboll = chr(code)
        secret += symboll
print('Текс зашифрован')

with open('code.txt','w', encoding='utf-8') as f:
    f.write(secret)
print('Файл "code.txt" для отправки сформирован')
