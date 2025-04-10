# Импорт библиотек
import warnings
import pandas as pd
import matplotlib.pyplot as plt
from sklearn import linear_model, ensemble
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score
from sklearn.preprocessing import LabelEncoder, OneHotEncoder

# Игнорирование предупреждений
warnings.simplefilter(action='ignore', category=FutureWarning)

# Загрузка данных
training_data = pd.read_excel('training_data.xlsx', usecols=lambda x: 'Unnamed' not in x)
test_data = pd.read_excel('test_data.xlsx', usecols=lambda x: 'Unnamed' not in x)

# Чтение данных
training_data = pd.read_excel('training_data.xlsx', usecols=lambda x: 'Unnamed' not in x)
test_data = pd.read_excel('test_data.xlsx', usecols=lambda x: 'Unnamed' not in x)

# Предобработка данных
def preprocess_data(df):
    df = df.dropna()
    return df._get_numeric_data()

training_data = preprocess_data(training_data)
test_data = preprocess_data(test_data)

# Разделение на признаки и целевую переменную
target_variable_name = 'price'
training_values = training_data[target_variable_name]
training_points = training_data.drop(target_variable_name, axis=1)
test_values = test_data[target_variable_name]
test_points = test_data.drop(target_variable_name, axis=1)

# Обучение моделей
linear_model = linear_model.LinearRegression()
linear_model.fit(training_points, training_values)

rf_model = ensemble.RandomForestRegressor(random_state=42)
rf_model.fit(training_points, training_values)

# Предсказания
test_pred_linear = linear_model.predict(test_points)
test_pred_rf = rf_model.predict(test_points)

# Оценка качества
print("Линейная регрессия:")
print(f"MAE: {mean_absolute_error(test_values, test_pred_linear):.2f}")
print(f"RMSE: {mean_squared_error(test_values, test_pred_linear)**0.5:.2f}")
print(f"R²: {r2_score(test_values, test_pred_linear):.2f}\n")

print("Случайный лес:")
print(f"MAE: {mean_absolute_error(test_values, test_pred_rf):.2f}")
print(f"RMSE: {mean_squared_error(test_values, test_pred_rf)**0.5:.2f}")
print(f"R²: {r2_score(test_values, test_pred_rf):.2f}")

# Бонус: Кодирование категориальных признаков (Label Encoding)
training_data = pd.read_excel('training_data.xlsx').dropna().drop('Unnamed: 0', axis=1)
test_data = pd.read_excel('test_data.xlsx').dropna().drop('Unnamed: 0', axis=1)

text_cols = ['title_status', 'transmission', 'drive', 'size']
le = LabelEncoder()

for col in text_cols:
    training_data[col] = le.fit_transform(training_data[col]) + 1
    test_data[col] = le.transform(test_data[col]) + 1

# Обучение модели с новыми признаками
X_train = training_data.drop('price', axis=1)
y_train = training_data['price']
X_test = test_data.drop('price', axis=1)
y_test = test_data['price']

rf_model_le = ensemble.RandomForestRegressor(random_state=42)
rf_model_le.fit(X_train, y_train)
test_pred_le = rf_model_le.predict(X_test)

print("\nСлучайный лес (с Label Encoding):")
print(f"MAE: {mean_absolute_error(y_test, test_pred_le):.2f}")
print(f"RMSE: {mean_squared_error(y_test, test_pred_le)**0.5:.2f}")

# Бонус: One-Hot Encoding
encoder = OneHotEncoder(sparse_output=False, handle_unknown='ignore')
categorical_cols = ['condition', 'cylinders', 'title_status', 'transmission', 'drive', 'size']

# Применение к обучающим данным
encoded_train = encoder.fit_transform(training_data[categorical_cols].astype(str))
encoded_train_df = pd.DataFrame(
    encoded_train,
    columns=encoder.get_feature_names_out(categorical_cols),
    index=training_data.index
)

# Применение к тестовым данным
encoded_test = encoder.transform(test_data[categorical_cols].astype(str))
encoded_test_df = pd.DataFrame(
    encoded_test,
    columns=encoder.get_feature_names_out(categorical_cols),
    index=test_data.index
)

# Объединение признаков
X_train_ohe = pd.concat([training_data.drop(categorical_cols + ['price'], axis=1), encoded_train_df], axis=1)
X_test_ohe = pd.concat([test_data.drop(categorical_cols + ['price'], axis=1), encoded_test_df], axis=1)

# Обучение модели с OHE
rf_model_ohe = ensemble.RandomForestRegressor(random_state=42)
rf_model_ohe.fit(X_train_ohe, y_train)
test_pred_ohe = rf_model_ohe.predict(X_test_ohe)

print("\nСлучайный лес (с One-Hot Encoding):")
print(f"MAE: {mean_absolute_error(y_test, test_pred_ohe):.2f}")
print(f"RMSE: {mean_squared_error(y_test, test_pred_ohe)**0.5:.2f}")

# Визуализация результатов (добавьте этот блок в конец)
plt.figure(figsize=(15, 5))

# График для линейной регрессии
plt.subplot(1, 3, 1)
plt.scatter(test_values, test_pred_linear, alpha=0.5)
plt.plot([0, max(test_values)], [0, max(test_values)], 'r--')
plt.title('Линейная регрессия')
plt.xlabel('Реальная цена')
plt.ylabel('Предсказанная цена')
plt.grid(True)

# График для случайного леса
plt.subplot(1, 3, 2)
plt.scatter(test_values, test_pred_rf, alpha=0.5, color='orange')
plt.plot([0, max(test_values)], [0, max(test_values)], 'r--')
plt.title('Случайный лес (базовая модель)')
plt.xlabel('Реальная цена')
plt.ylabel('Предсказанная цена')
plt.grid(True)

# График для One-Hot Encoding
plt.subplot(1, 3, 3)
plt.scatter(test_values, test_pred_ohe, alpha=0.5, color='green')
plt.plot([0, max(test_values)], [0, max(test_values)], 'r--')
plt.title('Случайный лес (One-Hot Encoding)')
plt.xlabel('Реальная цена')
plt.ylabel('Предсказанная цена')
plt.grid(True)

plt.tight_layout()
plt.show()

# Сравнение метрик
metrics = ['MAE', 'RMSE', 'R²']
linear_metrics = [
    mean_absolute_error(test_values, test_pred_linear),
    mean_squared_error(test_values, test_pred_linear)**0.5,
    r2_score(test_values, test_pred_linear)
]

rf_metrics = [
    mean_absolute_error(test_values, test_pred_rf),
    mean_squared_error(test_values, test_pred_rf)**0.5,
    r2_score(test_values, test_pred_rf)
]

ohe_metrics = [
    mean_absolute_error(y_test, test_pred_ohe),
    mean_squared_error(y_test, test_pred_ohe)**0.5,
    r2_score(y_test, test_pred_ohe)
]

x = range(len(metrics))
plt.figure(figsize=(12, 6))

plt.bar(x, linear_metrics, width=0.25, label='Линейная регрессия')
plt.bar([i + 0.25 for i in x], rf_metrics, width=0.25, label='Случайный лес')
plt.bar([i + 0.5 for i in x], ohe_metrics, width=0.25, label='One-Hot Encoding')

plt.xticks([i + 0.25 for i in x], metrics)
plt.title('Сравнение метрик качества моделей')
plt.ylabel('Значение метрики')
plt.legend()
plt.grid(True, axis='y', linestyle='--')
plt.show()