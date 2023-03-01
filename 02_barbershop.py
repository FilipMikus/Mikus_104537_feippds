"""
Modul obsahujúci implementáciu holičstva s predbiehaním.
"""


__authors__ = "Filip Mikuš, Marián Šebeňa"
__email__ = "xmikusf@stuba.sk, mariansebena@stuba.sk, xvavro@stuba.sk"
__license__ = "MIT"


from fei.ppds import Mutex, Semaphore, Thread, print
from time import sleep


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


def strihanie_vlasov_zakaznika(proces_id: int):

    print(f"Zákazník [id: {proces_id}] využíva služby barbéra.")
    sleep(3)


def strihanie_vlasov_barberom(proces_id: int):

    print(f"Barbér [id: {proces_id}] poskytuje svoje služby.")
    sleep(3)


def cakaren_prichod(proces_id: int):

    print(f"Zákazník [id: {proces_id}] vchádza do barbershopu.")


def cakaren_odchod(proces_id: int):

    print(f"Zákazník [id: {proces_id}] odchádza z barbershopu.")


def plna_cakaren_odchod(proces_id: int):

    print(f"Čakáreň je plná, zákazník [id: {proces_id}] odchádza z barbershopu.")
    sleep(5)


def rast_vlasov(proces_id: int):

    print(f"Zákazníkovi [id: {proces_id}] rastú vlasy.")
    sleep(5)


def zakaznik_proces(proces_id: int, barbershop: Barbershop):
    """
    Funkcia simulujúca proces reprezentujúci zákazníka.

    Argumenty:
        proces_id: Identifikátor procesu.
        barbershop: Barbershop objekt obsahujúci zdieľané premenné.
    """

    while True:
        # zamknutie mutex-u pred manipuláciou s premennou čakáreň
        barbershop.mutex.lock()
        cakaren_prichod(proces_id)
        # overenie, či je v čakárni voľné miesto
        if barbershop.cakaren == CAKAREN_MAX_KAPACITA:
            # plná čakáreň
            # odomknutie mutex-u po manipulácii s premennou čakáreň
            barbershop.mutex.unlock()
            plna_cakaren_odchod(proces_id)
        else :
            # voľná čakáreň
            barbershop.cakaren += 1
            # odomknutie mutex-u po manipulácii s premennou čakáreň
            barbershop.mutex.unlock()

            # signalizácia (rendezvous 1), že zákazník je pripravený na ostrihanie
            barbershop.zakaznik_pripraveny.signal()
            # čakanie (rendezvous 1) na barbéra pripraveného na strihanie
            barbershop.barber_pripraveny.wait()
            strihanie_vlasov_zakaznika(proces_id)
            # signalizácia (rendezvous 2), že zákazník je ostrihaný
            barbershop.zakaznik_koniec_obsluhy.signal()
            # čakanie (rendezvous 2) na dokončenie strihu barbérom
            barbershop.barber_koniec_obsluhy.wait()

            # zamknutie mutex-u pred manipuláciou s premennou čakáreň
            barbershop.mutex.lock()
            cakaren_odchod(proces_id)
            barbershop.cakaren -= 1
            # odomknutie mutex-u po manipulácii s premennou čakáreň
            barbershop.mutex.unlock()

            rast_vlasov(proces_id)


def barber_proces(proces_id: int, barbershop: Barbershop):

    while True:
        # signalizácia (rendezvous 1), že barbér je pripravený na strihanie
        barbershop.barber_pripraveny.signal()
        # čakanie (rendezvous 1) na zákazníka pripraveného na ostrihanie
        barbershop.zakaznik_pripraveny.wait()
        strihanie_vlasov_barberom(proces_id)
        # signalizácia (rendezvous 2), že barbér dokončil strih
        barbershop.barber_koniec_obsluhy.signal()
        # čakanie (rendezvous 2) na ostrihanie zákazníka
        barbershop.zakaznik_koniec_obsluhy.wait()


def main():

    barbershop: Barbershop = Barbershop()
    zakaznici: list = []

    for i in range(ZAKAZNIK_POCET):
        zakaznici.append(Thread(zakaznik_proces, i, barbershop))
    barber: Thread = Thread(barber_proces, 0, barbershop)

    for vlakno in zakaznici + [barber]:
        vlakno.join()


if __name__ == "__main__":
    main()