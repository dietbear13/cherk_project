import calendar
import datetime

import pymorphy2


def get_myrg():
    # Ежемесячно меняем прогнозы (trafic_forecast) на акутальные!
    # И меняем данные за прошлые года в текстах отчётов на 73-74, 91-92, 109-110 строках

    trafic_forecast = '113861'
    trafic_forecast_2 = '44792'
    trafic_forecast_3 = '35568'

    trafic_data = input(
        'Введи 3 числа: фактический трафик Пет,Пав и КЦ, можно с пробелами в любых местах:\n150 000, 84000,215 000\n\n' \
        'На выходе получаем прогноз на конец месяца по сегодняшнему дню.\n\nВводи числа: ')

    trafic_data_no_spaces = trafic_data.replace(" ", "")
    splitted_trafic_list = trafic_data_no_spaces.split(",")

    trafic_fact = int(splitted_trafic_list[0])
    trafic_fact_2 = int(splitted_trafic_list[1])
    trafic_fact_3 = int(splitted_trafic_list[2])

    date_today_number = int(datetime.date.today().strftime("%d"))
    last_month_number = date_today_number - 1
    percent_of_expectation = float(f"{(int(trafic_fact) / int(trafic_forecast) * 100)}")
    percent_of_expectation2 = float(f"{(int(trafic_fact_2) / int(trafic_forecast_2) * 100)}")
    percent_of_expectation3 = float(f"{(int(trafic_fact_3) / int(trafic_forecast_3) * 100)}")
    now = datetime.datetime.now()
    day_without_today = calendar.monthrange(now.year, now.month)[1]

    if date_today_number != 1:
        expectation = int(trafic_fact) * int(day_without_today) / (date_today_number - 1)
        expectation2 = int(trafic_fact_2) * int(day_without_today) / (date_today_number - 1)
        expectation3 = int(trafic_fact_3) * int(day_without_today) / (date_today_number - 1)

        mouth_number = str(datetime.date.today().strftime("%m"))

        month_table = {
            '01': 'январь',
            '02': 'февраль',
            '03': 'март',
            '04': 'апрель',
            '05': 'май',
            '06': 'июнь',
            '07': 'юиль',
            '08': 'август',
            '09': 'сентябрь',
            '10': 'октябрь',
            '11': 'ноябрь',
            '12': 'декабрь',
        }

        ### ПРОВЕРЯЕМ ЕСТЬ ЛИ ТЕКУЩИЙ МЕСЯЦ В СЛОВАРЕ
        if mouth_number in month_table:
            month = month_table[mouth_number]

        if mouth_number in month_table:
            month = month_table[mouth_number]

        ### СТАВИМ МЕСЯЦ В 3 ПАДЕЖА
        morph = pymorphy2.MorphAnalyzer()
        p = morph.parse(month)[0]
        month_nomn = p.inflect({"nomn"}).word
        month_gent = p.inflect({"gent"}).word
        month_loc2 = p.inflect({"loc2"}).word

        report_petel = '''
непересчитанный прогноз естественного трафика на {month_nomn} — {trafic_forecast}. 
выполнено на {date} {month_gent} — {trafic_fact} ({percent}% от непересчитанного реалистичного). 
В {month_loc2} 2019 — 112 427, {month_loc2} 2020 — 198 725, 
{month_loc2} 2021 — 213 171, {month_loc2} 2022 — 152 356,  
ожидание на {month_nomn} — {total} ({total_percent}% от непересчитанного естественного прогноза).
        '''.format(
            trafic_forecast=trafic_forecast,
            date=date_today_number,
            trafic_fact=trafic_fact,
            percent=round(percent_of_expectation, 1),
            total=round(expectation),
            total_percent=round(int(round(expectation)) / int(trafic_forecast) * 100, 1),
            month_nomn=month_nomn,
            month_gent=month_gent,
            month_loc2=month_loc2
        )

        report_pava = '''
непересчитанный прогноз естественного трафика на {month_nomn} — {trafic_forecast_2}. 
выполнено на {date} {month_gent} — {trafic_fact_2} ({percent}% от непересчитанного реалистичного). 
В {month_loc2} 2019 — 497, {month_loc2} 2020 — 4 497, 
{month_loc2} 2021 — 8 282, {month_loc2} 2022 — 49 596, 
ожидание на {month_nomn} — {total} ({total_percent}% от непересчитанного естественного прогноза).
        '''.format(
            trafic_forecast_2=trafic_forecast_2,
            date=date_today_number,
            trafic_fact_2=trafic_fact_2,
            percent=round(percent_of_expectation2, 1),
            total=round(expectation2),
            total_percent=round(int(round(expectation2)) / int(trafic_forecast_2) * 100, 1),
            month_nomn=month_nomn,
            month_gent=month_gent,
            month_loc2=month_loc2
        )

        report_kurinoe_tsarstvo = '''
непересчитанный прогноз естественного трафика на {month_nomn} — {trafic_forecast_3}. 
выполнено на {date} {month_gent} — {traficFact} ({percent}% от непересчитанного реалистичного). 
В {month_loc2} 2019 — 1 148, {month_loc2} 2020 — 13 924, 
{month_loc2} 2021 — 38 847, {month_loc2} 2022 — 49 684,
ожидание на {month_nomn} — {total} ({total_percent}% от непересчитанного естественного прогноза).
        '''.format(
            trafic_forecast_3=trafic_forecast_3,
            date=date_today_number,
            traficFact=trafic_fact_3,
            percent=round(percent_of_expectation3, 1),
            total=round(expectation3),
            total_percent=round(int(round(expectation3)) / int(trafic_forecast_3) * 100, 1),
            month_nomn=month_nomn,
            month_gent=month_gent,
            month_loc2=month_loc2
        )

        now = datetime.datetime.now()
        date = now.date()

        with open('report_cherk.txt', 'w') as f:
            f.write(report_petel + "\n")
            f.write(report_pava + "\n")
            f.write(report_kurinoe_tsarstvo)

        print("Файл report_cherk.txt сохранён")

    else:
        print("1ого числа каждого месяца не работаю, юзни калькулятор")


get_myrg()
