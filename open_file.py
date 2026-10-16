# file = open('tetx.txt','r', encoding='utf-8')
# # s = file.read()
# # s = file.readline()
# s = file.readlines()
# print(s)
# file.close()
#
# for i in open('tetx.txt','r', encoding='utf-8'):
#     print(i.rstrip())

with open('tetx.txt','r', encoding='utf-8') as file:
    ls = file.read().title().split()
ls.sort()
print(ls)

with open('tetx1.txt','w', encoding='utf-8') as file:
    for n, f in enumerate(ls, 1):
        file.write(f'{n}. {f}\n')