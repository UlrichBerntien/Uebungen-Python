#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Programmieraufgabe:
    Kamele beladen
    https://www.programmieraufgaben.ch/aufgabe/kamele-beladen/6gddr4zm

    Ein Kamel soll optimal beladen werden. Das Kamel kann maximal 270 kg tragen.
    Aktuell sind Waren mit den folgenden Gewichten zu transportieren: 5, 18, 32,
    34, 45, 57, 63, 69, 94, 98 und 121 kg. Nicht alle Gewichte müssen verwendet
    werden; die 270 kg sollen aber möglichst gut, wenn nicht sogar ganz ohne
    Rest beladen werden. Die Funktion
        beladeOptimal(kapazitaet: integer, vorrat: integer[]): integer[]
    erhält die maximal tragbare Last (kapazitaet) und eine Menge von
    aufzuteilenden Gewichten (vorrat). Das Resultat (hier integer[]) ist die
    Auswahl aus dem Vorrat, die der Belastbarkeit möglichst nahe kommt. Gehen
    Sie wie folgt rekursiv vor: Für jedes vorhandene Gewicht g aus dem Vorrat
    soll das Problem vereinfacht werden. Dazu wird dieses Gewicht probehalber
    aufgeladen:
        tmpLadung: integer[]
        tmpLadung := beladeOptimal(kapazitaet - g, "vorrat ohne g")
    Danach wird das beste Resultat tmpLadung + g gesucht und als Array
    zurückgegeben. Behandeln Sie in der Methode beladeOptimal() zunächst die
    Abbruchbedingungen:
        Vorrat leer
        alle vorhandenen Gewichte sind zu schwer
        nur noch ein Gewicht im Vorrat

Author:
    Ulrich Berntien, 2018-06-08

Sprache:
    Python 3.6.6
"""

from typing import *


def optimal_load(capacity: int, pool: Tuple[int, ...]) -> Tuple[int, ...]:
    """
    Suche eine optimale Beladung.
    Optimal ist eine Beladung, wenn die Kapazität möglichst weitgehend verwendet wird.
    :param capacity: Bis zu dieser Grenze sollen Elemente aus dem pool genommen werden.
    :param pool: Aus diesem Pool können Elemente genommen werden.
    :return: Die Elemente der optimalen Beladung.
    """
    tmp_optimal_load: int = 0
    tmp_optimal_bag: Tuple[int, ...] = tuple()
    for index in range(len(pool)):
        if pool[index] <= capacity:
            bag = optimal_load(capacity - pool[index], pool[0:index] + pool[index + 1:])
            total = sum(bag) + pool[index]
            if total > tmp_optimal_load:
                tmp_optimal_load = total
                tmp_optimal_bag = pool[index:index + 1] + bag
    assert sum(tmp_optimal_bag) <= capacity
    assert all(x in pool for x in tmp_optimal_bag)
    return tmp_optimal_bag


camel_capacity = 270
camel_pool = (5, 18, 32, 34, 45, 57, 63, 69, 94, 98, 121)
# Mit mehr Elementen dauer es wesentlioh länger:
# camel_capacity =  1000
# camel_pool = (181, 130, 128, 125, 124, 121, 104, 101, 98, 94, 69, 61, 13)
camel_bag = optimal_load(camel_capacity, camel_pool)
camel_load = sum(camel_bag)
print("Beladung:", camel_bag)
print("Summe Beladung:", camel_load)
print("Freie Kapazität:", camel_capacity - camel_load)
