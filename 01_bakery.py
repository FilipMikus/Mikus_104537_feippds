"""
Modul obsahujúci implementáciu Bakery algorytmu.
"""

__author__ = "Filip Mikuš"
__email__ = "xmikusf@stuba.sk"
__license__ = "MIT"

PROCES_POCET: int = 11
tiket: list = [0 for i in range(PROCES_POCET)]
vyber_tiket: list = [False for j in range(PROCES_POCET)]

def bakery_proces(proces_id: int):

    global PROCES_POCET, tiket, vyber_tiket

    i: int = proces_id
    vyber_tiket[i] = True
    tiket[i] = 1 + max(tiket)
    vyber_tiket[i] = False

    for j in range(PROCES_POCET):

        while vyber_tiket[j]:
            continue

        while tiket[j] != 0 and (tiket[j] < tiket[i] or (tiket[j] == tiket[i] and j < i)):
            continue