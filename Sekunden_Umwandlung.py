#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Sekunden-Umwandlung
https://www.programmieraufgaben.ch/aufgabe/sekunden-umwandlung/sxmwsks3
"""

# Programmieraufgabe:
#     Schreiben Sie ein Programm, das eine Anzahl Sekunden in die Form
#     "h:mm:ss" (h = Stunden, mm = Minuten und ss = Sekunden) bringt.
#     Zum Beispiel wird die Zahl 3674 in die Zeichenkette "1:01:14" umgewandelt.
#
# Autor, Erstellung:
#     Ulrich Berntien, 2018-08-06
#
# Sprache:
#     Python 3.6.6


import re


def hms_to_seconds(hms: str) -> int:
    """
    Konvertiert eine Angabe "h:mm:ss" in the Anzahl der Sekunden.
    :param hms: Zeit im Format "stunde:minuten:sekunden"
    :return: Zeit in Sekunden
    """
    match = re.match(r"(\d+):(\d+):(\d+)$", hms)
    if not match:
        raise RuntimeError("invalid hms format: " + hms)
    hours_part = int(match.group(1))
    minutes_part = int(match.group(2))
    seconds_part = int(match.group(3))
    if minutes_part > 59 or seconds_part > 59:
        raise RuntimeError("invalid hms format: " + hms)
    return seconds_part + ((hours_part * 60) + minutes_part) * 60


def seconds_to_hms(seconds: int) -> str:
    """
    Konvertiert Sekundenangabe in "h:mm:ss" Format.
    :param seconds: Anzahl der Sekunden.
    :return: Zeit in Stunden:Minuten:Sekunden Format.
    """
    if seconds < 0:
        sign = "-"
        seconds = -seconds
    else:
        sign = ""
    seconds_part = seconds % 60
    minutes = seconds // 60
    minutes_part = minutes % 60
    hours = minutes // 60
    return "%s%d:%02d:%02d" % (sign, hours, minutes_part, seconds_part)


# Tests der beiden Funktionen:
for seconds_test in (3674, 367400, -3674):
    print("seconds =", seconds_test, "-> hms =", seconds_to_hms(seconds_test))

for hms_test in ("1:01:14", "0:00:10", "0:01:00", "1:00:00", "100:00:00"):
    print("hms =", hms_test, "-> seconds =", hms_to_seconds(hms_test))
