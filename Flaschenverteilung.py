#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Programmieraufgabe:
    Flaschenverteilung (Algorithmen)
    https://www.programmieraufgaben.ch/aufgabe/flaschenverteilung-1/i9kdigw5

    Familie Kurse möchte Urlaub auf der trinkwasserlosen Insel Drøgø, deren
    Küste ringsherum sehr steil ist. Zum Glück gibt es einen Flaschenzug, mit
    dem die Getränkeflaschen nach oben gezogen werden können.Es stehen auch
    viele Behälter mit genügend Platz für alle Flaschen zur Verfügung, damit
    mehrere Flaschen auf einmal transportiert werden können.
    Bei 7 Flaschen und 2 Behältern, von denen in den einen 3 und in den anderen
    5 Flaschen passen, gibt es genau zwei Möglichkeiten: Der kleinere Behälter
    ist entweder ganz voll oder enthält genau 2 Flaschen. Auf 3 Behälter mit
    Platz für genau 2, 3 und 4 Flaschen lassen sich die sieben Flaschen auf
    genau sechs Arten verteilen.
    Schreiben Sie ein Programm, das eine Anzahl N von Flaschen, eine Anzahl k
    von Behältern und die k Fassungsvermögen der Behälter einliest und
    berechnet, auf wie viele Arten die Flaschen verteilt werden können. Die
    Flaschen sind nicht unterscheidbar, aber die Behälter sind es, auch wenn
    sie gleich groß sind.

Author:
    Ulrich Berntien, 2018-08-14

Sprache:
    Python 3.6.6
"""

from typing import *


def moeglichkeiten(flaschen: int, kisten: List[int]) -> int:
    """
    Bestimmt die Anzahl der Möglichkeiten die Flaschen zu verteilen.
    :param flaschen: Anzahl der Flaschen, die verteilt werden müssen.
    :param kisten: Liste mit den Größen der Kisten.
    :return: Anzahl der Möglichkeiten
    """
    assert flaschen >= 0
    if len(kisten) < 1:
        raise RuntimeError("Keine Kisten")
    if len(kisten) == 1:
        if flaschen > kisten[0]:
            raise RuntimeError("Flaschen passen nicht in die Kiste")
        else:
            # alle Flasch in die Kiste, es gibt nur eine Möglichkeit
            return 1
    if flaschen == 0:
        # Keine Flaschen.
        # Also genau eine Möglichkeit: alle Kisten leer
        return 1
    assert len(kisten) >= 2
    # In dieser Rekursionsstufe werden alle Möglichkeiten für die
    # Füllung der ersten Kiste betrachtet.
    (erste_kiste, *rest_kisten) = kisten
    assert erste_kiste > 0
    # Mindestens so viele Flaschen in die Kiste,
    # dass der Rest der Flaschen in den Rest der Kisten passt.
    min_flaschen = max(0, flaschen - sum(rest_kisten))
    # Höchstens so viele Flaschen in die Kiste,
    # dass alle Flaschen in der Kiste sind oder die Kiste voll ist.
    max_flaschen = min(flaschen, erste_kiste)
    # Alle Möglichkeiten aufsummieren,
    # wenn n Flaschen in diese Kiste gestellt werden.
    return sum(moeglichkeiten(flaschen - n, rest_kisten)
               for n in range(min_flaschen, 1 + max_flaschen))


# Testfälle aus der Aufgabe
# Liste mit Tupel aus Anzahl Flaschen, Liste der Kistengrößen
TEST_FAELLE: List[Tuple[int, List[int]]] = [
    (7, [3, 5]),
    (7, [2, 3, 4])
]

for test_flaschen, test_kisten in TEST_FAELLE:
    print("Anzahl Flaschen:         ", test_flaschen)
    print("Kistengrößen:            ", test_kisten)
    print("Verteilungsmöglichkeiten:", moeglichkeiten(test_flaschen, test_kisten))
    print("- " * 13)
