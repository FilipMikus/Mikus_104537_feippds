"""
Modul obsahujúci implementáciu hodujúcich divochov s viacerými kuchármi.
"""


__authors__ = "Filip Mikuš, Marián Šebeňa, Tomáš Vavro"
__email__ = "xmikusf@stuba.sk, mariansebena@stuba.sk, xvavro@stuba.sk"
__license__ = "MIT"


from fei.ppds import Event, Semaphore, Mutex, Thread, print
from time import sleep
from simplebarrier import SimpleBarrier


PORCIA_POCET = 5
DIVOCH_POCET = 3
KUCHAR_POCET = 5


class Usadlost:
    """
    Trieda reprezentujúca Usadlost a jeho zdieľané premenné.

    Atribúty:
        divoch_mutex: Mutex na manipuláciu divochom s premennou porcie.
        kuchar_mutex: Mutex na manipuláciu kuchárom s premennou porcie.
        porcie: Premenná reprezentujúca počet porcií v hrnci.
        plny_hrniec: Signalizačný Semafór plného hrnca.
        prazdny_hrniec: Signalizačný Semafór prázdneho hrnca.
        divoch_bariera_1: Bariéra (1.) synchronizujúca spoločné hodovanie divochov.
        divoch_bariera_2: Bariéra (2.) synchronizujúca spoločné hodovanie divochov.
    """

    def __init__(self):
        """
        Metóda na inicializáciu objektu Usadlost a jeho zdieľaných premenných.
        """

        self.divoch_mutex = Mutex()
        self.kuchar_mutex = Mutex()
        self.porcie = 0
        self.plny_hrniec = Semaphore(0)
        self.prazdny_hrniec = Event()
        self.divoch_bariera_1 = SimpleBarrier(DIVOCH_POCET)
        self.divoch_bariera_2 = SimpleBarrier(DIVOCH_POCET)


def hodovanie(proces_id: int):
    """
    Funkcia reprezentujúca hodovanie divocha.

    Argumenty:
        proces_id: Identifikátor procesu.
    """

    print(f"Divoch [id: {proces_id}] hoduje.")
    sleep(3)


def varenie(proces_id: int):
    """
    Funkcia reprezentujúca varenie kuchára.

    Argumenty:
        proces_id: Identifikátor procesu.
    """

    print(f"Kuchár [id: {proces_id}] varí.")
    sleep(5)


def nabratie_porcia(proces_id: int):
    """
    Funkcia reprezentujúca nabratie porcie divochom.

    Argumenty:
        proces_id: Identifikátor procesu.
    """

    print(f"Divoch [id: {proces_id}] si naberá porciu.")


def najdenie_prazdny_hrniec(proces_id: int):
    """
    Funkcia reprezentujúca nájdenie prázdneho hrnca divochom.

    Argumenty:
        proces_id: Identifikátor procesu.
    """

    print(f"Divoch [id: {proces_id}] našiel prázdny hrniec a upovedumuje kuchárov.")


def servirovanie_plny_hrniec(proces_id: int):
    """
    Funkcia reprezentujúca servírovanie plného hrnca kuchárom.

    Argumenty:
        proces_id: Identifikátor procesu.
    """

    print(f"Kuchár [id: {proces_id}] upovedomuje divochov o naplnení hrnca.")


def divoch_proces(proces_id: int, usadlost: Usadlost):
    """
    Funkcia simulujúca proces reprezentujúci divocha.

    Argumenty:
        proces_id: Identifikátor procesu.
        usadlost: Usadlost objekt obsahujúci zdieľané premenné.
    """

    while True:
        usadlost.divoch_bariera_1.wait()
        usadlost.divoch_bariera_2.wait()
        usadlost.divoch_mutex.lock()
        if usadlost.porcie == 0:
            # prázdny hrniec
            najdenie_prazdny_hrniec(proces_id)
            usadlost.prazdny_hrniec.signal()
            usadlost.plny_hrniec.wait()
        # hodovanie
        nabratie_porcia(proces_id)
        usadlost.porcie -= 1
        usadlost.divoch_mutex.unlock()
        hodovanie(proces_id)


def kuchar_proces(proces_id: int, usadlost: Usadlost):
    """
    Funkcia simulujúca proces reprezentujúci kuchára.

    Argumenty:
        proces_id: Identifikátor procesu.
        usadlost: Usadlost objekt obsahujúci zdieľané premenné.
     """

    while True:
        usadlost.prazdny_hrniec.wait()
        usadlost.kuchar_mutex.lock()
        if usadlost.porcie < PORCIA_POCET:
            # varenie a nakladanie porcii do hrnca
            usadlost.porcie += 1
            usadlost.kuchar_mutex.unlock()
            varenie(proces_id)
        else:
            # servírovanie plného hrnca
            servirovanie_plny_hrniec(proces_id)
            usadlost.prazdny_hrniec.clear()
            usadlost.plny_hrniec.signal()
            usadlost.kuchar_mutex.unlock()


def main():
    """
    Funkcia vykonávajúca všeobecnú funkcionalitu.
    """

    usadlost: Usadlost = Usadlost()
    divosi: list = []
    kuchari: list = []

    for i in range(DIVOCH_POCET):
        divosi.append(Thread(divoch_proces, i, usadlost))

    for i in range(KUCHAR_POCET):
        kuchari.append(Thread(kuchar_proces, i, usadlost))

    for vlakno in divosi + kuchari:
        vlakno.join()


if __name__ == "__main__":
    main()