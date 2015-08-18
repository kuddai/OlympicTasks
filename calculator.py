#!/usr/bin/env python
# -*- coding: utf-8 -*-
import sys
def calculator(number):
    #Список, где значением является минимальное число операций, чтобы 
    #получить данный идекс списка. 
    #Значения по умолчанию выбраны максимально большими (sys.maxint == 9223372036854775807).
    #Длина списка на 1 больше number, т.к. индекс ведется от нуля
    best = [sys.maxint] * (number + 1)
    #Даем начальное значение динамики
    best[1] = 0
    #xrange чтобы сэкономить память
    for x in xrange(1, len(best)):
        #операции калькулятора делаются в такой последовательности, 
        #что если какая-то из операций перевысит длину списка,
        #то и последющие операции также ее перевысят.
        try:
            num_operations = best[x] + 1
            #если наше количество операций короче старого, то
            #запоминаем новое лучшее значение
            best[x + 1] = min(best[x + 1], num_operations)
            best[x * 2] = min(best[x * 2], num_operations)
            best[x * 3] = min(best[x * 3], num_operations)
        except IndexError:
            continue

    return best[number]


number = int(raw_input())
print calculator(number)