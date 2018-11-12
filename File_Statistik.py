#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Programmieraufgabe:
    File Statistik
    https://www.programmieraufgaben.ch/aufgabe/file-statistik/gcx87ud7

    Schreiben Sie ein Programm, das von einer Datei (Textdatei oder Programm-
    Quellcode) die Anzahl Zeilen, die Anzahl Wörter und die Anzahl Buchstaben
    (ohne Leerschläge und Sonderzeichen) ausgibt.

Diskussion der Aufgabenstellung:
    - Welcher Zeichensatz (ASCII,Unicode,EBCDIC) wird in der Datei verwendet?
      Lösung: Standardmethode von Python verwenden und alle Sonderfälle
      ignorieren.
    - Mit welchem Zeichen wird eine Zeile abgeschlossen? (CR, CR+LF, LF)
      Lösung: Standardmethode von Python verwenden und alle Sonderfälle
      ignorieren.
    - Was ist ein Buchstabe (ä ist Buchstabe oder ein Sonderzeichen)?
      Lösung: isalpha Methode von Python verwenden.
    - Was ist ein Wort?
      Lösung: Eine Gruppe von Zeichen, die mit einem Leerzeichen oder dem
      Zeilenende getrennt sind und mindestens einn Buchstaben enthalten.
      Beispiele: Kein Wort: "12" oder "12."
      Ein Wort: "Test" oder "Test,Frage" oder "12-Ender"
    - Was ist ein Leerzeichen?
      Lösung: isspace Methode von Python verwenden.
    - Zeilenfortsetzungen behandeln?
      Lösung: Ignorieren.
    - Worttrennungen behandeln?
      Lösung: Das "-" als Trennzeichen behandeln, wie in der Test-Datei zur
      Aufgabe.

Author:
    Ulrich Berntien, 2018-08-03

Sprache:
    Python 3.6.6
"""

import fileinput
import sys

if len(sys.argv) != 2:
    print("Das Skript muss mit einen Dateinamen als Parameter aufgerufen werden.")
else:
    # Zähler für die Eingabe
    count_lines = 0
    count_words = 0
    count_alpha = 0
    count_printable = 0
    # Zähler nur innerhalb eines Worts
    count_alpha_inword = 0
    # fileinput erlaubt auch mehr als eine Datei.
    for line in fileinput.input():
        # Am Ende von line ist immer ein isspace, das CR o.ä. Zeichen
        assert line[-1].isspace()
        count_lines += 1
        for index, char in enumerate(line):
            if char.isalpha():
                count_alpha += 1
                count_alpha_inword += 1
            if char.isspace():
                if count_alpha_inword > 0:
                    # Nicht ein Teilwort mit "-" am Ende der Zeile zählen
                    if not (line[index - 1:index] == "-" and line[index:].isspace()):
                        count_words += 1
                        count_alpha_inword = 0
            if char.isprintable():
                count_printable += 1
    print("Anzahl Zeilen:", count_lines)
    print("Anzahl Wörter:", count_words)
    print("Anzahl Buchstaben:", count_alpha)
    print("Anzahl Zeichen:", count_printable)
