import pandas as pd
import xgboost as xgb
import matplotlib.pyplot as plt
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score

# Загрузка данных
training_data = pd.read_excel('training_data.xlsx').drop('Unnamed: 0', axis=1).dropna()
test_data = pd.read_excel('test_data.xlsx').drop('Unnamed: 0', axis=1).dropna()

# Обработка данных
text_columns = ['title_status', 'transmission', 'drive', 'size']
training_data = training_data.drop(text_columns, axis=1)
test_data = test_data.drop(text_columns, axis=1)

# Добавление упрощающих признаков 
for dataset in [training_data, test_data]:
    dataset['mileage_per_year'] = dataset['odometer'] / (2024 - dataset['year'] + 1)
    dataset['engine_power'] = dataset['cylinders'] * 50

# Подготовить данные для обучения
target_variable_name = 'price'
training_values = training_data[target_variable_name]
training_points = training_data.drop(target_variable_name, axis=1)

test_values = test_data[target_variable_name]
test_points = test_data.drop(target_variable_name, axis=1)

# Настраиваем и обучаем модель
xgb_model = xgb.XGBRegressor(
    n_estimators=1200,
    learning_rate=0.03,
    max_depth=6,
    subsample=0.8,
    colsample_bytree=0.9,
    random_state=42
)

xgb_model.fit(training_points, training_values)

# Валидация модели
test_predictions = xgb_model.predict(test_points)

print("\nРезультаты XGBoost:")
print("MAE: {0:7.2f}, RMSE: {1:7.2f}, R2: {2:7.2f}".format(
    mean_absolute_error(test_values, test_predictions),
    mean_squared_error(test_values, test_predictions)**0.5,
    r2_score(test_values, test_predictions)
))

# Визуализация

plt.figure(figsize=(7, 7))  # Задаем размер графика
plt.scatter(
    test_values,            # Настоящие цены (ось X)
    test_predictions,       # Предсказанные цены (ось Y)
    alpha=0.5,              # Прозрачность точек для лучшей видимости
    label='Предсказания'
)

# Рисуем идеальную линию (y = x)
max_price = max(max(test_values), max(test_predictions))
plt.plot(
    [0, max_price],         # Начало и конец линии по оси X
    [0, max_price],         # Начало и конец линии по оси Y
    color='red',            # Цвет линии
    linestyle='--',         # Стиль линии (пунктир)
    label='Идеальные предсказания'
)

plt.xlabel('Настоящая цена, $', fontsize=12)  # Подпись оси X
plt.ylabel('Предсказанная цена, $', fontsize=12)  # Подпись оси Y
plt.title('Сравнение предсказаний с реальными значениями', fontsize=14)  # Заголовок
plt.legend()  # Показываем легенду
plt.grid(alpha=0.3)  # Добавляем сетку с прозрачностью
plt.show()  # Показываем график