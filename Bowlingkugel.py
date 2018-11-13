#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Bowlingkugel (Simulationen)
https://www.programmieraufgaben.ch/aufgabe/bowlingkugel/sor45wf7
"""

# Programmieraufgabe:
#     Die Aufgabe besteht darin, in einem 100-stöckigen Haus das Stockwerk zu
#     bestimmen, aus welchem eine Bowlingkugel den freien Fall gerade noch
#     übersteht. Sie haben für die Versuche zwei identische Kugeln zur Verfügung,
#     welche beide in Bruch gehen dürfen. Nachdem die zweite Kugel defekt ist,
#     müssen Sie das Stockwerk angeben können. Ziel ist es, möglichst wenige
#     Fallversuche durchführen zu müssen.
#     Je nach Material der Kugeln gehen diese bereits in einem unteren Stockwerk
#     oder im extremen Fall gar nicht kaputt.
#
#     Schreiben Sie ein Programm, das mit möglichst wenigen Versuchen das gesuchte
#     Stockwerk ermittelt. Legen Sie zu Beginn des Programms das Stockwerk, bei
#     welchem die beiden Kugeln zerstört werden, per Zufallszahl zwischen 1 und
#     100 fest.
#
# Vorüberlegunng:
#     Es sind nur maximal 100 Stockwerke. Der Algorithmus kann daher für
#     jedes Stockwerk ausprobiert werden, wenn nur deterministische Algorithmen
#     verwendet werden.
#     Es soll ein Algorithmus gefunden werden, der möglichst wenige Würfe
#     benötigt. Das kann auf die maximale Anzahl von Würfe oder die
#     mittlere Anzahl von Würfe bezogen sein. Bei den Versuchen wurde beides
#     zusammen reduziert.
#     Die minimale Anzahl kann auch optimiert werden. Das Minimum ist 1 und wird
#     von dem einfachen schrittweisen Ausprobieren erreicht, hier haben alle
#     anderen Algotithmen ein Minimum von 2.
#
# Autor, Erstellung:
#     Ulrich Berntien, 2018-08-09
#
# Sprache:
#     Python 3.6.6

import math
import statistics
from typing import *

# Die Etagen tragen die Nummern 0, 1, .. 99
LEVELS = range(0, 100)

# Die Bowlingkugeln werden zerstört bei einem Fall aus Stockwerk.
# Es gibt die Möglichkeit, dass die Kugel den Fall aus dem höchsten
# Stockwerk (Nummer 99) übersteht
DESTROY_LEVELS = range(1, 101)

# Anzahl der Bowlingkugeln für einen Versuch
NUMBER_BALLS = 2


class Balls(object):
    """
    Ein Objekt der Klasse Balls ist das Modell für die beiden Bowlingkugeln.
    Die Funktion throw wift eine Kugel und gibt das Erebniss zurück.
    Automatisch werden die Würfe gezählt und auf die nächste Kugel gewechselt.
    """

    def __init__(self, destroy_level: int) -> None:
        """
        Bälle vorbereiten.
        :param destroy_level: Ab dieser Nummer werden die Kugel zerstört.
        """
        assert destroy_level in DESTROY_LEVELS
        self._destroy_level = destroy_level
        self._number_balls = NUMBER_BALLS
        self._number_throws = 0

    @property
    def number_throws(self) -> int:
        """
        Anzahl der bisherigen Würfe abfragen.
        :return: Anzahl der Würfe.
        """
        return self._number_throws

    @property
    def number_balls(self) -> int:
        """
        Anzahl der noch verfügbaren Kugeln
        :return: Anzahl der noch verfügbaren Kugeln.
        """
        return self._number_balls

    def throw(self, start_level: int) -> bool:
        """
        Ein Bowlingkugel werfen.
        Wurde vorher bei einem Wurf eine Kugel zerstört, wird die nächste verwendet.
        Sind alle Kugel zerstört, wird immer False ausgegeben.
        :param start_level: Aus dieser Höhe (Stockwerknummer) werfen.
        :return: True. falls die Kugel überstanden hat. False, wenn die Kugel zerstört ist.
        """
        assert start_level in LEVELS
        self._number_throws += 1
        if self._number_balls < 1:
            return False
        if start_level < self._destroy_level:
            return True
        assert start_level >= self._destroy_level
        self._number_balls -= 1
        return False


def calculate_throws(algorithm: Callable[[Balls], int], destroy_level: int) -> int:
    """
    Berechnet Anzahl der Würfe für die gegebene Höhe.
    :param algorithm: Diese Funktion ist der Algotithmus.
    :param destroy_level: Für diese Höhe soll der Algo verwendet werden.
    :return: Anzahl der Würfe, die der Algorithmus benötigt hat.
    """
    assert destroy_level in DESTROY_LEVELS
    balls = Balls(destroy_level)
    level = algorithm(balls)
    if level != destroy_level:
        raise RuntimeError("Algorithm fails at level " + str(destroy_level))
    return balls._number_throws


def algo_single_step(balls: Balls) -> int:
    """
    Einfacher Algorithmus:
    Immer ein Stockwerk höher, bis die Kugel zerstört ist.
    Das Stockwerk 0 muss nicht ausprobiert werden, weil jede Kugel den
    Fall aus dem Erdgeschoss übersteht.
    :param balls:  Die Kugeln für die Fallversuche.
    :return: Das Stockwerk, bei dem die Kugel zerstört wird.
    """
    for test_level in range(1, max(LEVELS) + 1):
        if not balls.throw(test_level):
            return test_level
    return max(LEVELS) + 1


def algo_matrix(balls: Balls) -> int:
    """
    'Matrix' oder 'Hacker' Algorithmus.
    Der Algo kennt die Simulation bzw. der Algo umgeht die Regeln. Eine
    Methode, die in der Praxis durchaus verwendet wird (siehe Manipulationen
    für verschiedene Testverfahren von verschiedenen Herstellern.)
    :param balls:  Die Kugeln für die Fallversuche.
    :return: Das Stockwerk, bei dem die Kugel zerstört wird.
    """
    return balls._destroy_level


def algo_binary(balls: Balls) -> int:
    """
    Algorithmus: Binäre-Suche mit der ersten Kugel, dann mit Einzelschritten suchen.
    :param balls: Die Kugeln für die Fallversuche.
    :return: Das Stockwerk, bei dem die Kugel zerstört wird.
    """
    last_ok_level = 0
    # Mit der ersten Kugel binäre Suche
    test_level = (min(LEVELS) + max(LEVELS)) // 2
    while test_level <= max(LEVELS) and balls.throw(test_level):
        last_ok_level = test_level
        test_level = max(test_level + 1, (test_level + max(LEVELS)) // 2)
    if balls.number_balls == 2:
        # Die while Schleife wurde beendet bevor die Kugel zerstört wurde.
        return max(LEVELS) + 1
    # Auf dem test_level wurde die Kugel zerstört
    fail_level = test_level
    test_level = last_ok_level + 1
    # Mit der zweiten Kugel nur noch die Stockwerk einzeln.
    while test_level < fail_level and balls.throw(test_level):
        test_level += 1
    return test_level


def algo_gold(balls: Balls) -> int:
    """
    Algorithmus: Binäre-Suche mit dem Teilverhältnis aus dem Goldnen Schnitt
    mit der ersten Kugel, dann mit Einzelschritten suchen.
    :param balls: Die Kugeln für die Fallversuche.
    :return: Das Stockwerk, bei dem die Kugel zerstört wird.
    """
    golden_ration = 0.38196601125
    last_ok_level = 0
    test_level = int((min(LEVELS) + max(LEVELS)) * golden_ration)
    while test_level <= max(LEVELS) and balls.throw(test_level):
        last_ok_level = test_level
        test_level += max(1, int((max(LEVELS) - test_level) * golden_ration))
    if balls.number_balls == 2:
        # Die while Schleife wurde beendet bevor die Kugel zerstört wurde.
        return max(LEVELS) + 1
    # Auf dem test_level wurde die Kugel zerstört
    fail_level = test_level
    test_level = last_ok_level + 1
    # Mit der zweiten Kugel nur noch die Stockwerk einzeln ausprobieren.
    while test_level < fail_level and balls.throw(test_level):
        test_level += 1
    return test_level


def algo_ration(balls: Balls) -> int:
    """
    Algorithmus: Binäre-Suche mit optimiertem Teilverhältnis mit der ersten Kugel,
    dann mit Einzelschritten suchen.
    Teilverhältnis -> Mittlere Anzahl: 0.10 -> 13.43 ; 0.19 -> 10.94 ;
    0.20 -> 10.94 ; 0.21 -> 10.96 ; 0.30 -> 12.30
    :param balls: Die Kugeln für die Fallversuche.
    :return: Das Stockwerk, bei dem die Kugel zerstört wird.
    """
    ration = 0.20
    last_ok_level = 0
    test_level = int((min(LEVELS) + max(LEVELS)) * ration)
    while test_level <= max(LEVELS) and balls.throw(test_level):
        last_ok_level = test_level
        test_level += max(1, int((max(LEVELS) - test_level) * ration))
    if balls.number_balls == 2:
        # Die while Schleife wurde beendet bevor die Kugel zerstört wurde.
        return max(LEVELS) + 1
    # Auf dem test_level wurde die Kugel zerstört
    fail_level = test_level
    test_level = last_ok_level + 1
    # Mit der zweiten Kugel nur noch die Stockwerk einzeln ausprobieren.
    while test_level < fail_level and balls.throw(test_level):
        test_level += 1
    return test_level


def algo_opt(balls: Balls) -> int:
    """
    Optimaler Algorithmus aus erster Musterlösung kopiert.
    Die Summe aus Würfe mit der ersten Kugel und maximal folgende Würfe
    mit der zweiten Kugel wird konstant gehalten. Entsprechend wird die
    Schrittweite (step) bei jedem Wurh der ersten Kugel um 1 reduziert.
    Der Startwert ergibt sich aus der Gaußschen Summenformel, aufgelöst
    nach der Anzahl der Werte.
    :param balls: Die Kugeln für die Fallversuche.
    :return: Das Stockwerk, bei dem die Kugel zerstört wird.
    """
    step = int(math.sqrt(2 * (max(LEVELS) - 2) + 1))
    last_ok_level = 0
    test_level = step
    while test_level <= max(LEVELS) and balls.throw(test_level):
        last_ok_level = test_level
        test_level += step
        step = max(1, step - 1)
    if balls.number_balls == 2:
        # Die while Schleife wurde beendet bevor die Kugel zerstört wurde.
        fail_level = max(LEVELS) + 1
    else:
        # Auf dem test_level wurde die Kugel zerstört
        fail_level = test_level
    test_level = last_ok_level + 1
    # Mit der zweiten Kugel nur noch die Stockwerk einzeln ausprobieren.
    while test_level < fail_level and balls.throw(test_level):
        test_level += 1
    return test_level


for algo in [algo_single_step, algo_matrix, algo_binary, algo_gold, algo_ration, algo_opt]:
    print("Teste Algorithmus", algo.__qualname__)
    number_throws = [calculate_throws(algo, destroy_level) for destroy_level in DESTROY_LEVELS]
    print("..", number_throws)
    print(".. maximale Anzahl", max(number_throws))
    print(".. minimale Anzahl", min(number_throws))
    print(".. mittlere Anzahl", statistics.mean(number_throws))
