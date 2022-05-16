from flask import Blueprint, render_template, request, flash, redirect, url_for
import pyodbc

auth = Blueprint('auth', __name__)


def db_auth():
    server = '176.99.158.202'
    database = 'Dashboard'
    username = 'guest'
    password = 'karramba'
    connect = pyodbc.connect(
        f'DRIVER={{ODBC Driver 17 for SQL Server}};SERVER={server};DATABASE={database};UID={username};PWD={password}')
    return connect.cursor()


def add_comma(num: [int, str]) -> str:
    new_num = ''
    num = str(num)
    count = 1
    for s, j in zip(range(len(num)), num[::-1]):
        if count % 4 == 0:
            new_num += ',' + j
        else:
            new_num += j
        count += 1

    return new_num[::-1]


@auth.route('/', methods=['GET', 'POST'])
def d_2020():
    if request.method != 'POST':
        year = 2020
    else:
        year = int(request.form['submit_button'])

    cursor = db_auth()
    cursor.execute('''
        select round(sum(Income)/sum([Target Income])*100, 0)
        from [Financial Statistics]
        where Year = ?
    ''', year)

    income_achieved = int(cursor.fetchone()[0])

    cursor.execute('''
        select sum(Income)
        from [Financial Statistics]
        where Year = ?
    ''', year)

    total_income = int(cursor.fetchone()[0])

    cursor.execute('''
        select sum(Counts)
        from [Financial Statistics]
        where Year = ?
    ''', year)

    total_quantity = int(cursor.fetchone()[0])

    income_source_value = dict()
    income_source_perc = dict()
    income_values = dict()
    for income_source in ('Advertising', 'Asset sale', 'Licensing', 'Renting', 'Subscription', 'Usage fees'):
        cursor.execute('''
            select SUM(Income)
            from [Financial Statistics]
            where Year = ?
            and [Income sources] = ?
        ''', year, income_source)

        income_from_source = cursor.fetchone()[0]

        income_values[income_source] = int(income_from_source)

        income_source_value[income_source] = add_comma(int(income_from_source))
        income_source_perc[income_source] = round(income_from_source / total_income * 100)

    income_value_max = max(income_values, key=lambda k: income_values.get(k))

    cursor.execute('''
        select distinct [Income Breakdowns]
        from [Financial Statistics]
        where Year = ?
    ''', year)

    breakdowns_value = dict()
    breakdowns_perc = dict()
    for breakdown in tuple([s[0] for s in cursor.fetchall()]):
        cursor.execute('''
            select sum(Income)
            from [Financial Statistics]
            where Year = ?
            and [Income Breakdowns] = ?
        ''', year, breakdown)

        income_from_breakdown = cursor.fetchone()[0]

        breakdowns_value[breakdown] = add_comma(round(income_from_breakdown))
        breakdowns_perc[breakdown] = round(income_from_breakdown / total_income * 100)

    quantity_value = dict()
    quantity_perc = dict()
    for income_source in ('Advertising', 'Asset sale', 'Licensing', 'Renting', 'Subscription', 'Usage fees'):
        cursor.execute('''
            select round(sum(Counts)/? * 100, 0)
            from [Financial Statistics]
            where Year = ?
            and [Income sources] = ?
        ''', total_quantity, year, income_source)

        perc = int(cursor.fetchone()[0])

        quantity_perc[income_source] = str(perc)

        cursor.execute('''
            select sum(Counts)
            from [Financial Statistics]
            where [Income sources] = ?
            and Year = ?
        ''', income_source, year)

        val = cursor.fetchone()[0]

        quantity_value[income_source] = str(round(val))

    cursor.execute('''
        select sum([Target Income])
        from [Financial Statistics]
        where Year = ?
    ''', year)

    target_income = int(cursor.fetchone()[0])

    monthly_income = dict()
    for month in ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']:
        cursor.execute('''
            select sum(Income)
            from [Financial Statistics]
            where Year = ?
            and Month = ?
        ''', year, month)

        monthly_income[month] = int(cursor.fetchone()[0])

    avg_monthly_income = add_comma(round(sum(monthly_income.values()) / len(monthly_income)))

    monthly_profit = dict()
    for month in ['Dec', 'Nov', 'Oct', 'Sep', 'Aug', 'Jul', 'Jun', 'May', 'Apr', 'Mar', 'Feb', 'Jan']:
        cursor.execute('''
            select sum([Operating profit])
            from [Financial Statistics]
            where Year = ?
            and Month = ?
        ''', year, month)

        monthly_profit[month] = int(cursor.fetchone()[0])

    cursor.execute('''
            select sum([Operating profit])
            from [Financial Statistics]
            where Year = ?
        ''', year)

    total_profit = add_comma(int(cursor.fetchone()[0]))

    cursor.execute('''
            select sum(Income)
            from [Financial Statistics]
            where Year = ?
            and [Marketing strategies] = ' B2B '
        ''', year)

    total_b2b = int(cursor.fetchone()[0])
    b2b_perc = round(total_b2b / total_income * 100, 2)

    cursor.execute('''
            select sum(Income)
            from [Financial Statistics]
            where Year = ?
            and [Marketing strategies] = ' B2C '
        ''', year)

    total_b2c = int(cursor.fetchone()[0])
    b2c_perc = round(total_b2c / total_income * 100, 2)

    total_income_comm = add_comma(total_income)
    target_income_comm = add_comma(target_income)
    for key, value in zip(quantity_value.keys(), quantity_value.values()):
        quantity_value[key] = add_comma(value)

    colors = ['white', 'black']
    background = ['#1D1D3A', 'white']

    return render_template("Income Sources 2020.html", income_value_max=income_value_max, year=year,
                           background=background, colors=colors, target_income_comm=target_income_comm,
                           total_income_comm=total_income_comm, income_achieved=income_achieved,
                           total_income=total_income,
                           total_quantity=total_quantity, quantity_value=quantity_value,
                           income_source_value=income_source_value,
                           income_source_perc=income_source_perc, breakdowns_value=breakdowns_value,
                           breakdowns_perc=breakdowns_perc, quantity_perc=quantity_perc,
                           target_income=target_income,
                           monthly_income=monthly_income, avg_monthly_income=avg_monthly_income,
                           monthly_profit=monthly_profit, total_profit=total_profit, total_b2b=total_b2b,
                           b2b_perc=b2b_perc, total_b2c=total_b2c, b2c_perc=b2c_perc)
