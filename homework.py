from __future__ import annotations  # для того, чтобы обработать без ошибок
# передачу инстанса записи record класса Record в ф-цию add_record
import datetime as dt
from typing import List


class Calculator:
    def __init__(self, limit: float):
        self.limit = limit
        self.records: List[Record] = list()

    def add_record(self, record: Record) -> None:
        self.records.append(record)

    def get_today_stats(self):
        today = dt.datetime.now().date()
        sum = 0
        for record in self.records:
            if record.date == today:
                sum += record.amount
        return sum

    def get_week_stats(self):
        today = dt.datetime.now().date()
        sum = 0
        week_before_day = dt.datetime.now().date() - dt.timedelta(days=6)
        for record in self.records:
            if record.date >= week_before_day and record.date <= today:
                sum += record.amount
        return sum


class CaloriesCalculator(Calculator):

    def get_calories_remained(self):
        remainder = self.limit - self.get_today_stats()  # остаток калорий
        if remainder > 0 and remainder < self.limit:
            return f'Сегодня можно съесть что-нибудь ещё, \
                    но с общей калорийностью не более {remainder} кКал'
        else:
            return 'Хватит есть!'


class CashCalculator(Calculator):
    USD_RATE = 74.77
    EURO_RATE = 80.65

    def get_today_cash_remained(self, currency: str):
        currency_dict = {'rub': 'руб', 'eur': 'Euro', 'usd': 'USD'}
        remainder = self.limit - self.get_today_stats()  # остаток в рублях
        if currency == 'rub':
            remainder_currency = remainder
        elif currency == 'eur':
            remainder_currency = round(remainder / self.EURO_RATE, 2)
        elif currency == 'usd':
            remainder_currency = round(remainder / self.USD_RATE, 2)
        if remainder > 0 and remainder < self.limit:
            return f'На сегодня осталось {remainder_currency}  \
                    {currency_dict[currency]}'
        elif remainder < 0:
            return f'Денег нет, держись: твой долг - {remainder_currency * (-1)} \
                    {currency_dict[currency]}'
        else:
            return 'Денег нет, держись'


class Record:
    def __init__(self, amount: float, comment: str,
                 date: str = dt.datetime.now().strftime('%d.%m.%Y')):
        self.amount = amount
        self.comment = comment
        self.date = dt.datetime.strptime(str(date), '%d.%m.%Y').date()
