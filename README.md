# Mikus_104537_feippds - Zadanie 02 (Problém holičstva s predbiehaním)

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

    python 02_barbershop.py

### Problém holičstva s predbiehaním

Problém holičstva s predbiehaním rieši koordináciu procesov klientov a barbéra. Holičstvo pozostáva z 2 miestoností, 
čakárne pre _N_ klientov a mestnosti barbéra. Ak nie je žiadny klient, barbér odpočíva. Ak klient vôjde a všetky stoličky 
sú obsadené, odíde, ak klient vôjde a barbér je obsadený, ale je voľná stolička, sadne a čaká na obslúženie a ak vôjde 
klient a barbér odpočíva, zobudí ho, sadne a čaká.

### Implementácia

Počet procesov klientov bol definovaný v globálnej premennej _ZAKAZNIK_POCET_, v globálnej premennej 
_CAKAREN_MAX_KAPACITA_ uchovávame maximálny povolený počet klientov v čakárni, respektívne v barbershope.

Trieda _Barbershop_ reprezentujúca abstrakciu Barbershop-u uchováva zdieľané premenné (_cakaren_) a objekty 
synchronizačných mechanizmov **Mutex** (_mutex_) a **Rendezvous** (_zakaznik_pripraveny - barber_pripraveny_, 
_zakaznik_koniec_obsluhy - barber_koniec_obsluhy_).

Funkcie _strihanie_vlasov_zakaznika_, _strihanie_vlasov_barberom_, _cakaren_prichod_, _cakaren_odchod_, 
_plna_cakaren_odchod_, _rast_vlasov_ slúžia na výpis činnosti (_print_ - _fei.ppds_), prípadne simuláciu časového 
intervalu danej činnosti (_sleep_ - time).

Funkcia _barber_proces_ implementuje astrakciu barbéra. V nekonečneom _while_ cykle najprv pomocou mechanizmu rendezvous, 
respektívne semafóru signalizuje potencionálnym čakajúcim klientom, že je pripravený na strihanie (_barber_pripraveny.signal()_ - rendezvous 1), 
následne je pomocou mechanizmu rendezvous, respektívne semafóru simulovaný odpočinok (čakanie) barbéra (_zakaznik_pripraveny.wait()_ - rendezvous 1), 
ktorý trvá do chvíľe, kým nie je zobudený klientom pripraveným na ostrihanie. Následne je simulované strihanie barbérom
pomocou funkcie _strihanie_vlasov_barberom()_. Po dokončení strihanie je pomocou druhej dvojice semafórov, teda druhého
mechanizmu rendezvous signalizované, že barbér dokončil strih (_barber_koniec_obsluhy.signal()_), po ktorom barbér čaká, 
kým klient rovnako strihanie považuje za dokončené (_zakaznik_koniec_obsluhy.wait()_).

Funkcia _zakaznik_proces_ implementuje abstrakciu klienta. V nekonečneom while cykle najprv zamkne mutex (_mutex.lock()_), 
aby pri kontrole počtu klientov v čakárni (_cakaren_) nenastalo porušenie integrity počítadla, respektívne aby inému 
klienotvi nebolo umožnéné počítadlo kontrolovať, inkrementovať alebo dekrementovať. Následne prebehne samotná 
kontrola, či je čakáreň naplnená na svoju maximálnu kapacitu (_CAKAREN_MAX_KAPACITA_). Ak je čakáreň naplnená, prebehne 
odomknutie mutex-u (_mutex.unlock()_) a simulácia odchodu klienta z plnej čakárne (_plna_cakaren_odchod()_). 
Ak je v čakárni aspoň jedno voľné miesto, prebehne inkrementácia počítadla počtu klientov v čakárni (_cakaren += 1_) a 
odomknutie mutex-u (_mutex.unlock()_). Po tomto kroku klient pomocou  mechanizmu rendezvous, respektívne semafóru signalizuje 
(budí z odpočinku) barbéra (_zakaznik_pripraveny.signal()_).
Následne pomocou mechanizmu rendezvous, respektívne semafóru implemetované čakanie, kým je aj barbér pripravený na strihanie
(_barber_pripraveny.wait()_). Po tomto kroku je simulované strihanie klienta barbérom pomocou funkcie 
_strihanie_vlasov_zakaznika()_. Po dokončení strihanie je pomocou druhej dvojice semafórov, teda druhého
mechanizmu rendezvous signalizované, že klient je ostrihaný (_zakaznik_koniec_obsluhy.signal()_),  po ktorom klient čaká, 
kým barbér rovnako strihanie považuje za dokončené (_barber_koniec_obsluhy.wait()_). Na záver je zamknutý mutex 
(_mutex.lock()_) (rovnako ako pri kontrole je nutné mutex-om zabezpečiť, aby nebola narušená integrita počítadla), 
je simulovaný odchod klienta z čakárne (_cakaren_odchod()_), počítadlo počtu klientov v čakárni je dekrementované 
(_barbershop.cakaren -= 1_), mutex je odomknutý (_mutex.unlock()_) a je simulovaný rast vlasov klienta (_rast_vlasov()_).


### Výpis z konzoly

    Zákazník [id: 0] vchádza do barbershopu.
    Zákazník [id: 1] vchádza do barbershopu.
    Zákazník [id: 2] vchádza do barbershopu.
    Barbér [id: 0] poskytuje svoje služby.
    Zákazník [id: 2] využíva služby barbéra.
    Zákazník [id: 3] vchádza do barbershopu.
    Čakáreň je plná, zákazník [id: 3] odchádza z barbershopu.
    Zákazník [id: 4] vchádza do barbershopu.
    Čakáreň je plná, zákazník [id: 4] odchádza z barbershopu.
    Zákazník [id: 2] odchádza z barbershopu.
    Zákazníkovi [id: 2] rastú vlasy.
    Barbér [id: 0] poskytuje svoje služby.
    Zákazník [id: 0] využíva služby barbéra.
    Zákazník [id: 3] vchádza do barbershopu.
    Zákazník [id: 4] vchádza do barbershopu.
    Čakáreň je plná, zákazník [id: 4] odchádza z barbershopu.
    Zákazník [id: 0] odchádza z barbershopu.
    Zákazníkovi [id: 0] rastú vlasy.
    Barbér [id: 0] poskytuje svoje služby.
    Zákazník [id: 1] využíva služby barbéra.
    Zákazník [id: 2] vchádza do barbershopu.
    Zákazník [id: 1] odchádza z barbershopu.
    Zákazníkovi [id: 1] rastú vlasy.
    Barbér [id: 0] poskytuje svoje služby.
    Zákazník [id: 2] využíva služby barbéra.
    Zákazník [id: 4] vchádza do barbershopu.
    Zákazník [id: 0] vchádza do barbershopu.
    Čakáreň je plná, zákazník [id: 0] odchádza z barbershopu.
    Zákazník [id: 2] odchádza z barbershopu.
    Zákazníkovi [id: 2] rastú vlasy.
    Barbér [id: 0] poskytuje svoje služby.
    Zákazník [id: 4] využíva služby barbéra.
    Zákazník [id: 1] vchádza do barbershopu.
    Zákazník [id: 4] odchádza z barbershopu.
    Zákazníkovi [id: 4] rastú vlasy.
    Barbér [id: 0] poskytuje svoje služby.
    Zákazník [id: 3] využíva služby barbéra.
    Zákazník [id: 0] vchádza do barbershopu.
    Zákazník [id: 2] vchádza do barbershopu.
    Čakáreň je plná, zákazník [id: 2] odchádza z barbershopu.
    Zákazník [id: 3] odchádza z barbershopu.
    Zákazníkovi [id: 3] rastú vlasy.
    
    ...

### Zdroje

__JÓKAY M., Paralelné programovanie a distribuované systémy - Mutex, multiplex, rendezvous, bariéra. [online]. Bratislava: FEI STU, 2022.__ Dostupné z: https://www.youtube.com/watch?v=sR5RWW1uj5g

__VAVRO T., ŠEBEŇA M., Paralelné programovanie a distribuované systémy - Cvičenie 3. [online]. Bratislava: FEI STU, 2023.__ Dostupné z: https://elearn.elf.stuba.sk/moodle/pluginfile.php/75802/mod_resource/content/1/PPDS_cv3.pdf

__VAVRO T., ŠEBEŇA M., Paralelné programovanie a distribuované systémy - ppds-2023-cvicenia (GitHub). [online]. Bratislava: FEI STU, 2023.__ Dostupné z: https://github.com/tj314/ppds-2023-cvicenia


