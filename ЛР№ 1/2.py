import pandas as pd
import matplotlib.pyplot as plt

data = pd.read_csv('MarketingSpend.csv', header=0, names=['Date', 'Offline', 'Online'], parse_dates=['Date'])
data1 = pd.read_csv('Retail.csv', parse_dates=['InvoiceDate'])
# MarketingSpend.csv

data['Month'] = data['Date'].dt.strftime('%Y-%m')
monthly_sales = data.groupby('Month')[['Offline', 'Online']].sum()

fig, ax = plt.subplots(figsize=(10, 6))
bar_height = 0.4
months = range(len(monthly_sales))

ax.barh(months, monthly_sales['Offline'], height=bar_height, label='offline spend', color='purple')
ax.barh(months, monthly_sales['Online'], height=bar_height, left=monthly_sales['Offline'], label='online spend', color='pink')

for i, (offline, online) in enumerate(zip(monthly_sales['Offline'], monthly_sales['Online'])):
    ax.text(offline / 2, i, f'{offline:.0f}', va='center', ha='center', color='white', fontsize=9)
    ax.text(offline + online / 2, i, f'{online:.0f}', va='center', ha='center', color='white', fontsize=9)
    ax.text(-max(monthly_sales['Offline'] + monthly_sales['Online']) * 0.1, i, f'{offline + online:.0f}', va='center', ha='right', color='black', fontsize=10, fontweight='bold')

ax.set_yticks(months)
ax.set_yticklabels(monthly_sales.index)
ax.set_xlabel('Сумма продаж')
ax.set_title('Зависимость онлайн и оффлайн-продаж по месяцам')
ax.legend()
plt.grid(axis='x', linestyle='--', alpha=0.7)
plt.show()

# Retail.csv

daily_sales = data1.groupby('InvoiceDate')['StockCode'].count().reset_index()
daily_sales['DayOfYear'] = daily_sales['InvoiceDate'].dt.dayofyear

plt.figure(figsize=(12, 6))
plt.scatter(daily_sales['DayOfYear'], daily_sales['StockCode'], color='#B87333', alpha=0.6)
plt.xlabel('День года (от 1 до 365)')
plt.ylabel('Количество проданных изделий')
plt.title('График рассеяния количества проданных изделий за каждый день')
plt.grid(True, linestyle='--', alpha=0.5)
plt.show()