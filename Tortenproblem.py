#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Tortenproblem
https://www.programmieraufgaben.ch/aufgabe/das-tortenproblem/8ijpjc7u
"""

# Programmieraufgabe:
#     k Kinder erhalten t Torten.
#
#     Die Torten sind alle gleich groß, haben aber verschiedene
#     Geschmacksrichtungen. Die Torten werden zunächst je in k Stücke geteilt.
#     Nun erhält jedes Kind von jeder Torte ein Stück.
#     Danach beginnen die Kinder zu tauschen, denn vielleicht mögen nicht alle
#     jede Sorte gleich gut. Beim Tauschen achten die Kinder darauf, dass immer
#     jedes Kind gleich viele Tortenstücke behält.
#     Auf wie viele Arten können die Kinder die Tortenstücke nun so verteilen,
#     dass immer noch alle Kinder gleich viele Stücke haben?
#     Alle Möglichkeiten sind auszugeben.
#
# Autor, Erstellung:
#     Ulrich Berntien, 2018-11-06
#
# Sprache:
#     Python 3.6.6


from typing import *


def minus(a: Tuple[int], b: Tuple[int]) -> Tuple[int]:
    """
    Vektor a minus Vektor b.
    :param a: Von den Werten in dieser Liste wird subtrahiert.
    :param b: Diese Werte werden subtrahiert.
    :return: Elementweise Differenz.
    """
    assert len(a) == len(b)
    return tuple(ax - bx for ax, bx in zip(a, b))


def plus(a: Tuple[int], b: Tuple[int]) -> Tuple[int]:
    """
    Vektor a plus Vektor b.
    :param a: Diese Werte werden addiert.
    :param b: Diese Werte werden addiert.
    :return: Elementweise Summe.
    """
    assert len(a) == len(b)
    return tuple(ax + bx for ax, bx in zip(a, b))


def combinations(pool: Tuple[int, ...], number: int) -> Tuple[int, ...]:
    """
    Alle Kombinationen von Elementen erzeugen.
    Es gibt einen Pool von Elementen unterschiedlichen Typs. Die Anzahl
    der verfügbaren Elementen pro Typ sind in "pool".
    Jede Kombination muss die gleiche Anzahl von Elementen enthalten: number.
    :param pool: Liste von unterschiedlichen Elementen. Der Wert[i] ist
     die Anzahl der verfügbaren Elemente der Sorte i
    :param number: Anzahl der Elemente die kombiniert werden müssen.
    :return: Generator für alle Kombinationen.
    """
    assert sum(pool) >= number
    assert all(p >= 0 for p in pool)
    # Anzahl unterschiedlicher Elemente
    n_types = len(pool)
    # Aktuell gewählte Anzahl von Elementen jedes Typs
    current_elements = [0] * n_types
    # Maximale Anzahl von Elementen, die von Typ i genommen werden können.
    max_elements = [0] * n_types
    # index der zuletzt geänderten Element-Anzahl
    index = -1
    # Anzahl der Elemente, die noch ausgewählt werden müssen nach index
    rest = number
    while True:
        # Auswahl der Elemente nach index: immer minimale Anzahl wählen
        while index < n_types - 1:
            index += 1
            max_elements[index] = min(pool[index], rest)
            current_elements[index] = max(0, rest - sum(pool[index + 1:]))
            rest -= current_elements[index]
        # Eine Kombination ist vollständig ausgewählt
        assert index == n_types - 1
        assert rest == 0
        assert number == sum(current_elements)
        assert all(c <= m for c, m in zip(current_elements, max_elements))
        yield tuple(current_elements)
        # Beim höchst möglichen index die Anzahl der Elemente um 1 vergrößern
        while current_elements[index] == max_elements[index]:
            index -= 1
            if index < 0:
                return
        current_elements[index] += 1
        rest = number - sum(current_elements[:index + 1])


def distributions(sources: Tuple[int], destinations: int) -> List[Tuple[int]]:
    """
    Verteilung von Elementen aus verschiedenen Typen.
    :param sources: Anzahl der verfügbaren Elemente von jedem Element-Typ.
    :param destinations: Auf diese Anahl soll verteilt werden.
    :return: Generator, der Listen liefert mit verteilten Elementen.
    """
    # Die Anzahl der Elemente, die jeder erhalten muss,
    per_destination = sum(sources) // destinations
    assert destinations > 0
    assert sum(sources) == per_destination * destinations
    index: int = -1
    rest = sources
    # Ein Generator erzeugt alle Kombintationen
    generator = [None] * destinations
    # Das ist die aktuell ausgewählte Kombination
    current = [None] * destinations
    while True:
        # Die möglichen Kombinationen für i-1 sind abhängig von den
        # ausgewählten Kombinationen 0..i. Wurde die Kombination für
        # i-1 geändert, dann müssen die Generatoren für i, i+1, ...
        # neu gestartet werden.
        while index < destinations - 1:
            index += 1
            generator[index] = combinations(rest, per_destination)
            current[index] = generator[index].__next__()
            # Die folgenden können aus dem rest auswählen.
            rest = minus(rest, current[index])
        assert index == destinations - 1
        assert all(r == 0 for r in rest)
        yield current
        # Die nächste Kombination nehmen.
        while index >= 0:
            try:
                rest = plus(rest, current[index])
                current[index] = generator[index].__next__()
                break
            except StopIteration:
                # Hier gab es keine weitere Kombination, also
                # einen Schritt zurück und dort die nächste
                # Kombination wählen.
                index -= 1
        rest = minus(rest, current[index])
        if index < 0:
            return


def tortenproblem(torten: int, kinder: int) -> None:
    """
    Alle möglichen Verteilungen von Tortenstücken auf Kinder.
    Die Anzahl der Stücke von jeder Torte ist gleich der Anzhl der Kinder.
    Die Anzahl der Stücke für jedes Kind ist gleich der Anzahl der Torten.
    :param torten: Anzahl der Torten.
    :param kinder: Anzahl der Kinder.
    """
    assert torten > 0
    assert kinder > 0
    print("Kinder:", kinder, "Torten:", torten)
    print("Ausgabe in jeder Zeile: Kind 1|Kind 2|....")
    print("Ausgabe für jedes Kind: Anzahl von Torte 1, Anzahl von Torte 2, ...")
    anzahl: int = 0
    # Die Anzahl der Stücke von jeder Torte ist gleich der Anzahl der Kinder.
    # Jedes Kind bekommt die gleiche Anzahl von Stücke.
    for verteilung in distributions((kinder,) * torten, kinder):
        print("|".join(",".join(str(t) for t in k) for k in verteilung))
        anzahl += 1
    print("------> Anzahl:", anzahl)


if __name__ == '__main__':
    tortenproblem(torten=2, kinder=3)
    tortenproblem(torten=3, kinder=2)
    tortenproblem(torten=5, kinder=4)
