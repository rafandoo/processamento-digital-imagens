import numpy as np
import cv2
import matplotlib.pyplot as plt
import csv
from collections import Counter


def equalize_histogram(image: np.ndarray) -> np.ndarray:
    """
    Equaliza o histograma de uma imagem em escala de cinza.

    Args:
        image (np.ndarray): Imagem de entrada (2D).

    Returns:
        np.ndarray: Imagem com histograma equalizado.
    """
    height, width = image.shape
    MN = height * width

    hist = Counter(image.flatten())

    L = 256
    p_r = np.array([hist.get(i, 0) / MN for i in range(L)])

    s_k = np.cumsum(p_r) * (L - 1)
    s_k = np.round(s_k).astype(int)

    equalized_image = np.array(
        [s_k[p] for p in image.flatten()], dtype=np.uint8).reshape(height, width)
    return equalized_image


def plot_histogram(image: np.ndarray, title: str, output_graph: str):
    """
    Gera e salva o histograma de uma imagem.

    Args:
        image (np.ndarray): Imagem de entrada.
        title (str): Título do gráfico.
        output_graph (str): Caminho para salvar o gráfico.
    """
    hist = Counter(image.flatten())
    plt.bar(hist.keys(), hist.values(), color='gray', edgecolor='black')
    plt.title(title)
    plt.xlabel('Intensidade')
    plt.ylabel('Frequência')
    plt.savefig(output_graph)
    plt.show()


def save_csv_histogram(image: np.ndarray, csv_filename: str):
    """
    Salva o histograma de uma imagem em um arquivo CSV.

    Args:
        image (np.ndarray): Imagem de entrada.
        csv_filename (str): Caminho do arquivo CSV.
    """
    hist = Counter(image.flatten())
    with open(csv_filename, 'w', newline='') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(['intensidade', 'frequencia'])
        for intensity in range(256):
            writer.writerow([intensity, hist.get(intensity, 0)])


# Processamento das imagens
image_files = [
    'src/main/resources/Fig0316(1)(top_left).tif',
    'src/main/resources/Fig0316(2)(2nd_from_top).tif',
    'src/main/resources/Fig0316(3)(third_from_top).tif',
    'src/main/resources/Fig0316(4)(bottom_left).tif'
]

for idx, image_file in enumerate(image_files):
    image = cv2.imread(image_file, cv2.IMREAD_GRAYSCALE)

    equalized_image = equalize_histogram(image)

    output_image_file = f"equalized_image_{idx + 1}.tif"
    cv2.imwrite(output_image_file, equalized_image)

    plot_histogram(
        image, f"Histograma Original - Imagem {idx + 1}", f"histogram_original_{idx + 1}.png")
    save_csv_histogram(image, f"histogram_original_{idx + 1}.csv")

    plot_histogram(equalized_image, f"Histograma Equalizado - Imagem {
                   idx + 1}", f"histogram_equalized_{idx + 1}.png")
    save_csv_histogram(equalized_image, f"histogram_equalized_{idx + 1}.csv")
