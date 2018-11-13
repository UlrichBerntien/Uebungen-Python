#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Buchstabenrätsel Summen
https://www.programmieraufgaben.ch/aufgabe/buchstabenraetsel-summen/mtt2cuwo
"""

# Programmieraufgabe:
#     Schreiben Sie ein Programm, das Symbolrätsel der folgenden Art (Summen)
#     löst:
#         aab + bbc = dde.
#     Dabei bedeuten gleiche Buchstaben auch immer gleiche Ziffern und
#     verschiedene Buchstaben bedeuten auch verschiedene Ziffern.
#
# Programmidee:
#     Sucht nach einer Lösung für die Buchtabenrätsel Summe. Es werden nicht alle
#     möglichen Lösungen gesucht, die Suche wird beim ersten Erfolg abgebrochen.
#     Gegeben ist eine Summe von Zahlen und das Ergebnis, dabei sind Ziffern durch
#     Buchstaben ersetzt. Jeder Buchstabe steht für eine andere Ziffer. Sind in der
#     Gleichung Ziffern enthalten, dann kann kein Buchstabe eine dieser Ziffern
#     sein. In den Summen und im Ergebnis können auch Ziffern vorgegeben sein.
#
#     Verwendet wird ein Backtracking-Algorithmus. Für ein Buchstaben werden alle
#     noch nicht verwendeten Ziffern ausprobiert.
#     Beschleunigt wird die Suche indem die Summe bereits teilweise berechnet wird.
#     So werden Fehler schneller erkannt und es können auch Buchstaben im Ergebnis
#     einer Ziffer zugeordnet werden.
#     Damit frühe gerechnet werden kann, werden die Buchstaben auf der rechten
#     Seite der Summanden zuerst durch Ziffern ersetzt.
#
# Autor, Erstellung:
#     Ulrich Berntien, 2018-10-30
#
# Sprache:
#     Python 3.6.6

import enum
import re
import string
from typing import *


def strip(strx: Any) -> Any:
    """
    Entfernt Leerzeichen am Anfang und Ende jedes Strings in der Struktur.
    :param strx: Dieser Struktur bearbeiten.
    :return: Neue Struktur mit allen Strings gestript.
    """
    if type(strx) is str:
        return strx.strip()
    else:
        return [strip(x) for x in strx]


def max_length(strx: Any) -> int:
    """
    Bestimmt die maximale Länge aller Strings in der Struktur.
    :param strx: Diese Struktur untersuchen.
    :return: Die maximale Stringlänge.
    """
    if type(strx) is str:
        return len(strx)
    elif type(strx) is dict:
        return max(max_length(value) for key, value in strx.items())
    else:
        return max(max_length(x) for x in strx)


def right_justified(strx: Any, width: int) -> Any:
    """
    Alle String in der Struktur rechtsbündig auf gleiche Länge bringen.
    :param strx: Diese Struktur bearbeiten.
    :param width: Auf diese Länge alle Strings bringen.
    :return: Kopie der Struktur mit den rechtsbündigen Strings.
    """
    if type(strx) is str:
        return strx.rjust(width)
    elif type(strx) is dict:
        result = {}
        for key, value in strx.items():
            result[key] = right_justified(value, width)
        return result
    else:
        return [right_justified(x, width) for x in strx]


def replace(strx: Any, old: str, new: str) -> Any:
    """
    In allen Strings der Struktur ersetzen.
    :param strx: In dieser Struktur ersetzen.
    :param old: Diesen Teil ersetzen.
    :param new: Diesen Teil einsetzen
    :return: Kopie mit der Ersetzung
    """
    if type(strx) is str:
        return strx.replace(old, new)
    elif type(strx) is dict:
        result = {}
        for key, value in strx.items():
            result[key] = replace(value, old, new)
        return result
    else:
        return [replace(x, old, new) for x in strx]


def remove(remove_from: str, to_remove: str) -> str:
    """
    Zeichen aus einem String entfernen.
    :param remove_from: Aus diesem String löschen.
    :param to_remove: Alle diese Zeichen aus dem String löschen.
    :return: Kopie des Strings ohne die Zeichen.
    """
    return "".join(c for c in remove_from if c not in to_remove)


def collect_letters(task: dict) -> str:
    """
    Alle verwendeten Buchstaben in der Aufgabe sammeln.
    Die Buchstaben werden sortiert in optimaler Lösungsreihenfolge.
    Zuerst kommen die Buchstaben, die rechts in den Summen benötigt werden.
    Sind die ersten Buchstaben bekannt, können weitere Stellen durch
    rechnen gefunden werden.
    :param task: Die Aufgabe.
    :return: Alle Buchstaben.
    """
    result = []
    # Von rechts die Buchstaben in den Summanden
    for index in reversed(range(len(task["calculate_letter_sum"]))):
        for summand in task["summands"]:
            c = summand[index]
            if c.isalpha() and c not in result:
                result.append(c)
    # Dann die Buchstaben in der Summe
    for c in task["calculate_letter_sum"]:
        if c.isalpha() and c not in result:
            result.append(c)
    return "".join(result)


def parse_letter_sum(letter_sum: str) -> dict:
    """
    Zerlegt die Buchstabenrätsel Summe in einzelne Summanden und ins Ergebnis.
    :param letter_sum: Die Buchstabenrätsel Summe.
    :return: Dictionary calculate_letter_sum: die Summe, summands: Liste der Summanden
    """
    left_right_split = re.fullmatch(r"\s*([a-zA-Z0-9]+\s*(?:\+\s*[a-zA-Z0-9]+)+)\s*=\s*([a-zA-Z0-9]+)", letter_sum)
    if left_right_split is None:
        raise RuntimeError("invalid calculate_letter_sum format" + letter_sum)
    summands = strip(left_right_split.group(1).split("+"))
    sum = left_right_split.group(2)
    return {"calculate_letter_sum": sum, "summands": summands}


def calculate_letter_sum(summands: List[str]) -> str:
    """
    Aufsummieren.
    :param summands: Liste der Summanden, die noch Buchstaben enthalten können.
    :return: Die Summe. Noch nicht berechenbare Stellen sind mit "?" gefüllt.
    """
    assert len(summands) > 0
    # Länge aller Zahlen ist gleich
    number_len = len(summands[0])
    # Ziffern in der Liste von hinten nach vorne sammeln
    result = []
    # ggf. Übertrag in die nächste Stelle
    overflow = 0
    # Flag wird gesetzt bei der ersten unbekannten Ziffer
    unknown = None
    for position in reversed(range(number_len)):
        accu = overflow
        for summand in summands:
            c = summand[position]
            if c.isdigit():
                accu += ord(c) - ord("0")
            elif c.isalpha():
                unknown = "?"
        result.append(chr(accu % 10 + ord("0")) if not unknown else unknown)
        overflow = accu // 10
    # Führende Nullen werden als Leerstellen geschrieben
    return "".join(reversed(result)).lstrip("0").rjust(number_len)


class CheckResult(enum.Enum):
    """
    Prüfungsergebmisse.
    """
    SOLVED = enum.auto()
    ERROR = enum.auto()
    OK = enum.auto()


def check(task: dict) -> Tuple[CheckResult, dict]:
    """
    Überprüfen wie weit die Aufgabe gelöst ist.
    CheckResult.SOLVED -> alle Ziffern sind gefunden und Summe ist korrekt.
    CheckResult.ERROR -> die vorhandenen Ziffern passen nicht zusammen.
    CheckResult.OK -> es ist kein Fehler sichtbar.
    :param task: Dise Aufgabe prüfen.
    :return: Tupel aus Ergebnis und gefundenen Ziffern für Buchstaben.
    """
    calculated_sum = calculate_letter_sum(task["summands"])
    task_sum = task["calculate_letter_sum"]
    if task_sum == calculated_sum:
        return CheckResult.SOLVED, {}
    found = {}
    for index in range(len(calculated_sum)):
        if task_sum[index] != calculated_sum[index]:
            if calculated_sum[index] in task["digits"] and task_sum[index].isalpha():
                found[task_sum[index]] = calculated_sum[index]
            elif calculated_sum[index].isdigit():
                return CheckResult.ERROR, {}
    return CheckResult.OK, found


def solve_step(task: dict, letter: str, digit: str) -> dict:
    """
    Eine Zuordnung in die Aufgabe eintragen.
    :param task: Diese Aufgabe ist zu lösen.
    :param letter: Dieser Buchstabe wird ersetzt.
    :param digit: Den Buchstaben durch diese Ziffer ersetzen.
    :return: Die teilweise gelöste Aufgabe
    """
    assert len(letter) == 1 and letter.isalpha()
    assert len(digit) == 1 and digit.isdigit()
    assert digit in task["digits"] and letter in task["letters"]
    # Den Buchstaben ersetzen
    task = replace(task, letter, digit)
    # Die Ziffer steht nicht mehr zur verfügung
    task["letters"] = remove(task["letters"], digit)
    # Der Buchstabe ist jetzt bekannt (wurde zur Ziffer)
    task["digits"] = remove(task["digits"], digit)
    assert digit not in task["digits"] and letter not in task["letters"]
    return task


def solve(task: dict) -> dict:
    """
    Rekursive Programmierung eines Backtracking Algorithmus.
    :param task: Teilwiese gelöste Aufgabe.
    :return: Vollständig gelöste Aufgabe oder Aufgabe ungelöst zurück.
    """
    status, founds = check(task)
    # Durch Rechnung gefundene Ziffern eintragen
    while founds:
        for letter, digit in founds.items():
            task = solve_step(task, letter, digit)
        # Nach dem Einsetzen können weitere Ziffern berechnet werden.
        status, founds = check(task)
    if status is CheckResult.OK:
        # bisher ist kein Fehler sichtbar
        if len(task["letters"]) > 0:
            # Es sind noch nicht alle Buchstaben zugeordnet
            letter = task["letters"][0]
            # Alle möglichen Ziffern für den Buchstaben ausprobieren
            for digit in task["digits"]:
                test = solve_step(task, letter, digit)
                test_result = solve(test)
                status, founds = check(test_result)
                # Bei einer Lösung die Suche abbrechen
                if status is CheckResult.SOLVED:
                    return test_result
    return task


def solve_letter_sum(letter_sum: str) -> str:
    """
    Sucht nach einer Lösung für die Buchtabenrätsel Summe.
    Gegeben ist eine Summe von Zahlen und das Ergebnis, dabei sind Ziffern durch
    Buchstaben ersetzt. Jeder Buchstabe steht für eine andere Ziffer. Sind in der
    Gleichung Ziffern enthalten, dann kann kein Buchstabe eine dieser Ziffern sein.
    :param letter_sum: Die Buchstabenrätsel Summe.
    :return: Eine Lösung, wenn keine Lösung gefunden wurde nur teilweise gelöst.
    """
    task = parse_letter_sum(letter_sum)
    # gleiche Anzahl von Stellen bei allen Zahlen vereinfacht rechnen und vergleichen
    # "+1" damit ist sichergestellt, dass ein möglicher Übertrag berücksichtigt wird
    task = right_justified(task, max_length(task) + 1)
    task["letters"] = collect_letters(task)
    task["digits"] = remove(string.digits, letter_sum)
    if len(task["digits"]) < len(["letters"]):
        raise RuntimeError("more letters than unused digits")
    solution = solve(task)
    return remove("+".join(solution["summands"]) + "=" + solution["calculate_letter_sum"], " ")


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
        solution = solve_letter_sum(test)
        # Nachrechnen der gefundenen Lösung
        assert eval(solution.replace("=", "=="))
        print(". . . .:", solution)
