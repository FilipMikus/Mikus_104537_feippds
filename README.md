# Mikus_104537_feippds - Zadanie 05 (CUDA grayscale prevodník)

[![python: 3.10.10](https://img.shields.io/badge/python-3.10.10-blue.svg)](https://www.python.org/downloads/release/python-31010/)
[![conventional commits: 1.0.0](https://img.shields.io/badge/conventional%20commits-1.0.0-green.svg)](https://conventionalcommits.org)
[![code style: PEP8](https://img.shields.io/badge/code%20style-PEP%208-orange.svg)](https://www.python.org/dev/peps/pep-0008/)
[![code style: PEP257](https://img.shields.io/badge/code%20style-PEP%20257-yellow.svg)](https://peps.python.org/pep-0257/)
[![license: MIT](https://img.shields.io/badge/license-MIT-red.svg)](https://opensource.org/licenses/MIT)

## Dokumentácia

### Požiadavky

Implementácia vyžaduje balíky _numpy_, _matplotlib_ a _numba_. Inštalácia pomocou _pip_:

    pip install --upgrade numpy
    pip install --upgrade matplotlib
    pip install --upgrade numba

Implementácia taktiež vyžaduje nastavenie premennej prostredia _NUMBA_ENABLE_CUDASIM_ na hodnotu _1_:
    
    export NUMBA_ENABLE_CUDASIM=1

### Spustenie

    python 05_grayscale_prevodnik_cuda.py

### Implementácia

Implementácia obsahuje prevodník obrázkov z rgb do grayscale formátu. Riešenie pozostáva z alternatívy pre CPU a GPU.

CPU alternatíva využíva funkcie _pixel_rgb_to_grayscale, _image_rgb_to_grayscale_cpu_ a  _images_rgb_to_grayscale_cpu_.
Funkcia _images_rgb_to_grayscale_cpu_ v cykle načíta obrázky zo vstupného priečinka do matice, následne vo funkcii 
_image_rgb_to_grayscale_cpu_ prebehne vytvorenie grayscale kópie vstupného obrázka sekvenčným prechodom všetkých 
pixelov v dvojitom cykle pomocou funkcie _pixel_rgb_to_grayscale_, ktorá na prevod využíva vzorec 
(_0.299 * r + 0.587 * g + 0.114 * b_). Následné sú grayscale kópie uložené do výstupného priečinka.

GPU alternatíva využíva funkcie _pixel_rgb_to_grayscale, _image_rgb_to_grayscale_cuda_jit_, _image_rgb_to_grayscale_gpu_ a  _images_rgb_to_grayscale_gpu_.
Funkcia _images_rgb_to_grayscale_cpu_ v cykle načíta obrázky zo vstupného priečinka do matice, následne vo funkcii 
_image_rgb_to_grayscale_cpu_ prebehne vytvorenie grayscale kópie vstupného obrázka výpočtom na GPU vo funkcii _image_rgb_to_grayscale_cuda_jit_ 
pomocou funkcie _pixel_rgb_to_grayscale_, ktorá na prevod využíva vzorec 
(_0.299 * r + 0.587 * g + 0.114 * b_). Následné sú grayscale kópie uložené do výstupného priečinka.

### Ukážka prevodu

<img src="https://github.com/FilipMikus/Mikus_104537_feippds/blob/05/input_images/1_7.jpg?raw=true" width="128">
<img src="https://github.com/FilipMikus/Mikus_104537_feippds/blob/05/output_images/1_7.jpg?raw=true" width="128">

### Porovnanie behu CPU - GPU

Porovnanie behu programu neuvádzame vzhľadom na beh v emulátore na stroji s procesorom Apple Silicon.

### Zdroje

__BERNÁT D., Paralelné programovanie a distribuované systémy - Synchronizačné mechanizmy. [online]. Bratislava: FEI STU, 2023.__ Dostupné z: https://elearn.elf.stuba.sk/moodle/pluginfile.php/75654/mod_resource/content/1/Ppds_1_2.pdf

__VAVRO T., ŠEBEŇA M., Paralelné programovanie a distribuované systémy - Cvičenie 4. [online]. Bratislava: FEI STU, 2023.__ Dostupné z: https://elearn.elf.stuba.sk/moodle/

__VAVRO T., ŠEBEŇA M., Paralelné programovanie a distribuované systémy - ppds-2023-cvicenia (GitHub). [online]. Bratislava: FEI STU, 2023.__ Dostupné z: https://github.com/tj314/ppds-2023-cvicenia
