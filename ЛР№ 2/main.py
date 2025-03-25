import pandas as pd

df = pd.read_csv('train.csv')

# 1. Количество мужчин и женщин
sex_counts = df['Sex'].value_counts()
print(f"1.Количество мужчин и женщин на пароходе: {sex_counts['male']} {sex_counts['female']}")

# 2. Пассажиры по портам посадки 
embarked_counts = df['Embarked'].value_counts()
print(f"2.Количество пассажиров, загрузившиеся в портах 'S','C','Q': {embarked_counts.get('S', 0)} {embarked_counts.get('C', 0)} {embarked_counts.get('Q', 0)}")

# 3. Доля погибших
survived_counts = df['Survived'].value_counts()
dead_count = survived_counts[0]
dead_percent = (dead_count / len(df)) * 100
print(f"3.Число и процент погибших: {dead_count} {dead_percent:.2f}%")

# 4. Доли пассажиров по классам
class_counts = df['Pclass'].value_counts(normalize=True) * 100
print(f"4.Доля пассажиров 1 класса: {class_counts[1]:.2f}%, 2: {class_counts[2]:.2f}%, 3: {class_counts[3]:.2f}%")

# 5. Корреляция SibSp и Parch
corr_sibsp_parch = df[['SibSp', 'Parch']].corr().iloc[0, 1]
print(f"5.Корреляция Пирсона между SibSp и Parch: {corr_sibsp_parch:.2f}")

# 6. Корреляции Survived с возрастом, полом и классом
# Возраст 
age_survived_corr = df[['Age', 'Survived']].dropna().corr().iloc[0, 1]
# Пол 
df['Sex_encoded'] = df['Sex'].map({'male': 1, 'female': 0})
sex_survived_corr = df[['Sex_encoded', 'Survived']].corr().iloc[0, 1]
# Класс
class_survived_corr = df[['Pclass', 'Survived']].corr().iloc[0, 1]
print(f"6.Корреляцмя Пирсона между: Age-Survived: {age_survived_corr:.2f}, Sex-Survived: {sex_survived_corr:.2f}, Class-Survived: {class_survived_corr:.2f}")

# 7. Статистика по возрасту
age_stats = df['Age'].describe()
print(f"7.Возраст пассажиров. Средний: {age_stats['mean']:.1f}, Медиана: {age_stats['50%']:.1f}, Мин: {age_stats['min']:.1f}, Макс: {age_stats['max']:.1f}")

# 8. Статистика по ценам билетов
fare_stats = df['Fare'].describe()
print(f"8.Цена билета. Средняя: {fare_stats['mean']:.2f}, Медиана: {fare_stats['50%']:.2f}, Мин: {fare_stats['min']:.2f}, Макс: {fare_stats['max']:.2f}")

# 9. Самое популярное мужское имя
male_names = df[df['Sex'] == 'male']['Name'].str.extract(r',\sMr\.\s([A-Za-z]+)')
most_common_male = male_names.value_counts().idxmax()
print(f"9.Самое популярное мужское имя: {most_common_male}")

# 10. Популярные имена среди лиц старше 15 лет
adult_passengers = df[df['Age'] > 15]
# Мужчины
adult_male_names = adult_passengers[adult_passengers['Sex'] == 'male']['Name'].str.extract(r',\sMr\.\s([A-Za-z]+)')
most_common_male_adult = adult_male_names.value_counts().idxmax()
# Женщины
adult_female_names = adult_passengers[adult_passengers['Sex'] == 'female']['Name'].str.extract(r',\s(?:Mrs\.|Miss\.)\s(?:\w+\s)?\(?([A-Za-z]+)')
most_common_female_adult = adult_female_names.value_counts().idxmax()
print(f"10.Самое популярные имена людей после 15 лет. Мужское: {most_common_male_adult}, Женское: {most_common_female_adult}")