# Mikus_104537_feippds - Zadanie 04 (Problém hodujúcich divochov)

[![python: 3.10.10](https://img.shields.io/badge/python-3.10.10-blue.svg)](https://www.python.org/downloads/release/python-31010/)
[![pip installation: fei.ppds](https://img.shields.io/badge/pip%20install-fei.ppds-blue.svg)](https://pypi.org/project/fei.ppds/)
[![conventional commits: 1.0.0](https://img.shields.io/badge/conventional%20commits-1.0.0-green.svg)](https://conventionalcommits.org)
[![code style: PEP8](https://img.shields.io/badge/code%20style-PEP%208-orange.svg)](https://www.python.org/dev/peps/pep-0008/)
[![code style: PEP257](https://img.shields.io/badge/code%20style-PEP%20257-yellow.svg)](https://peps.python.org/pep-0257/)
[![license: MIT](https://img.shields.io/badge/license-MIT-red.svg)](https://opensource.org/licenses/MIT)

## Dokumentácia

### Požiadavky

Implementácia vyžaduje balík _fei.ppds_. Inštalácia pomocou _pip_:

    pip install --upgrade fei.ppds

### Spustenie

    python 04_divosi_kuchari.py

### Problém Hodujúcich divochov

Divosi v Rovníkovej Guinei sú veľmi spoločenský a vyspelý typ divochov. Nielen, že každý deň jedia vždy spolu, ale majú 
medzi sebou aj šikovných kuchárov, ktorí pripravujú výborný guláš zo zebry. Potrebujú však spoľahlivý systém, v ktorom 
budú oznamovať všetky úkony, ktoré so spoločným hodovaním súvisia.
 - Divosi vždy začínajú jesť spolu. Posledný divoch, ktorý príde, všetkým signalizuje, že sú všetci a začať môžu hodovať.
 - Divosi si po jednom berú svoju porciu z hrnca dovtedy, kým nie je hrniec prázdny.
 - Divoch, ktorý zistí, že už je hrniec prázdny upozorní kuchárov, aby znovu navarili.
 - Divosi čakajú, kým kuchári doplnia plný hrniec.
 - Kuchár vždy navarí jednu porciu a vloží ju do hrnca.
 - Keď' je hrniec plný, divosi pokračujú v hodovaní.
 - Celý proces sa opakuje v nekonečnom cykle.

### Implementácia -  Hodujúci divosi s viacerými kuchármi

Počet procesov divochov bol definovaný v globálnej premennej _DIVOCH_POCET_, počet procesov kuchárov bol definovaný v 
globálnej premennej _KUCHAR_POCET_ a v globálnej premennej _PORCIA_POCET_ uchovávame počet porcii v hrnci.

    PORCIA_POCET = 5
    DIVOCH_POCET = 3
    KUCHAR_POCET = 5

Trieda _Usadlost_ reprezentujúca abstrakciu usadlosti uchováva zdieľané premenné (_porcie_) a objekty 
synchronizačných mechanizmov **Mutex** (_divoch_mutex_, _kuchar_mutex_),  **Signalizácia** (_plny_hrniec_ - Semaphore, 
_prazdny_hrniec_ - Event) a **Bariéra** (_divoch_bariera_1_ - SimpleBarrier, _divoch_bariera_2_ - SimpleBarrier).

    class Usadlost:
        def __init__(self):
            self.divoch_mutex = Mutex()
            self.kuchar_mutex = Mutex()
            self.porcie = 0
            self.plny_hrniec = Semaphore(0)
            self.prazdny_hrniec = Event()
            self.divoch_bariera_1 = SimpleBarrier(DIVOCH_POCET)
            self.divoch_bariera_2 = SimpleBarrier(DIVOCH_POCET)

Funkcie _hodovanie_, _varenie_, _nabratie_porcia_, _najdenie_prazdny_hrniec_, _servirovanie_plny_hrniec_ 
slúžia na výpis činnosti (_print_ - _fei.ppds_), prípadne simuláciu časového intervalu danej činnosti (_sleep_ - time).

    def hodovanie(proces_id: int):
        ...

    def varenie(proces_id: int):
        ...

    def nabratie_porcia(proces_id: int):
        ...
    
    def najdenie_prazdny_hrniec(proces_id: int):
        ...
    
    def servirovanie_plny_hrniec(proces_id: int):
        ...

Funkcia _divoch_proces_ implementuje astrakciu divocha. V nekonečneom _while_ cykle je najprv umiestnená bariéra 
(_divoch_bariera_1.wait()_, _divoch_bariera_2.wait()_), ktorá zabezpečuje spoločný začiatok hodovania všetkých divochov, 
následne dôjde k uzamknutiu mutex-u (_divoch_mutex.lock()_), aby pri kontrole porcii v hrnci (_porcie_) nenastalo 
porušenie integrity počítadla. 

    def divoch_proces(proces_id: int, usadlost: Usadlost):
        while True:
            usadlost.divoch_bariera_1.wait()
            usadlost.divoch_bariera_2.wait()
            usadlost.divoch_mutex.lock()

Následne prebehne samotná kontrola počtu porcii v hrnci (_porcie == 0_), pričom ak je hrniec prázdny 
prebehne simulácia nájdenia prázdneho hrnca divochom (_najdenie_prazdny_hrniec()_), potom je pomocou semafóru kuchárom
signalizované, že je hrniec prázdny (_prazdny_hrniec.signal()_) a napokon následuje čakanie na signalizáciu, že je hrniec 
naplnený kuchármi (_plny_hrniec.wait()_).

            if usadlost.porcie == 0:
                najdenie_prazdny_hrniec(proces_id)
                usadlost.prazdny_hrniec.signal()
                usadlost.plny_hrniec.wait()

Ak hrniec prázdny nie je, repsektívne ak bol naplnený, prebehne simulácia nabratia porcie divochom (_nabratie_porcia()_), 
dekrementovanie počítadla porcii v hrnci (_porcie -= 1_), odomknutie mutex-u (_divoch_mutex.unlock()_) a nakoniec
simulácia samotného hodovania divocha (_hodovanie()_).

            nabratie_porcia(proces_id)
            usadlost.porcie -= 1
            usadlost.divoch_mutex.unlock()
            hodovanie(proces_id)

Funkcia _kuchar_proces_ implementuje astrakciu kuchára. V nekonečneom _while_ cykle je najprv umiestené čakanie na 
signalizáciu od divochov, že je hrniec prázdny (_prazdny_hrniec.wait()_). Po signalizácii od divochov nasleduje uzamknutie 
mutex-u (_kuchar_mutex.lock()_), aby pri kontrole a manipulácii s počtadlom porcii v hrnci (_porcie_) nenastalo 
porušenie integrity. 

    def kuchar_proces(proces_id: int, usadlost: Usadlost):
        while True:
            usadlost.prazdny_hrniec.wait()
            usadlost.kuchar_mutex.lock()

Následne prebehne samotná kontrola počtu porcii v hrnci (_porcie < PORCIA_POCET_), pričom ak v hrncii nie je dostatočný
počet porcii príde k inkrementovaniu počítadla porcii (_.porcie += 1_), odomknutiu mutex-u (_kuchar_mutex.unlock()_) 
a nakoniec simulácia samotného varenia kuchára (_varenie()_).

            if usadlost.porcie < PORCIA_POCET:
                usadlost.porcie += 1
                usadlost.kuchar_mutex.unlock()
                varenie(proces_id)

Ak je v hrnci dostatočný počet porcii, prebehne simulácia servírovania plného hrnca kuchárom (_servirovanie_plny_hrniec()_),
vyčistenie (reset čakania) signalizácie prázdneho hrnca (_prazdny_hrniec.clear()_), signalizácia pomocou semafóru divochom, 
že je hrniec naplnený (_plny_hrniec.signal()_) a nakoniec odomknutie mutex-u (_kuchar_mutex.unlock()_).

            else:
                servirovanie_plny_hrniec(proces_id)
                usadlost.prazdny_hrniec.clear()
                usadlost.plny_hrniec.signal()
                usadlost.kuchar_mutex.unlock()

### Implementácia - Bariéra (SimpleBarrier)

Trieda implementujúca funkcionalitu synchronizačného mechanizmu bariéra pomocou synchronizačného mechanizmu Event
(_Event_ - fei.ppds). Podľa vzoru z https://www.youtube.com/watch?v=3KJv9hFTx6k&t=876s.

    class SimpleBarrier:
        def __init__(self, n):
            self.n = n
            self.c = 0
            self.mutex = Mutex()
            self.event = Event()
    
        def wait(self):
            self.mutex.lock()
            if self.c == 0:
                self.event.clear()
            self.c += 1
            if self.c == self.n:
                self.event.signal()
            self.mutex.unlock()
            self.event.wait()

### Charakteristika fungovania

Uvažujme nasledujúci príklad, pri 5 porciách, 3 divochoch a 5 kuchároch:

 - Všetci divosi [id: 0, 1, 2] sa dostavili na miesto večere, následne teda boli pripustený k hrncu.
 - Divoch [id: 0] kontroluje stav hrnca, ostatní divosi [id: 1, 2] čakajú "pred hrncom".
 - Divoch [id: 0] našiel prázdny hrniec, skutočnosť oznamuje kuchárom, následne sám čaká na naplnenie.
 - Kuchári [id: 0, 1, 2, 3, 4] sú po signalizácii spoločne pripustený k vareniu.
 - Kuchári [id: 0, 1, 2, 3, 4] potupne sériovo skontroluju, aký je počet porcii v hrnci, následne môžu konkurente variť 
po jednej porcii. (Ak by bol počet porcii väčší ako počet kuchárov, napríklad 6, jeden z kuchárov musí implicitne uvariť 1 porciu 2-krát.)
 - Kuchár [id: 1] následne počas kontroly (sériovo) zistí, že je hrniec naplnený na svoju maximálnu kapacitu, 
servíruje hrniec divochom, upevodomuje čakajúceho divocha, ktorý oznámil, že je prázdny o jeho naplnení a kuchári 
následne spoločne čakajú na ďalší signál o vyprázdnení hrnca.
 - Divoch [id: 0] je upovedomený o naplnení hrnca, naberá si (sériovo) svoju porciu a hoduje (konkurentne).
 - Divosi [id: 0, 1, 2] následne po jednom naberajú svoju porciu (sériovo) a hodujú (konkurentne).
 - Hodovanie divochov [id: 0, 1, 2] trvá do momentu, kým niektorí z nich nenachádza prázdny hrniec a upovedomuje kuchárov.
 - ... 


### Výpis z konzoly

Uvažujme výpis z uvedeného príkladu v sekcii **Charakteristika fungovania**:

    Divoch [id: 0] našiel prázdny hrniec a upovedumuje kuchárov.
    Kuchár [id: 0] varí.
    Kuchár [id: 1] varí.
    Kuchár [id: 2] varí.
    Kuchár [id: 3] varí.
    Kuchár [id: 4] varí.
    Kuchár [id: 1] upovedomuje divochov o naplnení hrnca.
    Divoch [id: 0] si naberá porciu.
    Divoch [id: 0] hoduje.
    Divoch [id: 1] si naberá porciu.
    Divoch [id: 1] hoduje.
    Divoch [id: 2] si naberá porciu.
    Divoch [id: 2] hoduje.
    Divoch [id: 1] si naberá porciu.
    Divoch [id: 1] hoduje.
    Divoch [id: 2] si naberá porciu.
    Divoch [id: 2] hoduje.
    Divoch [id: 0] našiel prázdny hrniec a upovedumuje kuchárov.

    ...

### Zdroje

__JÓKAY M., Paralelné programovanie a distribuované systémy - Bariéra, Producenti/Konzumenti, Čitatelia/Zapisovatelia, Lightswitch. [online]. Bratislava: FEI STU, 2021.__ Dostupné z: https://www.youtube.com/watch?v=3KJv9hFTx6k&t=876s

__BERNÁT D., Paralelné programovanie a distribuované systémy - Synchronizačné mechanizmy. [online]. Bratislava: FEI STU, 2023.__ Dostupné z: https://elearn.elf.stuba.sk/moodle/pluginfile.php/75654/mod_resource/content/1/Ppds_1_2.pdf

__VAVRO T., ŠEBEŇA M., Paralelné programovanie a distribuované systémy - Cvičenie 3. [online]. Bratislava: FEI STU, 2023.__ Dostupné z: https://elearn.elf.stuba.sk/moodle/

__VAVRO T., ŠEBEŇA M., Paralelné programovanie a distribuované systémy - PPDS Veľké zadanie. [online]. Bratislava: FEI STU, 2023.__ Dostupné z: https://elearn.elf.stuba.sk/moodle/

__VAVRO T., ŠEBEŇA M., Paralelné programovanie a distribuované systémy - ppds-2023-cvicenia (GitHub). [online]. Bratislava: FEI STU, 2023.__ Dostupné z: https://github.com/tj314/ppds-2023-cvicenia
