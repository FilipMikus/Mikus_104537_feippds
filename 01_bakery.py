"""
Modul obsahujúci implementáciu Bakery algorytmu.
"""

__author__ = "Filip Mikuš"
__email__ = "xmikusf@stuba.sk"
__license__ = "MIT"

PROCES_POCET: int = 11
tiket: list = [0 for i in range(PROCES_POCET)]
vyber_tiket: list = [False for j in range(PROCES_POCET)]