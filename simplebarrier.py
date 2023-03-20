"""
Modul obsahujúci implementáciu jednoducej bariéry s využitím objektu Event (fei.ppds).
Zdroj: https://www.youtube.com/watch?v=3KJv9hFTx6k&t=876s
"""


__authors__ = "Filip Mikuš, Matúš Jókay"
__email__ = "xmikusf@stuba.sk, matus.jokay@stuba.sk"
__license__ = "MIT"


from fei.ppds import Mutex, Event


class SimpleBarrier:
    """
    Trieda implementujúca funkcionalitu synchronizačného mechanizmu bariéra.

    Atribúty:
        n: Premenná reprezentujúca celkový počet synchronizovaných procesov.
        c: Premenná reprezentujúca počítadlo procesov čakajúcich pri bariére.
        mutex: Mutex na manipuláciu s premennou c.
        event: Synchronizačný mechanizmus (Event).
    """

    def __init__(self, n):
        """
        Metóda na inicializáciu objektu SimpleBarrier, jeho premenných a objektov.

        Argumenty:
            n: Počet synchronizovaných procesov.
        """

        self.n = n
        self.c = 0
        self.mutex = Mutex()
        self.event = Event()


    def wait(self):
        """
        Metóda implementujúca čakanie volajúceho procesu pri bariére.
        """

        self.mutex.lock()
        if self.c == 0:
            self.event.clear()
        self.c += 1
        if self.c == self.n:
            self.event.signal()
        self.mutex.unlock()
        self.event.wait()