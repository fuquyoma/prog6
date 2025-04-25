import timeit
import matplotlib.pyplot as plt
import numpy as np

# Импорт обеих версий
from main import fermat_factorization as python_version
from ferma_fact import fermat_factorization as cython_version

# Тестовые данные
test_numbers = [111, 9777, 13719, 131909, 619373]

# Параметры тестирования
number_of_runs = 100
repeat_times = 5

def benchmark():
    results = []
    total_py_time = 0.0
    total_cy_time = 0.0
    
    for n in test_numbers:
        # Тестирование Python-версии
        py_timer = timeit.Timer(lambda: python_version(n))
        py_times = py_timer.repeat(repeat=repeat_times, number=number_of_runs)
        py_total = sum(py_times)
        total_py_time += py_total
        
        # Тестирование Cython-версии
        cy_timer = timeit.Timer(lambda: cython_version(n))
        cy_times = cy_timer.repeat(repeat=repeat_times, number=number_of_runs)
        cy_total = sum(cy_times)
        total_cy_time += cy_total
        
        # Лучшее время для одной операции
        py_best = min(py_times) / number_of_runs
        cy_best = min(cy_times) / number_of_runs
        results.append((n, py_best, cy_best))
    
    return results, total_py_time, total_cy_time

# Запуск бенчмарка
results, total_py, total_cy = benchmark()

# Вывод результатов
print("\nРезультаты тестирования (время на одну операцию):")
print("-" * 75)
print(f"{'Число':<15} | {'Python (s)':>12} | {'Cython (s)':>12} | {'Ускорение':>12}")
print("-" * 75)
for n, py, cy in results:
    speedup = py / cy
    print(f"{n:<15} | {py:>10.2e} | {cy:>10.2e} | {speedup:>10.1f}x")

# Вывод общего времени
print("\nОбщее время выполнения всех тестов:")
print("-" * 45)
print(f"Python: {total_py:.2e} секунд")
print(f"Cython: {total_cy:.2e} секунд")
print(f"Ускорение: {total_py / total_cy:.1f}x")

# Подготовка данных для графиков
labels = [str(n) for n in test_numbers]
py_times = [res[1] for res in results]
cy_times = [res[2] for res in results]
total_py = sum(py_times)
total_cy = sum(cy_times)

# График 1: Сравнение по отдельным числам
plt.figure(figsize=(12, 6))
x = np.arange(len(labels))
width = 0.35

plt.bar(x - width/2, py_times, width, label='Python', color='green', alpha=0.7)
plt.bar(x + width/2, cy_times, width, label='Cython', color='pink', alpha=0.7)

plt.title('Сравнение производительности для разных чисел', fontsize=14)
plt.xticks(x, labels, rotation=45)
plt.ylabel('Время (секунды)')
plt.yscale('log')
plt.legend()
plt.grid(True, which='major', linestyle='--', alpha=0.5)
plt.tight_layout()

# График 2: Общее сравнение
plt.figure(figsize=(8, 6))
plt.bar(['Python', 'Cython'], [total_py, total_cy], color=['green', 'pink'])

plt.title('Общее время выполнения всех тестов', fontsize=14)
plt.ylabel('Суммарное время (секунды)')
plt.yscale('log')
plt.grid(True, which='major', linestyle='--', alpha=0.5)
plt.tight_layout()

plt.show()