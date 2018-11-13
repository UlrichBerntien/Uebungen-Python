#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Code knacken
https://www.programmieraufgaben.ch/aufgabe/code-knacken/d4kocgvt
"""

# Programmieraufgabe:
#     Hannas fünfstelliges Zahlenschloss wurde verstellt. Das Zahlenschloss
#     besteht aus fünf Ringen mit je zehn möglichen Einstellungen ('0', '1', '2',
#     ..., '9').
#     Irgend eine Klassenkameradin hat ihr den Code abgeschaut und nun neu
#     eingestellt. Die Klassenkameradin hat den neuen Code leider vergessen.
#     Aufgrund von Lieblingszahlen und Mustern haben die beiden zusammen jedoch
#     folgendes rekonstruieren können:
#         Der neue Code enthält keine 5.
#         Der neue Code enthält mindestens einmal die Ziffer 3.
#         Der neue Code enthält mindestens einmal die Ziffer 6.
#         Der neue Code startet nicht mit einer geraden Ziffer, auch nicht mit
#         der Null ("0").
#         Der neue Code ist fast aufsteigend. Das heißt, die nachfolgenden Ziffern
#         sind nicht kleiner als die vorangehenden (z. b. "23368"). Dies jedoch
#         mit maximal einer Ausnahme. An einer Stelle darf die Ziffernfolge
#         absteigend sein (z. b. 23326); aber wie erwähnt: maximal einmal!
#     Schreiben Sie ein Programm, das alle verbleibenden Möglichkeiten ausgibt.
#
# Autor, Erstellung:
#     Ulrich Berntien, 2018-06-08
#
# Sprache:
#     Python 3.6.6


import itertools
from typing import *


def is_hannas_code(code: Tuple[int, ...]) -> bool:
    """
    Die Funktion prüft ob es eine Kombination von Hanna sein kann.
    :param code: Zu überprüfenden Zahlencode.
    :return: True, genau dann, wenn der Code von Hanna sein kann.
    """
    # Bereits vorher wurde festgelegt: keine 5 enthalten und erste Ziffer ungerade
    assert 5 not in code
    assert code[0] % 2 == 1
    # Ziffer 3 und 6 müssen enthalten sein
    # erste Ziffer muss ungerade und keine 0 sein
    # Nur maximal einmal darf die Ziffernfolge aufsteigend sein
    return 3 in code and \
           6 in code and \
           sum(a > b for (a, b) in zip(code, code[1:])) <= 1


print("Programmieraufgabe Code Knacken, http://www.programmieraufgaben.ch")
# Die Kombination besteht aus den Ziffer 0..9 ohne die Ziffer 5
hannas_digits = [digit for digit in range(10) if digit != 5]
# Die erste Ziffer muss ungerade und keine 0 sein.
hannas_first_digit = [digit for digit in hannas_digits if digit % 2 == 1]
# Hannas Kombination hat 5 Stellen und weitere Kritrien müssen erfüllt sein.
hannas_options = [code for code in itertools.product(hannas_first_digit, *(hannas_digits,) * 4) if is_hannas_code(code)]
for number in hannas_options:
    print(number)
print("Anzahl der Kombinationen:", len(hannas_options))
print("Bei 3s pro Kombination und 50% ausprobieren: {:.0f}min".format(len(hannas_options) * 3 / 2 / 60))
