# Mikus_104537_feippds - Zadanie 03 (Problém večerajúcich filozofov - Ľavák/Pravák)

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

    python 03_philosophers.py

### Problém večerajúcich filozofov

Problém večerajúcich filozofov (Edsger W. Dijkstra, 1965) je koncept reprezentujúci synchronizáciu a správu procesov. 
Koncept je definovaný nasledovne:
 - Na stole je v kruhu 5 tanierov a 5 vidličiek. Za stolom sedí 5 filozofov, ktorí striedavo premýšľajú a jedia.
 - Filozof potrebuje na jedenie vždy dve vidličky. Po premýšľaní, keď vyhladne, pokúsi sa vziať ľavú a pravú vidličku. 
Potom môže jesť.
 - Keď doje, obe vidličky položí späť na stôl.
 - Je potrebné predísť vyhladovaniu filozofov.
 - Je potrebné predísť uviaznutiu (deadlock).

### Implementácia - Ľavák/Pravák

V našom riešení sme implementovali variantu Ľavák/Pravák. 

Počet procesov filozofov bol definovaný v globálnej premennej _FILOZOF_POCET_.

Trieda _Jedalen_ reprezentujúca abstrakciu Jedálne uchováva zdieľanú premennú synchronizačného mechanizmu **list(Mutex)** (_vidlicky_).

Funkcie _premyslanie_ a  _stravovanie_ slúžia na výpis činnosti (_print_ - _fei.ppds_), prípadne simuláciu časového 
intervalu danej činnosti (_sleep_ - time).

Funkcia _filozof_proces_ implementuje abstrakciu filozofa. V nekonečneom while cykle je najprv simulované premýšlanie 
filozofa (_premyslanie()_), následné podľa identifikátora procesu (_proces_id_) prebehne kontrola, či ide o ľaváka 
(_if proces_id == 0_) alebo praváka (_else_). Ak ide o ľaváka, prebehne zdvihnutie (zamknutie) ľavej vidličky 
(_vidlicky[(proces_id + 1) % FILOZOF_POCET].lock()_) a následne pravej vidličky (_vidlicky[proces_id].lock()_), respektívne 
zdvihnutie pravej a následne ľavej vidličky, ak ide o praváka. Po uchopení (zamknutí) vidličiek je simulované stravoanie 
filozofa (_stravovanie()_). Po dokončení stravovania sú vydličky uvoľnené (odomknuté) 
(_vidlicky[(proces_id + 1) % FILOZOF_POCET].unlock()_ a _vidlicky[proces_id].unlock()_).




### Porovnanie implementácii Čašník - Ľavák/Pravák

Pri variante problému N večerajúcich filozofov s inštitútom čašníka je funkčnosť celého riešenia zabezpečená možnosťou 
stravovania, respektívne možnosti uchopenia vidličiek v jeden moment maximálne pre N-1 (v našom prípade 4) filozofov.
Táto skutočnosť je zabezpečená použitím synchronizačného mechanizmu Semafór (inicializovaného na _semaphore = Semaphore(N-1)_), 
kde je po premýšlaní umiestené volanie _semaphore.wait()_. To zabezpečuje, že ak sa "dostaví k stolu" posledný filozof, 
stravovanie mu nie je umožnené (predídenie uviaznutia (deadlock)) až do momentu, kým nie uvoľnené miesto pri stole zavolaním
_semaphore.signal()_, následne môže byť čakajúci filozof pripustený k stolu. Vyhľadovanie môže pri tejto variante nastať,
ak k stolu nie je pustený niektorý z filozofov (pri špecifickej postupnosti stravujúcich sa filozofov). Tento problém je 
možné vyriešiť pomocou silného semafóru (Strong Semaphore), ktorý na zabezpečenie spravodlivosti prístupu k zdrojom 
využíva frontu (Queue).

Pri variante problému N večerajúcich filozofov s jedným ľavákom je funkčnosť celého riešenia zabezpečená skutočnosťou, 
že jeden filozof berie vidličky v opačnom poradí ako ostatní (jeden je ľavák, ostatní praváci). Táto alternatíva je zabezpečená 
synchronizačným mechanizmom Mutex (list[Mutex]) a jednoduchou podmienkou, kde jeden filozof berie (uzamyká) vidličky (Mutex)
v opačnom poradí ako všetci ostatní (predídenie uviaznutia (deadlock)). Varianta riešenia s jedným ľavákom je však náchylnejšia
na vyhľadovanie, nakoľko pri častom jedení filozofa - ľavaká môžu niektorí filozofi - praváci hľadovať 
(pri špecifickej postupnosti stravujúcich sa filozofov - pravákov).

### Zdroje

__BERNÁT D., Paralelné programovanie a distribuované systémy - Synchronizačné mechanizmy. [online]. Bratislava: FEI STU, 2023.__ Dostupné z: https://elearn.elf.stuba.sk/moodle/pluginfile.php/75654/mod_resource/content/1/Ppds_1_2.pdf

__VAVRO T., ŠEBEŇA M., Paralelné programovanie a distribuované systémy - Cvičenie 4. [online]. Bratislava: FEI STU, 2023.__ Dostupné z: https://elearn.elf.stuba.sk/moodle/

__VAVRO T., ŠEBEŇA M., Paralelné programovanie a distribuované systémy - ppds-2023-cvicenia (GitHub). [online]. Bratislava: FEI STU, 2023.__ Dostupné z: https://github.com/tj314/ppds-2023-cvicenia