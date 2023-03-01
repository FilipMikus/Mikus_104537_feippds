"""
Modul obsahujúci implementáciu holičstva s predbiehaním.
"""


__authors__ = "Filip Mikuš, Marián Šebeňa"
__email__ = "xmikusf@stuba.sk, mariansebena@stuba.sk, xvavro@stuba.sk"
__license__ = "MIT"


from fei.ppds import Mutex, Semaphore


ZAKAZNIK_POCET: int = 5
CAKAREN_MAX_KAPACITA: int = 3


class Barbershop(object):

    def __init__(self):

        self.mutex: Mutex = Mutex()
        self.cakaren: int = 0
        # rendezvous 1
        self.zakaznik_pripraveny: Semaphore = Semaphore(0)
        self.barber_pripraveny: Semaphore = Semaphore(0)
        # rendezvous 2
        self.zakaznik_koniec_obsluhy: Semaphore = Semaphore(0)
        self.barber_koniec_obsluhy: Semaphore = Semaphore(0)