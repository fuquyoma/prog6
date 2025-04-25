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
