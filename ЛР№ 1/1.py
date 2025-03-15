import pandas as pd

# MarketingSpend.csv

print("MarketingSpend.csv ")

data = pd.read_csv('MarketingSpend.csv', header=0, names=['Date', 'Offline', 'Online'])

# Анализ колонки 'Online'
print("\n[Online-траты]")
print(f"• Минимальное значение: {data['Online'].min():.1f}")
print(f"• Максимальное значение: {data['Online'].max():.1f}")
print(f"• Среднее значение: {data['Online'].mean():.3f}")
print(f"• Стандартное отклонение: {data['Online'].std():.3f}")
print(f"• Дисперсия: {data['Online'].var():.3f}")

# Анализ колонки 'Offline'
print("\n[Offline-траты]")
print(f"• Минимальное значение: {data['Offline'].min():.1f}")
print(f"• Максимальное значение: {data['Offline'].max():.1f}")
print(f"• Среднее значение: {data['Offline'].mean():.3f}")
print(f"• Стандартное отклонение: {data['Offline'].std():.3f}")
print(f"• Дисперсия: {data['Offline'].var():.3f}")

# describe MarketingSpend.csv
print("\n" + "-" * 80)
print("describe (MarketingSpend.csv):")
print(data.describe())


# info MarketingSpend.csv
print("\n" + "-" * 80)
print("info (MarketingSpend.csv):")
print(data.info())



# Анализ данных из Retail.csv
print("\n" " Retail.csv ")

# Загрузка данных
data1 = pd.read_csv('Retail.csv')

# 1. Количество инвойсов
num_invoices = data1['InvoiceNo'].nunique()
print(f"\n1. Количество инвойсов: {num_invoices}")

# 2. Количество товаров (StockCode)
num_stockcodes = data1['StockCode'].nunique()
print(f"\n2. Количество уникальных товаров: {num_stockcodes}")

# 3. Топ-10 товаров по количеству заказов
top_10_stockcodes = data1['StockCode'].value_counts().head(10)
print("\n3. Топ-10 товаров (StockCode) по количеству заказов:")
print(top_10_stockcodes.to_string())  # to_string() для красивого вывода

# describe Retail.csv
print("\n" + "-" * 80)
print("describe (Retail.csv):")
print(data1.describe())