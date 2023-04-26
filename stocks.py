from tkinter import ttk, StringVar
import tkinter as tk
from datetime import datetime, timedelta, date
from dateutil.relativedelta import *
from dateutil.relativedelta import relativedelta
import json


def load_json() -> dict:
        with open('stocks.json') as fp:
            return json.load(fp)
        

def save_json(json_file: dict) -> None:
        with open('stocks.json', 'w', encoding='utf-8') as fp:
            json.dump(json_file, fp, indent=4, ensure_ascii=False)


def window():
    

    def entryEdited(event):
        try:
            nonlocal input_money
            input_money = float(event.get())
            label['text'] = f'Ввод: {input_money}'
            remove_btn['text'] = f'Вычесть {input_money}'
        except ValueError:
            label['text'] = 'Ввод:'
            remove_btn['text'] = 'Вычесть '

    
    def calc_weeks(date_start, date):
        nonlocal weeks
        weeks = relativedelta(date, date_start)
        temp_weeks = datetime.now()
        weeks = temp_weeks - (temp_weeks - weeks)
        weeks = weeks.days // 7
        print(weeks)
    

    def calc_money(json_file: dict) -> None:
        nonlocal money
        nonlocal input_money
        nonlocal money_log
        money = input_money
        money += json_file['money']
        money = round(money, 3)
        json_file['money'] = money
        json_file['date'] = f'{date.year}.{date.month}.{date.day}'
        money_log['add'] += input_money

    
    def save(json_file: dict, func) -> None:
        func(json_file)
        label_from_json['text'] = f"Из файла: {json_file['money']}"
        save_json(json_file)
        print(json_file)

    
    def remove(json_file: dict) -> None:
        if json_file['money'] <= input_money: json_file['money'] = 0.0
        else: json_file['money'] -= input_money
        money_log['remove'] += input_money

    
    def calc_percent(json_file, date_start):
        nonlocal money
        nonlocal weeks
        if weeks > 0:
            for _ in range(weeks): money += (money * 0.1)
            money = round(money, 3)
            date_start += relativedelta(weeks=+weeks)
            json_file['date_start'] = f'{date_start.year}.{date_start.month}.{date_start.day}'
            json_file['money'] = money
        label_calc_perc['text'] = f'Процент за {weeks} недель: {round(money * 0.1 * weeks, 3)}'
        label_from_json['text'] = f"Из файла: {json_file['money']}"
        print(json_file)
        save_json(json_file)


    def report():
        with open('report.txt', 'a+', encoding='utf-8') as fp:
            fp.writelines(f'Дата: {datetime.strptime(str(datetime.now()), "%Y-%m-%d %H:%M:%S.%f")} | +: {money_log["add"]} | -: {money_log["remove"]}\n')
        root.destroy()

    
    root = tk.Tk()
    root.title('Подсчет процентов')
    root.geometry(f'300x300+{int(root.winfo_screenwidth() / 2) - int(300 / 2)}+{int(root.winfo_screenheight() / 2) - int(300 / 2)}')

    money = 0.0
    input_money = 0.0
    weeks = 0
    money_log = {'add': 0.0, 'remove': 0.0}
    date = datetime.now()
    date = datetime(year=date.year, month=date.month, day=date.day)
    date_start = date

    json_file = {}
    try:
        json_file = load_json()
        money = json_file['money']
    except FileNotFoundError:
        json_file = {'date_start': f'{date.year}.{date.month}.{date.day}',
                     'date': f'{date.year}.{date.month}.{date.day}',
                     'money': money}
    date_start = datetime(*map(int, json_file['date_start'].split('.')))
    calc_weeks(date_start, date)
         

    sv = StringVar()
    sv.trace('w', lambda name, index, mode, sv=sv: entryEdited(sv))

    entry = tk.Entry(root, textvariable=sv)
    entry.pack()

    save_btn = ttk.Button(command=lambda: save(json_file, calc_money))
    save_btn['text'] = 'Сохранить'
    save_btn.pack()

    remove_btn = ttk.Button(command=lambda: save(json_file, remove))
    remove_btn['text'] = 'Вычесть '
    remove_btn.pack()

    label = tk.Label()
    label['text'] = 'Ввод:'
    label.pack()

    label_from_json = tk.Label()
    label_from_json['text'] = f"Из файла: {json_file['money']}"
    label_from_json.pack()

    label_calc_perc = tk.Label()
    label_calc_perc['text'] = ''
    label_calc_perc.pack()

    root.protocol('WM_DELETE_WINDOW', report)


    calc_percent(json_file, date_start)

    root.mainloop()

if __name__ == '__main__':
    window() 