"""
Modul obsahujúci implementáciu večerajúcich filozofov (ľavák-pravák).
"""


__authors__ = "Filip Mikuš, Tomáš Vavro"
__email__ = "xmikusf@stuba.sk, mariansebena@stuba.sk, xvavro@stuba.sk"
__license__ = "MIT"


from fei.ppds import Mutex, Thread, print
from time import sleep


FILOZOF_POCET: int = 5


class Jedalen:
    """
    Trieda reprezentujúca Jedalen a jeho zdieľané premenné.

    Atribúty:
        vidlicky: List Mutex-ov reprezentujúce vidličky.
    """

    def __init__(self):
        """
        Metóda na inicializáciu objektu Jedalen a jeho zdieľaných premenných.
        """

        self.vidlicky: list[Mutex] = [Mutex() for _ in range(FILOZOF_POCET)]


def premyslanie(proces_id: int):
    """
    Funkcia reprezentujúca premýšlanie filozofa.

    Argumenty:
        proces_id: Identifikátor procesu.
    """

    print(f"Filozof [id: {proces_id}] premýšla.")
    sleep(3)


def stravovanie(proces_id: int):
    """
    Funkcia reprezentujúca stravovanie filozofa.

    Argumenty:
        proces_id: Identifikátor procesu.
    """

    print(f"Filozof [id: {proces_id}] sa stravuje.")
    sleep(3)


def filozof_proces(proces_id: int, jedalen: Jedalen):
    """
    Funkcia simulujúca proces reprezentujúci filozofa.

    Argumenty:
        proces_id: Identifikátor procesu.
        jedalen: Jedalen objekt obsahujúci zdieľané premenné.
    """

    while True:
        premyslanie(proces_id)

        if proces_id == 0:
            # filozof - ľavák
            jedalen.vidlicky[(proces_id + 1) % FILOZOF_POCET].lock()
            jedalen.vidlicky[proces_id].lock()
        else:
            # filozof - pravák
            jedalen.vidlicky[proces_id].lock()
            jedalen.vidlicky[(proces_id + 1) % FILOZOF_POCET].lock()

        stravovanie(proces_id)

        jedalen.vidlicky[(proces_id + 1) % FILOZOF_POCET].unlock()
        jedalen.vidlicky[proces_id].unlock()


def main():
    """
    Funkcia vykonávajúca všeobecnú funkcionalitu.
    """

    jedalen: Jedalen = Jedalen()
    filozofi: list[Thread] = []

    for i in range(FILOZOF_POCET):
        filozofi.append(Thread(filozof_proces, i, jedalen))

    for filozof in filozofi:
        filozof.join()


if __name__ == "__main__":
    main()