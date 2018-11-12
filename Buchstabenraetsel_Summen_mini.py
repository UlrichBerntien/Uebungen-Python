#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Programmieraufgabe:
    Buchstabenrätsel Summen
    https://www.programmieraufgaben.ch/aufgabe/buchstabenraetsel-summen/mtt2cuwo

    Schreiben Sie ein Programm, das Symbolrätsel der folgenden Art (Summen)
    löst:
        aab + bbc = dde.
    Dabei bedeuten gleiche Buchstaben auch immer gleiche Ziffern und
    verschiedene Buchstaben bedeuten auch verschiedene Ziffern.

Programmidee:

    Sucht nach einer Lösung für die Buchtabenrätsel Summe. Es werden nicht alle
    möglichen Lösungen gesucht, die Suche wird beim ersten Erfolg abgebrochen.
    Gegeben ist eine Summe von Zahlen und das Ergebnis, dabei sind Ziffern durch
    Buchstaben ersetzt. Jeder Buchstabe steht für eine andere Ziffer. Sind in
    der Gleichung Ziffern enthalten, dann kann kein Buchstabe eine dieser Ziffern
    sein. In den Summen und im Ergebnis können auch Ziffern vorgegeben sein.

    Verwendet wird ein Backtracking-Algorithmus. Ziel ist ein kurzes Programm mit
    dem Verzicht auf einen optimierten Lösungsalgorithmus.

Author:
    Ulrich Berntien, 2018-10-30

Sprache:
    Python 3.6.6
"""

from typing import *


def save_eval(equation: str) -> bool:
    """
    Gleichung ausrechnen mit Abfangen von Exceptions.
    Achtung: Code wird ohne Prüfung ausgeführt.
    :param equation: Gleichung in Python-Syntax.
    :return: True falls die Gleichung True ergibt, sonst False.
    """
    try:
        return eval(equation)
    except SyntaxError:
        return False


def solve(equation: str, letters: Set[str], digits: List[str]) -> str:
    """
    Backtracking Algorithmus mit rekursiver Realisierung.
    :param equation: Die teilweise gelöste Gleichung.
    :param letters:  Diese Buchstaben sind noch festzulegen.
    :param digits:  Diese Ziffern sind noch verfügbar.
    :return: Die Lösung oder ein leerer String.
    """
    if not letters and save_eval(equation):
        # Eine Lösung ist gefunden
        return equation
    elif not letters or not digits:
        # keine Buchstaben oder Ziffern mehr verfügbar
        return ""
    else:
        # Alle Ziffern für einen Buchstaben ausprobieren
        try_letters = letters.copy()
        letter = try_letters.pop()
        for digit in digits:
            try_digits = digits.copy()
            try_digits.remove(digit)
            result = solve(equation.replace(letter, digit), try_letters, try_digits)
            if result:
                # Bei diesem Versuch wurde eine Lösuzng gefunden
                return result


def solve_letter_sum(letter_sum: str) -> str:
    """
    Sucht nach einer Lösung für die Buchtabenrätsel Summe.
    :param letter_sum: Die Buchstabenrätsel Summe.
    :return: Eine Lösung, wenn keine Lösung gefunden wurde ein leerer String.
    """
    # Gleichung ins Python-Format für Kontrollberechnungen
    # Achtung: keine Kontrolle der Gleichung für minimiale Programmlänge
    equation = letter_sum.replace("=", "==")
    letters = set(c for c in equation if c.isalpha())
    digits = [d for d in "0123456789" if d not in equation]
    return solve(equation, letters, digits)


# Kontrolle der Lösungsfunktion
if __name__ == '__main__':
    testcases = ("aab + bbc = dde",
                 "SEND + MORE = MONEY",
                 "abc+111=468",
                 "abc+111=dab",
                 "abc+def+ghi=acfe",
                 "12ab+cdef=dg12",
                 "abc+abc=268",
                 "a+b=8")
    for test in testcases:
        print("Aufgabe:", test)
        print(". . . .:", solve_letter_sum(test))
