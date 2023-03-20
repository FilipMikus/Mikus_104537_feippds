from fei.ppds import Event, Semaphore, Mutex, Thread, print
from time import sleep
from simplebarrier import SimpleBarrier


PORCIA_POCET = 5
DIVOCH_POCET = 3
KUCHAR_POCET = 5


class Usadlost:

    def __init__(self):

        self.divoch_mutex = Mutex()
        self.kuchar_mutex = Mutex()
        self.porcie = 0
        self.plny_hrniec = Semaphore(0)
        self.prazdny_hrniec = Event()
        self.divoch_bariera_1 = SimpleBarrier(DIVOCH_POCET)
        self.divoch_bariera_2 = SimpleBarrier(DIVOCH_POCET)


def hodovanie(proces_id: int):

    print(f"Divoch [id: {proces_id}] hoduje.")
    sleep(3)


def varenie(proces_id: int):

    print(f"Kuchár [id: {proces_id}] varí.")
    sleep(5)


def nabratie_porcia(proces_id: int):

    print(f"Divoch [id: {proces_id}] si naberá porciu.")


def najdenie_prazdny_hrniec(proces_id: int):

    print(f"Divoch [id: {proces_id}] našiel prázdny hrniec a upovedumuje kuchárov.")


def servirovanie_plny_hrniec(proces_id: int):

    print(f"Kuchár [id: {proces_id}] upovedomuje divochov o naplnení hrnca.")


def divoch_proces(proces_id: int, usadlost: Usadlost):

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