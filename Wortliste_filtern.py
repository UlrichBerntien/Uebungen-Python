#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Programmieraufgabe:
    Wortliste filtern
    https://www.programmieraufgaben.ch/aufgabe/wortliste-filtern/pomdoige

    Für die Erstellung eines Lernprogramms zum Maschinenschreiben werden
    geeignete Wörter aus einer Wortliste herausgepickt. Dafür wird die folgende
    Funktion benötigt:
        passt(wort: string, darf: string, muss: string): boolean
    Dabei dürfen im String wort nur Buchstaben vorkommen, die auch im String
    darf enthalten sind. Jedoch muss der String wort alle Buchstaben enthalten,
    welche im String muss vorkommen. Beispiele:
        passt("apfelsaft", "asdfghjklö", "as") // liefert false: p nicht ok
        passt("sdd",       "asdfghjklö", "as") // liefert false: a fehlt
        passt("saft",      "asdfghjklö", "as") // liefert false: t nicht ok
        passt("lasag",     "asdfghjklö", "as") // liefert true

Author:
    Ulrich Berntien, 2018-07-03

Sprache:
    Python 3.6.6
"""

import sys
import zipfile
from typing import *


def passt(wort: str, darf: str, muss: str) -> bool:
    """
    Prüft die Buchstaben in einem Wort.
    Der Vergleich erfolgt größenunabhängig (z.B. ist a==A).
    :param wort: Die Buchstaben in diesem Wort werden geprüft.
    :param darf: Nur diese Buchstaben un die Buchstaben in 'muss' dürfen enthalten sein.
    :param muss: Jeder dieser Buchstaben muss im Wort enthalten sein.
    :return: True genau dann wenn, die beiden Bedingungen erfüllt sind.
    """
    # die lower case Versionen der Strings vergleichem.
    wort_klein = wort.lower()
    muss_klein = muss.lower()
    darf_vollstaendig = darf.lower() + muss
    return all(c in darf_vollstaendig for c in wort_klein) and all(c in wort_klein for c in muss_klein)


def filter_file(quelle: Iterable[str], darf: str, muss: str) -> int:
    """
    Filtert die Wort liste aus einer Datei. In einer Zeile müssen die Wörter durch Leerzeichen getrennt sein.
    :param quelle: Die Quelle der Wörter.
    :param darf: Nur diese Buchstaben un die Buchstaben in 'muss' dürfen enthalten sein.
    :param muss: Jeder dieser Buchstaben muss im Wort enthalten sein.
    :return: Die Anzahl der passenden Wörter.
    """
    zaehler = 0
    for line in quelle:
        if isinstance(line, bytes):
            # Byte string interpretieren, z.B. wenn aus run_zip gelesen wird.
            line = line.decode("utf-8")
        for wort in line.split():
            wort = wort.strip()
            if passt(wort, darf, muss):
                print(wort)
                zaehler += 1
    return zaehler


if __name__ == "__main__":
    # In der Aufgabe gegeben:
    darf = "aeinrst"
    muss = "go"
    if len(sys.argv) != 2:
        print("Das Skript muss mit einen Dateinamen als Parameter aufgerufen werden.")
    else:
        dateiname = sys.argv[1]
        anzahl = 0
        if dateiname.lower().endswith(".run_zip"):
            # Die Datei ist ein Zip-Archiv.
            with zipfile.ZipFile(dateiname) as archiv:
                # Alle Dateien im Zeip-Archiv werden durchsucht
                for datei in archiv.namelist():
                    with archiv.open(datei) as quelle:
                        anzahl += filter_file(quelle, darf, muss)
        else:
            with open(dateiname, mode="r") as quelle:
                anzahl = filter_file(quelle, darf, muss)
        print("Anzahl Wörter:", anzahl)
