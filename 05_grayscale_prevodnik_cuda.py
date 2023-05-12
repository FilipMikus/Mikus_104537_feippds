"""
Modul obsahujúci implementáciu sekvečného a paralelného (CUDA) prevodníka obrázkov do grayscale formátu.
"""


__authors__ = "Filip Mikuš, Marián Šebeňa, Tomáš Vavro"
__email__ = "xmikusf@stuba.sk, mariansebena@stuba.sk, xvavro@stuba.sk"
__license__ = "MIT"


import numpy as np
from matplotlib import pyplot as plt
from numba import cuda
from time import time
import os


INPUT_IMAGES_DIR = 'input_images'
OUTPUT_IMAGES_DIR = 'output_images'


def pixel_rgb_to_grayscale(input_image: np.ndarray, x: int, y: int):
    """
    Funkcia na konverziu pixelu z rgb do grayscale.

    Argumenty:
        input_image: Vstupný obrázpk.
        x: X-ová súradnica pixelu.
        y: Y-ová súradnica pixelu.
    """
    return 0.299 * input_image[x, y, 0] + 0.587 * input_image[x, y, 1] + 0.114 * input_image[x, y, 2]


def image_rgb_to_grayscale_cpu(input_image: np.ndarray):
    """
    Funkcia na CPU konverziu obrázka z rgb do grayscale.

    Argumenty:
        input_image: Vstupný obrázok.
    """
    output_image = np.empty((input_image.shape[0], input_image.shape[1], input_image.shape[2]), dtype=np.float32)
    for x in range(len(input_image)):
        for y in range(len(input_image[x])):
            output_image[x, y] = pixel_rgb_to_grayscale(input_image, x, y)
    return output_image


@cuda.jit
def image_rgb_to_grayscale_cuda_jit(input_image: np.ndarray, output_image: np.ndarray):
    """
    Funkcia na CUDA konverziu obrázka z rgb do grayscale.

    Argumenty:
        input_image: Vstupný obrázok.
        output_image: Výstupný obrázok.
    """
    x, y = cuda.grid(2)
    if x < input_image.shape[0] and y < input_image.shape[1]:
        output_image[x, y] = pixel_rgb_to_grayscale(input_image, x, y)


def image_rgb_to_grayscale_gpu(input_image: np.ndarray):
    """
    Funkcia na GPU konverziu obrázka z rgb do grayscale.

    Argumenty:
        input_image: Vstupný obrázok.
    """
    output_image = np.empty((input_image.shape[0], input_image.shape[1], input_image.shape[2]), dtype=np.float32)
    d_input_image = cuda.to_device(input_image)
    d_output_image = cuda.to_device(output_image)
    threads_per_block = (32, 32)
    blocks_per_grid_x = (input_image.shape[0] + threads_per_block[0] - 1) // threads_per_block[0]
    blocks_per_grid_y = (input_image.shape[1] + threads_per_block[1] - 1) // threads_per_block[1]
    blocks_per_grid = (blocks_per_grid_x, blocks_per_grid_y)
    image_rgb_to_grayscale_cuda_jit[blocks_per_grid, threads_per_block](d_input_image, d_output_image)
    return d_output_image.copy_to_host()


def images_rgb_to_grayscale_cpu(input_images_directory: str, output_images_directory: str):
    """
    Funkcia na CPU konverziu priečinka obrázkov a meranie času.

    Argumenty:
        input_images_directory: Vstupný obrázk.
        output_images_directory: Vstupný obrázpk.
    """
    begin_time = time()
    for image_file in os.listdir(input_images_directory):
        input_image = plt.imread(os.path.join(input_images_directory, image_file))
        output_image = np.clip(image_rgb_to_grayscale_cpu(input_image), 0, 255).astype(np.uint8)
        plt.imsave(os.path.join(output_images_directory, image_file), output_image)
    end_time = time()
    return end_time - begin_time


def images_rgb_to_grayscale_gpu(input_images_directory: str, output_images_directory: str):
    """
    Funkcia na GPU konverziu priečinka obrázkov a meranie času.

    Argumenty:
        input_images_directory: Vstupný obrázk.
        output_images_directory: Vstupný obrázpk.
    """
    begin_time = time()
    for image_file in os.listdir(input_images_directory):
        input_image = plt.imread(os.path.join(input_images_directory, image_file))
        output_image = np.clip(image_rgb_to_grayscale_gpu(input_image), 0, 255).astype(np.uint8)
        plt.imsave(os.path.join(output_images_directory, image_file), output_image)
    end_time = time()
    return end_time - begin_time


if __name__ == '__main__':
    switch = 'gpu'
    if switch == 'cpu':
        cpu_time = images_rgb_to_grayscale_cpu(INPUT_IMAGES_DIR, OUTPUT_IMAGES_DIR)
        print(f"Čas výpočtu na CPU: {cpu_time}")
    elif switch == 'gpu':
        cpu_time = images_rgb_to_grayscale_gpu(INPUT_IMAGES_DIR, OUTPUT_IMAGES_DIR)
        print(f"Čas výpočtu na GPU: {cpu_time}")
