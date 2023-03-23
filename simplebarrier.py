"""
Modul obsahujúci implementáciu jednoducej bariéry.
Zdroj: https://www.youtube.com/watch?v=3KJv9hFTx6k&t=876s
"""


__authors__ = "Filip Mikuš, Matúš Jókay"
__email__ = "xmikusf@stuba.sk, matus.jokay@stuba.sk"
__license__ = "MIT"


from fei.ppds import Mutex, Semaphore, print


class SimpleBarrier:
    """
    Trieda implementujúca funkcionalitu synchronizačného mechanizmu bariéra.

    Atribúty:
        n: Premenná reprezentujúca celkový počet synchronizovaných procesov.
        c: Premenná reprezentujúca počítadlo procesov čakajúcich pri bariére.
        mutex: Mutex na manipuláciu s premennou c.
        semaphore: Synchronizačný mechanizmus (Semaphore).
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
        self.semaphore = Semaphore(0)


    def wait(self):
        """
        Metóda implementujúca čakanie volajúceho procesu pri bariére.
        """

        self.mutex.lock()
        self.c += 1
        if self.c == self.n:
            self.c = 0
            self.semaphore.signal(self.n)
        self.mutex.unlock()
        self.semaphore.wait()


    def wait_vypis(self, vlakno_vypis, vlakna_stretnutie_vypis):
        """
        Metóda implementujúca čakanie volajúceho procesu pri bariére.
        """

        self.mutex.lock()
        self.c += 1
        print(vlakno_vypis)
        if self.c == self.n:
            self.c = 0
            print(vlakna_stretnutie_vypis)
            self.semaphore.signal(self.n)
        self.mutex.unlock()
        self.semaphore.wait()