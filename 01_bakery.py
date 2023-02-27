from time import sleep
from fei.ppds import Thread

"""
Modul obsahujúci implementáciu Bakery algorytmu.
"""

__author__ = "Filip Mikuš"
__email__ = "xmikusf@stuba.sk"
__license__ = "MIT"

PROCES_POCET = 11
tiket = [0 for i in range(PROCES_POCET)]
vyber_tiket = [False for j in range(PROCES_POCET)]


def bakery_proces(proces_id: int):
    """
    Funkcia simulujúca proces.

    Argumenty:
        proces_id: Identifikátor procesu.
    """

    global PROCES_POCET, tiket, vyber_tiket

    i = proces_id
    vyber_tiket[i] = True
    tiket[i] = 1 + max(tiket)
    vyber_tiket[i] = False

    for j in range(PROCES_POCET):

        while vyber_tiket[j]:
            continue

        while tiket[j] != 0 and \
                (tiket[j] < tiket[i] or (tiket[j] == tiket[i] and j < i)):
            continue

    print(f"Proces [id: {proces_id}] vykonáva kritickú oblasť.")
    sleep(3)

    tiket[i] = 0


if __name__ == '__main__':
    procesy = [Thread(bakery_proces, i) for i in range(PROCES_POCET)]
    [proces.join() for proces in procesy]
