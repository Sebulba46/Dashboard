from FRONTEND.website.auth import db_auth

year = 2022

cursor = db_auth()
cursor.execute('''
    select round(sum(Income)/sum([Target Income])*100, 0)
    from [Financial Statistics]
    where Year = ?
''', year)

income_achieved = str(int(cursor.fetchone()[0])) + '%'

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
for income_source in ('Advertising', 'Asset sale', 'Licensing', 'Renting', 'Subscription', 'Usage fees'):
    cursor.execute('''
        select SUM(Income)
        from [Financial Statistics]
        where Year = ?
        and [Income sources] = ?
    ''', year, income_source)

    income_from_source = cursor.fetchone()[0]

    income_source_value[income_source] = int(income_from_source)
    income_source_perc[income_source] = round(income_from_source/total_income * 100)


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

    breakdowns_value[breakdown] = round(income_from_breakdown)
    breakdowns_perc[breakdown] = round(income_from_breakdown/total_income * 100)


quantity_perc = dict()
for income_source in ('Advertising', 'Asset sale', 'Licensing', 'Renting', 'Subscription', 'Usage fees'):
    cursor.execute('''
        select round(sum(Counts)/? * 100, 0)
        from [Financial Statistics]
        where Year = ?
        and [Income sources] = ?
    ''', total_quantity, year, income_source)

    quantity_perc[income_source] = int(cursor.fetchone()[0])

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

avg_monthly_income = round(sum(monthly_income.values())/len(monthly_income))
print(avg_monthly_income)


monthly_profit = dict()
for month in ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec'][::-1]:
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

total_profit = int(cursor.fetchone()[0])

cursor.execute('''
        select sum(Income)
        from [Financial Statistics]
        where Year = ?
        and [Marketing strategies] = ' B2B '
    ''', year)

total_B2B = int(cursor.fetchone()[0])
B2B_perc = round(total_B2B/total_income * 100, 2)

cursor.execute('''
        select sum(Income)
        from [Financial Statistics]
        where Year = ?
        and [Marketing strategies] = ' B2C '
    ''', year)

total_B2C = int(cursor.fetchone()[0])
B2C_perc = round(total_B2C/total_income * 100, 2)

print(B2B_perc, B2C_perc)











