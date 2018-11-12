#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Programmieraufgabe:
    Ganze Zufallszahlen
    https://www.programmieraufgaben.ch/aufgabe/ganze-zufallszahlen/8v6nj82y

    Die meisten Programmiersprachen kennen einen Zufallszahlengenerator, der
    eine (pseudo-)zufällige Zahl zwischen 0.0 (inklusive) und 1.0 (exklusive)
    erzeugt.
    Schreiben Sie eine Funktion, die eine solche gleichverteilte Zufallszahl
    in eine ganze Zufallszahl von min bis max umwandelt:

Author:
    Ulrich Berntien, 2018-10-27

Sprache:
    Python 3.6.6
"""

import collections
import random
from typing import *


def zufall(nullEinsVerteilt: float, min: int, max: int) -> int:
    """
    Transformiere Zahl aus [0,1( auf den Bereich min..max mit Ganzen Zahlen.
    :param nullEinsVerteilt: Zahl [0,1(
    :param min: Kleinste Ganze Zahl
    :param max: Größte Ganze Zahl
    :return: Ganze Zahl aus dem definierten Bereich.
    """
    assert 0.0 <= nullEinsVerteilt < 1.0
    assert int(min) == min and int(max) == max and min < max
    return int(min + (max - min + 1) * nullEinsVerteilt)


if __name__ == '__main__':
    counter = collections.Counter()
    for i in range(30):
        counter[zufall(random.random(), 5, 7)] += 1
    for number in sorted(counter.keys()):
        print("Zahl", number, "aufgetaucht", counter[number], "mal")
