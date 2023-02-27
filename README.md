# Mikus_104537_feippds - Zadanie 01 (Bakery algoritmus)

[![python: 3.10.10](https://img.shields.io/badge/python-3.10.10-blue.svg)](https://www.python.org/downloads/release/python-31010/)
[![pip installation: fei.ppds](https://img.shields.io/badge/pip%20install-fei.ppds-blue.svg)](https://pypi.org/project/fei.ppds/)
[![conventional commits: 1.0.0](https://img.shields.io/badge/conventional%20commits-1.0.0-green.svg)](https://conventionalcommits.org)
[![code style: PEP8](https://img.shields.io/badge/code%20style-PEP%208-orange.svg)](https://www.python.org/dev/peps/pep-0008/)
[![code style: PEP257](https://img.shields.io/badge/code%20style-PEP%20257-yellow.svg)](https://peps.python.org/pep-0257/)
[![license: MIT](https://img.shields.io/badge/license-MIT-red.svg)](https://opensource.org/licenses/MIT)

## Dokumentácia

### Požiadavky

Impelemntácia vyžaduje balík _fei.ppds_. Inštalácia pomocou _pip_:

    pip install --upgrade fei.ppds

### Spustenie

    python 01_bakery.py
  
### Bakery algoritmus
Bakery algoritmus (Leslie Lamport, 1973) predstavuje algoritmus pre vzájomné vylúčenie procesov fungujúci na princípe čakania procesu na poradie, 
teda na takzvaný tiket. 

Vďaka fungovaniu na princípe tiket algoritmu je zaručená spravodlivosť prístupu do kritickej oblasti, nakoľko je dodržané 
poradie, v ktorom procesy obdržali tikety. Na rozdiel od pôvodného Tiket algoritmu však nevyžaduje špecálne inštrukcie a 
podporu hardvéru.

Popis fungovania algoritmu pre každý proces je nasledovný:
1.  Obdržanie tiketu s hodnotou o jeden väčšou, ako má tiket s momentálne najvyššou hodnotou, pričom ak sú všetky 
tikety neaktívne s hodnotou 0, má prvý obdržaný tiket hodnotu 1.
2. Kontrola, či niektorý z procesov nie je vo fáze obdržania nového tiketu (1. krok). Ak niektorý z procesov dostáva
nový tiket, ostatné procesy nemôžu pristúpiť ku kontrole tiketov (3. krok) a čakajú, nakoľko by mohlo nastať kontrola neaktuálnych hodnôt.
3. Kontrola hodnôt tiketov, po ktorej je povolené vykonanie kritickej oblasti (4. krok) procesu s tiketom s najnižšou hodnotou, 
respektívne pri rovnosti hodnôt viacerých tiketov tomu s nižším identifátorom. Ostatné procesy na tejto kontrole čakajú, 
kým nepríde na rad ich tiket.
4. Vykonanie kritickej oblasti.
5. Deaktivácia tiketu, respektívne nastavenie hodnoty na 0.

### Vzájomné vylúčenie

1. V kritickej oblasti sa smie vykonávať v každom čase najviac jeden proces.
2. Proces, ktorý sa vykonáva mimo kritickej oblasti nesmie brániť iným vstúpiť do nej.
3. Rozhodnutie o vstupe musí prísť v konečnom čase.
4. Procesy nemôžu pri vstupe do kritickej oblasti predpokladať nič o vzájomnom časovaní (plánovaní).

Princíp vzájomného výlúčenia a všetky jeho nutné podmienky sú dodržané práve vďaka tiketom, kde je do kritickej oblasti 
pripustený vždy práve jeden proces, a to ten, ktorý vlastní tiket s najnižšou hodnotou, respektívne pri rovnosti 
hodnôt viacerých tiketov ten s nižším identifátorom (1., 2., 3.), rozhodnutie sa vykoná v konečnom čase (3.). Tikety sú 
pridelované s jedinečnou hodnotou (respektívne pri rovnosti zabezpečuje jedinečnosť index (alebo identifikátor) procesu), 
čo zaručuje jasné poradie vykonávania (FIFO) procesov (4.). Hodnota tiketu je následne po vykonaní kritikcej oblasti 
vynulovaná (2.).

### Implementácia

Počet procesov bol definovaný v globálnej premennej _PROCES_POCET_, v globálnej premennej _tiket_ uchovávame hodoty tiketov a 
v globálnej premennej _vyber_tiket_ uchovávame, ktoré procesy dostávajú tiket. 

Abstrakcia procesu je implementovaná ako funkcia _bakery_proces(proces_id)_, ktorej argument _proces_id_ obsahuje 
jedinečný identifikátor procesu.

Proces najprv deklaruje, že je vo fáze obdržania tiketu nastavením listu _vyber_tiket_ na indexe _proces_id_ na hodnotu True. 

Proces následne nastaví hodnotu listu _tiket_ na indexe _proces_id_ na hodnotu tiketu s maximánou hodnotou plus jeden. 

Po tomto kroku je hodnota v liste _vyber_tiket_ na indexe _proces_id_ nastavená na False. 

Vo _for_ cykle následne iterujeme cez všetky procesy, kde v prvom _while_ cykle kontrolujeme, či iterovaný proces 
nie je vo fáze obdržania nového tiketu pomocou premennej _vyber_tiket_ a v druhom _while_ cykle kontrolujeme, či tiket 
konkrétneho procesu nebsahuje najnižšiu hodnotu pomocou porovnania s iterovaným procesom cez premennú _tiket_.

Kritická oblasť je simulovaná jedoduchým výpisom a zavolaním funkcie _sleep(3)_.

Ako posledné je vynulovaná hodnota tiketu konkrétneho procesu v premennej _tiket_ na indexe _proces_id_ na hodnotu 0.

### Zdroje
__BERNÁT D., Paralelné programovanie a distribuované systémy - Synchronizačné mechanizmy. [online]. Bratislava: FEI STU, 2023.__ Dostupné z: https://elearn.elf.stuba.sk/moodle/pluginfile.php/75654/mod_resource/content/1/Ppds_1_2.pdf
