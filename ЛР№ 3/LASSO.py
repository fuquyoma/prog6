import pandas as pd
import numpy as np
from sklearn.linear_model import LassoCV
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score

# ----------------------------------------------------------
# 1. Загрузка и предобработка данных
# ----------------------------------------------------------
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

# Масштабирование признаков
scaler = StandardScaler()
X_train_scaled = scaler.fit_transform(X_train)
X_test_scaled = scaler.transform(X_test)

# ----------------------------------------------------------
# 2. Обучение модели LASSO с кросс-валидацией
# ----------------------------------------------------------
# Подбор alpha (коэффициента регуляризации) 
alphas = np.logspace(-3, 1, 50)  # Диапазон: от 0.001 до 10

model = LassoCV(
    alphas=alphas,
    cv=5,
    max_iter=10000,
    random_state=42
)
model.fit(X_train_scaled, y_train)

# ----------------------------------------------------------
# 3. Предсказание и оценка
# ----------------------------------------------------------
predictions = model.predict(X_test_scaled)

print("\nРезультаты LASSO:")
print(f"Выбранный alpha: {model.alpha_:.4f}")
print(f"MAE: {mean_absolute_error(y_test, predictions):.2f}")
print(f"RMSE: {mean_squared_error(y_test, predictions)**0.5:.2f}")
print(f"R²: {r2_score(y_test, predictions):.2f}")
print(f"Количество ненулевых коэффициентов: {np.sum(model.coef_ != 0)}")