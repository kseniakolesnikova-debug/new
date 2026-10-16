import requests
# from tkinter import *
# from tkinter import ttk
# from tkinter import messagebox as mb

from bs4 import BeautifulSoup

""""https:// www.hse.ru/staff/allat"""
def get_mail(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    name = soup.find('h1', class_='person-caption').text
    pos = soup.find('span', class_='person-appointment-title').text[:-2]

    lang = soup.find('dt', class_='b').find_all('dd')

    res = (name, pos)
    print(res)
    for l in lang:
        print(l.text)

#
# get_mail('https://www.hse.ru/staff/allat')
# get_mail('https://www.hse.ru/org/persons/135897')
# get_mail('https://www.hse.ru/org/persons/63890353')


pul_adress = (
    'https://www.hse.ru/staff/allat',
    'https://www.hse.ru/org/persons/135897',
    'https://www.hse.ru/org/persons/63890353'
)

endpoints= ('135897', '63890353')
for adress in pul_adress:
    get_mail(adress)
