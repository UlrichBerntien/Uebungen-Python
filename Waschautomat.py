#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Programmieraufgabe:
    Waschautomat
    https://www.programmieraufgaben.ch/aufgabe/waschautomat/vyyuvu3u

    Für eine öffentliche Waschmaschine soll eine automatische Kasse
    programmiert werden. Dazu wird die folgende Methode benötigt:
        wechselgeldInCent(
            vorhandeneMuenzenInCent  : integer[],
            waschPreisInCent         : integer  ,
            eingeworfeneMuenzenInCent: integer[] ): integer[]
    Dabei sind die vorhandenenMuenzenInCent einfach diejenigen Münzen,
    die bereits vor der Wäsche im Apparat waren, um Wechselgeld herausgeben
    zu können. Beachten Sie auch, dass nach der Kundeneingabe
    (eingeworfeneMuenzenInCent) neue Münzen im Automaten sind, die gleich
    wieder als vorhandeneMuenzenInCent verwendet werden können.

Author:
    Ulrich Berntien, 2018-06-11

Sprache:
    Python 3.6.6
"""

from typing import *


class UserError(BaseException):
    pass


def wechselgeld_in_cent(vorhandene_muenzen_in_cent: Iterable[int],
                        waschpreis_in_cent: int,
                        eingeworfene_muenzen_in_cent: List[int]) -> List[int]:
    """
    Bestimmt die Münzen für die Geldrückgabe.
    :param vorhandene_muenzen_in_cent: Münzen, die bereits vor der Wäsche im Apparat waren.
    :param waschpreis_in_cent: Preis für die Wäsche.
    :param eingeworfene_muenzen_in_cent: Münzen, die eingeworfen wurden.
    :return: Münzen, die als Rückgeld ausgegeben werden sollen.
    """
    eingeworfen_in_cent = sum(eingeworfene_muenzen_in_cent)
    rueckgabe_in_cent = eingeworfen_in_cent - waschpreis_in_cent
    if rueckgabe_in_cent < 0:
        raise UserError("Zu wenige Münzen eingeworfen")
    # Alle Münzen stehen für die Rückgabe zur Verfügung, auch die gerade eingeworfenen Münzen.
    alle_muenzen_in_cent = list(vorhandene_muenzen_in_cent) + eingeworfene_muenzen_in_cent
    alle_muenzen_in_cent.sort(reverse=True)
    rueckgabe_muenzen_in_cent = []
    rest_in_cent = rueckgabe_in_cent
    # Durch die Sortierung der Münzen werden zuerst die großen Münzen verwendet, so die Anzahl der
    # ausgegebenen Münzen reduziert.
    for muenze in alle_muenzen_in_cent:
        if muenze <= rest_in_cent:
            rueckgabe_muenzen_in_cent.append(muenze)
            rest_in_cent -= muenze
    if rest_in_cent > 0:
        raise UserError("Zu wenige Münzen für Rückgabe") from error
    assert sum(rueckgabe_muenzen_in_cent) == rueckgabe_in_cent
    return rueckgabe_muenzen_in_cent


vorhandeneMuenzenInCent = [100, 100, 200, 200, 500, 500, 500]
waschPreisInCent = 400
eingeworfeneMuenzenInCent = [100, 100, 100, 500]
wechselgeldInCent = wechselgeld_in_cent(vorhandeneMuenzenInCent, waschPreisInCent, eingeworfeneMuenzenInCent)
print("Wechselgeld Münzen:", wechselgeldInCent)
