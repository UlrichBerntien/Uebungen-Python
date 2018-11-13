#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Schnurlängen
https://www.programmieraufgaben.ch/aufgabe/schnurlaengen/acgo5ap7
"""

# Programmieraufgabe:
#     Eine Schnur mit einer Gesamtlänge von 450 m soll in Teilstücke der Länge
#     17 m, 19m und 21 m geteilt werden. Ist das ohne Rest möglich? Die Frage
#     reduziert sich darauf, ob eine der drei Differenzen
#         450 - 17 = 433,
#         450 - 19 = 431 und
#         450 - 21 = 429
#     ohne Rest aufgeschnitten werden kann. Denn wenn dies für eine der genannten
#     drei Differenzen möglich ist, so ist es sicher auch für 450 m möglich.
#     Schreiben Sie eine Methode zerlegbar(gesamt, laenge1, laenge2, laenge3),
#     die im Wesentlichen prüft, ob eine der drei Bedingungen
#         zerlegbar(gesamt-laenge1, laenge1, laenge2, laenge3),
#         zerlegbar(gesamt-laenge2, laenge1, laenge2, laenge3) oder
#         zerlegbar(gesamt-laenge3, laenge1, laenge2, laenge3)
#     zutrifft.
#
# Autor, Erstellung:
#     Ulrich Berntien, 2018-08-24
#
# Sprache:
#     Python 3.6.6


from typing import *


def zerlegbar(gesamt_laenge: int, teil_laengen: Iterable[int]) -> bool:
    """
    Kontrolliert ob Gesamtlänge in einzelne Längen zerlebar ist.
    :param gesamt_laenge:  Die zu zerlegende Gesamtlänge.
    :param teil_laengen:  In diese Längen kann zerlegt werden.
    :return: True, genau dann wenn die Gesamtlänge ohne Rest in die Teillängen zerlegbar ist.
    """
    assert gesamt_laenge > 0
    assert all(l > 0 for l in teil_laengen)
    for laenge in teil_laengen:
        if gesamt_laenge == laenge:
            # passt genau
            return True
        elif gesamt_laenge > laenge:
            if zerlegbar(gesamt_laenge - laenge, teil_laengen):
                return True
    # Keine Möglichkeit gefunden
    return False


tests = ((450, (17, 19, 21)),
         (100, (17, 19, 21)),
         (101, (17, 19, 21)))
for (test_gesamt, test_laengen) in tests:
    test_zerlegbar = zerlegbar(test_gesamt, test_laengen)
    print("Gesamtlänge {0} zerlegbar in {1}: {2}".format(test_gesamt, test_laengen, test_zerlegbar))
