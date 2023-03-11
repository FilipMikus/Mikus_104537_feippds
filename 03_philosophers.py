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

    def __init__(self):

        self.vidlicky: list[Mutex] = [Mutex() for _ in range(FILOZOF_POCET)]


def premyslanie(proces_id: int):

    print(f"Filozof [id: {proces_id}] premýšla.")
    sleep(3)


def stravovanie(proces_id: int):

    print(f"Filozof [id: {proces_id}] sa stravuje.")
    sleep(3)