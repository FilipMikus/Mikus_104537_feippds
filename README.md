# Mikus_104537_feippds - Zadanie 06 (Voľby - MPI)

[![conventional commits: 1.0.0](https://img.shields.io/badge/conventional%20commits-1.0.0-green.svg)](https://conventionalcommits.org)
[![license: MIT](https://img.shields.io/badge/license-MIT-red.svg)](https://opensource.org/licenses/MIT)

## Dokumentácia

### Požiadavky

Implementácia vyžaduje rozhranie _MPI (Message Passing Interface)_. Inštalácia pomocou _brew_:

    brew install mpich

### Spustenie

    mpicc 06_volby_mpi.c -o 06_volby_mpi.o
    mpirun -np <pocet_procesorov> 06_volby_mpi.o

### Voľby

V spojených voľbách do regionálnych samospráv kandidujú tisíce kandidátov. Viacerí kandidáti majú svoje profily na 
známej sociálnej sieti a chceli by zistiť, akú majú šancu uspieť. Kvôli tomu by potrebovali odhad „analýzy úspešnosti“. 
Napíšte paralelný program, ktorý dostane na vstup „mapu“ časti sociálnej siete vo forme orientovaného grafu, pričom 
vrcholy grafu sú jednotlivé profily osôb. Váš program by mal ohodnotiť každý profil na základe počtu „followerov“, 
pričom by mal použiť algoritmus _PageRank_.

### Formát vstupu

    # Nodes:4
    0 1
    0 2
    1 3
    2 0
    2 1
    2 3
    3 2

    ... 

### Závislosť času behu od počtu procesorov

#### Vstup 1: 4 vrcholy, 7 hrán

| **Počet procesorov** | **Čas behu (s)** |
|:--------------------:|:----------------:|
|           1          |     0.000015     |
|           2          |     0.001429     |
|           3          |     0.000743     |
|           4          |     0.000254     |

<img src="https://github.com/FilipMikus/Mikus_104537_feippds/blob/06/charts/chart1.png?raw=true" width="70%">

#### Vstup 2: 77 360 vrcholov, 905 468 hrán

| **Počet procesorov** | **ˇCas behu (s)** |
|:--------------------:|:-----------------:|
|           1          |        1432       |
|           2          |        1016       |
|           3          |        875        |
|           4          |        786        |

<img src="https://github.com/FilipMikus/Mikus_104537_feippds/blob/06/charts/chart2.png?raw=true" width="70%">

