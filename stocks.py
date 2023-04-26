from tkinter import ttk, StringVar
import tkinter as tk
from datetime import datetime, timedelta, date
from dateutil.relativedelta import *
from dateutil.relativedelta import relativedelta
import json


def load_json():
        with open('stocks.json') as fp:
            return json.load(fp)
        

def save_json(json_file: dict) -> None:
        with open('stocks.json', 'w', encoding='utf-8') as fp:
            json.dump(json_file, fp, indent=4, ensure_ascii=False)


def window():
    root = tk.Tk()
    root.title('Stocks')
    root.geometry('200x200')

    money = 0
    date = datetime.now()
    date = datetime(year=date.year, month=date.month, day=date.day)

    json_file = {}
    try:
        json_file = load_json()
        money = json_file['money']
    except FileNotFoundError:
        json_file = {'date_start': f'{date.year}.{date.month}.{date.day}',
                     'date': f'{date.year}.{date.month}.{date.day}',
                     'money': money}
    
    def entryEdited(event):
        try:
            nonlocal money
            money = float(int(event.get()))
            label['text'] = f'Ввод: {money}'
        except ValueError:
            label['text'] = 'Ввод:'

    
    def save(json_file: dict) -> None:
        nonlocal money
        money += json_file['money']
        date_start = datetime(*map(int, json_file['date_start'].split('.')))
        weeks = relativedelta(date, date_start)
        weeks = weeks.days // 7
        print(weeks)
        if weeks > 0:
            for _ in range(weeks):
                money += (money * 0.1)
            date_start += relativedelta(weeks=+weeks)
            json_file['date_start'] = f'{date_start.year}.{date_start.month}.{date_start.day}'
        json_file['money'] = money
        json_file['date'] = f'{date.year}.{date.month}.{date.day}'
        save_json(json_file)
        print(json_file)


    sv = StringVar()
    sv.trace('w', lambda name, index, mode, sv=sv: entryEdited(sv))

    entry = tk.Entry(root, textvariable=sv)
    entry.pack()

    ok_btn = ttk.Button(command=lambda: save(json_file))
    ok_btn['text'] = 'Сохранить'
    ok_btn.pack()

    label = tk.Label()
    label.pack()

    label_from_json = tk.Label()
    label_from_json['text'] = f"Из файла: {json_file['money']}"
    label_from_json.pack()

    root.mainloop()

if __name__ == '__main__':
    window() 