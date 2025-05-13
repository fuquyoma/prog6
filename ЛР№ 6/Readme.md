# Лабораторная работа № 6
## Выполнил: Гневнов А.Е., ИВТ 2.1
## Шаг 1: переписать функции для нахождения чисел с помощью Cython
### Готовим файлы для компиляции Cython
Переписанная функция на [Cython](https://github.com/fuquyoma/prog6/blob/main/ЛР№%206/ferma_fact.pyx) и [setup.py](https://github.com/fuquyoma/prog6/blob/main/ЛР№%206/setup.py)
### Компилируем Cython
``` python
python setup.py build_ext --inplace
```
### Создаём файл для сравнения Python и Cython
[Файл](https://github.com/fuquyoma/prog6/blob/main/ЛР№%206/FarmaXXX.py) запускает timeit с аналогичными параметрами и сравнивает два варианта и строит графики
### Результаты сравнения Python и Cython
![image](https://github.com/user-attachments/assets/8937a691-9c93-4609-979d-287e4a0f62c3)
### Сравнение общего времени выполнения Python и Cython
![image](https://github.com/user-attachments/assets/96db29f6-c7b6-4b45-aa1a-d2d24b2ca2bb)
### Сравнение времени выполнения для каждого числа
![image](https://github.com/user-attachments/assets/e3eb615d-8118-4ae6-ac5b-3bde15192329)
## Шаг 2: Написать код так, чтобы массив данных для вычисления распределялся на несколько "вычислителей"  
### Создаём и готовим файл для вычисления через потоки и процессы.
Функция для вычисления через потоки
``` python
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
```
Функция для вычисления через процессы
``` python
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
```
*Дальше код проводит вычисления сначала Python, потом Cython реализацию и строит график сравнения*
### Сравнение времени выполнения потоков и процессов Python и Cython реализации
![image](https://github.com/user-attachments/assets/46577191-9ec8-45e5-bb7d-6ef2b8f57136)

![compare_timing2](https://github.com/user-attachments/assets/9f053d04-e569-48c7-9db2-5fbcd541359e)

## Шаг 3: Использование GIL
### Пишем новый файл Cython и редактируем setup.py
