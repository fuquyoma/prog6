import pandas as pd
from lightgbm import LGBMRegressor
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score

# Загрузка данных
train_data = pd.read_excel('training_data.xlsx').drop('Unnamed: 0', axis=1).dropna()
test_data = pd.read_excel('test_data.xlsx').drop('Unnamed: 0', axis=1).dropna()

# Удаление текстовых признаков
text_cols = ['title_status', 'transmission', 'drive', 'size']
train_data = train_data.drop(text_cols, axis=1)
test_data = test_data.drop(text_cols, axis=1)

# Разделение данных
X_train = train_data.drop('price', axis=1)
y_train = train_data['price']
X_test = test_data.drop('price', axis=1)
y_test = test_data['price']

# Создание и обучение модели
model = LGBMRegressor(
    n_estimators=1000,
    learning_rate=0.05,
    random_state=42,
    n_jobs=-1
)

model.fit(X_train, y_train)

# Предсказание и оценка
predictions = model.predict(X_test)

print("\nРезультаты LightGBM:")
print(f"MAE: {mean_absolute_error(y_test, predictions):.2f}")
print(f"RMSE: {mean_squared_error(y_test, predictions)**0.5:.2f}")
print(f"R²: {r2_score(y_test, predictions):.2f}")