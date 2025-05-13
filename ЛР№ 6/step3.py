import time
import concurrent.futures
import matplotlib.pyplot as plt
import numpy as np

from main import fermat_factorization as python_version
from ferma_factGIL import fermat_factorization as cython_version

# Тестовые числа
TEST_LST = [111, 9777, 13719, 131909, 619373]

# Количество "вычислителей"
NUM_WORKERS = 4

# Параметры тестирования
number_of_runs = 100  
repeat_times = 5    

def run_in_threads(func, data):
    durations = []
    for _ in range(repeat_times):
        with concurrent.futures.ThreadPoolExecutor(max_workers=NUM_WORKERS) as executor:
            start = time.perf_counter()
            for _ in range(number_of_runs):
                results = list(executor.map(func, data))
            end = time.perf_counter()
            durations.append(end - start)
    return results, np.mean(durations)

def run_in_processes(func, data):
    durations = []
    for _ in range(repeat_times):
        with concurrent.futures.ProcessPoolExecutor(max_workers=NUM_WORKERS) as executor:
            start = time.perf_counter()
            for _ in range(number_of_runs):
                results = list(executor.map(func, data))
            end = time.perf_counter()
            durations.append(end - start)
    return results, np.mean(durations)

def main():
    timings = {}

    print("▶ Используем Python-реализацию")
    _, t1 = run_in_threads(python_version, TEST_LST)
    _, t2 = run_in_processes(python_version, TEST_LST)

    timings["Python-потоки"] = t1
    timings["Python-процессы"] = t2

    print("▶ Используем Cython-реализацию")
    _, t3 = run_in_threads(cython_version, TEST_LST)
    _, t4 = run_in_processes(cython_version, TEST_LST)

    timings["Cython-потоки"] = t3
    timings["Cython-процессы"] = t4

    print("\n⏱ Средние результаты за", repeat_times, "повторов:")
    for k, v in timings.items():
        print(f"{k}: {v:.4f} сек")

    # График
    labels = list(timings.keys())
    values = [timings[k] for k in labels]

    plt.figure(figsize=(10, 6))
    bars = plt.bar(labels, values, color=["skyblue", "steelblue", "salmon", "tomato"])
    plt.ylabel("Время (сек)")
    plt.title("Сравнение скорости: Потоки vs Процессы (Python vs Cython)")

    for bar in bars:
        yval = bar.get_height()
        plt.text(bar.get_x() + bar.get_width()/2, yval + 0.01, f"{yval:.2f}", ha='center', va='bottom')

    plt.xticks(rotation=30)
    plt.tight_layout()
    plt.savefig("compare_timing3.png")
    plt.show()

if __name__ == "__main__":
    main()
