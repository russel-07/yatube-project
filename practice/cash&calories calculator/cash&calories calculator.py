import datetime as dt

class Record:
    def __init__(self, amount, comment, date=dt.datetime.now().strftime('%d.%m.%Y')):
        self.amount = amount
        self.comment = comment
        self.date = dt.datetime.strptime(date, '%d.%m.%Y').date()


class Calculator:
    def __init__(self, limit):
        self.limit = limit
        self.records = []
    
    def add_record(self, record):
        self.records.append(record)
 
    def get_today_stats(self):
        today_stats = 0
        today = dt.date.today()
        for rec in self.records:
            if rec.date == today:
                today_stats += rec.amount
        return today_stats
    
    def get_week_stats(self):
        week_stats = 0
        today = dt.date.today()
        toweek = today - dt.timedelta(weeks=1)
        for rec in self.records:
            if toweek < rec.date <= today :
                week_stats += rec.amount
        return week_stats


class CaloriesCalculator(Calculator):
    def __init__(self, limit):
        super().__init__(limit)
    
    def get_calories_remained(self):
        today_stats = self.get_today_stats()
        if today_stats < self.limit:
            calories_balance = self.limit - today_stats
            return (f'Сегодня можно съесть что-нибудь ещё, но с общей калорийностью не более {calories_balance} кКал')
        else:
            return ('Хватит есть!')


class CashCalculator(Calculator):
    RUB_RATE = 1.00
    USD_RATE = 70.10
    EUR_RATE = 75.10

    def __init__(self, limit):
        super().__init__(limit)
    
    def get_today_cash_remained(self, currency = 'rub'):
        currencies = {
            'rub': ('руб', self.RUB_RATE),
            'usd': ('USD', self.USD_RATE),
            'eur': ('Euro', self.EUR_RATE)
        }
        if currency not in currencies:
             return 'Неправильно указана валюта!'
        currency_name, currency_rate = currencies[currency]
        today_stats = self.get_today_stats()
        cash_balance = round((self.limit - today_stats)/currency_rate, 2)
        if cash_balance > 0:
            return(f'На сегодня осталось {cash_balance} {currency_name}')
        elif cash_balance == 0:
            return('Денег нет, держись')
        else:
            cash_balance *= -1
            return(f'Денег нет, держись: твой долг - {cash_balance} {currencies[currency][0]}')


calories_calculator = CaloriesCalculator(50)

calories_calculator.add_record(Record(amount = 1, comment = 'raz',date = '19.01.2023'))
calories_calculator.add_record(Record(amount = 2, comment = 'dva', date = '20.01.2023'))
calories_calculator.add_record(Record(amount = 3, comment = 'tri', date = '21.01.2023'))
calories_calculator.add_record(Record(amount = 4, comment = 'che', date = '22.01.2023'))
calories_calculator.add_record(Record(amount = 5, comment = 'pya', date = '23.01.2023'))
calories_calculator.add_record(Record(amount = 6, comment = 'she', date = '24.01.2023'))
calories_calculator.add_record(Record(amount = 7, comment = 'sem', date = '25.01.2023'))
calories_calculator.add_record(Record(amount = 8, comment = 'vos', date = '26.01.2023'))
calories_calculator.add_record(Record(amount = 9, comment = 'dev'))
calories_calculator.add_record(Record(amount = 10, comment = 'dec', date = '27.01.2023'))
calories_calculator.add_record(Record(amount = 11, comment = 'odi'))
calories_calculator.add_record(Record(amount = 12, comment = 'dve', date = '28.01.2023'))
calories_calculator.add_record(Record(amount = 13, comment = 'ttr', date = '29.01.2023'))


cash_calculator = CashCalculator(3000)

cash_calculator.add_record(Record(amount = 100, comment = 'raz', date = '19.01.2023'))
cash_calculator.add_record(Record(amount = 200, comment = 'dva', date = '20.01.2023'))
cash_calculator.add_record(Record(amount = 300, comment = 'tri', date = '21.01.2023'))
cash_calculator.add_record(Record(amount = 400, comment = 'che', date = '22.01.2023'))
cash_calculator.add_record(Record(amount = 500, comment = 'pya', date = '23.01.2023'))
cash_calculator.add_record(Record(amount = 600, comment = 'she', date = '24.01.2023'))
cash_calculator.add_record(Record(amount = 700, comment = 'sem', date = '25.01.2023'))
cash_calculator.add_record(Record(amount = 800, comment = 'vos', date = '26.01.2023'))
cash_calculator.add_record(Record(amount = 900, comment = 'dev'))
cash_calculator.add_record(Record(amount = 1000, comment = 'dec', date = '27.01.2023'))
cash_calculator.add_record(Record(amount = 1100, comment = 'odi'))
cash_calculator.add_record(Record(amount = 1200, comment = 'dve', date = '28.01.2023'))
cash_calculator.add_record(Record(amount = 1300, comment = 'ttr', date = '29.01.2023'))

print('')

print(calories_calculator.get_calories_remained())

print('')

print(cash_calculator.get_today_cash_remained('rub'))

print('')
