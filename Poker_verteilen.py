#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Programmieraufgabe:
    Poker verteilen
    https://www.programmieraufgaben.ch/aufgabe/poker-verteilen/i4si4ts5

    Schreiben Sie ein Programm, das vier Spielerinnen je fünf Pokerkarten verteilt.
    Dabei ist ein Array zunächst mit den Zahlen 1 bis 55 zu füllen. Am einfachsten
    verwenden Sie dazu die Indizes 1 bis 55. 1-13 entspricht den Herz-Karten,
    14-26 sind die Pik-Karten, danach folgen 13 Karo- und zuletzt die Kreuz-Karten.
    Die Nummern 53, 54 und 55 sind die drei Joker-Karten. Die erste bis und mit
    die zehnte Karte pro Farbe sind jeweils die Zahl-Karten, die elfte entspricht
    dem Jungen (J), die zwölfte der Queen (Q = Dame) und die dreizehnte. ist der
    König (K).
    Mischen Sie den Array nach folgendem Algorithmus (D. Knuth: The Art of
    Computer Programming Vol. 2; ISBN 0-201-89684-2; Addison-Wesley; S. 145
    Shuffling) und verteilen Sie die ersten 20 Karten reihum an vier Spielende.
    Misch-Algorithmus:
        mischenAbPos := 1
        while(mischenAbPos < 55)
        {
          zufallsPos   := zufällige Position aus den Zahlen [mischenAbPos bis 55]
          vertausche die Elemente "array[mischenAbPos]" mit "array[zufallsPos]"
          mischenAbPos := mischenAbPos + 1
        }

Author:
    Ulrich Berntien, 2018-08-31

Sprache:
    Python 3.6.6
"""

from typing import *
import random


class Karte:
    """
    Eine Spielkarte.
    Alle Spielkarten sind mit einem Code 1 .. 55 versehen über den die Karte erzeugt wird.
    """

    def __init__(self, code: int) -> None:
        """
        Eine Karte mit gegebenen Code erzeugen.
        :param code: Code der Karte, Bereich 1 .. 54.
        """
        assert 1 <= code <= 55
        self._code: int = code

    @property
    def code(self) -> int:
        """
        Der Code der Karte.
        :return: Der Code der Karte.
        """
        return self._code

    def __eq__(self, other) -> bool:
        """
        Vergleichsoperator.
        :param other: Mit diesem Objekt wird verglichen.
        :return: True, genau dann, wenn die Karten den gleichen Code haben.
        """
        return isinstance(self, other.__class__) and self._code == other.code

    def __repr__(self) -> str:
        """
        Darstellung der Karte.
        :return: Name der Karte.
        """
        assert 1 <= self._code <= 55
        assert len(self._wert_name) == 13
        if self._code <= 52:
            return self._gruppen_name[(self._code - 1) // 13] + " " + self._wert_name[(self._code - 1) % 13]
        else:
            return "Joker"

    # Namen der Kartengruppen. Jede Gruppe enthält 13 Werte
    _gruppen_name: Tuple[str, ...] = ("Herz", "Pik", "Karo", "Kreuz")

    # Namen der 13 Werte
    _wert_name: Tuple[str, ...] = tuple(str(i) for i in range(1, 11)) + ("Junge", "Dame", "König")


def riffle(block: List) -> None:
    """
    Mischen einer Liste mit dem gegebenen Algorithmus.
    :param block: Der Inhalt dieser Liste wird gemischt.
    """
    for index_a in range(len(block)):
        index_b = random.randrange(index_a, len(block))
        assert index_a <= index_b < len(block)
        block[index_a], block[index_b] = block[index_b], block[index_a]


kartenspiel = [Karte(i) for i in range(1, 56)]
print(kartenspiel)
riffle(kartenspiel)
# Kontrolle: Alle Karten sind noch im Spiel
assert all(Karte(i) in kartenspiel for i in range(1, 56))
# Kontrolle: Die Anzahl der Karten stimmt noch, also kann keine Karte doppelt sein.
assert len(kartenspiel) == 55
for person in range(4):
    print("Karten für Person {}:".format(person + 1), kartenspiel[person * 5:person * 5 + 5])
